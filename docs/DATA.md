# Data Files Reference

All data files are in the `/data` directory except the main corpus CSV which is at the project root.

## syriac_nt_traditional22_unicode.csv

The source corpus: the entire Syriac Peshitta New Testament in Unicode.

**Location:** Project root
**Format:** CSV with columns: `book_order,book,chapter,verse,reference,syriac`
**Size:** 7,440 verses across 22 books (traditional Peshitta canon)

**Books included (in order):**
Matthew, Mark, Luke, John, Acts, Romans, 1 Corinthians, 2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1 Thessalonians, 2 Thessalonians, 1 Timothy, 2 Timothy, Titus, Philemon, Hebrews, James, 1 Peter, 1 John

**Note:** The traditional Peshitta canon excludes 2 Peter, 2 John, 3 John, Jude, and Revelation.

**Sample row:**
```
1,Matthew,1,1,Matthew 1:1,ܟܬܒܐ ܕܝܠܝܕܘܬܗ ܕܝܫܘܥ ܡܫܝܚܐ ܒܪܗ ܕܕܘܝܕ ܒܪܗ ܕܐܒܪܗܡ
```

---

## data/i18n.json

UI translations for Spanish and English.

**Structure:**
```json
{
  "es": {
    "app_title": "Buscador de Raíces Trilíteras",
    "app_subtitle": "Explora las raíces...",
    "search_tab_root": "Buscar por Raíz",
    "search_tab_cognate": "Buscar por Cognado",
    "search_placeholder": "ej. K-TH-B (escribir)",
    "search_button": "Buscar",
    "lang_toggle": "English",
    "settings_script": "Transliteración",
    ...
  },
  "en": { ... }
}
```

**Key sections:**
- App chrome (title, subtitle, buttons, labels)
- Search UI (tabs, placeholders, error messages)
- Results UI (section headers, column labels)
- Browse page (pagination, table headers)
- Stats tooltips
- Settings labels (transliteration: 4 options; translation: 4 options)
- Reader page labels
- Book name translations (English → Spanish)
- Verse modal labels

---

## data/cognates.json

Hebrew and Arabic cognates for Syriac roots, with bilingual glosses, semantic outlier flags, and semantic bridges.

**Size:** 397 root entries, 3,780 cognate words (1,929 Hebrew + 1,851 Arabic), 651 outliers, 363 semantic bridges across 207 roots

**Structure:**
```json
{
  "roots": {
    "k-th-b": {
      "root_syriac": "ܟܬܒ",
      "gloss_es": "escribir",
      "gloss_en": "write",
      "hebrew": [
        {
          "word": "כָּתַב",
          "transliteration": "katav",
          "meaning_es": "escribir",
          "meaning_en": "to write",
          "outlier": false
        }
      ],
      "arabic": [
        {
          "word": "كَتَبَ",
          "transliteration": "kataba",
          "meaning_es": "escribir",
          "meaning_en": "to write"
        }
      ],
      "semantic_bridges": {
        "ar:raha": {
          "target_root": "sh-b-th",
          "relationship": "semantic_neighbor",
          "bridge_concept_en": "Rest/comfort connects to SH-B-TH (sabbath, rest)",
          "bridge_concept_es": "Descanso/confort conecta con SH-B-TH (sábado, descansar)"
        }
      }
    }
  }
}
```

**Key format rules:**
- Root keys are lowercase Latin, dash-separated (e.g., `k-th-b`)
- `root_syriac` is the 3-letter Syriac Unicode
- Each root can have multiple Hebrew and Arabic cognate words
- All meanings are bilingual (ES/EN)
- `outlier: true` flags cognates that have drifted semantically from the root's core meaning
- `semantic_bridges` maps outlier keys (e.g., `ar:raha`) to target roots where the outlier's meaning is core

**Semantic bridge fields:**

| Field | Description |
|-------|-------------|
| `target_root` | Root key where the outlier's meaning is central (e.g., `sh-b-th`) |
| `relationship` | One of: `semantic_neighbor`, `antonym_root`, `metonymic_shift`, `functional_drift` |
| `bridge_concept_en` | English explanation of the semantic connection |
| `bridge_concept_es` | Spanish explanation of the semantic connection |

