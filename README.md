# Peshitta Triliteral Root Finder

A bilingual (Spanish/English) web application for researching the Syriac Peshitta New Testament through its triliteral root system. Enter a Syriac root in simplified Latin transliteration and find every word form and verse occurrence in the 22-book traditional canon, along with Hebrew and Arabic cognates, semantic outlier detection, and interactive cross-root semantic bridges.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Root search** — Enter a triliteral root (e.g., `K-T-B`) and find all derived word forms across 7,440 verses
- **Semitic sound correspondence** — Searching `S-L-M` automatically finds `SH-L-M` (Arabic س ↔ Hebrew/Syriac שׁ and other regular correspondences)
- **Dual transliteration** — Academic (š, ḥ, ṭ, ṣ, ʾ, ʿ) and simplified Latin shown side by side
- **Verse popup** — Click any reference to view the full Syriac verse with word highlighting, transliterations, and English/Spanish translations (WEB + Reina Valera 1909)
- **Hebrew & Arabic cognates** — 397 root entries with 3,780 cognate words
- **Semantic outlier detection** — AI-powered identification of 651 cognates that have drifted semantically from their root's core meaning
- **Semantic bridges** — 363 cross-root connections showing how an outlier word's meaning belongs to another root family (click to expand in visualizer)
- **Root family visualizer** — Interactive D3.js force-directed graph showing root families with Hebrew, Arabic, and Syriac cognates; fullscreen mode
- **Autocomplete** — Type-ahead suggestions with automatic dash insertion
- **Bilingual UI** — Full interface in Spanish (default) and English
- **Peshitta Reader** — Interlinear chapter reader with clickable words for root lookup
- **Collapsible transliteration reference** — 22-letter Syriac alphabet table for input guidance

## Transliteration Input

Dashes are inserted automatically as you type. Special mappings:

| Syriac | Input | Letter |
|--------|-------|--------|
| ܚ | `KH` | Heth |
| ܫ | `SH` | Shin |
| ܬ | `TH` | Taw |
| ܨ | `TS` | Sadhe |
| ܥ | `E` or `O` | Ayin |
| ܐ | `A` | Alaph |

All other letters use their standard Latin equivalent (B, G, D, H, W, Z, T, Y, K, L, M, N, S, P, Q, R).

### Semitic Sound Correspondences

The app automatically resolves cross-language consonant equivalences when searching:

| You type | Finds | Correspondence |
|----------|-------|----------------|
| S-L-M | SH-L-M (peace) | Arabic س → Syriac/Hebrew שׁ |
| S-M-E | SH-M-E (hear) | Arabic س → Syriac/Hebrew שׁ |
| TH-Q-N | T-Q-N | Arabic ث → Syriac ܛ |

Supported pairs: S ↔ SH, TH ↔ T, D ↔ TH, TS ↔ S.

## Quick Start

### Requirements

- Python 3.11+
- Flask 3.0+

### Installation

```bash
# Clone the repository
git clone https://github.com/Jossifresben/peshitta.git
cd peshitta

# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python -m peshitta_roots
```

The app will start on `http://localhost:8080` and open your browser automatically.

## Project Structure

```
peshitta/
├── README.md
├── requirements.txt
├── syriac_nt_traditional22_unicode.csv   # Corpus: 7,440 verses, UTF-8 Syriac
├── data/
│   ├── cognates.json          # 397 roots, 3,780 cognates, 651 outliers, 363 bridges
│   ├── i18n.json              # Spanish & English UI translations
│   ├── known_roots.json       # Curated root dictionary with glosses
│   ├── stopwords.json         # Function words excluded from indexing
│   └── translations.json      # Verse translations (WEB + RV1909 + Hebrew + Arabic)
├── peshitta_roots/
│   ├── __init__.py
│   ├── __main__.py            # CLI entry point
│   ├── app.py                 # Flask routes and API endpoints
│   ├── affixes.py             # Syriac prefix/suffix stripping
│   ├── characters.py          # Transliteration maps, parsing, sound correspondences
│   ├── cognates.py            # Cognate lookup engine with outlier/bridge support
│   ├── corpus.py              # CSV parser and word index
│   ├── extractor.py           # Root extraction engine
│   ├── glosser.py             # Morphological glossing & stem detection
│   ├── static/
│   │   ├── style.css
│   │   ├── logo.svg
│   │   └── favicon.svg
│   └── templates/
│       ├── index.html         # Main search page
│       ├── browse.html        # Browse all roots
│       ├── read.html          # Interlinear chapter reader
│       ├── visualize.html     # D3.js root family visualizer
│       └── help.html          # Help & documentation page
├── scripts/
│   ├── expand_cognates.py     # Batch expand Hebrew/Arabic cognates via Claude API
│   ├── tag_outliers.py        # AI-powered semantic outlier detection
│   ├── generate_bridges.py    # Generate cross-root semantic bridges via Claude API
│   ├── fix_bridge_concepts.py # Fix mismatched bridge concept text
│   └── fetch_translations.py  # Utility to download Bible translations
└── docs/
    ├── API.md                 # API reference
    ├── ARCHITECTURE.md        # Architecture overview
    ├── DATA.md                # Data files reference
    ├── DEVELOPMENT.md         # Development guide
    ├── FRONTEND.md            # Frontend reference
    └── MODULES.md             # Python modules reference
```

## API Endpoints

### `GET /`
Main search page. Query parameters:
- `q` — Root in Latin transliteration (e.g., `K-T-B`)
- `lang` — Language: `es` (default) or `en`

### `GET /visualize/<root_key>`
Interactive D3.js root family visualizer with semantic bridges.

### `GET /api/verse`
Returns verse data as JSON.
- `ref` — Verse reference (e.g., `Matthew 1:1`)
- `lang` — Language for translations

### `GET /api/root-family`
Returns full root family data for the visualizer, including cognates, outliers, and semantic bridges.
- `root` — Root key (e.g., `K-TH-B` or `S-L-M`)

### `GET /api/suggest`
Autocomplete suggestions.
- `prefix` — Partial root input (e.g., `K-T`)

## Corpus

The corpus is a UTF-8 Unicode Syriac dataset derived from the ETCBC/syrnt plain-text corpus, restricted to the traditional 22-book Peshitta NT canon:

Matthew, Mark, Luke, John, Acts, Romans, 1–2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1–2 Thessalonians, 1–2 Timothy, Titus, Philemon, Hebrews, James, 1 Peter, 1 John.

**Important:** This is NOT a diplomatic transcription of the Khabouris manuscript. It is a Unicode Syriac dataset for search, NLP, and indexing purposes.

## Verse Translations

- **English:** World English Bible (WEB) — public domain
- **Spanish:** Reina Valera 1909 — public domain
- **Hebrew:** Hebrew Modern translation
- **Arabic:** Smith & Van Dyke (SVD)

## Stats

- **2,535** unique triliteral root patterns extracted
- **397** roots with Hebrew/Arabic cognate data
- **3,780** cognate words (1,929 Hebrew + 1,851 Arabic)
- **651** semantic outliers detected via AI
- **363** semantic bridges across 207 root families
- **15,261** unique surface word forms
- **7,440** verses across 22 books

## License

MIT
