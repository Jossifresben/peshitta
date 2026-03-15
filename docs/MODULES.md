# Python Modules Reference

## characters.py — Transliteration & Script Handling

The foundational module. All other modules depend on it for character mapping and parsing.

### Constants

| Name | Type | Description |
|------|------|-------------|
| `SYRIAC_CONSONANTS` | frozenset | 22 Syriac letters (ܐ through ܬ, U+0710–U+072C) |
| `WEAK_LETTERS` | frozenset | ܐ, ܘ, ܝ — can be root consonants or vowel markers |
| `PROCLITIC_LETTERS` | frozenset | ܕ, ܘ, ܒ, ܠ — particles that attach to words |

### Transliteration Maps

| Map | Direction | Example |
|-----|-----------|---------|
| `SYRIAC_TO_LATIN` | ܟ → k, ܫ → sh | Basic Latin transliteration |
| `LATIN_TO_SYRIAC` | k → ܟ, sh → ܫ | User input parsing (handles digraphs) |
| `SYRIAC_TO_ACADEMIC` | ܟ → k, ܬ → ṯ | Scholarly notation with diacritics |
| `SYRIAC_TO_HEBREW` | ܟ → כ, ܫ → ש | 22 Syriac → 22 Hebrew characters |
| `SYRIAC_TO_ARABIC` | ܟ → ك, ܫ → ش | 22 Syriac → Arabic characters |
| `HEBREW_TO_LATIN` | כ → k | For cognate word input parsing |
| `ARABIC_TO_LATIN` | ك → k | For cognate word input parsing |

### Functions

**`parse_root_input(user_input: str) -> str | None`**
Parses user input into a 3-letter Syriac root. Accepts:
- Dash-separated Latin: `K-TH-B`
- Space-separated Latin: `K TH B`
- Plain Latin: `KTB` (with digraph detection)
- Hebrew script: `כתב`
- Arabic script: `كتب`
- Syriac script: `ܟܬܒ`

Returns `None` if input doesn't resolve to exactly 3 consonants.

**`transliterate_syriac(text: str) -> str`** — Syriac → Latin lowercase
**`transliterate_syriac_academic(text: str) -> str`** — Syriac → scholarly notation
**`transliterate_syriac_to_hebrew(text: str) -> str`** — Syriac → Hebrew script
**`transliterate_syriac_to_arabic(text: str) -> str`** — Syriac → Arabic script
**`transliterate_hebrew(text: str) -> str`** — Hebrew → Latin
**`transliterate_arabic(text: str) -> str`** — Arabic → Latin

**`detect_script(text: str) -> str`** — Returns `'hebrew'`, `'arabic'`, `'syriac'`, or `'latin'` based on Unicode ranges.

**`strip_diacritics(text: str) -> str`** — Removes Hebrew niqqud (U+0591–U+05BD, U+05BF–U+05C7) and Arabic tashkil (U+0610–U+061A, U+064B–U+065F, U+0670).

**`syriac_consonants_of(word: str) -> str`** — Extracts only consonant characters from a Syriac word.

---

## corpus.py — CSV Parser & Word Indexing

Loads the Syriac NT corpus from CSV and provides word/verse lookup.

### Dataclass: `WordOccurrence`
```python
word: str           # Surface form (e.g., ܟܬܒܐ)
reference: str      # "Matthew 1:1"
book: str           # "Matthew"
chapter: int
verse: int
position: int       # 0-based word position in verse
```

### Class: `PeshittaCorpus`

**Constructor:** `PeshittaCorpus(csv_path: str)`

**Key Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `load()` | None | Parse CSV, build word index and verse index |
| `get_unique_words()` | set[str] | All unique surface forms (~15,261) |
| `get_occurrences(word)` | list[WordOccurrence] | All instances of a word |
| `word_frequency()` | Counter | Word → count mapping |
| `total_words()` | int | Total tokens (~134,000) |
| `total_unique()` | int | Unique forms (~15,261) |
| `get_verse_text(ref)` | str \| None | Full Syriac text of a verse |
| `get_verse_translation(ref, lang)` | str | EN or ES translation (lazy-loads translations.json) |
| `get_adjacent_ref(ref, direction)` | str \| None | Previous (-1) or next (+1) verse reference |

**CSV Format:** `book_order,book,chapter,verse,reference,syriac`

---

## extractor.py — Root Extraction Engine

Processes the corpus to identify triliteral roots and map word forms to them.

### Dataclass: `RootMatch`
```python
form: str                 # Word form (e.g., ܘܕܟܬܒ)
transliteration: str      # Latin transliteration
references: list[str]     # Verse locations
count: int                # Frequency
```

### Dataclass: `RootEntry`
```python
root: str                 # 3-letter Syriac root (e.g., ܟܬܒ)
root_transliteration: str
matches: list[RootMatch]  # All word forms derived from this root
total_occurrences: int    # Sum of all match counts
```

### Class: `RootExtractor`

**Constructor:** `RootExtractor(corpus: PeshittaCorpus, data_dir: str)`

**Key Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `build_index()` | None | Process entire corpus, extract roots, build index |
| `lookup_root(root_syriac)` | RootEntry \| None | Get pre-built root entry |
| `get_all_roots()` | list[RootEntry] | All roots sorted by frequency (descending) |
| `get_root_count()` | int | Number of unique roots (~2,535) |
| `get_root_gloss(root_syriac)` | str | Gloss from known_roots.json |

