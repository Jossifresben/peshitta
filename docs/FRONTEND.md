# Frontend Reference

## Template System

All pages extend `base.html`, which provides a shared layout using Jinja2 block inheritance. The base template includes the sticky header, language/settings/theme/share controls, Google Analytics, font imports, and the global JS bundle.

### Jinja2 Blocks

| Block | Purpose | Default behavior |
|-------|---------|-----------------|
| `title` | Page `<title>` | `{{ t.app_title }}` |
| `head_extra` | Additional `<head>` content (per-page CSS, meta) | Empty |
| `lang_links` | Language toggle links in header dropdown | ES/EN links with `?lang=` params |
| `header_settings` | Settings dropdown (script, translation, Syriac font) | Full settings widget |
| `header_share` | Share button in header | QR/share button |
| `share_modal` | Share modal overlay with QR code and URL copy | Full share modal |
| `content` | Main page body inside `<main>` | Empty |
| `scripts` | Additional `<script>` tags before `</body>` | Empty |

Pages can override any block. For example, `about.html` empties `header_settings`, `header_share`, and `share_modal` since it needs none of those controls.

---

## Templates

### index.html (Main Search Page)

**URL:** `GET /`

**Layout:**

```
+---------------------------------------------+
| [Sticky Header]                             |
|   Lang Toggle | Help | Settings | Theme | Share |
+---------------------------------------------+
| Title + Subtitle                            |
| Stats Bar: Roots | Words | Unique Forms     |
|                                             |
| [Search by Root] [Search by Cognate]        | <- Tabs
| +------------------------------------------+|
| | Search Input + Button                    ||
| | [Transliteration Table toggle]           ||
| +------------------------------------------+|
|                                             |
| Results (when query provided):              |
| +------------------------------------------+|
| | Root Header: KTB K-TH-B "write"         ||
| +------------------------------------------+|
| | Peshitta Panel (word forms table)        ||
| | Hebrew Cognates Panel                    ||
| | Arabic Cognates Panel                    ||
| +------------------------------------------+|
|                                             |
| Footer                                      |
+---------------------------------------------+

+---------------------------------------------+
| [Verse Modal - overlay]                     |
| +------------------------------------------+|
| | [Sticky modal header]                   ||
| | Up-arrow Previous verse                  ||
| | Reference: Mateo 1:1 / Root: K-TH-B     ||
| | Syriac text (RTL, highlighted word)      ||
| | Academic transliteration                 ||
| | Simple transliteration                   ||
| | English translation                      ||
| | Spanish translation                      ||
| | Down-arrow Next verse                    ||
| | [Copy]                                   ||
| +------------------------------------------+|
+---------------------------------------------+
```

**Key JavaScript Features:**

| Feature | Function | Description |
|---------|----------|-------------|
| Tab switching | `switchTab(tab)` | Toggles between root search and cognate search panels |
| Autocomplete | inline listener | Fetches `/api/suggest?prefix=...`, shows dropdown, auto-inserts dashes |
| Dash insertion | inline | Smart parsing of digraphs (SH, KH, TH, TS) in search input |
| Verse modal | `showVerseModal(ref, form)` | Opens modal, fetches `/api/verse`, highlights matched word |
| Modal navigation | arrows in modal | Loads previous/next verses, accumulates up to 4 passages |
| Copy to clipboard | `copyModalContent()` | Formats all visible passages with metadata, copies to clipboard |
| Word highlighting | inline | Matches word form in verse text, wraps in `<mark>` |
| Script switching | settings dropdown | Saves to localStorage, reloads page with `script` param (4 options: latin, syriac, hebrew, arabic) |
| Translation lang | settings dropdown | Saves to localStorage, reloads page with `trans` param (4 options: en, es, he, ar) |
| Dark mode | theme toggle | Saves to localStorage, respects `prefers-color-scheme` |
| Book name translation | `translate_ref()` | Replaces English book names with localized names in references |

**Transliteration Table:**
A toggleable reference grid showing all 22 Syriac consonants with their Latin equivalents. Hidden by default, toggled by clicking the "show/hide" link.

---

### browse.html (Browse All Roots)

**URL:** `GET /browse`

**Layout:**

```
+---------------------------------------------+
| [Sticky Header] (same as index)             |
+---------------------------------------------+
| Title: Browse Roots                         |
| <- Back to Search                           |
|                                             |
| Pagination: <- Prev | Page X of Y | ->     |
| +------------------------------------------+|
| | Root | Translit | Meaning | Forms |      ||
| | -----+----------+---------+-------+      ||
| | AMR  | A-M-R    | say     | 42    |      ||
| | HWA  | H-W-A    | be      | 38    |      ||
| | ...  | ...      | ...     | ...   |      ||
| +------------------------------------------+|
| Pagination (bottom)                         |
| Footer                                      |
+---------------------------------------------+
```

