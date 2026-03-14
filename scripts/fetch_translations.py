#!/usr/bin/env python3
"""
Fetch WEB (English) and RV1909 (Spanish) Bible translations for the
Peshitta 22-book New Testament canon.

Sources:
  - English (WEB):  bible-api.com /data/web/BOOK/CHAPTER  (public domain)
  - Spanish (RV1909): GitHub thiagobodruk/bible  (public domain)

Output: data/translations.json
Format: { "Matthew 1:1": {"en": "...", "es": "..."}, ... }

Usage:
    python3 scripts/fetch_translations.py
"""

import csv
import json
import os
import time

import requests

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "translations.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "data", "translations_progress.json")
PESHITTA_CSV = os.path.join(BASE_DIR, "syriac_nt_traditional22_unicode.csv")

DELAY_BETWEEN_REQUESTS = 3.0  # seconds between API calls

# Spanish Bible JSON from GitHub (RV1909, public domain)
RV1909_URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/es_rvr.json"

# Books in the Peshitta 22-book NT canon
# (display_name, bible_api_slug, rv1909_book_name, num_chapters)
BOOKS = [
    ("Matthew",          "MAT", "Matthew",          28),
    ("Mark",             "MRK", "Mark",             16),
    ("Luke",             "LUK", "Luke",             24),
    ("John",             "JHN", "John",             21),
    ("Acts",             "ACT", "Acts",             28),
    ("Romans",           "ROM", "Romans",           16),
    ("1 Corinthians",    "1CO", "1 Corinthians",    16),
    ("2 Corinthians",    "2CO", "2 Corinthians",    13),
    ("Galatians",        "GAL", "Galatians",         6),
    ("Ephesians",        "EPH", "Ephesians",         6),
    ("Philippians",      "PHP", "Philippians",       4),
    ("Colossians",       "COL", "Colossians",        4),
    ("1 Thessalonians",  "1TH", "1 Thessalonians",   5),
    ("2 Thessalonians",  "2TH", "2 Thessalonians",   3),
    ("1 Timothy",        "1TI", "1 Timothy",         6),
    ("2 Timothy",        "2TI", "2 Timothy",         4),
    ("Titus",            "TIT", "Titus",             3),
    ("Philemon",         "PHM", "Philemon",          1),
    ("Hebrews",          "HEB", "Hebrews",          13),
    ("James",            "JAS", "James",             5),
    ("1 Peter",          "1PE", "1 Peter",           5),
    ("1 John",           "1JN", "1 John",            5),
]

