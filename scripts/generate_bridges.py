#!/usr/bin/env python3
"""Generate semantic bridges for outlier words in cognates.json.

For each outlier, asks Claude which OTHER triliteral root has the outlier's
meaning as part of its core semantic field, creating a "semantic bridge".

Usage:
    python scripts/generate_bridges.py                    # Process all
    python scripts/generate_bridges.py --dry-run          # Preview
    python scripts/generate_bridges.py --root r-w-kh      # Single root
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
You are a Semitic linguistics expert. Given a triliteral root and one of its \
semantic outliers, identify which OTHER triliteral root has the outlier's \
meaning as part of its CORE semantic field.

Rules:
- The target root must be a DIFFERENT real Semitic triliteral root
- The outlier's meaning must be CENTRAL to the target root (not peripheral)
- Use lowercase dash-separated Latin transliteration for the target root (e.g., r-kh-m)
- RESPOND WITH ONLY JSON. No explanation.
- If no clear target root exists, return {"target_root": null}

Relationship types:
- semantic_neighbor: meanings are adjacent/related concepts
- antonym_root: meanings are opposites
- metonymic_shift: meaning shifted via metonymy
- functional_drift: grammatical/functional change caused semantic shift

Example:
Root: R-W-KH (spirit, wind)
Outlier: raha (Arabic) = rest, comfort
{"target_root": "n-w-kh", "relationship": "semantic_neighbor", \
"bridge_concept_en": "Rest/comfort connects to N-W-KH (to rest, settle down)", \
"bridge_concept_es": "Descanso/confort conecta con N-W-KH (descansar, asentarse)"}
"""


def _find_related_roots(missed_target: str, meaning: str,
                        all_root_keys: set, all_roots_glosses: dict) -> list[str]:
    """Find candidate roots that might semantically match the outlier meaning."""
    candidates = []
    meaning_words = set(meaning.lower().replace(',', ' ').split())
    for k, g in all_roots_glosses.items():
        g_words = set(g.lower().replace(',', ' ').split())
        if meaning_words & g_words:
            candidates.append(f"{k} ({g})")
    return candidates[:10]


def find_bridge(client, root_key: str, gloss: str, outlier_translit: str,
                outlier_lang: str, outlier_meaning: str,
                all_root_keys: set, all_roots_glosses: dict,
                dry_run: bool = False) -> dict | None:
    """Ask Claude for a semantic bridge target for this outlier."""
    lang_full = 'Hebrew' if outlier_lang == 'heb' else 'Arabic'

    prompt = (
        f"Root: {root_key.upper()} (gloss: {gloss})\n"
        f"Outlier: {outlier_translit} ({lang_full}) = {outlier_meaning}\n"
        f"This word's meaning has drifted from the core field of \"{gloss}\".\n\n"
        f"Which OTHER triliteral root has \"{outlier_meaning}\" as CORE meaning?\n"
        f"The target must be DIFFERENT from {root_key.upper()}.\n"
        f"IMPORTANT: Pick from ONLY these roots (our available database):\n"
        f"{', '.join(sorted(all_root_keys))}\n"
        f"If NONE of these roots match, return {{\"target_root\": null}}.\n\n"
        f"Return JSON only."
    )

    if dry_run:
        print(f"    Would query: {outlier_translit} ({lang_full}) = {outlier_meaning}")
        return None

    for attempt in range(3):
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except anthropic._exceptions.OverloadedError:
            if attempt < 2:
                print(f"[retry {attempt+1}]", end=' ', flush=True)
                time.sleep(5 * (attempt + 1))
            else:
                return None

    text = response.content[0].text.strip()
    result = _parse_json(text)
    if result is None:
        print(f"    WARNING: Could not parse: {text[:100]}")
        return None

    # Validate
    target = result.get('target_root')
    if not target:
        return None
    target = target.lower().strip()

    # Must be different from source
    if target == root_key:
        return None

    # Must exist in our data — if not, try a second query with explicit candidates
    if target not in all_root_keys:
        # Find candidate roots with related glosses
        candidates = _find_related_roots(target, outlier_meaning, all_root_keys, all_roots_glosses)
        if candidates:
            retry_prompt = (
                f"The root {target} is not available. "
                f"For the outlier \"{outlier_translit}\" meaning \"{outlier_meaning}\", "
                f"which of these roots is the best semantic match?\n"
                f"{', '.join(candidates)}\n"
                f"Return JSON: {{\"target_root\": \"x-y-z\"}} or {{\"target_root\": null}}"
            )
            try:
                retry_resp = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=150,
                    messages=[{"role": "user", "content": retry_prompt}],
                )
                retry_result = _parse_json(retry_resp.content[0].text.strip())
                if retry_result and retry_result.get('target_root'):
                    alt = retry_result['target_root'].lower().strip()
                    if alt in all_root_keys and alt != root_key:
                        result['target_root'] = alt
                        target = alt
                    else:
                        return None
                else:
                    return None
            except Exception:
                return None
        else:
            return None

    valid_rels = {'semantic_neighbor', 'antonym_root', 'metonymic_shift', 'functional_drift'}
    if result.get('relationship') not in valid_rels:
        result['relationship'] = 'semantic_neighbor'

    if not result.get('bridge_concept_en'):
        return None

    result['target_root'] = target
    return result


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


