# Development Guide

## Prerequisites

- Python 3.11+
- pip

## Local Setup

```bash
# Clone
git clone https://github.com/Jossifresben/peshitta.git
cd peshitta

# Install dependencies
pip install -r requirements.txt

# Run locally
python3 -m flask --app peshitta_roots.app run --port 5003
```

The app will be available at `http://localhost:5003`.

**Port note:** Avoid port 5000 on macOS — it conflicts with the ControlCenter service.

## Alternative: CLI Mode

```bash
python3 -m peshitta_roots
```

This opens a browser window automatically (uses port 8080).

## Claude Code Preview Server

The project includes `.claude/launch.json` for Claude Code's preview server:

```json
{
  "configurations": [
    {
      "name": "peshitta",
      "runtimeExecutable": "python3",
      "runtimeArgs": ["-m", "flask", "--app", "peshitta_roots.app", "run", "--port", "5003"],
      "port": 5003
    }
  ]
}
```

## Deployment (Render.com)

The app deploys automatically to Render on push to `main`.

**Config:** `render.yaml`
```yaml
services:
  - type: web
    name: peshitta-root-finder
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn peshitta_roots.app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.6"
```

**Deploy workflow:**
```bash
git add <files>
git commit -m "message"
git push origin main
# Render auto-deploys from main branch
```

**Free tier note:** Render free tier spins down after inactivity. First request after idle period may take 30-60 seconds (cold start).

## Project Conventions

### Languages
- Default UI language: Spanish (`lang=es`)
- Toggle to English via `lang=en`
- All user-facing strings go through `data/i18n.json`

### Transliteration
- Default script: Latin (`script=latin`)
- Options: `latin`, `syriac`, `hebrew`, `arabic`
  - `latin` — ABC (standard Latin letters, digraphs SH/KH/TH/TS)
  - `syriac` — uses `transliterate_syriac_academic()` (scholarly ʾbg notation with diacritics)
  - `hebrew` — Hebrew script (אבג)
  - `arabic` — Arabic script (ابج)
- Persisted in `localStorage('script')` on client side
- Passed as `script` query parameter to server

### Translation Language
- Default: follows UI language (`trans` defaults to `lang`)
- Options: `en` (English), `es` (Spanish), `he` (Hebrew Modern), `ar` (Arabic SVD)
- Persisted in `localStorage('trans')` on client side
- Passed as `trans` query parameter to server
- RTL support for `he` and `ar` translations

### Root Format
- Internal: Syriac Unicode (e.g., `ܟܬܒ`)
- Display: Dash-separated Latin uppercase (e.g., `K-TH-B`)
- Digraphs: `SH`, `KH`, `TH`, `TS` (always treated as single consonants)

### Adding New Data

**To add cognates:**
Edit `data/cognates.json`. Add entries under `roots` with key in lowercase dash-separated Latin (e.g., `sh-l-m`). Include `root_syriac`, bilingual glosses, and Hebrew/Arabic cognate words.

**To add word gloss overrides:**
Edit `data/word_glosses_override.json`. Add the Syriac word form as key with `en` and `es` glosses. These override the algorithmic glosser.

**To add known roots:**
Edit `data/known_roots.json`. Add the Syriac root under `roots` with a `gloss` and list of known `forms`. This improves extraction accuracy.

**To add UI translations:**
Edit `data/i18n.json`. Add the key to both `es` and `en` sections.

## Data Pipeline Scripts

Scripts in `/scripts` are batch tools for generating and maintaining cognate data. They require the `anthropic` Python package and a valid `ANTHROPIC_API_KEY`.

### expand_cognates.py
Expands Hebrew and Arabic cognate words for all roots using Claude API. Adds derived forms, related words, and additional meanings. Includes checkpoint saves (every 20 roots) and retry logic for API errors.

```bash
python scripts/expand_cognates.py              # Process all roots
python scripts/expand_cognates.py --dry-run    # Preview only
```

### tag_outliers.py
Uses Claude AI to identify semantic outliers — cognate words that share the triliteral root but have drifted in meaning from the root's core semantic field. Tags words with `"outlier": true` in cognates.json.

