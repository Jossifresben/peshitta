#!/usr/bin/env python3
"""Tag semantic outliers in cognates.json using Claude API.

For each root family, sends the root gloss + all cognate meanings to Claude
and asks which cognates have semantically drifted from the core meaning.

Usage:
    python scripts/tag_outliers.py                # Process all roots
    python scripts/tag_outliers.py --dry-run      # Preview without writing
    python scripts/tag_outliers.py --root r-w-kh   # Process single root
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
You are a Semitic linguistics expert. Given a triliteral root and its cognates, \
identify semantic OUTLIERS — cognates whose meaning has genuinely diverged from \
the core semantic field with NO clear metaphorical or etymological bridge.

Rules:
- The core field is defined PRIMARILY by the root's gloss, NOT by majority vote of cognates
- A word is an outlier if its meaning has NO clear semantic bridge to the ROOT GLOSS
- Metaphorical extensions OF THE GLOSS are NOT outliers (library→writing=related, scent→wind/breath=related)
- Words meaning something unrelated to the gloss ARE outliers even if multiple cognates share that meaning
- Example: if gloss is "spirit/wind" then ALL words meaning "rest/comfort" are outliers, even if there are several
- RESPOND WITH ONLY A JSON ARRAY. No explanation. No text. Just the array.
- If no outliers: []

Each cognate is formatted as lang:transliteration=meaning (heb or ar prefix).

Examples:
Root R-W-KH (spirit/wind): heb:ruakh=spirit/wind; heb:reakh=scent/aroma; heb:ravah=wind/breeze; heb:hitravea(h)=to rest/breathe; ar:ruh=spirit; ar:rih=wind; ar:raha=rest/comfort; ar:rawaha=to rest/take ease
["ar:raha", "ar:rawaha", "heb:hitravea(h)"]
(rest/comfort has no bridge to spirit/wind — all rest-words are outliers)

Root K-TH-B (write): heb:katav=to write; heb:ktovet=address; ar:kataba=to write; ar:kitab=book; ar:maktaba=library
[]
(address, library are extensions of writing — not outliers)

Root E-L-M (world/eternity): heb:olam=world/eternity; heb:alam=to hide; ar:alam=world; ar:alim=scholar; ar:ilm=knowledge
["heb:alam"]

Root SH-L-M (peace/complete): heb:shalom=peace; heb:shalem=complete; heb:shilem=to pay; ar:salaam=peace; ar:taslim=surrender
[]
"""


def analyze_root(client, root_key: str, entry: dict, dry_run: bool = False) -> list[str]:
    """Send a root family to Claude and get back outlier transliterations."""
    gloss = entry.get('gloss_en', '') or entry.get('gloss_es', '')

    # Collect all cognate words with their meanings — use lang:translit as unique key
    words = []
    for lang_key in ('hebrew', 'arabic'):
        lang_short = 'heb' if lang_key == 'hebrew' else 'ar'
        for w in entry.get(lang_key, []):
            meaning = w.get('meaning_en', '') or w.get('meaning_es', '')
            words.append(f"{lang_short}:{w['transliteration']}={meaning}")

    if not words:
        return []

    # If only 1 word, no outliers possible
    if len(words) == 1:
        return []

    prompt = f"Root: {root_key.upper()} (gloss: {gloss})\nCognates: {'; '.join(words)}\n\nReturn ONLY a JSON array of outlier transliterations. Be extremely conservative — most roots have zero outliers. Only flag words with absolutely no semantic bridge to the majority."

    if dry_run:
        print(f"  Would analyze: {prompt}")
        return []

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    # Parse response — expect a JSON array, but model may wrap in text
    text = response.content[0].text.strip()

    # Try direct parse first
    try:
        outliers = json.loads(text)
        if isinstance(outliers, list):
            return [str(o).lower().strip() for o in outliers]
    except json.JSONDecodeError:
        pass

    # Extract JSON array from markdown code blocks
    if '```' in text:
        text_inner = text.split('```')[1]
        if text_inner.startswith('json'):
            text_inner = text_inner[4:]
        text_inner = text_inner.strip()
        try:
            outliers = json.loads(text_inner)
            if isinstance(outliers, list):
                return [str(o).lower().strip() for o in outliers]
        except json.JSONDecodeError:
            pass

    # Extract JSON array from prose using regex
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if match:
        try:
            outliers = json.loads(match.group())
            if isinstance(outliers, list):
                return [str(o).lower().strip() for o in outliers]
        except json.JSONDecodeError:
            pass

    print(f"  WARNING: Could not parse response for {root_key}: {text[:100]}")
    return []


def main():
    parser = argparse.ArgumentParser(description='Tag semantic outliers in cognates.json')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing')
    parser.add_argument('--root', type=str, help='Process a single root (e.g., r-w-kh)')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    print(f"Loaded {len(roots)} roots from cognates.json")

    client = anthropic.Anthropic()

    # First, clear existing outlier flags
    total_flagged = 0
    roots_to_process = {args.root: roots[args.root]} if args.root else roots

    for i, (key, entry) in enumerate(roots_to_process.items()):
        # Skip roots with only 0-1 cognates (no outliers possible)
        total_cognates = len(entry.get('hebrew', [])) + len(entry.get('arabic', []))
        if total_cognates <= 1:
            continue

        print(f"[{i+1}/{len(roots_to_process)}] Analyzing {key.upper()}...", end=' ')

        outlier_translits = analyze_root(client, key, entry, dry_run=args.dry_run)

        if outlier_translits:
            print(f"→ outliers: {outlier_translits}")
            # Tag matching cognates — outlier_translits may be "lang:translit" or just "translit"
            for lang_key in ('hebrew', 'arabic'):
                lang_short = 'heb' if lang_key == 'hebrew' else 'ar'
                for w in entry.get(lang_key, []):
                    translit = w['transliteration'].lower().strip()
                    qualified = f"{lang_short}:{translit}"
                    if qualified in outlier_translits or translit in outlier_translits:
                        w['outlier'] = True
                        total_flagged += 1
                    elif 'outlier' in w:
                        del w['outlier']  # Clear previous flag if no longer outlier
        else:
            print("→ no outliers")
            # Clear any previous flags
            for lang_key in ('hebrew', 'arabic'):
                for w in entry.get(lang_key, []):
                    if 'outlier' in w:
                        del w['outlier']

        # Small delay to avoid rate limiting
        if not args.dry_run:
            time.sleep(0.1)

    print(f"\nTotal outliers flagged: {total_flagged}")

    if not args.dry_run:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Written to {DATA_PATH}")
    else:
        print("(dry run — no changes written)")


if __name__ == '__main__':
    main()
