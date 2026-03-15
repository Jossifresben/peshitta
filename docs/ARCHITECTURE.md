# Architecture Overview

## What This App Does

The **Peshitta Triliteral Root Finder** is a bilingual (Spanish/English) Flask web app for searching and analyzing triliteral roots in the Syriac Peshitta New Testament. Users can search by Syriac root (in Latin, Hebrew, or Arabic transliteration), or by a cognate word in Hebrew/Arabic. The app shows all word forms derived from that root, their verse references, glosses, verb stems, and cognate words in Hebrew and Arabic.

## Project Structure

```
peshitta/
├── peshitta_roots/              # Python package
│   ├── __init__.py
│   ├── __main__.py              # CLI entry point (opens browser)
│   ├── app.py                   # Flask routes & initialization
│   ├── characters.py            # Transliteration maps & script detection
│   ├── corpus.py                # CSV parser & word indexing
│   ├── extractor.py             # Root extraction engine
│   ├── affixes.py               # Prefix/suffix stripping rules
│   ├── cognates.py              # Hebrew/Arabic cognate lookup
│   ├── glosser.py               # Morphological glossing & stem detection
│   ├── templates/
│   │   ├── index.html           # Main search page (689 lines)
│   │   └── browse.html          # Browse all roots (170 lines)
│   └── static/
│       └── style.css            # Full CSS with dark/light themes (1,173 lines)
├── data/
│   ├── i18n.json                # UI translations (ES/EN)
│   ├── cognates.json            # 284 roots with Hebrew/Arabic cognates
│   ├── known_roots.json         # Curated root dictionary with glosses
│   ├── stopwords.json           # Function words to exclude
│   ├── translations.json        # EN/ES verse translations (7,440 verses)
│   └── word_glosses_override.json  # 1,015 manual gloss overrides
├── syriac_nt_traditional22_unicode.csv  # Source corpus (7,440 verses)
├── scripts/
│   └── fetch_translations.py    # Utility to fetch translations
├── requirements.txt             # flask>=3.0, gunicorn>=21.2
├── render.yaml                  # Render.com deployment config
└── docs/                        # This documentation
```

## Module Dependency Graph

```
app.py (Flask routes, initialization)
├── characters.py    (transliteration, parsing, script detection)
├── corpus.py        (CSV loading, word indexing, verse lookup)
├── extractor.py     (root extraction from corpus)
│   ├── characters.py
│   ├── corpus.py
│   └── affixes.py   (prefix/suffix stripping rules)
│       └── characters.py
├── cognates.py      (Hebrew/Arabic cognate lookup)
│   └── characters.py
└── glosser.py       (morphological glossing, stem detection)
    ├── affixes.py
    └── characters.py
```

## Data Flow

### Initialization (lazy, thread-safe, on first request)

```
_init()
  ├── Load i18n.json → _i18n dict
  ├── Load CSV → PeshittaCorpus (builds word index, verse index)
  ├── RootExtractor.build_index()
  │   ├── Load known_roots.json (curated roots + forms)
  │   ├── Load stopwords.json
  │   ├── For each unique word in corpus:
  │   │   ├── Skip stopwords
  │   │   ├── Try direct lookup in known forms
  │   │   ├── Extract consonants → if 3, candidate root
  │   │   ├── If >3 consonants → strip affixes → re-extract
  │   │   ├── Score candidates (known root bonus)
  │   │   └── Assign word to best root
  │   └── Sort roots by total frequency
  ├── Load cognates.json → CognateLookup (builds reverse indexes)
  └── Initialize WordGlosser (loads word_glosses_override.json)
```

### Request Flow: Root Search (`GET /?q=K-TH-B&lang=es&script=latin`)

```
1. parse_root_input("K-TH-B") → ܟܬܒ (Syriac Unicode)
2. extractor.lookup_root(ܟܬܒ) → RootEntry with all word forms
3. cognate_lookup.lookup(ܟܬܒ) → CognateEntry (Hebrew כתב, Arabic كتب)
4. For each word form:
   ├── glosser.gloss(form, root, lang) → composed gloss string
   ├── glosser.get_stem(form, root) → verb stem label or None
   └── transliterate per selected script
5. Render index.html with results
```

### Request Flow: Verse Modal (`GET /api/verse?ref=Matthew+1:1&lang=es&script=hebrew`)

```
1. corpus.get_verse_text("Matthew 1:1") → Syriac text
2. Split into words → transliterate each (academic + script-specific)
3. corpus.get_verse_translation(ref, 'en'/'es')
4. corpus.get_adjacent_ref(ref, ±1) → prev/next verse refs
5. Translate book name via i18n book_names
6. Return JSON → modal JS renders with word highlighting
```

## Global State & Thread Safety

All heavy objects are initialized once and shared across requests:

```python
_corpus: PeshittaCorpus          # ~134k words indexed
_extractor: RootExtractor        # ~2,535 roots indexed
_cognate_lookup: CognateLookup   # 284 cognate entries
_glosser: WordGlosser            # 1,015 override entries
_i18n: dict                      # UI translations
_initialized: bool               # Guard flag
_init_lock: threading.Lock()     # Double-checked locking
```

The `_init()` function uses double-checked locking:
- Fast path: if `_initialized` is True, return immediately (no lock)
- Slow path: acquire lock, check again, then initialize

## Key Corpus Statistics

| Metric | Value |
|--------|-------|
| Books | 22 (traditional Peshitta NT canon) |
| Verses | 7,440 |
| Total word tokens | ~134,000 |
| Unique surface forms | ~15,261 |
| Extracted triliteral roots | ~2,535 |
| Cognate entries | 284 |
| Manual gloss overrides | 1,015 |
| Known/curated roots | ~200 |