Each root row links to `/?q=<root>&lang=<lang>#results`.

**Root column** shows both Syriac script and Latin transliteration (e.g., `HWA H-W-A`).

---

### visualize.html (Root Family Visualizer)

**URL:** `GET /visualize/<root_key>`

**Layout:**

```
+---------------------------------------------+
| [Sticky Header] (same as other pages)       |
+---------------------------------------------+
| Title: Root Visualizer                      |
| <- Back to results                          |
|                                             |
| [x Hebrew] [x Arabic] [x Syriac]           |
| [o Outlier] [o Bridge] [Fullscreen]         |
|                                             |
| +------------------------------------------+|
| |          D3.js Force Graph               ||
| |                                          ||
| |      [heb]   [ar]                        ||
| |         |       |                        ||
| |      [  CENTER    ]                      ||
| |      [ root+gloss ]                      ||
| |         |       |                        ||
| |      [syr]   [syr]                       ||
| +------------------------------------------+|
| [Tooltip on hover]                          |
+---------------------------------------------+
```

**Key JavaScript Features:**

| Feature | Description |
|---------|-------------|
| D3 force simulation | Radial layout with center root, satellite cognates |
| Language toggles | Checkboxes to show/hide Hebrew, Arabic, Syriac nodes |
| Outlier detection | Dashed gold border on semantic outliers |
| Bridge expansion | Click bridge-outlier -> fetch target root family -> expand graph |
| Bridge collapse | Click again to collapse bridge nodes |
| Bridge visual | Animated gold dashed link, pulsing outer ring on bridge outliers |
| "bridge" label | Text below bridge-outlier nodes |
| Fullscreen | Native Fullscreen API, controls float as overlay |
| Zoom/drag | D3 zoom + node dragging |
| Tooltip | Word details, outlier info, bridge concept on hover |
| Multi-line meaning | Meanings wrap to 2 lines inside bubbles |

**Node types and colors:**

| Type | Color | Radius |
|------|-------|--------|
| center | #8B4513 (brown) | 64 |
| hebrew | #2E5090 (blue) | 52 |
| arabic | #2D7D46 (green) | 52 |
| syriac | #A0522D (terracotta) | 48 |
| bridge-center | #B8860B (dark gold) | 56 |
| bridge-hebrew | #5B7DB8 (light blue) | 46 |
| bridge-arabic | #5BA87A (light green) | 46 |

---

### read.html (Peshitta Reader -- Interlinear Chapter View)

**URL:** `GET /read`

**Layout:**

```
+-------------------------------------------+
| [Sticky Header] (same as other pages)     |
+-------------------------------------------+
| Book dropdown | Chapter dropdown          |
| [< Prev] [Next >]                        |
|                                           |
| Verse 1:                                  |
|   Syriac text (RTL, clickable words)      |
|   Transliteration                         |
|   Translation (in selected language)      |
|                                           |
| Verse 2:                                  |
|   ...                                     |
+-------------------------------------------+
| Footer                                    |
+-------------------------------------------+

+-------------------------------------------+
| [Root Lookup Modal - on word click]       |
|   Word: xxxxxxx                           |
|   Root: xxx (X-X-X)                       |
|   Link to search page                     |
+-------------------------------------------+
```

**Key Features:**
- Book and chapter navigation via dropdowns with prev/next buttons
- Three interlinear lines per verse: Syriac script, transliteration, translation
- Clickable Syriac words trigger root lookup modal (calls `/api/word-root`)
- Root hover tooltips show Latin transliteration (e.g., Y-L-D)
- When `syriac` script is selected, the duplicate transliteration line is hidden (since Syriac is already shown)

---

### constellation.html (Passage Constellation View)

**URL:** `GET /constellation`

**Query params:** `book`, `chapter`, `v_start`, `v_end`, `lang`, `script`, `trans`

**Layout:**

```
+-------------------------------------------+
| [Sticky Header]                           |
+-------------------------------------------+
| Title: Constellation / Constelacion       |
| Reference: e.g. Luke 1:26-38             |
|                                           |
| +------- Two-column layout --------------+|
| | Passage panel  |  D3 star-map graph    ||
| | (left, fixed   |  (right, flex)        ||
| |  320px)        |                       ||
| |                |  Root nodes as        ||
| | Syriac verses  |  stars, sized by      ||
| | with clickable |  occurrence count,    ||
| | words, verse   |  colored by POS       ||
| | numbers on     |                       ||
| | the right      |  Constellation lines  ||
| |                |  connect co-occurring ||
| |                |  roots                ||
| +----------------+-----------------------+|
|                                           |
| Root detail panel (below graph on click)  |
+-------------------------------------------+
```

