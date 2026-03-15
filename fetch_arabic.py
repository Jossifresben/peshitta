#!/usr/bin/env python3
"""Fetch Arabic SVD translations from getBible API and add to translations.json."""

import json
import time
import urllib.request
import urllib.error
import ssl
import os

# Workaround for macOS SSL certificate issue
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "data", "translations.json")

BOOKS = {
    40: "Matthew",
    41: "Mark",
    42: "Luke",
    43: "John",
    44: "Acts",
    45: "Romans",
    46: "1 Corinthians",
    47: "2 Corinthians",
    48: "Galatians",
    49: "Ephesians",
    50: "Philippians",
    51: "Colossians",
    52: "1 Thessalonians",
    53: "2 Thessalonians",
    54: "1 Timothy",
    55: "2 Timothy",
    56: "Titus",
    57: "Philemon",
    58: "Hebrews",
    59: "James",
    60: "1 Peter",
    62: "1 John",
}

def main():
    # Load existing translations
    with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
        translations = json.load(f)

    total_added = 0
    total_missing = 0

    for book_num, book_name in BOOKS.items():
        url = f"https://api.getbible.net/v2/arabicsv/{book_num}.json"
        print(f"Fetching {book_name} (book {book_num})...")

        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "PeshittaRootFinder/1.0")
            with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"  HTTP error {e.code} for {book_name}, skipping.")
            time.sleep(1)
            continue
        except Exception as e:
            print(f"  Error fetching {book_name}: {e}, skipping.")
            time.sleep(1)
            continue

        book_added = 0
        book_missing = 0

        # The response has chapters keyed by chapter number
        chapters = data.get("chapters", [])
        for chapter_data in chapters:
            chapter_num = chapter_data.get("chapter")
            verses = chapter_data.get("verses", [])
            for verse_obj in verses:
                verse_num = verse_obj.get("verse")
                text = verse_obj.get("text", "").strip()
                ref = f"{book_name} {chapter_num}:{verse_num}"
                if ref in translations:
                    translations[ref]["ar"] = text
                    book_added += 1
                else:
                    book_missing += 1

        print(f"  Added: {book_added}, Not in translations.json: {book_missing}")
        total_added += book_added
        total_missing += book_missing

        # Rate limit: 1 second between books
        time.sleep(1)

    # Save updated translations
    with open(TRANSLATIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Total Arabic verses added: {total_added}")
    print(f"Verses in API but not in translations.json: {total_missing}")

if __name__ == "__main__":
    main()