### Root Extraction Algorithm

For each unique word in the corpus (excluding stopwords):

1. **Direct lookup** — Check if word is a known form in `known_roots.json`
2. **Consonant extraction** — Get consonants from the word
3. **If exactly 3 consonants** — Validate as root candidate
4. **If >3 consonants** — Generate candidate stems via `affixes.generate_candidate_stems()`:
   - Strip proclitics (ܘ, ܕ, ܒ, ܠ, and compounds like ܘܒ, ܘܠ, ܕܒ, etc.)
   - Strip verbal prefixes (ܐܬ, ܡ, ܢ, ܬ, ܐ)
   - Strip suffixes (24+ endings, longest-first)
   - Extract consonants from each candidate stem
   - If 4 consonants → try removing weak letters (ܘ, ܝ)
   - If 2 consonants → try inserting weak letters
5. **Score candidates** — Base 0.5 + 0.4 if known root + 0.1 if minimal stripping
6. **Assign word to highest-scoring root**

---

## affixes.py — Prefix & Suffix Stripping

Provides morphological analysis by stripping Syriac affixes.

### Dataclass: `StrippingResult`
```python
stem: str                       # Remaining stem after stripping
prefixes_removed: list[str]     # Prefixes that were stripped
suffixes_removed: list[str]     # Suffixes that were stripped
```

### Affix Categories

| Category | Count | Examples |
|----------|-------|---------|
| Single proclitics | 4 | ܘ (and), ܕ (of/that), ܒ (in), ܠ (to) |
| Compound proclitics | 8 | ܘܒ (and-in), ܘܠ (and-to), ܕܒ, ܕܠ, etc. |
| Verbal prefixes | 6 | ܐܬ (Ethpeel), ܡ (participle), ܢ (3ms impf), ܬ, ܐ |
| Suffixes | 24+ | Pronominal, state, number, aspect markers |

### Key Function

**`generate_candidate_stems(word: str) -> list[StrippingResult]`**

Generates all valid stem candidates by trying all combinations of proclitic + verbal prefix + suffix stripping. Minimum stem length: 2 consonants.

---

## cognates.py — Hebrew/Arabic Cognate Lookup

Maps Syriac roots to their Hebrew and Arabic cognates with bilingual glosses.

### Dataclass: `CognateWord`
```python
word: str                 # Script form (e.g., כָּתַב or كَتَبَ)
transliteration: str      # Latin (e.g., "katav" or "kataba")
meaning_es: str           # Spanish meaning
meaning_en: str           # English meaning
```

### Dataclass: `CognateEntry`
```python
root_syriac: str          # Syriac root (e.g., ܟܬܒ)
gloss_es: str             # Root meaning in Spanish
gloss_en: str             # Root meaning in English
hebrew: list[CognateWord]
arabic: list[CognateWord]
```

### Class: `CognateLookup`

**Constructor:** `CognateLookup(data_dir: str)`

**Key Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `load()` | None | Parse cognates.json, build reverse indexes |
| `lookup(root_syriac)` | CognateEntry \| None | By Syriac root |
| `lookup_by_cognate_word(word)` | list[CognateEntry] | By Hebrew/Arabic word or transliteration |
| `has_cognates(root_syriac)` | bool | Quick existence check |

**Reverse Indexes** (built on load for cognate word search):
- `_hebrew_word_to_keys` — Hebrew script → root keys
- `_hebrew_translit_to_keys` — Hebrew transliteration → root keys
- `_arabic_word_to_keys` — Arabic script → root keys
- `_arabic_translit_to_keys` — Arabic transliteration → root keys

---

## glosser.py — Morphological Glossing & Stem Detection

Composes human-readable glosses for word forms and detects verb stems.

### Gloss Maps

| Map | Examples |
|-----|---------|
| `PROCLITIC_GLOSSES` | ܘ → "and-", ܕ → "of-", ܒ → "in-", ܠ → "to-", ܘܒ → "and-in-" |
| `VERBAL_PREFIX_GLOSSES` | ܐܬ → "[pass]", ܡ → "[ptcp]", ܢ → "[impf]" |
| `SUFFIX_GLOSSES` | Various pronominal, state, and number suffixes |

### Verb Stem Detection

**`detect_verb_stem(prefixes, suffixes, stem, root) -> str | None`**

| Stem | Detection Rule |
|------|---------------|
| Eshtaphal | ܐܫܬ prefix |
| Ethpeel | ܐܬ prefix |
| Aphel | ܐ prefix + stem matches root consonants |
| Peal | No verbal prefix + root consonants match |
| None | Ambiguous, or form is nominal (emphatic ܐ suffix, plural ܝܢ, abstract ܘܬܐ) |

### Class: `WordGlosser`

**Constructor:** `WordGlosser(cognate_lookup, extractor, data_dir)`

**Key Methods:**

| Method | Returns | Description |
|--------|---------|-------------|
| `gloss(form, root_syriac, lang)` | str | Full composed gloss (e.g., "and-of-write") |
| `get_stem(form, root_syriac)` | str \| None | Verb stem label |

**Glossing Algorithm:**
1. Check `word_glosses_override.json` for exact match → return if found
2. Get root meaning from cognates or known_roots
3. Generate candidate parses via `affixes.generate_candidate_stems()`
4. Find best parse (one whose consonants match the root)
5. Compose: prefix glosses + root meaning + suffix glosses
