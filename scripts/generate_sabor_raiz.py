#!/usr/bin/env python3
"""Generate sabor_raiz (semantic field summary) for each root in cognates.json.

Uses Claude Haiku to generate a poetic 3-5 word semantic field phrase
from each root's gloss and cognate meanings.

Usage:
    python scripts/generate_sabor_raiz.py                    # Process all
    python scripts/generate_sabor_raiz.py --dry-run          # Preview prompt
    python scripts/generate_sabor_raiz.py --root sh-l-m      # Single root
"""

import argparse
import json
import os
import sys
import time

import anthropic

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cognates.json')

SYSTEM_PROMPT = """\
You are a Semitic linguistics expert specializing in triliteral root semantics.
Given a triliteral root with its gloss and cognate meanings across Syriac, Hebrew,
and Arabic, produce a short poetic semantic field summary (3-5 words) that captures
the ROOT's essential meaning — the deep semantic core that unifies all its derivatives.

Rules:
- Output ONLY a JSON object: {"sabor_raiz_es": "...", "sabor_raiz_en": "..."}
- Each value should be 3-5 words, comma-separated concepts
- Capture the ESSENCE, not a list of translations
- Think of it as the "flavor" or "aroma" of the root
- Spanish and English should convey the same concepts idiomatically (not literal translations)

Examples:
Root: SH-L-M | Gloss: peace, complete
Cognates: shalom, salaam, shalem, islam, mushlam
→ {"sabor_raiz_es": "integridad, completud, paz", "sabor_raiz_en": "wholeness, completion, peace"}

Root: K-TH-B | Gloss: write
Cognates: katav, kitab, ketaba, maktub
→ {"sabor_raiz_es": "escritura, inscripción, registro", "sabor_raiz_en": "writing, inscription, record"}

Root: R-W-KH | Gloss: spirit, wind
Cognates: rukha, ruakh, ruh, rawha
→ {"sabor_raiz_es": "aliento, viento, espíritu", "sabor_raiz_en": "breath, wind, spirit"}
"""


def build_user_prompt(key: str, entry: dict) -> str:
    """Build the user prompt for a single root."""
    gloss_combined = f"{entry.get('gloss_en', '')} / {entry.get('gloss_es', '')}"

    cognate_words = []
    for hw in entry.get('hebrew', []):
        if not hw.get('outlier', False):
            cognate_words.append(f"{hw['transliteration']} ({hw.get('meaning_en', '')})")
    for aw in entry.get('arabic', []):
        if not aw.get('outlier', False):
            cognate_words.append(f"{aw['transliteration']} ({aw.get('meaning_en', '')})")

    cognates_str = ', '.join(cognate_words[:12]) if cognate_words else 'none'

    return f"Root: {key.upper().replace('-', '-')} | Gloss: {gloss_combined}\nCognates: {cognates_str}"


def generate_sabor(client: anthropic.Anthropic, key: str, entry: dict) -> dict | None:
    """Call Claude Haiku to generate sabor_raiz for one root."""
    user_prompt = build_user_prompt(key, entry)

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text.strip()
        # Strip markdown code blocks if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
            if text.endswith('```'):
                text = text[:-3].strip()
        result = json.loads(text)
        if 'sabor_raiz_es' in result and 'sabor_raiz_en' in result:
            return result
        print(f"  WARNING: Unexpected response for {key}: {text}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"  WARNING: Invalid JSON for {key}: {text}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR for {key}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description='Generate sabor_raiz fields')
    parser.add_argument('--dry-run', action='store_true', help='Preview without calling API')
    parser.add_argument('--root', type=str, help='Process a single root (e.g., sh-l-m)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing sabor_raiz')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    client = None if args.dry_run else anthropic.Anthropic()

    if args.root:
        keys_to_process = [args.root.lower()]
    else:
        keys_to_process = list(roots.keys())

    skipped = 0
    processed = 0
    failed = 0

    for i, key in enumerate(keys_to_process):
        if key not in roots:
            print(f"Root '{key}' not found in cognates.json", file=sys.stderr)
            continue

        entry = roots[key]

        # Skip if already has sabor_raiz (unless --overwrite)
        if not args.overwrite and entry.get('sabor_raiz_es') and entry.get('sabor_raiz_en'):
            skipped += 1
            continue

        prompt = build_user_prompt(key, entry)

        if args.dry_run:
            print(f"\n--- {key} ---")
            print(prompt)
            continue

        print(f"[{i+1}/{len(keys_to_process)}] {key}...", end=' ', flush=True)
        result = generate_sabor(client, key, entry)

        if result:
            entry['sabor_raiz_es'] = result['sabor_raiz_es']
            entry['sabor_raiz_en'] = result['sabor_raiz_en']
            print(f"✓ {result['sabor_raiz_es']} / {result['sabor_raiz_en']}")
            processed += 1
        else:
            failed += 1

        # Rate limiting — Haiku is fast but let's be gentle
        if not args.dry_run and i < len(keys_to_process) - 1:
            time.sleep(0.3)

        # Save every 20 roots
        if processed > 0 and processed % 20 == 0:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [Saved checkpoint at {processed} roots]")

    if not args.dry_run and processed > 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {processed} generated, {skipped} skipped, {failed} failed")


if __name__ == '__main__':
    main()
