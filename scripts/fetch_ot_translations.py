#!/usr/bin/env python3
"""Fetch public domain Bible translations for OT books and merge into translations JSON.

Sources (all via bible.helloao.org, no rate limits):
- English: World English Bible (eng_web, public domain)
- Spanish: Reina-Valera 1909 (spa_r09, public domain)

Usage:
    python scripts/fetch_ot_translations.py                # Fetch all 4 books, both languages
    python scripts/fetch_ot_translations.py --books Psalms  # Single book
    python scripts/fetch_ot_translations.py --langs en       # English only
    python scripts/fetch_ot_translations.py --dry-run       # Preview without saving
"""

import argparse
import json
import os
import sys
import time

import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

# Books to fetch and their chapter counts
OT_BOOKS = {
    'Psalms': 150,
    'Proverbs': 31,
    'Isaiah': 66,
    'Ezekiel': 48,
}

# bible.helloao.org book codes
HELLOAO_BOOKS = {
    'Psalms': 'PSA',
    'Proverbs': 'PRO',
    'Isaiah': 'ISA',
    'Ezekiel': 'EZK',
}

# Translation IDs on bible.helloao.org
HELLOAO_TRANSLATIONS = {
    'en': 'eng_web',    # World English Bible
    'es': 'spa_r09',    # Reina-Valera 1909
    'he': 'hbo_wlc',    # Westminster Leningrad Codex (Masoretic Hebrew)
}


def fetch_chapter_helloao(translation_id: str, book_code: str, chapter: int) -> dict:
    """Fetch a chapter from bible.helloao.org. Returns {verse_num: text}."""
    url = f"https://bible.helloao.org/api/{translation_id}/{book_code}/{chapter}.json"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        data = r.json()
        verses = {}
        for item in data.get('chapter', {}).get('content', []):
            if item.get('type') == 'verse':
                v_num = item['number']
                parts = []
                for part in item.get('content', []):
                    if isinstance(part, str):
                        parts.append(part)
                    elif isinstance(part, dict):
                        parts.append(part.get('text', ''))
                text = ' '.join(parts).strip()
                if text:
                    verses[v_num] = text
        return verses
    except Exception as e:
        print(f"    ERROR: {e}", file=sys.stderr)
        return {}


def fetch_book(book_ref_name: str, max_chapters: int, lang: str,
               dry_run: bool = False) -> dict:
    """Fetch all chapters of a book. Returns {reference: text}."""
    results = {}
    for ch in range(1, max_chapters + 1):
        if dry_run:
            print(f"  Would fetch: {book_ref_name} ch {ch} ({lang})")
            continue

        if ch % 10 == 1 or ch == max_chapters:
            print(f"  Ch {ch}/{max_chapters}...", end=' ', flush=True)

        translation_id = HELLOAO_TRANSLATIONS[lang]
        book_code = HELLOAO_BOOKS[book_ref_name]
        verses = fetch_chapter_helloao(translation_id, book_code, ch)

        for v_num, text in verses.items():
            ref = f"{book_ref_name} {ch}:{v_num}"
            results[ref] = text

        if ch % 10 == 0 or ch == max_chapters:
            print(f"{len(results)} total", flush=True)

        # Rate limiting
        time.sleep(0.2)

    return results


def main():
    parser = argparse.ArgumentParser(description='Fetch OT translations from public domain Bibles')
    parser.add_argument('--books', nargs='*', help='Books to fetch (default: all 4)')
    parser.add_argument('--langs', nargs='*', default=['en', 'es', 'he'], help='Languages (default: en es he)')
    parser.add_argument('--dry-run', action='store_true', help='Preview without fetching')
    args = parser.parse_args()

    books = {}
    if args.books:
        for b in args.books:
            if b in OT_BOOKS:
                books[b] = OT_BOOKS[b]
            else:
                print(f"Unknown book: {b}. Available: {list(OT_BOOKS.keys())}", file=sys.stderr)
                sys.exit(1)
    else:
        books = OT_BOOKS

    for lang in args.langs:
        if lang not in HELLOAO_TRANSLATIONS:
            print(f"Unsupported language: {lang}. Use one of: {list(HELLOAO_TRANSLATIONS.keys())}", file=sys.stderr)
            continue

        trans_file = os.path.join(DATA_DIR, f'translations_{lang}.json')

        # Load existing translations
        if os.path.exists(trans_file):
            with open(trans_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = {}

        source = f"{HELLOAO_TRANSLATIONS[lang]} (bible.helloao.org)"
        print(f"\n=== {lang.upper()} — {source} ===")
        print(f"Existing translations: {len(existing)}")

        total_new = 0
        for book_ref_name, max_chapters in books.items():
            print(f"\n{book_ref_name} ({max_chapters} chapters):")

            new_verses = fetch_book(book_ref_name, max_chapters, lang, args.dry_run)
            if new_verses:
                existing.update(new_verses)
                total_new += len(new_verses)
                print(f"  Fetched: {len(new_verses)} verses")

        if not args.dry_run and total_new > 0:
            with open(trans_file, 'w', encoding='utf-8') as f:
                json.dump(existing, f, ensure_ascii=False)
            print(f"\nSaved {total_new} new verses to {trans_file}")
            print(f"Total translations now: {len(existing)}")
        elif args.dry_run:
            total_ch = sum(books.values())
            print(f"\nDry run: would fetch {total_ch} chapters for {lang}")


if __name__ == '__main__':
    main()
