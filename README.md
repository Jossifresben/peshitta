# Peshitta Triliteral Root Finder

A bilingual (Spanish/English) web application for researching the Syriac Peshitta New Testament through its triliteral root system. Enter a Syriac root in simplified Latin transliteration and find every word form and verse occurrence in the 22-book traditional canon, along with Hebrew and Arabic cognates.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Root search** — Enter a triliteral root (e.g., `K-T-B`) and find all derived word forms across 7,440 verses
- **Dual transliteration** — Academic (š, ḥ, ṭ, ṣ, ʾ, ʿ) and simplified Latin shown side by side
- **Verse popup** — Click any reference to view the full Syriac verse with word highlighting, transliterations, and English/Spanish translations (WEB + Reina Valera 1909)
- **Hebrew & Arabic cognates** — 164 root entries with Semitic cognate data
- **Autocomplete** — Type-ahead suggestions with automatic dash insertion
- **Bilingual UI** — Full interface in Spanish (default) and English
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
│   ├── cognates.json          # 164 Hebrew/Arabic cognate entries
│   ├── i18n.json              # Spanish & English UI translations
│   ├── known_roots.json       # Curated root dictionary with glosses
│   ├── stopwords.json         # Function words excluded from indexing
│   └── translations.json      # Verse translations (WEB + RV1909)
├── peshitta_roots/
│   ├── __init__.py
│   ├── __main__.py            # CLI entry point
│   ├── app.py                 # Flask routes and API endpoints
│   ├── affixes.py             # Syriac prefix/suffix stripping
│   ├── characters.py          # Transliteration maps and parsing
│   ├── cognates.py            # Cognate lookup engine
│   ├── corpus.py              # CSV parser and word index
│   ├── extractor.py           # Root extraction engine
│   ├── static/
│   │   └── style.css
│   └── templates/
│       └── index.html
└── scripts/
    └── fetch_translations.py  # Utility to download Bible translations
```

## API Endpoints

### `GET /`
Main search page. Query parameters:
- `q` — Root in Latin transliteration (e.g., `K-T-B`)
- `lang` — Language: `es` (default) or `en`

### `GET /api/verse`
Returns verse data as JSON.
- `ref` — Verse reference (e.g., `Matthew 1:1`)
- `lang` — Language for translations

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

## Stats

- **2,535** unique triliteral roots extracted
- **15,261** unique surface word forms
- **7,440** verses across 22 books
- **164** root entries with Hebrew/Arabic cognates

## License

MIT