---

## data/known_roots.json

Curated dictionary of Syriac roots with their known word forms and English glosses.

**Size:** ~200 root entries (~657 lines)

**Structure:**
```json
{
  "roots": {
    "ܟܬܒ": {
      "gloss": "write",
      "forms": ["ܟܬܒ", "ܟܬܒܐ", "ܟܬܒܬ", "ܟܬܒܘ", "ܟܬܝܒ"]
    }
  }
}
```

**Purpose:**
- Provides direct form-to-root mappings (bypasses extraction algorithm)
- Supplies fallback glosses when cognates.json doesn't have the root
- The `forms` list is used to build a reverse index for fast word → root lookup
- Roots listed here get a +0.4 scoring bonus during extraction

---

## data/stopwords.json

Function words excluded from root extraction.

**Size:** ~40 entries (~21 lines)

**Structure:**
```json
{
  "particles": ["ܕܝܢ", "ܓܝܪ", "ܐܦ", "ܗܟܝܠ", "ܡܢ"],
  "pronouns": ["ܐܢܐ", "ܐܢܬ", "ܗܘ", "ܗܝ", "ܚܢܢ", "ܐܢܬܘܢ", "ܗܢܘܢ"],
  "prepositions": ["ܒ", "ܕ", "ܘ", "ܠ"],
  "negation": ["ܠܐ"]
}
```

**Purpose:** These words are skipped during root indexing — they're either too short to have meaningful roots, or they're function words that would pollute the root index.

---

## data/translations.json

Verse translations in four languages for all 7,440 verses.

**Size:** Lazy-loaded on first verse request.

**Structure:**
```json
{
  "Matthew 1:1": {
    "en": "The book of the genealogy of Jesus Christ, the son of David, the son of Abraham.",
    "es": "LIBRO de la generación de Jesucristo, hijo de David, hijo de Abraham.",
    "he": "ספר תולדות ישוע המשיח בן דוד בן אברהם",
    "ar": "كتاب ميلاد يسوع المسيح ابن داود ابن ابراهيم"
  },
  "Matthew 1:2": { ... },
  ...
}
```

**Languages:**

| Key | Language | Source | Verses |
|-----|----------|--------|--------|
| `en` | English | World English Bible (WEB) — public domain | 7,440 |
| `es` | Spanish | Reina Valera 1909 — public domain | 7,440 |
| `he` | Hebrew Modern | Hebrew Modern translation | 7,440 |
| `ar` | Arabic | Smith & Van Dyke (SVD) via getBible API | 7,440 |

**RTL support:** Hebrew and Arabic translations are rendered with `direction: rtl` in the UI.

---

## data/word_glosses_override.json

Manual gloss overrides for words that can't be glossed compositionally.

**Size:** 1,015 entries (~1,047 lines)

**Structure:**
```json
{
  "ܐܢܐ": {"en": "I", "es": "yo"},
  "ܗܘ": {"en": "he/it", "es": "él"},
  "ܠܐ": {"en": "not", "es": "no"},
  "ܕܐܢܐ": {"en": "that-I", "es": "que-yo"},
  "ܘܠܐ": {"en": "and-not", "es": "y-no"},
  ...
}
```

**Categories of overrides:**
- Personal pronouns (ܐܢܐ, ܐܢܬ, ܗܘ, ܗܝ, etc.)
- Demonstratives (ܗܢܐ, ܗܕܐ, ܗܠܝܢ)
- Interrogatives (ܡܢ, ܡܢܐ, ܐܝܟܐ)
- Particles and conjunctions
- Preposition + pronoun suffix compounds (ܠܗ, ܒܗ, ܡܢܗ, etc.)
- Compound forms with ܕ-, ܘ-, ܠ-, ܒ- prefixes
- Possessed nouns (ܐܒܘܗܝ "his-father", ܐܡܗ "his-mother")
- Common verb conjugations
- Numbers and proper nouns

**Priority:** These overrides take precedence over the algorithmic glosser. The glosser checks this file first before attempting compositional analysis.
