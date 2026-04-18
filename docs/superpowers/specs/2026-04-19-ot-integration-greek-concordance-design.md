# OT Integration + Greek-Syriac Translation Concordance

**Date:** 2026-04-19
**Status:** Approved

## Overview

Two independent features that together create a cross-corpus, cross-linguistic research tool:

1. **OT Integration** — Merge 4 OT books (Psalms, Isaiah, Ezekiel, Proverbs; 5,929 verses) into the existing NT corpus. All features (search, browse, reader, KWIC, co-occurrence, semantic fields) work across both testaments.

2. **Greek-Syriac Translation Concordance** — New "By Greek" search tab. Inverts the existing `greek_parallel` data from cognates.json to let users search from Greek lemma to Syriac root(s). Shows all Syriac roots used to translate a given Greek word.

## 1. OT Integration

### Data

- Source: `syriac_ot_selected_unicode.csv` (already in repo)
- Format: identical to NT CSV (`book_order,book,chapter,verse,reference,syriac`)
- Books: Psalms (2,454 verses), Isaiah (1,290), Ezekiel (1,271), Proverbs (914)
- No OT translations initially — reader shows Syriac + transliteration only

### Corpus Loading

- `PeshittaCorpus` loads both CSVs into the same `_verses` dict
- No reference collisions (OT books have different names than NT books)
- New `_testament` dict maps book name to `'nt'` or `'ot'`
- Method `get_testament(book)` returns `'nt'` or `'ot'`
- `get_books()` returns all books, ordered: NT books first, then OT books

### Root Extraction

- `RootExtractor` runs over merged corpus — same algorithm, more data
- Root counts now reflect both testaments
- No changes to extraction logic

### Search & Browse

- Browse page: testament filter toggle (All / NT / OT) above existing views
- Root search results: `NT` / `OT` badge on references
- Browse table stats: split counts ("45 NT / 23 OT")
- Semantic fields, reverse search, co-occurrence all work automatically over merged corpus

### Reader

- Book selector adds OT books, grouped by testament (optgroup or visual separator)
- OT verses: Syriac + transliteration, no translation line
- Constellation and word-click modal work the same
- Audio player appears only for chapters with audio data (unchanged)

### Impact

- Corpus grows from 7,440 to ~13,400 verses
- Cold start extraction time roughly doubles (~4-6s), cached after
- New OT roots appear in browse/search but lack cognate data until enriched

## 2. Greek-Syriac Translation Concordance

### Data Source

Existing `greek_parallel` field in `data/cognates.json`. 436 roots have entries:

```json
"m-l-k": {
  "greek_parallel": {
    "word": "βασιλεύς",
    "transliteration": "basileus",
    "meaning_en": "king",
    "meaning_es": "rey"
  }
}
```

### Reverse Index

Built lazily on first request (same pattern as `_reverse_idx`):

```python
_greek_idx = {
  "βασιλεύς": [{"root_key": "m-l-k", "root_syriac": "ܡܠܟ", "gloss": "king", "occurrences": 200}],
  "γράφω": [{"root_key": "k-th-b", ...}],
  ...
}
```

Some Greek words map to multiple Syriac roots. The index captures all mappings.

### UI: New Search Tab

- Position: 6th tab after "Full text" — labeled "By Greek" / "Por griego" / "ביוונית" / "باليونانية" / "Op Grieks"
- Input: text field with autocomplete from the Greek index
- Results: cards showing Greek lemma + transliteration + meaning, then all mapped Syriac roots with:
  - Root in Syriac script + transliteration
  - Gloss
  - Occurrence count badge
  - Link to root visualizer
  - Semantic field tag (if available)

### API

`GET /api/greek-concordance?q=βασιλεύς&lang=en`

Response:
```json
{
  "query": "βασιλεύς",
  "transliteration": "basileus",
  "meaning": "king",
  "roots": [
    {
      "key": "m-l-k",
      "root_syriac": "ܡܠܟ",
      "gloss": "king, reign",
      "occurrences": 200,
      "sabor": "dominion, sovereignty"
    }
  ]
}
```

### Browse Mode

Below the search input, a full alphabetical list of all Greek lemmas in the index. Clickable to show their Syriac root mappings. Useful for browsing without knowing a specific Greek word.

## Files to Modify

### OT Integration
- `peshitta_roots/corpus.py` — load second CSV, add testament metadata
- `peshitta_roots/app.py` — pass testament info to templates, add filter params
- `peshitta_roots/templates/browse.html` — testament toggle
- `peshitta_roots/templates/read.html` — OT books in selector, optgroup
- `peshitta_roots/templates/index.html` — NT/OT badges on references
- `data/i18n.json` — new keys: "All", "New Testament", "Old Testament", OT book names

### Greek Concordance
- `peshitta_roots/app.py` — `_build_greek_index()`, `/api/greek-concordance` route
- `peshitta_roots/templates/index.html` — new search tab + results panel + JS
- `peshitta_roots/static/style.css` — greek concordance result cards
- `data/i18n.json` — new keys for Greek tab labels

## Not In Scope

- OT translations (English, Spanish, etc.) — add later
- Word-level Greek-Syriac alignment — future enhancement
- New cognate entries for OT-only roots — enrichment task, not blocking
- Hebrew OT parallel text — future, similar to SBLGNT integration

## Verification

1. Search for SH-L-M → results show both NT and OT occurrences, tagged
2. Browse with OT filter → shows only OT roots
3. Reader → select Psalms 23 → Syriac + transliteration, no translation
4. Click word in OT reader → root modal works, shows OT + NT occurrences
5. Greek tab → search βασιλεύς → shows M-L-K with stats
6. Greek browse → alphabetical list of all Greek lemmas
7. Co-occurrence search → finds roots co-occurring across testaments
