#!/usr/bin/env python3
"""Generate cognate entries for Syriac roots that have no cognates yet.

Sends batches of uncovered roots to Claude, which:
1. Filters out non-roots (particles, proclitic combos, proper nouns, pronouns)
2. For genuine triliteral roots, generates Hebrew & Arabic cognates

Usage:
    python scripts/generate_new_cognates.py                    # Process all
    python scripts/generate_new_cognates.py --dry-run          # Preview
    python scripts/generate_new_cognates.py --batch-size 20    # Process N batches
    python scripts/generate_new_cognates.py --min-occ 5        # Min occurrences
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
You are a Semitic linguistics expert. You will receive a batch of Syriac (Aramaic) \
three-letter patterns extracted from the Peshitta New Testament. Many of these are \
NOT real triliteral roots — they may be:
- Proclitic + particle combos (e.g., ܘܠܐ = w+la "and not")
- Pronominal suffix patterns (e.g., ܠܘܗ = l+wh "to him")
- Proper nouns (e.g., ܡܘܣ = Moses)
- Function words, conjunctions, particles

Your job:
1. FILTER: identify which patterns are genuine Syriac triliteral verbal roots
2. GENERATE: for each real root, provide Hebrew and Arabic cognates

For each real root, provide:
- gloss_es: Spanish gloss
- gloss_en: English gloss
- hebrew: array of cognate words with word (Hebrew script + nikkud), transliteration, meaning_es, meaning_en
- arabic: array of cognate words with word (Arabic script + tashkil), transliteration, meaning_es, meaning_en
- Aim for 2-4 words per language

RESPOND WITH ONLY valid JSON. Format:
{
  "roots": {
    "x-y-z": {
      "root_syriac": "ܝܝܝ",
      "gloss_es": "...",
      "gloss_en": "...",
      "hebrew": [{"word": "...", "transliteration": "...", "meaning_es": "...", "meaning_en": "..."}],
      "arabic": [{"word": "...", "transliteration": "...", "meaning_es": "...", "meaning_en": "..."}]
    }
  },
  "skipped": ["pattern1", "pattern2"]
}

The "skipped" array lists patterns that are NOT real triliteral roots.
"""


def generate_batch(client, batch: list[tuple], dry_run: bool = False) -> dict:
    """Send a batch of uncovered roots to Claude and get cognate entries back.

    batch: list of (syriac_root, transliteration, occurrences) tuples
    """
    lines = []
    for syr, translit, occ in batch:
        lines.append(f"  {syr} ({translit}) — {occ} occurrences")

    prompt = (
        f"Here are {len(batch)} Syriac three-letter patterns from the Peshitta NT.\n"
        f"Identify which are real triliteral roots and generate cognates for them.\n\n"
        + "\n".join(lines)
        + "\n\nReturn JSON only."
    )

    if dry_run:
        print(f"  Would process batch of {len(batch)}")
        return {"roots": {}, "skipped": []}

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text.strip()
    result = _parse_json(text)
    if result is None:
        print(f"  WARNING: Could not parse batch response: {text[:150]}")
        return {"roots": {}, "skipped": []}

    return result


def _parse_json(text: str) -> dict | None:
    """Extract JSON object from model response."""
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


def _validate_entry(entry: dict) -> bool:
    """Check that a root entry has minimum required fields."""
    return (
        isinstance(entry, dict)
        and entry.get('root_syriac', '').strip()
        and (entry.get('gloss_en', '').strip() or entry.get('gloss_es', '').strip())
        and (entry.get('hebrew') or entry.get('arabic'))
    )


def main():
    parser = argparse.ArgumentParser(description='Generate cognates for uncovered roots')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--batch-size', type=int, default=0, help='Max batches to process (0=all)')
    parser.add_argument('--min-occ', type=int, default=3, help='Min occurrences to consider')
    parser.add_argument('--roots-per-batch', type=int, default=10, help='Roots per API call')
    args = parser.parse_args()

    # Load corpus to get all roots
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from peshitta_roots.corpus import PeshittaCorpus
    from peshitta_roots.extractor import RootExtractor

    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            'syriac_nt_traditional22_unicode.csv')
    corpus = PeshittaCorpus(csv_path)
    extractor = RootExtractor(corpus)

    all_entries = extractor.get_all_roots()

    # Load existing cognates
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    roots = data.get('roots', {})

    # Build set of already-covered syriac roots
    covered_syriac = set()
    for k, v in roots.items():
        if 'root_syriac' in v:
            covered_syriac.add(v['root_syriac'])

    # Find uncovered triliteral roots with enough occurrences
    uncovered = []
    for entry in all_entries:
        if len(entry.root) != 3:
            continue
        if entry.root in covered_syriac:
            continue
        if entry.total_occurrences < args.min_occ:
            continue
        uncovered.append((entry.root, entry.root_transliteration, entry.total_occurrences))

    # Sort by occurrences descending
    uncovered.sort(key=lambda x: x[2], reverse=True)
    print(f"Uncovered triliteral roots (>= {args.min_occ} occ): {len(uncovered)}")
    print(f"Already covered: {len(covered_syriac)}")

    client = anthropic.Anthropic()

    # Process in batches
    total_new_roots = 0
    total_skipped = 0
    batches_processed = 0

    for batch_start in range(0, len(uncovered), args.roots_per_batch):
        if args.batch_size and batches_processed >= args.batch_size:
            print(f"\nBatch limit reached ({args.batch_size})")
            break

        batch = uncovered[batch_start:batch_start + args.roots_per_batch]
        batch_num = batch_start // args.roots_per_batch + 1
        total_batches = (len(uncovered) + args.roots_per_batch - 1) // args.roots_per_batch

        print(f"\n[Batch {batch_num}/{total_batches}] Processing {len(batch)} patterns...",
              flush=True)

        result = generate_batch(client, batch, dry_run=args.dry_run)
        batches_processed += 1

        new_roots = result.get('roots', {})
        skipped = result.get('skipped', [])
        total_skipped += len(skipped)

        for key, entry in new_roots.items():
            key = key.lower().strip()
            if not _validate_entry(entry):
                print(f"  Skipped invalid entry: {key}")
                continue
            if key in roots:
                print(f"  Already exists: {key}")
                continue

            roots[key] = entry
            covered_syriac.add(entry.get('root_syriac', ''))
            total_new_roots += 1
            heb_count = len(entry.get('hebrew', []))
            ar_count = len(entry.get('arabic', []))
            print(f"  + {key.upper()} ({entry.get('gloss_en', '')}) — "
                  f"{heb_count} heb, {ar_count} ar")

        if skipped:
            print(f"  Skipped {len(skipped)} non-roots: {', '.join(skipped[:5])}"
                  + (f"... +{len(skipped)-5}" if len(skipped) > 5 else ""))

        if not args.dry_run:
            time.sleep(0.3)

    print(f"\n{'='*50}")
    print(f"New roots added: {total_new_roots}")
    print(f"Patterns skipped (not real roots): {total_skipped}")
    print(f"Total roots now: {len(roots)}")

    if not args.dry_run and total_new_roots > 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written to {DATA_PATH}")
    else:
        print("(no changes written)")


if __name__ == '__main__':
    main()