**Key Features:**
- Two-column layout: passage text (left, 320px fixed) and D3 force-directed star-map (right)
- Syriac words are clickable; clicking highlights the root node in the graph
- Verse numbers and constellation icons are positioned on the right (RTL-aligned)
- Root nodes sized by occurrence count, colored by part-of-speech
- Constellation lines connect roots that co-occur within the same verse
- Hovering a root node highlights all its occurrences in the passage text
- Root detail panel appears below the graph when a node is clicked

---

### methodology.html (Methodology / About the Method)

**URL:** `GET /methodology`

**Layout:**

```
+-------------------------------------------+
| [Sticky Header]                           |
+-------------------------------------------+
| Title: "A bridge between traditions"      |
| Subtitle: "It tastes better in Aramaic"   |
|                                           |
| Long-form prose (max-width: 720px)        |
|   - Introduction to Semitic root system   |
|   - The five tasks of the method          |
|   - Worked examples (Luke 24:39, Jn 11)  |
|   - Constellations of meaning             |
|   - Tool descriptions with internal links |
|   - References (Vicente Haya's works)     |
|   - Reference dictionaries                |
+-------------------------------------------+
```

**Key Features:**
- Bilingual ES/EN content via `{% if lang == 'es' %}` conditional blocks
- Internal links to search results, reader passages, constellation views, and visualizations
- Styled with `.methodology-content` scoped CSS (blockquotes, example blocks, task lists, reference lists)
- No settings or share controls (inherits base defaults)

---

### about.html (About the Author)

**URL:** `GET /about`

**Layout:**

```
+-------------------------------------------+
| [Sticky Header] (no settings/share)       |
+-------------------------------------------+
|                                           |
|        [Author photo, circular]           |
|                                           |
|            Jossi Fresco                   |
|                                           |
| Bio text (max-width: 640px)              |
|                                           |
| Projects & expressions:                   |
|   - Podcast link                          |
|   - Spotify link                          |
|   - Substack link                         |
|   - Other project links                   |
|                                           |
| Footer                                    |
+-------------------------------------------+
```

**Key Features:**
- Overrides `header_settings`, `header_share`, and `share_modal` blocks to empty (no settings or share on this page)
- Circular author photo with accent-colored border
- Bilingual ES/EN bio text
- External links to projects open in new tabs
- Scoped CSS via `.about-content`

---

## CSS (style.css)

### Design System

Uses CSS custom properties organized into design tokens:

**Spacing scale:**
```css
--space-xs: 0.25rem;   --space-sm: 0.5rem;   --space-md: 1rem;
--space-lg: 1.5rem;    --space-xl: 2rem;      --space-2xl: 3rem;
--space-3xl: 4rem;
```

**Type scale:**
```css
--text-xs: 0.75rem;    --text-sm: 0.875rem;   --text-base: 1rem;
--text-lg: 1.125rem;   --text-xl: 1.25rem;    --text-2xl: 1.5rem;
--text-3xl: 1.875rem;
```

**Radius scale:**
```css
--radius-sm: 6px;      --radius-md: 10px;     --radius-lg: 14px;
```

### Theme System — Olive & Stone Palette

Uses CSS custom properties with `[data-theme]` attribute on `<html>`:

```css
:root {
  /* Olive & Stone (Mediterranean/Levantine) */
  --bg-page: #f7f6f1;
  --accent: #6b7a5e;
  --accent-dark: #3d4a3c;
  --accent-gold: #a89048;
  --text-primary: #1c1e1a;
  --text-secondary: #555a50;
  --bg-header: #3d4a3c;
  ...
}

[data-theme="dark"] {
  /* Olive-tinted dark theme */
  --bg-page: #12140f;
  --accent: #9aac84;
  --accent-dark: #b8cca0;
  --accent-gold: #c4a84c;
  --text-primary: #e2e4dc;
  --bg-header: #242820;
  ...
}
```

### Key Components