```bash
python scripts/tag_outliers.py                 # Process all roots
python scripts/tag_outliers.py --dry-run       # Preview only
python scripts/tag_outliers.py --root r-w-kh   # Single root
```

### generate_bridges.py
For each outlier word, asks Claude which OTHER root in our database has the outlier's meaning as its CORE meaning, creating semantic bridges between root families. Validates that target roots exist in cognates.json.

```bash
python scripts/generate_bridges.py             # Process all outliers
python scripts/generate_bridges.py --dry-run   # Preview only
python scripts/generate_bridges.py --root r-w-kh  # Single root
```

### fix_bridge_concepts.py
Fixes bridge entries where the `target_root` doesn't match the `bridge_concept_en/es` text (caused by the fallback mechanism selecting an alternative root after the concept text was generated).

```bash
python scripts/fix_bridge_concepts.py          # Fix all mismatches
python scripts/fix_bridge_concepts.py --dry-run  # Preview only
```

### generate_greek_parallels.py
Generates `greek_parallel` (translation degradation) data for each root. Uses Claude Haiku to produce the Greek NT equivalent and a prose analysis of what semantic nuance was lost in the Aramaic -> Greek -> modern translation chain.

```bash
python scripts/generate_greek_parallels.py             # Process all
python scripts/generate_greek_parallels.py --dry-run   # Preview prompt
python scripts/generate_greek_parallels.py --root r-w-kh  # Single root
```

### generate_sabor_raiz.py
Generates `sabor_raiz_es` / `sabor_raiz_en` (semantic field summary) for each root. Uses Claude Haiku to produce a poetic 3-5 word phrase capturing the root's semantic field from its gloss and cognate meanings.

```bash
python scripts/generate_sabor_raiz.py             # Process all
python scripts/generate_sabor_raiz.py --dry-run   # Preview prompt
python scripts/generate_sabor_raiz.py --root sh-l-m  # Single root
```

### generate_hebrew_parallels.py
Generates `hebrew_parallel` (translation shift) data for each root. Uses Claude Opus to analyze what shifts when Hebrew is rendered into its Aramaic sister language (Peshitta OT).

```bash
python scripts/generate_hebrew_parallels.py             # Process all
python scripts/generate_hebrew_parallels.py --dry-run   # Preview prompt
python scripts/generate_hebrew_parallels.py --root kh-k-m  # Single root
```

### generate_new_cognates.py
Generates cognate entries for Syriac roots that have no cognates yet. Sends batches of uncovered roots to Claude, which filters out non-roots (particles, proper nouns, pronouns) and generates Hebrew and Arabic cognates for genuine triliteral roots.

```bash
python scripts/generate_new_cognates.py             # Process all
python scripts/generate_new_cognates.py --dry-run   # Preview
```

### convert_ot_text.py
Converts ETCBC/Peshitta plain text files to CSV format matching the NT corpus structure.

```bash
python scripts/convert_ot_text.py /tmp/etcbc-peshitta/plain/0.2 --books Proverbs
python scripts/convert_ot_text.py /tmp/etcbc-peshitta/plain/0.2  # All books
```

### fetch_ot_translations.py
Fetches public domain Bible translations (WEB English, Reina-Valera 1909 Spanish) for OT books via bible.helloao.org and merges them into the translations JSON.

```bash
python scripts/fetch_ot_translations.py                # All 4 books, both languages
python scripts/fetch_ot_translations.py --books Psalms  # Single book
```

### Other utility scripts

- **dedup_cognates.py** — Removes duplicate Hebrew/Arabic entries from cognates.json.
- **flag_modern_hebrew.py** — Flags and removes modern Israeli Hebrew forms not attested in BDB.
- **apply_priority1_fixes.py** — Applies Priority 1 corrections from BDB/Lane/Payne audits to cognates.json.
- **fetch_translations.py** — Fetches WEB (English) and RV1909 (Spanish) translations for the Peshitta 22-book NT canon.
