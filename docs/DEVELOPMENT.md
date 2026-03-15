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
- Options: `latin`, `hebrew`, `arabic`
- Persisted in `localStorage('script')` on client side
- Passed as `script` query parameter to server

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

## Code Review Findings (as of 2026-03-15)

### Fixed
- **DRY violation:** Dash-form builder was duplicated 4 times → consolidated into `_translit_to_dash()`
- **Thread safety:** `_init()` now uses double-checked locking with `threading.Lock()`

### Open (Important, not critical)
- Cached sorted roots (sorted on every call to `get_all_roots()`)
- No `SECRET_KEY` configured (needed if sessions/CSRF ever added)
- No security headers (X-Content-Type-Options, X-Frame-Options, CSP)
- No input length limits on query parameters
- Dependencies not pinned to exact versions in `requirements.txt`