| Class | Purpose |
|-------|---------|
| `.sticky-header` | Fixed top bar (z-index: 200) |
| `.container` | Main content wrapper (max-width: 1120px) |
| `.search-section` | Search form area |
| `.panel` | Card container for results |
| `.panel-header` | Card header with title |
| `.panel-body` | Card content area |
| `.peshitta-table` | Results table (responsive) |
| `.modal-overlay` | Full-screen verse modal backdrop |
| `.modal-content` | Modal card |
| `.modal-sticky-header` | Sticky header inside modals (stays pinned at top during scroll, with gradient fade) |
| `.autocomplete-list` | Search suggestions dropdown |
| `.count-badge` | Occurrence count pill |
| `.stem-badge` | Verb stem label pill |
| `.stat-item` | Stats bar item with tooltip |
| `.settings-dropdown` | Script/translation/font selection dropdown (three sections) |
| `.translit-table` | Alphabet reference grid |
| `.reader-nav` | Book/chapter navigation bar in reader |
| `.verse-block` | Individual verse container in reader |
| `.verse-syriac` | Syriac text line in reader (RTL) |
| `.verse-translit` | Transliteration line in reader |
| `.verse-translation` | Translation line in reader |
| `.root-latin` | Latin transliteration next to Syriac root in browse table |
| `.viz-container` | Visualizer wrapper (supports fullscreen mode) |
| `.viz-controls` | Language toggle checkboxes and legend |
| `.viz-svg-wrap` | D3 SVG container |
| `.viz-tooltip` | Hover tooltip for nodes |
| `.viz-outlier-key` | Legend: outlier indicator |
| `.viz-bridge-key` | Legend: bridge indicator |
| `.viz-fullscreen-btn` | Fullscreen toggle button |
| `.bridge-link-animated` | Animated dashed bridge link |
| `.bridge-outlier-ring` | Pulsing gold ring on bridge outliers |
| `.constellation-layout` | Two-column flex layout for constellation page |
| `.constellation-passage` | Left passage panel (320px fixed) |
| `.constellation-verse-num` | Verse number badge (right-aligned / RTL-positioned) |

### Responsive Breakpoints

| Breakpoint | Changes |
|------------|---------|
| <=768px | Table -> card layout, reduced padding, full-width buttons |
| <=480px | Smaller fonts, compact layout |

### Font Families

| Class | Font | Use |
|-------|------|-----|
| (body default) | 'Inter', system-ui, sans-serif | All body text |
| `.syriac` | var(--syriac-font) — 'Noto Sans Syriac' (default), Eastern, or Western variant | Syriac text |
| `.hebrew` | 'Noto Sans Hebrew', serif | Hebrew transliteration |
| `.arabic` | 'Noto Sans Arabic', serif | Arabic transliteration |
| `.ac-translit` | monospace | Latin/academic transliteration |

The Syriac font variant is selectable via settings (Estrangela, Eastern, Western) and stored in `localStorage` as `syriac-font`. The `[data-syriac-font]` attribute on `<html>` switches the `--syriac-font` CSS variable.

### RTL Support

Hebrew and Arabic transliteration elements get `direction: rtl` and appropriate `font-family` when the script setting is active. Applied in results tables, verse modal, and reader translation lines. Hebrew (`he`) and Arabic (`ar`) translations also render RTL in the reader and modal views.

Verse numbers and constellation icons in the constellation page are positioned on the right (RTL-aligned).

### Settings Dropdown

The settings dropdown has three sections on all pages:

1. **Transliteration** (4 options): Latin (ABC), Syriac (ʾbg), Hebrew (ABG), Arabic (ABJ)
2. **Translation** (4 options): English, Spanish, Hebrew Modern, Arabic SVD
3. **Syriac Font** (3 options): Estrangela, Eastern, Western

All are persisted via `localStorage` (`script`, `trans`, and `syriac-font` keys).

---

## JavaScript

### global.js (Shared Behaviors)

Loaded on every page via `base.html`. Runs as an IIFE. Handles:

| Feature | Description |
|---------|-------------|
| Dark mode | Reads `localStorage('theme')`, falls back to `prefers-color-scheme`. Toggles `data-theme` attribute on `<html>`. Icon switches between `sunny` and `bedtime`. |
| Language dropdown | Opens/closes `.lang-dropdown`, auto-closes settings dropdown when language opens. |
| Settings dropdown | Opens/closes `.settings-dropdown`. Handles `data-script` and `data-trans` option clicks: saves to `localStorage`, updates URL params, reloads page. |
| Syriac font variant | Reads `localStorage('syriac-font')`, sets `data-syriac-font` attribute on `<html>`. Toggles active state on font buttons. |
| Stored preferences redirect | On page load, if `script` or `trans` are in `localStorage` but not in URL params, redirects with those params appended. |
| Share / QR modal | Opens share modal, generates QR code (via qrcodejs library) with theme-aware colors, populates URL input, handles copy-to-clipboard. |
