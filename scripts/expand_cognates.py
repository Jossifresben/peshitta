#!/usr/bin/env python3
"""Expand cognates.json by asking Claude to add more Hebrew & Arabic cognates.

For each root that already exists, asks Claude to suggest additional cognate
words beyond what we already have. Uses structured JSON output.

Usage:
    python scripts/expand_cognates.py                    # Process all roots
    python scripts/expand_cognates.py --dry-run           # Preview without writing
    python scripts/expand_cognates.py --root k-th-b       # Process single root
    python scripts/expand_cognates.py --batch-size 50     # Process N roots then stop
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
You are a Semitic linguistics expert specializing in comparative etymology across \
Syriac (Aramaic), Hebrew, and Arabic. Given a Syriac triliteral root with its \
existing cognates, add MORE cognate words that are missing.

Requirements for each new word:
- Must share the same triliteral root consonants (allowing regular sound shifts)
- Include the word in its native script (Hebrew with nikkud, Arabic with tashkil)
- Include a Latin transliteration
- Include meaning in both Spanish (meaning_es) and English (meaning_en)
- Only add well-established, commonly known words — no obscure/archaic terms
- Do NOT repeat words already listed in "existing"
- Aim for 2-4 additional words per language when possible
- Include both verbs and derived nouns/adjectives

RESPOND WITH ONLY valid JSON, no explanation. Format:
{
  "hebrew": [
    {"word": "הֶבְרֵיו", "transliteration": "translit", "meaning_es": "...", "meaning_en": "..."}
  ],
  "arabic": [
    {"word": "عَرَبِي", "transliteration": "translit", "meaning_es": "...", "meaning_en": "..."}
  ]
}

If no additional cognates can be added for a language, use an empty array.
"""


def expand_root(client, root_key: str, entry: dict, dry_run: bool = False) -> dict:
    """Ask Claude for additional cognates for this root."""
    gloss_en = entry.get('gloss_en', '')
    gloss_es = entry.get('gloss_es', '')

    # Existing words summary
    existing_heb = [f"{w['transliteration']}={w.get('meaning_en', '')}"
                    for w in entry.get('hebrew', [])]
    existing_ar = [f"{w['transliteration']}={w.get('meaning_en', '')}"
                   for w in entry.get('arabic', [])]

    prompt = (
        f"Syriac root: {root_key.upper()} (Syriac: {entry.get('root_syriac', '')})\n"
        f"Gloss: {gloss_en} / {gloss_es}\n"
        f"Existing Hebrew: {'; '.join(existing_heb) if existing_heb else 'none'}\n"
        f"Existing Arabic: {'; '.join(existing_ar) if existing_ar else 'none'}\n\n"
        f"Add more Hebrew and Arabic cognates that are missing. "
        f"Return ONLY JSON."
    )

    if dry_run:
        print(f"  Would expand: {root_key.upper()}")
        return {'hebrew': [], 'arabic': []}

    for attempt in range(3):
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}],
            )
            break
        except anthropic._exceptions.OverloadedError:
            if attempt < 2:
                print(f"[overloaded, retry {attempt+1}]", end=' ', flush=True)
                time.sleep(5 * (attempt + 1))
            else:
                print(f"[overloaded, giving up]", end=' ', flush=True)
                return {'hebrew': [], 'arabic': []}

    text = response.content[0].text.strip()

    # Parse JSON response
    result = _parse_json(text)
    if result is None:
        print(f"  WARNING: Could not parse response for {root_key}: {text[:120]}")
        return {'hebrew': [], 'arabic': []}

    return result


def _parse_json(text: str) -> dict | None:
    """Try to extract a JSON object from model response."""
    # Direct parse
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # Markdown code block
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

    # Find JSON object in prose
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    return None


def _validate_word(w: dict) -> bool:
    """Check that a word entry has all required fields."""
    return (
        isinstance(w, dict)
        and w.get('word', '').strip()
        and w.get('transliteration', '').strip()
        and (w.get('meaning_en', '').strip() or w.get('meaning_es', '').strip())
    )


def main():
    parser = argparse.ArgumentParser(description='Expand cognates with additional words')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--root', type=str, help='Process a single root')
    parser.add_argument('--batch-size', type=int, default=0, help='Process N roots then stop (0=all)')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    print(f"Loaded {len(roots)} roots from cognates.json")

    client = anthropic.Anthropic()

    if args.root:
        roots_to_process = {args.root: roots[args.root]}
    else:
        roots_to_process = dict(roots)

    total_added_heb = 0
    total_added_ar = 0
    processed = 0

    for i, (key, entry) in enumerate(roots_to_process.items()):
        if args.batch_size and processed >= args.batch_size:
            print(f"\nBatch limit reached ({args.batch_size})")
            break

        print(f"[{i+1}/{len(roots_to_process)}] Expanding {key.upper()}...", end=' ', flush=True)

        new_cognates = expand_root(client, key, entry, dry_run=args.dry_run)
        processed += 1

        # Deduplicate: check transliterations already present
        existing_heb_t = {w['transliteration'].lower().strip()
                         for w in entry.get('hebrew', [])}
        existing_ar_t = {w['transliteration'].lower().strip()
                        for w in entry.get('arabic', [])}

        added_h = 0
        for w in new_cognates.get('hebrew', []):
            if not _validate_word(w):
                continue
            if w['transliteration'].lower().strip() in existing_heb_t:
                continue
            entry.setdefault('hebrew', []).append(w)
            existing_heb_t.add(w['transliteration'].lower().strip())
            added_h += 1

        added_a = 0
        for w in new_cognates.get('arabic', []):
            if not _validate_word(w):
                continue
            if w['transliteration'].lower().strip() in existing_ar_t:
                continue
            entry.setdefault('arabic', []).append(w)
            existing_ar_t.add(w['transliteration'].lower().strip())
            added_a += 1

        total_added_heb += added_h
        total_added_ar += added_a

        if added_h or added_a:
            print(f"→ +{added_h} heb, +{added_a} ar")
        else:
            print("→ no new words")

        if not args.dry_run:
            time.sleep(0.15)
            # Save every 20 roots to avoid losing progress
            if processed % 20 == 0 and (total_added_heb or total_added_ar):
                with open(DATA_PATH, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  [checkpoint saved at {processed} roots]")

    print(f"\nTotal new words: +{total_added_heb} Hebrew, +{total_added_ar} Arabic")

    if not args.dry_run and (total_added_heb or total_added_ar):
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written to {DATA_PATH}")
    else:
        print("(no changes written)")


if __name__ == '__main__':
    main()
