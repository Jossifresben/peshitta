#!/usr/bin/env python3
"""Apply BDB audit fixes to cognates.json.

Categories of fixes:
1. REMOVE - fabricated/wrong-root words to delete
2. CORRECT - fix meanings, transliterations, or vocalizations
3. FLAG - add 'period' field for modern/post-biblical/Aramaic forms
4. NOTE - add 'note' field for semantic mismatches
"""
import json
import copy
import sys
import os
import tempfile

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COGNATES_PATH = os.path.join(_SCRIPT_DIR, "..", "data", "cognates.json")

def load():
    with open(COGNATES_PATH, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    """Atomic write: write to temp file first, then rename."""
    dir_name = os.path.dirname(COGNATES_PATH)
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        os.replace(tmp_path, COGNATES_PATH)
    except Exception:
        os.unlink(tmp_path)
        raise

def remove_hebrew_words(root_data, words_to_remove):
    """Remove Hebrew entries whose 'word' field matches any in words_to_remove."""
    if "hebrew" not in root_data:
        return 0
    before = len(root_data["hebrew"])
    root_data["hebrew"] = [
        h for h in root_data["hebrew"]
        if h["word"] not in words_to_remove
    ]
    return before - len(root_data["hebrew"])

def flag_hebrew_words(root_data, words, period):
    """Add a 'period' field to matching Hebrew entries."""
    count = 0
    for h in root_data.get("hebrew", []):
        if h["word"] in words:
            h["period"] = period
            count += 1
    return count

def flag_all_hebrew(root_data, period):
    """Add 'period' field to ALL Hebrew entries in this root."""
    count = 0
    for h in root_data.get("hebrew", []):
        h["period"] = period
        count += 1
    return count

def correct_hebrew_word(root_data, old_word, new_data):
    """Replace a Hebrew entry's fields."""
    for h in root_data.get("hebrew", []):
        if h["word"] == old_word:
            h.update(new_data)
            return True
    return False

def add_note(root_data, note):
    """Add a note to the root entry."""
    root_data["cognate_note"] = note

def apply_fixes(data):
    roots = data["roots"]
    stats = {"removed": 0, "flagged": 0, "corrected": 0, "noted": 0, "errors": []}

    # ── 1. REMOVE fabricated/wrong-root words ──

    # k-th-b: remove modern כְּתִיבָה, fix מִכְתּוֹב → already fixed to מִכְתָּב in data? Check.
    if "k-th-b" in roots:
        stats["removed"] += remove_hebrew_words(roots["k-th-b"], {"כְּתִיבָה"})
        # Correct מִכְתּוֹב to מִכְתָּב if present
        if correct_hebrew_word(roots["k-th-b"], "מִכְתּוֹב", {
            "word": "מִכְתָּב", "transliteration": "mikhtav",
            "meaning_es": "carta", "meaning_en": "letter"
        }):
            stats["corrected"] += 1

    # k-s-p: remove כַּסְפּוֹמָט (ATM!)
    if "k-s-p" in roots:
        stats["removed"] += remove_hebrew_words(roots["k-s-p"], {"כַּסְפּוֹמָט"})

    # n-p-q: remove all Hebrew (they're from Y-TS-A, not N-P-Q)
    if "n-p-q" in roots:
        stats["removed"] += remove_hebrew_words(roots["n-p-q"], {"יָצָא", "מוֹצָא", "הוֹצִיא"})
        add_note(roots["n-p-q"], "No direct Hebrew cognate from same triliteral root. Hebrew semantic parallel: Y-TS-A (יצא).")
        stats["noted"] += 1

    # d-kh-l: remove wrong-root Hebrew (P-KH-D)
    if "d-kh-l" in roots:
        stats["removed"] += remove_hebrew_words(roots["d-kh-l"], {"פַּחַד", "פַּחְדָּן"})
        add_note(roots["d-kh-l"], "No direct Hebrew triliteral cognate. Hebrew semantic parallel: P-KH-D (פחד 'fear').")
        stats["noted"] += 1

    # a-z-l: remove all wrong Hebrew
    if "a-z-l" in roots:
        stats["removed"] += remove_hebrew_words(roots["a-z-l"], {"אֲיָלִים", "אֱלַי", "הָלְכָה"})
        add_note(roots["a-z-l"], "No direct Hebrew cognate. Previous entries were from unrelated roots (A-Y-L, H-L-K).")
        stats["noted"] += 1

    # sh-r-r: remove wrong-root יָשָׁר (from Y-SH-R)
    if "sh-r-r" in roots:
        stats["removed"] += remove_hebrew_words(roots["sh-r-r"], {"יָשָׁר"})

    # z-b-n: remove wrong-root Z-M-N forms
    if "z-b-n" in roots:
        stats["removed"] += remove_hebrew_words(roots["z-b-n"], {"זְמַן"})
        add_note(roots["z-b-n"], "No common Hebrew cognate from Z-B-N. Previously listed Z-M-N forms are from a different root.")
        stats["noted"] += 1

    # ts-l-a: remove wrong-root צְלִיל (from TS-L-L)
    if "ts-l-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["ts-l-a"], {"צְלִיל"})

    # k-r-z: remove wrong-root Q-R-A forms
    if "k-r-z" in roots:
        stats["removed"] += remove_hebrew_words(roots["k-r-z"], {"קָרָא"})
        # Check if כָּרַז is already there; if not we could add it but let's not fabricate

    # b-r-k: correct בִּרְכָּה meaning from 'knee' to 'pool, pond'
    if "b-r-k" in roots:
        if correct_hebrew_word(roots["b-r-k"], "בִּרְכָּה", {
            "word": "בִּרְכָּה", "transliteration": "birkah",
            "meaning_es": "estanque, piscina", "meaning_en": "pool, pond"
        }):
            stats["corrected"] += 1

    # n-w-n: remove fabricated forms
    if "n-w-n" in roots:
        stats["removed"] += remove_hebrew_words(roots["n-w-n"], {"לִינוֹן", "נָאוֹן", "נִינָה"})

    # z-y-n: remove fabricated forms
    if "z-y-n" in roots:
        stats["removed"] += remove_hebrew_words(roots["z-y-n"], {"ליזון", "זניין"})

    # sh-d-r: remove wrong-root SH-L-KH forms
    if "sh-d-r" in roots:
        stats["removed"] += remove_hebrew_words(roots["sh-d-r"], {"שָׁלַח", "שְׁלִיחַ"})
        add_note(roots["sh-d-r"], "No direct Hebrew cognate. Hebrew semantic parallel: SH-L-KH (שלח 'to send').")
        stats["noted"] += 1

    # a-th-a: remove fabricated forms (keep אָתָה if present)
    if "a-th-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["a-th-a"], {"אָתִיל", "אִתּוּת"})

    # q-w-m: correct vocalization קָאָם → קָם
    if "q-w-m" in roots:
        if correct_hebrew_word(roots["q-w-m"], "קָאָם", {
            "word": "קָם", "transliteration": "qam",
            "meaning_es": "levantarse", "meaning_en": "to rise"
        }):
            stats["corrected"] += 1

    # ts-b-a: add semantic note
    if "ts-b-a" in roots:
        add_note(roots["ts-b-a"], "Syriac ܨܒܐ means 'to desire/want'; Hebrew צָבָא means 'army/host'. Same consonantal root but significant semantic divergence.")
        stats["noted"] += 1

    # q-r-sh: remove wrong-root Q-R-KH forms
    if "q-r-sh" in roots:
        stats["removed"] += remove_hebrew_words(roots["q-r-sh"], {"קֶרַח", "קָרֵחַ"})

    # y-h-b: remove wrong-root מוֹנָה (from M-N-H)
    if "y-h-b" in roots:
        stats["removed"] += remove_hebrew_words(roots["y-h-b"], {"מוֹנָה"})

    # n-s-b: remove wrong-root forms
    if "n-s-b" in roots:
        stats["removed"] += remove_hebrew_words(roots["n-s-b"], {"נִסָּה", "נֶסַח"})

    # kh-d-a: remove wrong-meaning חִדּוּד ('sharpening', not 'joy')
    if "kh-d-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["kh-d-a"], {"חִדּוּד"})

    # s-g-a: remove fabricated שִׂגְיוֹן
    if "s-g-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["s-g-a"], {"שִׂגְיוֹן"})
        # Flag remaining as biblical Aramaic
        stats["flagged"] += flag_all_hebrew(roots["s-g-a"], "biblical_aramaic")

    # d-n-kh: remove all wrong Hebrew
    if "d-n-kh" in roots:
        stats["removed"] += remove_hebrew_words(roots["d-n-kh"], {"נָדַח", "נַחַת", "נוֹחַ"})
        add_note(roots["d-n-kh"], "No direct Hebrew cognate for D-N-KH ('to dawn/shine').")
        stats["noted"] += 1

    # k-a-p: remove wrong-root K-B-D forms
    if "k-a-p" in roots:
        stats["removed"] += remove_hebrew_words(roots["k-a-p"], {"כָּבַד", "כְּבִיר", "כְּבִיָּה"})

    # s-n-q: remove wrong-root TS-R-KH forms
    if "s-n-q" in roots:
        stats["removed"] += remove_hebrew_words(roots["s-n-q"], {"צָרִיךְ", "צֹרֶךְ", "מַסְנֵיק"})
        add_note(roots["s-n-q"], "No direct Hebrew cognate from S-N-Q. Hebrew semantic parallel: TS-R-KH (צרך 'need').")
        stats["noted"] += 1

    # b-e-a: remove fabricated בּוֹאֵב
    if "b-e-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["b-e-a"], {"בּוֹאֵב"})

    # e-th-d: remove wrong-root K-W-N forms (keep עָתִיד, עֲתִידוֹת, עָתַד)
    if "e-th-d" in roots:
        stats["removed"] += remove_hebrew_words(roots["e-th-d"], {"הֶתְּכִין", "הֲכָנָה", "נָכוֹן"})

    # r-m-y: remove wrong-root R-W-M forms
    if "r-m-y" in roots:
        stats["removed"] += remove_hebrew_words(roots["r-m-y"], {"רָמָה", "רָמוֹת"})

    # z-k-a: remove wrong-root Z-K-R forms
    if "z-k-a" in roots:
        stats["removed"] += remove_hebrew_words(roots["z-k-a"], {"זָכוֹר", "זִכָּרוֹן"})

    # sh-kh-kh: remove wrong-root forms
    if "sh-kh-kh" in roots:
        stats["removed"] += remove_hebrew_words(roots["sh-kh-kh"], {"מָצָא", "מִשְׁכָּן"})

    # th-r-e: remove wrong-root SH-'-R forms
    if "th-r-e" in roots:
        stats["removed"] += remove_hebrew_words(roots["th-r-e"], {"שַׁעַר", "שְׁעָרִים"})
        add_note(roots["th-r-e"], "Hebrew semantic parallel: SH-'-R (שער 'gate'). Aramaic תַּרְעָא is the cognate form.")
        stats["noted"] += 1

    # n-p-l: remove fabricated מַנָּפֵל
    if "n-p-l" in roots:
        stats["removed"] += remove_hebrew_words(roots["n-p-l"], {"מַנָּפֵל"})

    # q-r-b: remove wrong-root מִלְחָמָה (from L-KH-M)
    if "q-r-b" in roots:
        stats["removed"] += remove_hebrew_words(roots["q-r-b"], {"מִלְחָמָה"})

    # p-l-sh: note duplicate with p-l-kh
    if "p-l-sh" in roots:
        add_note(roots["p-l-sh"], "Hebrew forms overlap with P-L-KH entry. Both Syriac roots share Hebrew cognate פלח.")
        stats["noted"] += 1

    # ── 2. FLAG modern Hebrew forms ──

    # sh-l-m: flag מוּשְׁלָם
    if "sh-l-m" in roots:
        stats["flagged"] += flag_hebrew_words(roots["sh-l-m"], {"מוּשְׁלָם"}, "modern")

    # b-y-th: flag modern forms
    if "b-y-th" in roots:
        stats["flagged"] += flag_hebrew_words(roots["b-y-th"], {"בַּיְתָנוּת", "בַּיְתָנִי", "בַּיְתָאִי"}, "modern")

    # s-p-r: flag סִפְרִיָּה
    if "s-p-r" in roots:
        stats["flagged"] += flag_hebrew_words(roots["s-p-r"], {"סִפְרִיָּה"}, "modern")

    # y-d-e: flag modern forms
    if "y-d-e" in roots:
        stats["flagged"] += flag_hebrew_words(roots["y-d-e"], {"מַדָּע", "מוּדָע"}, "modern")

    # y-w-m: flag יֹומַן
    if "y-w-m" in roots:
        stats["flagged"] += flag_hebrew_words(roots["y-w-m"], {"יֹומַן"}, "modern")

    # p-l-g: flag modern political terms
    if "p-l-g" in roots:
        stats["flagged"] += flag_hebrew_words(roots["p-l-g"], {"מִפְלָגָה", "פַּלְגָּנוּת"}, "modern")

    # l-m-d: flag לַמָּדוּת
    if "l-m-d" in roots:
        stats["flagged"] += flag_hebrew_words(roots["l-m-d"], {"לַמָּדוּת"}, "modern")

    # kh-sh-b: flag חֲשִׁיבוּת
    if "kh-sh-b" in roots:
        stats["flagged"] += flag_hebrew_words(roots["kh-sh-b"], {"חֲשִׁיבוּת"}, "modern")

    # ── 3. FLAG post-biblical / Rabbinic ──

    # sh-b-kh: flag all as post-biblical
    if "sh-b-kh" in roots:
        stats["flagged"] += flag_all_hebrew(roots["sh-b-kh"], "post_biblical")

    # sh-m-sh: flag verbal forms as post-biblical
    if "sh-m-sh" in roots:
        stats["flagged"] += flag_hebrew_words(roots["sh-m-sh"], {"שִׁמֵּשׁ", "שַׁמָּשׁ", "שָׁמוּשׁ"}, "post_biblical")

    # g-l-a: flag הִתְגַּלּוּת
    if "g-l-a" in roots:
        stats["flagged"] += flag_hebrew_words(roots["g-l-a"], {"הִתְגַּלּוּת"}, "post_biblical")

    # ── 4. FLAG biblical Aramaic ──

    # m-r-y: flag Aramaic forms
    if "m-r-y" in roots:
        stats["flagged"] += flag_hebrew_words(roots["m-r-y"], {"מָרִי", "מָרָן", "מָר", "מַרְיָה"}, "biblical_aramaic")
        add_note(roots["m-r-y"], "Hebrew אָדוֹן (adon) is a semantic parallel from root A-D-N, not a cognate.")
        stats["noted"] += 1

    # n-h-r: flag Aramaic forms
    if "n-h-r" in roots:
        stats["flagged"] += flag_hebrew_words(roots["n-h-r"], {"נָהִיר", "מַנְהִיר"}, "biblical_aramaic")

    # ── 5. Handle duplicates ──

    # th-l-m: remove L-M-D forms that don't belong here
    if "th-l-m" in roots:
        stats["removed"] += remove_hebrew_words(roots["th-l-m"], {"לִמּוּד", "מַלְמֵד"})
        # Fix לֶמַד → לָמַד if present
        if correct_hebrew_word(roots["th-l-m"], "לֶמַד", {
            "word": "לָמַד", "transliteration": "lamad",
            "meaning_es": "aprender", "meaning_en": "to learn"
        }):
            stats["corrected"] += 1

    # e-m-r: add note about false cognates
    if "e-m-r" in roots:
        add_note(roots["e-m-r"], "False cognates: Syriac ܥܡܪ means 'to dwell/inhabit' but Hebrew עמר means 'to gather sheaves'. Same consonants, completely different meanings.")
        stats["noted"] += 1

    return stats

def main():
    data = load()

    # Make backup
    backup = copy.deepcopy(data)

    stats = apply_fixes(data)

    print(f"Hebrew words removed: {stats['removed']}")
    print(f"Hebrew words flagged: {stats['flagged']}")
    print(f"Hebrew words corrected: {stats['corrected']}")
    print(f"Notes added: {stats['noted']}")

    if stats["errors"]:
        print(f"\nErrors:")
        for e in stats["errors"]:
            print(f"  - {e}")

    # Count roots with empty hebrew after fixes
    empty_roots = []
    for key, root in data["roots"].items():
        if "hebrew" in root and len(root["hebrew"]) == 0:
            empty_roots.append(key)

    if empty_roots:
        print(f"\nRoots with empty Hebrew list after fixes: {empty_roots}")

    # Verify totals
    total_heb = sum(len(r.get("hebrew", [])) for r in data["roots"].values())
    total_heb_before = sum(len(r.get("hebrew", [])) for r in backup["roots"].values())
    print(f"\nHebrew words before: {total_heb_before}")
    print(f"Hebrew words after: {total_heb}")
    print(f"Net change: {total_heb - total_heb_before}")

    save(data)
    print("\nSaved to", COGNATES_PATH)

if __name__ == "__main__":
    main()
