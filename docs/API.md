# API Reference

All endpoints return HTML or JSON. No authentication required.

## Pages

### `GET /` — Main Search Page

Renders `index.html` with search form and results.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | `""` | Root query in dash-separated Latin (e.g., `K-TH-B`) |
| `cw` | string | `""` | Cognate word search (Hebrew/Arabic script or Latin transliteration) |
| `lang` | string | `es` | UI language: `es` or `en` |
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, `arabic`, or `syriac` |
| `trans` | string | `<lang>` | Translation language: `en`, `es`, `he`, or `ar` (defaults to UI language) |

**Behavior:**
- If `q` is provided: parse as root, show word forms + cognates
  - Semitic sound correspondences are applied automatically (e.g., `S-L-M` finds `SH-L-M`)
- If `cw` is provided (and no `q`): look up cognate word
  - Single match → auto-redirects to root search
  - Multiple matches → shows disambiguation list
  - No matches → error message
- If neither: shows empty search form with stats

---

### `GET /browse` — Browse All Roots

Renders `browse.html` with paginated table of all roots sorted by frequency.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `lang` | string | `es` | UI language |
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, `arabic`, or `syriac` |
| `trans` | string | `<lang>` | Translation language: `en`, `es`, `he`, or `ar` |
| `page` | int | `1` | Page number (50 roots per page) |

**Root column** now displays both Syriac script and Latin transliteration side by side (e.g., `ܗܘܐ H-W-A`).

---

### `GET /read` — Peshitta Reader (Interlinear Chapter Reader)

Renders `read.html` with an interlinear chapter reading view.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `book` | string | `Matthew` | Book name (English) |
| `chapter` | int | `1` | Chapter number |
| `lang` | string | `es` | UI language |
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, `arabic`, or `syriac` |
| `trans` | string | `<lang>` | Translation language: `en`, `es`, `he`, or `ar` |

**Features:**
- Book/chapter navigation with dropdowns and prev/next buttons
- Three lines per verse: Syriac script, transliteration, translation
- Clickable words with root lookup modal (via `/api/word-root`)
- Root hover tooltips showing Latin transliteration (e.g., Y-L-D)

---

### `GET /visualize/<root_key>` — Root Family Visualizer

Renders `visualize.html` with an interactive D3.js force-directed graph.

**URL Parameters:**
- `root_key` — Root in dash-separated Latin (e.g., `R-W-KH`)

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `lang` | string | `es` | UI language |
| `script` | string | `latin` | Transliteration script |
| `trans` | string | `<lang>` | Translation language for cognate meanings |

**Features:**
- Center node: Syriac root with gloss
- Satellite nodes: Hebrew (blue), Arabic (green), Syriac (brown) cognates
- Language toggle checkboxes (Hebrew/Arabic/Syriac)
- Semantic outliers: dashed gold border (plain outliers) or solid gold ring with pulsing glow (bridge outliers)
- Clickable bridge outliers: expand to show target root family with animated gold bridge link
- Fullscreen mode: button in controls bar to enter native fullscreen
- Zoom and drag support

---

### `GET /help` — Help Page

Renders `help.html` with app documentation, capabilities, and stats.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `lang` | string | `es` | UI language |

---

## JSON APIs

### `GET /api/verse` — Verse Lookup

Returns verse text with word-level data for the modal viewer.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `ref` | string | required | Verse reference (e.g., `Matthew 1:1`) |
| `lang` | string | `es` | Language for book name translation |
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, `arabic`, or `syriac` |

**Response (200):**

```json
{
  "reference": "Matthew 1:1",
  "reference_display": "Mateo 1:1",
  "syriac": "ܟܬܒܐ ܕܝܠܝܕܘܬܗ ...",
  "transliteration": "kthba dylydwthh ...",
  "words": ["ܟܬܒܐ", "ܕܝܠܝܕܘܬܗ", "..."],
  "words_translit": ["kthba", "dylydwthh", "..."],
  "words_translit_academic": ["kṯāḇā", "dīlīḏūṯēh", "..."],
  "translation_en": "The book of the genealogy...",
  "translation_es": "LIBRO de la generación...",
  "prev_ref": null,
  "next_ref": "Matthew 1:2",
  "script": "latin"
}
```

