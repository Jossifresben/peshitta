#!/usr/bin/env python3
"""Import Hebrew Modern NT translations from he_modern.json into translations.json."""

import json
import os

TRANSLATIONS_PATH = os.path.join(os.path.dirname(__file__), "data", "translations.json")
HEBREW_PATH = "/tmp/he_modern.json"

# Map Hebrew book numbers to English book names (matching translations.json keys)
BOOKS = {
    40: "Matthew", 41: "Mark", 42: "Luke", 43: "John",
    44: "Acts", 45: "Romans", 46: "1 Corinthians", 47: "2 Corinthians",
    48: "Galatians", 49: "Ephesians", 50: "Philippians", 51: "Colossians",
    52: "1 Thessalonians", 53: "2 Thessalonians", 54: "1 Timothy",
    55: "2 Timothy", 56: "Titus", 57: "Philemon", 58: "Hebrews",
    59: "James", 60: "1 Peter", 61: "2 Peter", 62: "1 John",
    63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation",
}

def main():
    with open(TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
        translations = json.load(f)

    with open(HEBREW_PATH, "r", encoding="utf-8") as f:
        hebrew_data = json.load(f)

    total_added = 0
    total_missing = 0

    for verse in hebrew_data["verses"]:
        book_num = verse["book"]
        if book_num < 40:
            continue
        book_name = BOOKS.get(book_num)
        if not book_name:
            continue
        ref = f"{book_name} {verse['chapter']}:{verse['verse']}"
        text = verse["text"].strip().lstrip("¶ ").strip()
        if ref in translations:
            translations[ref]["he"] = text
            total_added += 1
        else:
            total_missing += 1

    with open(TRANSLATIONS_PATH, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"Done! Total Hebrew verses added: {total_added}")
    print(f"Verses not in translations.json: {total_missing}")

if __name__ == "__main__":
    main()
