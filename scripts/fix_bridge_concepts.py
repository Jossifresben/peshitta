#!/usr/bin/env python3
"""Fix mismatched bridge_concept_en/es fields in cognates.json.

When generate_bridges.py's fallback mechanism replaced a target_root with an
alternative root, the bridge_concept text was left referencing the original
(unavailable) root. This script detects those mismatches and uses Claude to
regenerate ONLY the concept text fields.

Usage:
    python scripts/fix_bridge_concepts.py              # Fix all mismatches
    python scripts/fix_bridge_concepts.py --dry-run    # Preview mismatches only
"""

import argparse
import json
import os
import re
import sys
import time

import anthropic

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cognates.json')

SYSTEM_PROMPT = """\
You are a Semitic linguistics expert. You will be given a semantic bridge entry \
that has a mismatch: the target_root field points to one root, but the concept \
text references a different root.

Your job: rewrite ONLY the bridge_concept_en and bridge_concept_es fields so \
they correctly reference the ACTUAL target root and its gloss.

Rules:
- Keep the same style and structure as the original concept text
- Reference the correct target root (uppercase, dash-separated) and its gloss
- The concept should explain how the outlier word's meaning connects to the target root
- RESPOND WITH ONLY JSON: {"bridge_concept_en": "...", "bridge_concept_es": "..."}
- No explanation outside the JSON.
"""


def _parse_json(text: str) -> dict | None:
    """Extract JSON object from model response."""
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    if '```' in text:
        inner = text.split('```')[1]
        if inner.startswith('json'):
            inner = inner[4:]
        inner = inner.strip()
        try:
            obj = json.loads(inner)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    return None


def is_mismatch(bridge: dict) -> bool:
    """Check if target_root is NOT mentioned in bridge_concept_en."""
    target = bridge.get('target_root', '')
    concept = bridge.get('bridge_concept_en', '')
    if not target or not concept:
        return False
    return target.upper() not in concept.upper()


def fix_concept(client, root_key: str, root_gloss: str,
                bridge_key: str, bridge: dict,
                target_gloss: str) -> dict | None:
    """Use Claude to regenerate bridge concept text for correct target root."""
    target = bridge['target_root']

    # Extract outlier info from bridge_key (format: "lang:transliteration")
    parts = bridge_key.split(':', 1)
    lang_full = 'Hebrew' if parts[0] == 'heb' else 'Arabic'
    outlier_translit = parts[1] if len(parts) > 1 else bridge_key

    prompt = (
        f"Source root: {root_key.upper()} (gloss: {root_gloss})\n"
        f"Outlier word: {outlier_translit} ({lang_full})\n"
        f"Actual target root: {target.upper()} (gloss: {target_gloss})\n"
        f"Relationship: {bridge.get('relationship', 'semantic_neighbor')}\n\n"
        f"Current (WRONG) concept text:\n"
        f"  EN: {bridge.get('bridge_concept_en', '')}\n"
        f"  ES: {bridge.get('bridge_concept_es', '')}\n\n"
        f"Rewrite the concept text to correctly reference {target.upper()} "
        f"({target_gloss}) instead. Return JSON only."
    )

    for attempt in range(5):
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except anthropic._exceptions.OverloadedError:
            wait = 5 * (2 ** attempt)
            print(f" [overloaded, retry {attempt+1} in {wait}s]", end='', flush=True)
            time.sleep(wait)
        except Exception as e:
            print(f" [error: {e}]", end='', flush=True)
            if attempt < 4:
                time.sleep(3)
            else:
                return None
    else:
        return None

    text = response.content[0].text.strip()
    result = _parse_json(text)
    if result is None:
        print(f" [parse error: {text[:80]}]", end='', flush=True)
        return None

    en = result.get('bridge_concept_en', '')
    es = result.get('bridge_concept_es', '')
    if not en or not es:
        return None

    return {'bridge_concept_en': en, 'bridge_concept_es': es}


def main():
    parser = argparse.ArgumentParser(description='Fix mismatched bridge concept text')
    parser.add_argument('--dry-run', action='store_true', help='Preview mismatches only')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    print(f"Loaded {len(roots)} roots from cognates.json")

    # Collect all mismatches
    mismatches = []
    total_bridges = 0
    for root_key, root_data in roots.items():
        bridges = root_data.get('semantic_bridges', {})
        for bridge_key, bridge in bridges.items():
            total_bridges += 1
            if is_mismatch(bridge):
                mismatches.append((root_key, bridge_key, bridge))

    print(f"Total bridges: {total_bridges}")
    print(f"Mismatches found: {len(mismatches)} ({len(mismatches)/total_bridges*100:.1f}%)")

    if args.dry_run:
        print("\n--- Dry run: listing mismatches ---")
        for root_key, bridge_key, bridge in mismatches:
            target = bridge['target_root']
            concept = bridge.get('bridge_concept_en', '')[:100]
            print(f"  {root_key} / {bridge_key}: target={target}, concept={concept}...")
        print(f"\nTotal: {len(mismatches)} mismatches to fix")
        return

    if not mismatches:
        print("No mismatches to fix!")
        return

    client = anthropic.Anthropic()
    fixed = 0
    failed = 0

    for i, (root_key, bridge_key, bridge) in enumerate(mismatches):
        root_data = roots[root_key]
        root_gloss = root_data.get('gloss_en', '') or root_data.get('gloss_es', '')
        target_root = bridge['target_root']

        # Get target root's gloss
        target_data = roots.get(target_root, {})
        target_gloss = target_data.get('gloss_en', '') or target_data.get('gloss_es', '') or '(unknown)'

        print(f"[{i+1}/{len(mismatches)}] {root_key}/{bridge_key} → {target_root} ({target_gloss})", end='', flush=True)

        result = fix_concept(client, root_key, root_gloss, bridge_key, bridge, target_gloss)

        if result:
            bridge['bridge_concept_en'] = result['bridge_concept_en']
            bridge['bridge_concept_es'] = result['bridge_concept_es']
            fixed += 1
            print(f" ✓")
        else:
            failed += 1
            print(f" ✗ (skipped)")

        time.sleep(0.1)

        # Checkpoint every 20 fixes
        if fixed > 0 and fixed % 20 == 0:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [checkpoint saved at {fixed} fixes]")

    # Final save
    if fixed > 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nDone! Fixed {fixed}/{len(mismatches)} mismatches ({failed} failed)")
        print(f"Saved to {DATA_PATH}")
    else:
        print(f"\nNo fixes applied ({failed} failed)")


if __name__ == '__main__':
    main()
