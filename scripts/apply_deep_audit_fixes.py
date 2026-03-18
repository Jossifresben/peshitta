#!/usr/bin/env python3
"""Apply deep audit fixes to cognates.json (61 issues found beyond original BDB audit)."""
import json
import copy

COGNATES_PATH = "data/cognates.json"

def load():
    with open(COGNATES_PATH, encoding="utf-8") as f:
        return json.load(f)

def save(data):
    with open(COGNATES_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")

def remove_hebrew_words(root_data, words_to_remove):
    if "hebrew" not in root_data:
        return 0
    before = len(root_data["hebrew"])
    root_data["hebrew"] = [h for h in root_data["hebrew"] if h["word"] not in words_to_remove]
    return before - len(root_data["hebrew"])

def flag_hebrew_words(root_data, words, period):
    count = 0
    for h in root_data.get("hebrew", []):
        if h["word"] in words:
            h["period"] = period
            count += 1
    return count

def flag_all_hebrew(root_data, period):
    count = 0
    for h in root_data.get("hebrew", []):
        h["period"] = period
        count += 1
    return count

def correct_hebrew_word(root_data, old_word, new_data):
    for h in root_data.get("hebrew", []):
        if h["word"] == old_word:
            h.update(new_data)
            return True
    return False

def add_note(root_data, note):
    root_data["cognate_note"] = note

def apply_fixes(data):
    roots = data["roots"]
    s = {"removed": 0, "flagged": 0, "corrected": 0, "noted": 0}

    # ═══════════════════════════════════════════
    # CATEGORY 1: WRONG ROOT ASSIGNMENT (remove)
    # ═══════════════════════════════════════════

    # 1. T-w-r: tsur from TS-W-R, tsiyya and mits'ar unrelated
    if "T-w-r" in roots:
        s["removed"] += remove_hebrew_words(roots["T-w-r"], {"צוּר", "צִיָּה", "מִצְעָר"})

    # 2. sh-t-q: sheqet/shoqet from SH-Q-T
    if "sh-t-q" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-t-q"], {"שֶׁקֶט", "שׁוֹקֵט"})

    # 3. e-sh-n: all from '-TS-M, not '-SH-N
    if "e-sh-n" in roots:
        s["removed"] += remove_hebrew_words(roots["e-sh-n"], {"עָצֵם", "עֹצֶם", "עָצוּם"})

    # 4. e-l-m: illem from A-L-M (mute)
    if "e-l-m" in roots:
        s["removed"] += remove_hebrew_words(roots["e-l-m"], {"עִלֵּם"})

    # 5. sh-l-T: shilshlit from SH-L-SH
    if "sh-l-T" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-l-T"], {"שִׁלְשְׁלִית"})

    # 6. n-p-sh: nishmah from N-SH-M
    if "n-p-sh" in roots:
        s["removed"] += remove_hebrew_words(roots["n-p-sh"], {"נִשְׁמָה"})
        # Also nafish is a proper name, not "distinguished"
        s["removed"] += remove_hebrew_words(roots["n-p-sh"], {"נָפִיש"})

    # 7. m-sh-r: makhaneh from KH-N-H
    if "m-sh-r" in roots:
        s["removed"] += remove_hebrew_words(roots["m-sh-r"], {"מַחֲנֶה"})

    # 8. kh-b-sh: asir from A-S-R, kevel from K-B-L
    if "kh-b-sh" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-b-sh"], {"אֲסִיר", "כֶּבַל"})

    # 9. m-th-l: hishtammesh/mishtammesh from SH-M-SH
    if "m-th-l" in roots:
        s["removed"] += remove_hebrew_words(roots["m-th-l"], {"הִשְׁתַּמֵּשׁ", "מִשְׁתַּמֵּשׁ"})

    # 10. kh-b-b: ahavah/ohev from A-H-B
    if "kh-b-b" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-b-b"], {"אֲהָבָה", "אָהֵב"})

    # 11. w-h-b: mamtsi from M-TS-A, nadav from N-D-B
    if "w-h-b" in roots:
        s["removed"] += remove_hebrew_words(roots["w-h-b"], {"מַמְצִיא", "נָדָב"})

    # 12. k-r-y: all from Q-TS-R
    if "k-r-y" in roots:
        s["removed"] += remove_hebrew_words(roots["k-r-y"], {"קָצָר", "קֹצֶר", "קָצֵר"})

    # 13. t-n-p: from T-M-A
    if "t-n-p" in roots:
        s["removed"] += remove_hebrew_words(roots["t-n-p"], {"טֻמְאָה", "טִמֵּא"})

    # 14. kh-a-r: khofshi from KH-P-SH, khazah/khozeh from KH-Z-H, khiyyur from KH-W-R
    if "kh-a-r" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-a-r"], {"חָפְשִׁי", "חָזָה", "חֹזֶה", "חִיּוּר"})

    # 15. k-p-n: ra'ev from R-'-B
    if "k-p-n" in roots:
        s["removed"] += remove_hebrew_words(roots["k-p-n"], {"רָעֵב"})

    # ═══════════════════════════════════════════
    # CATEGORY 2: FABRICATED / NOT IN BDB (remove)
    # ═══════════════════════════════════════════

    # 16. s-g-d: Aramaic root, not biblical Hebrew
    if "s-g-d" in roots:
        s["removed"] += remove_hebrew_words(roots["s-g-d"], {"סָגוּד", "סְגִידָה", "מִסְתַּגֵּד"})
        add_note(roots["s-g-d"], "Root S-G-D is Aramaic; no biblical Hebrew cognates attested in BDB.")
        s["noted"] += 1

    # 17. q-T-l: qetel and maqtel not in BDB
    if "q-T-l" in roots:
        s["removed"] += remove_hebrew_words(roots["q-T-l"], {"קֶטֶל", "מַקְטֵל"})

    # 18. p-l-kh: Aramaic forms
    if "p-l-kh" in roots:
        s["flagged"] += flag_hebrew_words(roots["p-l-kh"], {"פְּלָח", "פִּלּוֹחַ"}, "biblical_aramaic")

    # 19. g-b-r: correct givrah to gevirah
    if "g-b-r" in roots:
        if correct_hebrew_word(roots["g-b-r"], "גִּבְרָה", {
            "word": "גְּבִירָה", "transliteration": "gevirah",
            "meaning_es": "señora, reina madre", "meaning_en": "lady, queen mother"
        }):
            s["corrected"] += 1

    # 20. p-r-q: pruqah not in BDB
    if "p-r-q" in roots:
        s["removed"] += remove_hebrew_words(roots["p-r-q"], {"פְּרוּקָה"})

    # 21. b-y-sh: beyesh and bishut not in BDB
    if "b-y-sh" in roots:
        s["removed"] += remove_hebrew_words(roots["b-y-sh"], {"בֵּיֵשׁ", "בִּישׁוּת"})

    # 22. ts-w-m: metsuvam not in BDB
    if "ts-w-m" in roots:
        s["removed"] += remove_hebrew_words(roots["ts-w-m"], {"מְצֻוָּם"})

    # 23. sh-p-e: shafol not in BDB
    if "sh-p-e" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-p-e"], {"שָׁפוּל"})

    # 24. kh-p-y: khefyah not in BDB
    if "kh-p-y" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-p-y"], {"חֶפְיָה"})

    # 25. n-q-p: naqqaf and nequf not in BDB
    if "n-q-p" in roots:
        s["removed"] += remove_hebrew_words(roots["n-q-p"], {"נַקָּף", "נֵקוּף"})

    # 26. p-sh-q: pishqon not in BDB
    if "p-sh-q" in roots:
        s["removed"] += remove_hebrew_words(roots["p-sh-q"], {"פִּשְׁקוֹן"})

    # 27. e-d-l: entire root doesn't exist in biblical Hebrew
    if "e-d-l" in roots:
        s["removed"] += remove_hebrew_words(roots["e-d-l"], {"עָדַל", "עֵדֶל", "עִדּוּל"})
        add_note(roots["e-d-l"], "Root '-D-L is not attested in biblical Hebrew (BDB).")
        s["noted"] += 1

    # 28. d-r-b: not in BDB, post-biblical
    if "d-r-b" in roots:
        s["removed"] += remove_hebrew_words(roots["d-r-b"], {"דָּרַב", "הִדְרֵב", "דֶּרֶב", "מִדְרֵב"})

    # 29. r-d-y: not in BDB
    if "r-d-y" in roots:
        s["removed"] += remove_hebrew_words(roots["r-d-y"], {"רְדַיָּה", "רַדָּי", "רִדְיָה"})

    # 30. sh-r-b: sharevet not standard BDB
    if "sh-r-b" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-r-b"], {"שָׁרֶבֶת"})

    # 31. sh-r-k: not standard Hebrew
    if "sh-r-k" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-r-k"], {"שָׁרֵיתָ", "שָׁרוּת"})

    # 32. n-g-d: negidah not standard BDB
    if "n-g-d" in roots:
        s["removed"] += remove_hebrew_words(roots["n-g-d"], {"נְגִידָה"})

    # 33. d-g-l: fabricated forms
    if "d-g-l" in roots:
        s["removed"] += remove_hebrew_words(roots["d-g-l"], {"מַדְגִּיל", "דַּגָּל", "הִתְדַּגֵּל"})

    # 34. kh-r-n: havarah from H-B-R, makhrekhet not in BDB
    if "kh-r-n" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-r-n"], {"הֲבָרָה", "מַחְרֶרֶת"})

    # ═══════════════════════════════════════════
    # CATEGORY 3: MODERN HEBREW (flag or remove)
    # ═══════════════════════════════════════════

    # 35. p-sh-T: pishton "piston"
    if "p-sh-T" in roots:
        s["removed"] += remove_hebrew_words(roots["p-sh-T"], {"פִּשְׁטוֹן"})

    # 36. sh-w-a: shivyon and hishtavut
    if "sh-w-a" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-w-a"], {"שִׁוְיוֹן", "הִשְׁתַּוּוּת"})

    # 37. kh-w-r: khiver and khivaron
    if "kh-w-r" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-w-r"], {"חִוֵּר", "חִוָּרוֹן"})

    # 38. e-b-d: ma'avad "manufacture"
    if "e-b-d" in roots:
        s["removed"] += remove_hebrew_words(roots["e-b-d"], {"מַעֲבָד"})

    # 39. s-b-r: sabbaran "reasonable"
    if "s-b-r" in roots:
        s["removed"] += remove_hebrew_words(roots["s-b-r"], {"סַבָּרָן"})

    # 40. r-g-l: rogel "espionage"
    if "r-g-l" in roots:
        s["removed"] += remove_hebrew_words(roots["r-g-l"], {"רֹגֶל"})

    # 41. r-g-sh: modern Hebrew sensitivity words
    if "r-g-sh" in roots:
        s["removed"] += remove_hebrew_words(roots["r-g-sh"], {"רְגִישׁ", "רְגֵשָׁה", "רָגִיש"})

    # 42. e-q-r: ikkur "uprooting" (modern)
    if "e-q-r" in roots:
        s["removed"] += remove_hebrew_words(roots["e-q-r"], {"עִיקּוּר"})

    # 43. kh-l-sh: post-biblical
    if "kh-l-sh" in roots:
        s["flagged"] += flag_hebrew_words(roots["kh-l-sh"], {"חַלָּשׁ", "חֻלְשָׁה", "הִתְחַלֵּשׁ"}, "post_biblical")

    # 44. ts-l-m: matslem "photographer"
    if "ts-l-m" in roots:
        s["removed"] += remove_hebrew_words(roots["ts-l-m"], {"מַצְלֵם"})

    # 45. m-z-g: mazgan and mimzag
    if "m-z-g" in roots:
        s["removed"] += remove_hebrew_words(roots["m-z-g"], {"מַזְגָּן", "מִמְזָג"})

    # 46. p-kh-m: pakhmit
    if "p-kh-m" in roots:
        s["removed"] += remove_hebrew_words(roots["p-kh-m"], {"פַּחְמִית"})

    # 47. kh-l-b: khalavah "dairy"
    if "kh-l-b" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-l-b"], {"חָלָבָה"})

    # 48. kh-p-t: khafuz
    if "kh-p-t" in roots:
        s["removed"] += remove_hebrew_words(roots["kh-p-t"], {"חָפוּז"})

    # ═══════════════════════════════════════════
    # CATEGORY 4: WRONG MEANING (correct)
    # ═══════════════════════════════════════════

    # 49. z-q-p: zeqef = cantillation mark, not "crucifixion"
    if "z-q-p" in roots:
        if correct_hebrew_word(roots["z-q-p"], "זֶקֶף", {
            "word": "זֶקֶף", "transliteration": "zeqef",
            "meaning_es": "signo de cantilación (erguirse)", "meaning_en": "cantillation mark (to stand upright)"
        }):
            s["corrected"] += 1

    # 50. sh-m-n: shminit = "eighth" (musical term), not "greasy"
    if "sh-m-n" in roots:
        if correct_hebrew_word(roots["sh-m-n"], "שְׁמִינִית", {
            "word": "שְׁמִינִית", "transliteration": "shminit",
            "meaning_es": "octava (término musical)", "meaning_en": "eighth (musical term)"
        }):
            s["corrected"] += 1

    # ═══════════════════════════════════════════
    # CATEGORY 5: ARAMAIC MISLABELED AS HEBREW
    # ═══════════════════════════════════════════

    # 53. kh-m-r: khamarta has Aramaic suffix
    if "kh-m-r" in roots:
        s["flagged"] += flag_hebrew_words(roots["kh-m-r"], {"חֲמַרְתָּא"}, "biblical_aramaic")

    # 54. s-m-y: Aramaic forms
    if "s-m-y" in roots:
        s["flagged"] += flag_hebrew_words(roots["s-m-y"], {"סוּמָא", "סִוֵּם", "סַמְיָן"}, "biblical_aramaic")

    # 55. k-w-n: kinun post-biblical
    if "k-w-n" in roots:
        s["flagged"] += flag_hebrew_words(roots["k-w-n"], {"כִּינוּן"}, "post_biblical")

    # ═══════════════════════════════════════════
    # CATEGORY 6: MISCELLANEOUS
    # ═══════════════════════════════════════════

    # 56. k-m-r: questionable, leave for now

    # 57. sh-w-q: Aramaic forms from Peshitta
    if "sh-w-q" in roots:
        s["flagged"] += flag_hebrew_words(roots["sh-w-q"], {"שָׁאוֹק", "שֶׁיק", "שַׁוָּק"}, "biblical_aramaic")

    # 59. sh-a-d: wrong meanings
    if "sh-a-d" in roots:
        correct_hebrew_word(roots["sh-a-d"], "שָׁאָה", {
            "word": "שָׁאָה", "transliteration": "sha'ah",
            "meaning_es": "devastación, desolación", "meaning_en": "devastation, desolation"
        })
        s["corrected"] += 1
        # shedefet means blight, not "demonic possession"
        correct_hebrew_word(roots["sh-a-d"], "שֶׁדֶפֶת", {
            "word": "שְׁדֵפָה", "transliteration": "shedefah",
            "meaning_es": "tizón, plaga", "meaning_en": "blight"
        })
        s["corrected"] += 1

    # 60. k-r-h: kharash = "to plow/be deaf", not "sick"; kholeh from KH-L-H
    if "k-r-h" in roots:
        s["removed"] += remove_hebrew_words(roots["k-r-h"], {"חָרַשׁ", "חוֹלֶה"})

    # 61. sh-b-e: shevet from SH-B-T, not SH-B-'
    if "sh-b-e" in roots:
        s["removed"] += remove_hebrew_words(roots["sh-b-e"], {"שֵׁבֶט"})

    return s

def main():
    data = load()
    backup = copy.deepcopy(data)

    stats = apply_fixes(data)

    print(f"Hebrew words removed: {stats['removed']}")
    print(f"Hebrew words flagged: {stats['flagged']}")
    print(f"Hebrew words corrected: {stats['corrected']}")
    print(f"Notes added: {stats['noted']}")

    # Count roots with empty hebrew
    empty_roots = []
    for key, root in data["roots"].items():
        if "hebrew" in root and len(root["hebrew"]) == 0:
            empty_roots.append(key)
    if empty_roots:
        print(f"\nRoots with empty Hebrew list after fixes: {empty_roots}")

    total_heb = sum(len(r.get("hebrew", [])) for r in data["roots"].values())
    total_heb_before = sum(len(r.get("hebrew", [])) for r in backup["roots"].values())
    print(f"\nHebrew words before: {total_heb_before}")
    print(f"Hebrew words after: {total_heb}")
    print(f"Net change: {total_heb - total_heb_before}")

    save(data)
    print("\nSaved to", COGNATES_PATH)

if __name__ == "__main__":
    main()
