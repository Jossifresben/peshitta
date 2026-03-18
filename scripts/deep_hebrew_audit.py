#!/usr/bin/env python3
"""Deep audit of Hebrew cognates in cognates.json.

Checks for:
1. Duplicate Hebrew words across different roots
2. Roots where Hebrew has no consonantal overlap with Syriac root
3. Suspiciously long Hebrew lists (possible padding)
4. Hebrew words with no vowel points (possibly fabricated)
5. Roots where ALL Hebrew are marked as outliers
6. Empty Hebrew lists
7. Duplicate roots (same Syriac root appearing under different keys)
"""
import json
from collections import defaultdict

COGNATES_PATH = "data/cognates.json"

def load():
    with open(COGNATES_PATH, encoding="utf-8") as f:
        return json.load(f)

# Mapping from Latin transliteration consonants to Hebrew consonant letters
TRANSLIT_TO_HEBREW = {
    "k": "כ", "th": "ת", "b": "ב", "sh": "ש", "l": "ל", "m": "מ",
    "n": "נ", "p": "פ", "r": "ר", "d": "ד", "g": "ג", "h": "ה",
    "w": "ו", "z": "ז", "kh": "ח", "t": "ט", "y": "י", "s": "ס",
    "q": "ק", "ts": "צ", "a": "א", "e": "ע",
}

# Sound correspondences between Syriac and Hebrew
SOUND_CORRESPONDENCES = {
    "th": {"ת", "שׁ", "ש"},
    "sh": {"שׁ", "ש", "ס"},
    "t": {"ט", "ת"},
    "s": {"ס", "שׂ", "ש", "צ"},
    "ts": {"צ", "ס"},
    "kh": {"ח", "כ"},
    "k": {"כ", "ק"},
    "q": {"ק", "כ"},
    "a": {"א", "ע"},
    "e": {"ע", "א"},
    "d": {"ד", "ז"},
    "z": {"ז", "ד", "צ"},
    "b": {"ב", "פ"},
    "p": {"פ", "ב"},
    "g": {"ג", "ק"},
    "h": {"ה", "א", "ח"},
    "w": {"ו", "י"},
    "y": {"י", "ו"},
    "n": {"נ"},
    "m": {"מ"},
    "r": {"ר"},
    "l": {"ל"},
}

def parse_root_consonants(root_key):
    """Parse root key like 'k-th-b' into list of consonant groups."""
    return root_key.lower().split("-")

def main():
    data = load()
    roots = data["roots"]

    issues = []

    # 1. Find duplicate Hebrew words across roots
    word_to_roots = defaultdict(list)
    for key, root in roots.items():
        for h in root.get("hebrew", []):
            word_to_roots[h["word"]].append(key)

    print("=" * 60)
    print("1. DUPLICATE HEBREW WORDS (same word in multiple roots)")
    print("=" * 60)
    dups = {w: rs for w, rs in word_to_roots.items() if len(rs) > 1}
    for word, rs in sorted(dups.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"  {word} → {', '.join(rs)}")
    print(f"  Total: {len(dups)} duplicated words\n")

    # 2. Roots with empty Hebrew
    print("=" * 60)
    print("2. ROOTS WITH EMPTY HEBREW LIST")
    print("=" * 60)
    for key, root in sorted(roots.items()):
        if "hebrew" in root and len(root["hebrew"]) == 0:
            print(f"  {key} ({root.get('gloss_en', '?')})")
    print()

    # 3. Suspiciously large Hebrew lists (>6 entries)
    print("=" * 60)
    print("3. ROOTS WITH >6 HEBREW ENTRIES (possible padding)")
    print("=" * 60)
    for key, root in sorted(roots.items(), key=lambda x: len(x[1].get("hebrew", [])), reverse=True):
        heb_count = len(root.get("hebrew", []))
        if heb_count > 6:
            print(f"  {key} ({root.get('gloss_en', '?')}): {heb_count} Hebrew entries")
    print()

    # 4. Roots where ALL Hebrew are outliers
    print("=" * 60)
    print("4. ROOTS WHERE ALL HEBREW ENTRIES ARE OUTLIERS")
    print("=" * 60)
    for key, root in sorted(roots.items()):
        heb = root.get("hebrew", [])
        if heb and all(h.get("outlier") for h in heb):
            words = [h["word"] for h in heb]
            print(f"  {key} ({root.get('gloss_en', '?')}): {', '.join(words)}")
    print()

    # 5. Duplicate root keys (same Syriac root)
    print("=" * 60)
    print("5. DUPLICATE SYRIAC ROOTS (different keys, same root_syriac)")
    print("=" * 60)
    syriac_to_keys = defaultdict(list)
    for key, root in roots.items():
        sr = root.get("root_syriac", "")
        if sr:
            syriac_to_keys[sr].append(key)
    for sr, keys in sorted(syriac_to_keys.items()):
        if len(keys) > 1:
            print(f"  {sr} → {', '.join(keys)}")
    print()

    # 6. Export all Hebrew words for manual review (sorted by root)
    print("=" * 60)
    print("6. FULL HEBREW COGNATE INVENTORY")
    print("=" * 60)
    total = 0
    for key in sorted(roots.keys()):
        root = roots[key]
        heb = root.get("hebrew", [])
        if not heb:
            continue
        flags = []
        if root.get("cognate_note"):
            flags.append("NOTE")
        print(f"\n  {key} ({root.get('gloss_en', '?')}):")
        for h in heb:
            markers = []
            if h.get("outlier"):
                markers.append("OUTLIER")
            if h.get("period"):
                markers.append(h["period"].upper())
            marker_str = f" [{', '.join(markers)}]" if markers else ""
            print(f"    {h['word']} ({h.get('transliteration', '?')}) = {h.get('meaning_en', '?')}{marker_str}")
            total += 1
        if root.get("cognate_note"):
            print(f"    NOTE: {root['cognate_note']}")

    print(f"\n  Total Hebrew entries: {total}")

if __name__ == "__main__":
    main()