TOTAL_CHAPTERS = sum(b[3] for b in BOOKS)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(data):
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def get_peshitta_references():
    """Load verse references from the Peshitta CSV corpus."""
    if not os.path.exists(PESHITTA_CSV):
        return None
    refs = []
    with open(PESHITTA_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref = row.get("reference", "").strip()
            if ref:
                refs.append(ref)
    return refs


# ---------------------------------------------------------------------------
# Spanish: Download full RV1909 from GitHub (one request)
# ---------------------------------------------------------------------------

def download_rv1909():
    """Download the complete RV1909 Bible and return a dict:
    { "BookName": [[verse1, verse2, ...], [ch2 verses], ...], ... }
    Book names in the JSON use English names.
    """
    print("Downloading RV1909 Spanish Bible from GitHub...")
    resp = requests.get(RV1909_URL, timeout=60)
    resp.raise_for_status()
    data = json.loads(resp.content.decode("utf-8-sig"))

    # Build lookup by book name
    books = {}
    for book in data:
        name = book["name"]
        books[name] = book["chapters"]  # list of lists, 0-indexed

    print(f"  Downloaded {len(data)} books, {sum(len(b['chapters']) for b in data)} chapters")
    return books


# Map from our display names to RV1909 JSON book names
RV1909_NAME_MAP = {
    "Matthew": "Matthew",
    "Mark": "Mark",
    "Luke": "Luke",
    "John": "John",
    "Acts": "Acts",
    "Romans": "Romans",
    "1 Corinthians": "1 Corinthians",
    "2 Corinthians": "2 Corinthians",
    "Galatians": "Galatians",
    "Ephesians": "Ephesians",
    "Philippians": "Philippians",
    "Colossians": "Colossians",
    "1 Thessalonians": "1 Thessalonians",
    "2 Thessalonians": "2 Thessalonians",
    "1 Timothy": "1 Timothy",
    "2 Timothy": "2 Timothy",
    "Titus": "Titus",
    "Philemon": "Philemon",
    "Hebrews": "Hebrews",
    "James": "James",
    "1 Peter": "1 Peter",
    "1 John": "1 John",
}


# ---------------------------------------------------------------------------
# English: Fetch WEB chapter by chapter from bible-api.com
# ---------------------------------------------------------------------------

def fetch_web_chapter(book_slug, chapter):
    """Fetch a WEB chapter. Returns {verse_num: text} or None."""
    url = f"https://bible-api.com/data/web/{book_slug}/{chapter}"
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [WEB] Error fetching {book_slug} {chapter}: {e}")
        return None

    verses = {}
    if "verses" in data:
        for v in data["verses"]:
            vn = v.get("verse")
            text = v.get("text", "").strip()
            if vn and text:
                verses[int(vn)] = text
    else:
        print(f"  [WEB] Unexpected response for {book_slug} {chapter}: {list(data.keys())}")
        return None

    return verses


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Fetching WEB (English) and RV1909 (Spanish) translations")
    print("for Peshitta 22-book NT canon")
    print("=" * 60)

    # Load Peshitta references for ordering and cross-checking
    peshitta_refs = get_peshitta_references()
    if peshitta_refs:
        print(f"Loaded {len(peshitta_refs)} Peshitta verse references.")
    else:
        print("Peshitta corpus not found; will skip cross-check.")

    # Download Spanish Bible (one bulk request)
    rv1909 = download_rv1909()

    # Check name mapping
    for book_name, _, rv_name, _ in BOOKS:
        if rv_name not in rv1909:
            print(f"  WARNING: '{rv_name}' not found in RV1909 data.")
            print(f"  Available: {sorted(rv1909.keys())}")
            return

    # Load progress (for resuming English API calls)
    results = load_progress()
    if results:
        existing = len([k for k in results if not k.startswith("__done__")])
        print(f"Resuming: {existing} verses already fetched.")

    chapters_done = 0

    for book_name, book_slug, rv_name, num_chapters in BOOKS:
        print(f"\n--- {book_name} ({num_chapters} chapters) ---")

        # Get Spanish chapters for this book (0-indexed list of lists)
        es_chapters = rv1909.get(rv_name, [])

        for ch in range(1, num_chapters + 1):
            chapters_done += 1
            sentinel = f"__done__{book_name}_{ch}"

            if sentinel in results:
                print(f"  Ch {ch}: already done (skipping)")
                continue

            print(f"  Ch {ch}  [{chapters_done}/{TOTAL_CHAPTERS}]", end="", flush=True)

            # --- English: fetch from API ---
            time.sleep(DELAY_BETWEEN_REQUESTS)
            en_verses = fetch_web_chapter(book_slug, ch)
            if en_verses is None:
                print(" ... WEB failed, will retry next run")
                continue

            # --- Spanish: from downloaded data (0-indexed) ---
            es_verses = {}
            if ch - 1 < len(es_chapters):
                for i, text in enumerate(es_chapters[ch - 1], start=1):
                    es_verses[i] = text.strip()

            # Merge
            all_nums = sorted(set(en_verses.keys()) | set(es_verses.keys()))
            added = 0
            for vn in all_nums:
                ref = f"{book_name} {ch}:{vn}"
                en = en_verses.get(vn, "")
                es = es_verses.get(vn, "")
                if en or es:
                    results[ref] = {"en": en, "es": es}
                    added += 1

            results[sentinel] = True
            print(f" ... {added} verses")
            save_progress(results)

    # --- Write final output ---
    final = {k: v for k, v in results.items() if not k.startswith("__done__")}

    # Order by Peshitta corpus order if available
    if peshitta_refs:
        peshitta_set = set(peshitta_refs)
        ordered = {}
        for ref in peshitta_refs:
            if ref in final:
                ordered[ref] = final[ref]
        for ref in final:
            if ref not in ordered:
                ordered[ref] = final[ref]
        final = ordered

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"Done! {len(final)} verses written to {OUTPUT_FILE}")
    print(f"{'='*60}")

    # Cross-check
    if peshitta_refs:
        peshitta_set = set(peshitta_refs)
        missing = [r for r in peshitta_refs if r not in final]
        extra = [r for r in final if r not in peshitta_set]
        if missing:
            print(f"\nWARNING: {len(missing)} Peshitta verses missing:")
            for r in missing[:10]:
                print(f"  {r}")
            if len(missing) > 10:
                print(f"  ... and {len(missing)-10} more")
        if extra:
            print(f"\nNOTE: {len(extra)} extra verses (not in Peshitta):")
            for r in extra[:10]:
                print(f"  {r}")
        if not missing and not extra:
            print("\nAll Peshitta references matched perfectly!")

    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("Progress file cleaned up.")


if __name__ == "__main__":
    main()