**Error Responses:**
- `400`: Missing `ref` parameter
- `404`: Verse not found

---

### `GET /api/suggest` — Autocomplete Suggestions

Returns up to 20 roots matching a Latin-letter prefix.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `prefix` | string | required | Dash-separated prefix (e.g., `K-TH`) |

**Response (200):**

```json
[
  {"root": "ܟܬܒ", "translit": "K-TH-B", "count": 265},
  {"root": "ܟܬܫ", "translit": "K-TH-SH", "count": 10},
  {"root": "ܟܬܢ", "translit": "K-TH-N", "count": 10}
]
```

**Notes:**
- Input `O` is normalized to `E` (both represent Ayin ܥ)
- If user typed `O`, display uses `O` instead of `E`
- Max 20 results

---

### `GET /api/roots` — Paginated Root List

Returns all roots sorted by frequency, paginated.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | `1` | Page number |
| `per_page` | int | `50` | Results per page (max 100) |

**Response (200):**

```json
{
  "page": 1,
  "per_page": 50,
  "total": 2535,
  "total_pages": 51,
  "roots": [
    {
      "root": "ܐܡܪ",
      "translit": "A-M-R",
      "forms": 42,
      "occurrences": 1847,
      "gloss": "say"
    }
  ]
}
```

**Note:** Glosses are English-only in this endpoint (used by browse page which handles language separately).

---

### `GET /api/root-family` — Root Family Data (Visualizer)

Returns full root family data for the D3.js visualizer, including cognates, outliers, and semantic bridges.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `root` | string | required | Root in dash-separated Latin (e.g., `K-TH-B` or `S-L-M`) |
| `lang` | string | `es` | UI language |
| `script` | string | `latin` | Transliteration script |
| `trans` | string | `<lang>` | Translation language for cognate meanings |

**Response (200):**

```json
{
  "root": "ܫܠܡ",
  "root_translit": "SH-L-M",
  "gloss": "peace, complete",
  "sabor_raiz": "peace, complete",
  "syriac_words": [
    {
      "word": "ܫܠܡܐ",
      "translit": "shlma",
      "meaning": "peace",
      "references": ["Matthew 10:13", "..."]
    }
  ],
  "hebrew": [
    {
      "word": "שָׁלוֹם",
      "translit": "shalom",
      "meaning": "peace",
      "outlier": false
    }
  ],
  "arabic": [
    {
      "word": "سَلَام",
      "translit": "salam",
      "meaning": "peace"
    }
  ],
  "semantic_bridges": [
    {
      "outlier_key": "ar:rāwaḥa",
      "target_root": "sh-b-th",
      "relationship": "semantic_neighbor",
      "bridge_concept": "To rest, take ease connects to SH-B-TH (sabbath, rest)"
    }
  ]
}
```

**Notes:**
- Semitic sound correspondences are applied (e.g., `root=s-l-m` resolves to `SH-L-M`)
- `outlier: true` appears only on flagged cognate words
- `semantic_bridges` lists bridges for outlier words that connect to other root families
- The visualizer uses `target_root` to fetch the bridge family via a second `/api/root-family` call

**Error Responses:**
- `400`: Missing `root` parameter
- `400`: Invalid root (can't parse to Syriac)

---

### `GET /api/word-root` — Word Root Lookup

Returns the root for a given Syriac word form (used by the reader's clickable words).

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `word` | string | required | Syriac word form (e.g., `ܟܬܒܐ`) |
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, `arabic`, or `syriac` |

**Response (200):**

```json
{
  "word": "ܟܬܒܐ",
  "root": "ܟܬܒ",
  "root_translit": "K-TH-B"
}
```

**Error Responses:**
- `400`: Missing `word` parameter
- `404`: Root not found for the given word
