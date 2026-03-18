# Architecture Overview

## What This App Does

The **Peshitta Triliteral Root Finder** is a bilingual (Spanish/English) Flask web app for searching and analyzing triliteral roots in the Syriac Peshitta New Testament. Users can search by Syriac root (in Latin, Hebrew, Arabic, or Syriac academic transliteration), or by a cognate word in Hebrew/Arabic. The app shows all word forms derived from that root, their verse references, glosses, verb stems, and cognate words in Hebrew and Arabic. It also includes an interlinear chapter reader (`/read`) with clickable word-level root lookup, a D3.js root family visualizer (`/visualize/<root>`), a passage constellation viewer (`/constellation`), a methodology page (`/methodology`), and an about page (`/about`). Translations are available in four languages: English, Spanish, Hebrew Modern, and Arabic SVD.

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
│   │   ├── base.html            # Shared layout: header, nav, dark mode, settings, footer blocks
│   │   ├── index.html           # Main search page
│   │   ├── browse.html          # Browse all roots
│   │   ├── read.html            # Interlinear chapter reader
│   │   ├── visualize.html       # D3.js root family visualizer with semantic bridges
│   │   ├── constellation.html   # Passage constellation: multi-verse root network graph
│   │   ├── methodology.html     # Semitic exegesis methodology description
│   │   ├── about.html           # Author bio, photo, and project links
│   │   └── help.html            # Help & documentation page
│   └── static/
│       ├── style.css            # Full CSS with dark/light themes, visualizer, reader & RTL styles
│       └── js/
│           └── global.js        # Shared JS: dark mode toggle, settings dropdown, share modal
├── data/
│   ├── i18n.json                # UI translations (ES/EN)
│   ├── cognates.json            # 394 roots with cognates, greek parallels, sabor raiz, paradigmatic notes
│   ├── known_roots.json         # Curated root dictionary with glosses
│   ├── stopwords.json           # Function words to exclude
│   ├── translations.json        # EN/ES/HE/AR verse translations (7,440 verses x 4 langs)
│   └── word_glosses_override.json  # 1,015 manual gloss overrides
├── syriac_nt_traditional22_unicode.csv  # Source corpus (7,440 verses)
├── scripts/
│   ├── expand_cognates.py       # Batch expand Hebrew/Arabic cognates via Claude API
│   ├── tag_outliers.py          # AI-powered semantic outlier detection
│   ├── generate_bridges.py      # Generate cross-root semantic bridges via Claude API
│   ├── fix_bridge_concepts.py   # Fix mismatched bridge concept text
│   ├── fetch_translations.py    # Utility to fetch translations
│   ├── generate_sabor_raiz.py   # Generate "sabor de raiz" flavor text for roots
│   ├── generate_greek_parallels.py  # Generate Greek parallel & translation degradation data
│   ├── generate_hebrew_parallels.py # Generate Hebrew parallel data
│   ├── generate_new_cognates.py # Add new cognate entries
│   ├── apply_priority1_fixes.py # Apply priority 1 cognate audit corrections
│   ├── dedup_cognates.py        # Remove duplicate cognate words
│   ├── flag_modern_hebrew.py    # Flag modern Hebrew words in cognates
│   ├── convert_ot_text.py       # Convert OT text format
│   └── fetch_ot_translations.py # Fetch OT translations
├── fetch_arabic.py              # Script to fetch Arabic SVD from getBible API
├── fetch_hebrew.py              # Script to import Hebrew Modern from he_modern.json
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
├── cognates.py      (Hebrew/Arabic cognate lookup, outliers, semantic bridges)
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
  │   Each root entry may include:
  │   ├── gloss_es/en, root_syriac
  │   ├── hebrew[], arabic[] (cognate words, with outlier flags)
  │   ├── semantic_bridges {} (cross-root connections)
  │   ├── sabor_raiz_es/en (evocative root "flavor" description)
  │   ├── greek_parallel {} (word, transliteration, aramaic/greek semantic ranges, lost-in-translation)
  │   ├── paradigmatic_ref (key verse override)
  │   └── paradigmatic_note_es/en (exegetical note for the key verse)
  └── Initialize WordGlosser (loads word_glosses_override.json)
```

### Request Flow: Root Search (`GET /?q=K-TH-B&lang=es&script=latin`)

```
1. parse_root_input("K-TH-B") → ܟܬܒ (Syriac Unicode)
2. extractor.lookup_root(ܟܬܒ) → RootEntry with all word forms
3. cognate_lookup.lookup(ܟܬܒ) → CognateEntry (Hebrew כתב, Arabic كتب)
   - If not found: try semitic_root_variants() (e.g., S-L-M → SH-L-M)
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
3. corpus.get_verse_translation(ref, 'en'/'es'/'he'/'ar')
4. corpus.get_adjacent_ref(ref, ±1) → prev/next verse refs
5. Translate book name via i18n book_names
6. Return JSON → modal JS renders with word highlighting
```

### Request Flow: Reader (`GET /read?book=Matthew&chapter=1&trans=he`)

```
1. corpus.get_books() → list of (book_name, chapter_count)
2. corpus.get_chapter_verses(book, chapter) → list of (verse_num, syriac_text, reference)
3. For each verse: transliterate, get translation in selected lang
4. extractor.lookup_word_root(word) → root for hover tooltip
5. Render read.html with interlinear display
```

### Request Flow: Constellation (`GET /constellation?book=Matthew&chapter=1&v_start=1&v_end=5`)

```
1. Render constellation.html with book, chapter, verse range params
2. Client JS calls GET /api/passage-constellation with same params
3. Server collects verses in range:
   ├── For each verse: split into words, look up each word's root
   └── Collect translations in selected language
4. Build root map: unique roots with frequency counts & word forms
5. For each root:
   ├── Look up cognates (Hebrew, Arabic, outliers)
   ├── Look up semantic bridges
   └── Detect inter-root connections:
       ├── Semantic bridges between roots in the passage
       └── Sister roots (2 of 3 shared consonants)
6. Return JSON: verses, roots (sorted by frequency), connections
7. Client renders D3.js force-directed graph
```

### Request Flow: Methodology (`GET /methodology`)

```
1. Detect language, load i18n translations
2. Render methodology.html (static content page using base.html layout)
```

### Request Flow: About (`GET /about`)

```
1. Detect language, load i18n translations
2. Render about.html (author bio, photo, project links using base.html layout)
```

## Global State & Thread Safety

All heavy objects are initialized once and shared across requests:

```python
_corpus: PeshittaCorpus          # ~134k words indexed
_extractor: RootExtractor        # ~2,535 roots indexed
_cognate_lookup: CognateLookup   # 394 cognate entries with greek parallels, sabor raiz, paradigmatic notes
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
| Cognate entries | 394 |
| Greek parallels | 394 (translation degradation data) |
| Sabor raiz entries | 356 (evocative root flavor descriptions) |
| Paradigmatic notes | 7 (deep exegetical key-verse notes) |
| Manual gloss overrides | 1,015 |
| Known/curated roots | ~200 |
