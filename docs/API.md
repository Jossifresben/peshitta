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
| `script` | string | `latin` | Transliteration script: `latin`, `hebrew`, or `arabic` |

**Behavior:**
- If `q` is provided: parse as root, show word forms + cognates
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
| `script` | string | `latin` | Transliteration script |
| `page` | int | `1` | Page number (50 roots per page) |

---

## JSON APIs

### `GET /api/verse` — Verse Lookup

Returns verse text with word-level data for the modal viewer.

**Query Parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `ref` | string | required | Verse reference (e.g., `Matthew 1:1`) |
| `lang` | string | `es` | Language for book name translation |
| `script` | string | `latin` | Transliteration script |

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
