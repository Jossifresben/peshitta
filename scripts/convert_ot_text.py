#!/usr/bin/env python3
"""Convert ETCBC/peshitta plain text files to CSV format matching the NT corpus.

Usage:
    python scripts/convert_ot_text.py /tmp/etcbc-peshitta/plain/0.2 --books Proverbs
    python scripts/convert_ot_text.py /tmp/etcbc-peshitta/plain/0.2  # all books
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# Canonical OT book order and display names
# Using standard English names that match common Bible reference format
OT_BOOKS = [
    ("Genesis", "Genesis"),
    ("Exodus", "Exodus"),
    ("Leviticus", "Leviticus"),
    ("Numbers", "Numbers"),
    ("Deuteronomy", "Deuteronomy"),
    ("Joshua", "Joshua"),
    ("Judges", "Judges"),
    ("Ruth", "Ruth"),
    ("Samuel_1", "1 Samuel"),
    ("Samuel_2", "2 Samuel"),
    ("Kings_1", "1 Kings"),
    ("Kings_2", "2 Kings"),
    ("Chronicles_1", "1 Chronicles"),
    ("Chronicles_2", "2 Chronicles"),
    ("Ezra", "Ezra"),
    ("Nehemia", "Nehemiah"),
    ("Esther", "Esther"),
    ("Job", "Job"),
    ("Psalms", "Psalms"),
    ("Proverbs", "Proverbs"),
    ("Ecclesiastes", "Ecclesiastes"),
    ("Song_of_Songs", "Song of Songs"),
    ("Isaiah", "Isaiah"),
    ("Jeremiah", "Jeremiah"),
    ("Lamentations", "Lamentations"),
    ("Ezekiel", "Ezekiel"),
    ("Daniel", "Daniel"),
    ("Hosea", "Hosea"),
    ("Joel", "Joel"),
    ("Amos", "Amos"),
    ("Obadiah", "Obadiah"),
    ("Jonah", "Jonah"),
    ("Micah", "Micah"),
    ("Nahum", "Nahum"),
    ("Habakkuk", "Habakkuk"),
    ("Zephaniah", "Zephaniah"),
    ("Haggai", "Haggai"),
    ("Zechariah", "Zechariah"),
    ("Malachi", "Malachi"),
]


def parse_plain_text(filepath: Path, book_name: str) -> list[dict]:
    """Parse an ETCBC plain text file into verse records.

    Format:
        Chapter N
        <blank line>
        1 syriac text...
        2 syriac text...
        continuation line (no number prefix)
        3 syriac text...
    """
    verses = []
    chapter = 0
    current_verse = 0
    current_text = ""

    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            # Chapter header
            m = re.match(r"^Chapter\s+(\d+)$", line)
            if m:
                # Save previous verse if any
                if current_verse > 0 and current_text:
                    verses.append({
                        "book": book_name,
                        "chapter": chapter,
                        "verse": current_verse,
                        "syriac": current_text.strip(),
                    })
                    current_text = ""
                    current_verse = 0
                chapter = int(m.group(1))
                continue

            # Blank line
            if not line.strip():
                continue

            # Verse line: starts with a number
            m = re.match(r"^(\d+)\s+(.+)$", line)
            if m:
                # Save previous verse
                if current_verse > 0 and current_text:
                    verses.append({
                        "book": book_name,
                        "chapter": chapter,
                        "verse": current_verse,
                        "syriac": current_text.strip(),
                    })
                current_verse = int(m.group(1))
                current_text = m.group(2)
            else:
                # Continuation line — append to current verse
                if current_text:
                    current_text += " " + line.strip()

    # Don't forget the last verse
    if current_verse > 0 and current_text:
        verses.append({
            "book": book_name,
            "chapter": chapter,
            "verse": current_verse,
            "syriac": current_text.strip(),
        })

    return verses


def main():
    parser = argparse.ArgumentParser(description="Convert ETCBC plain text to CSV")
    parser.add_argument("source_dir", help="Path to ETCBC plain/ version directory")
    parser.add_argument("--books", nargs="*", help="Book filenames to convert (default: all)")
    parser.add_argument("--output", "-o", help="Output CSV path (default: stdout)")
    args = parser.parse_args()

    source = Path(args.source_dir)
    if not source.is_dir():
        print(f"Error: {source} is not a directory", file=sys.stderr)
        sys.exit(1)

    # Filter books if specified
    if args.books:
        books = [(fn, name) for fn, name in OT_BOOKS if fn in args.books]
        if not books:
            print(f"Error: no matching books found for {args.books}", file=sys.stderr)
            sys.exit(1)
    else:
        books = OT_BOOKS

    all_verses = []
    for book_order, (filename, display_name) in enumerate(books, start=1):
        filepath = source / f"{filename}.txt"
        if not filepath.exists():
            print(f"Warning: {filepath} not found, skipping", file=sys.stderr)
            continue
        verses = parse_plain_text(filepath, display_name)
        for v in verses:
            v["book_order"] = book_order
            v["reference"] = f"{display_name} {v['chapter']}:{v['verse']}"
        all_verses.extend(verses)
        print(f"  {display_name}: {len(verses)} verses", file=sys.stderr)

    print(f"Total: {len(all_verses)} verses", file=sys.stderr)

    # Write CSV
    out = open(args.output, "w", newline="", encoding="utf-8") if args.output else sys.stdout
    writer = csv.DictWriter(out, fieldnames=["book_order", "book", "chapter", "verse", "reference", "syriac"])
    writer.writeheader()
    writer.writerows(all_verses)
    if args.output:
        out.close()
        print(f"Written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