def main():
    parser = argparse.ArgumentParser(description='Generate semantic bridges for outliers')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--root', type=str, help='Process a single root')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    all_root_keys = set(roots.keys())
    all_roots_glosses = {k: v.get('gloss_en', '') or v.get('gloss_es', '') for k, v in roots.items()}
    print(f"Loaded {len(roots)} roots from cognates.json")

    client = anthropic.Anthropic()

    # Collect all roots with outliers
    roots_with_outliers = {}
    for key, entry in roots.items():
        if args.root and key != args.root:
            continue
        outliers = []
        for lang_key in ('hebrew', 'arabic'):
            lang_short = 'heb' if lang_key == 'hebrew' else 'ar'
            for w in entry.get(lang_key, []):
                if w.get('outlier'):
                    outliers.append((lang_short, w))
        if outliers:
            roots_with_outliers[key] = (entry, outliers)

    print(f"Roots with outliers: {len(roots_with_outliers)}")
    total_outliers = sum(len(v[1]) for v in roots_with_outliers.values())
    print(f"Total outlier words: {total_outliers}")

    total_bridges = 0
    processed = 0

    for i, (key, (entry, outliers)) in enumerate(roots_with_outliers.items()):
        gloss = entry.get('gloss_en', '') or entry.get('gloss_es', '')
        print(f"[{i+1}/{len(roots_with_outliers)}] {key.upper()} ({gloss}):", flush=True)

        bridges = entry.get('semantic_bridges', {})

        for lang_short, w in outliers:
            translit = w['transliteration']
            meaning = w.get('meaning_en', '') or w.get('meaning_es', '')
            bridge_key = f"{lang_short}:{translit.lower().strip()}"

            print(f"  → {bridge_key} = {meaning}", end=' ', flush=True)

            result = find_bridge(
                client, key, gloss, translit, lang_short, meaning,
                all_root_keys, all_roots_glosses, dry_run=args.dry_run,
            )

            if result and result.get('target_root'):
                bridges[bridge_key] = {
                    'target_root': result['target_root'],
                    'relationship': result['relationship'],
                    'bridge_concept_en': result.get('bridge_concept_en', ''),
                    'bridge_concept_es': result.get('bridge_concept_es', ''),
                }
                total_bridges += 1
                print(f"→ bridges to {result['target_root'].upper()}")
            else:
                print("→ no bridge")

            if not args.dry_run:
                time.sleep(0.1)

        if bridges:
            entry['semantic_bridges'] = bridges

        processed += 1
        # Checkpoint every 20 roots
        if not args.dry_run and processed % 20 == 0:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [checkpoint saved]")

    print(f"\nTotal bridges created: {total_bridges}")

    if not args.dry_run and total_bridges > 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written to {DATA_PATH}")
    else:
        print("(no changes written)")


if __name__ == '__main__':
    main()
