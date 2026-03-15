# Frontend Reference

## Templates

### index.html (Main Search Page)

**URL:** `GET /`

**Layout:**

```
┌─────────────────────────────────────────┐
│ [Sticky Header]                         │
│   Lang Toggle | Settings ⚙️ | Theme ☀️  │
├─────────────────────────────────────────┤
│ Title + Subtitle                        │
│ Stats Bar: Roots | Words | Unique Forms │
│                                         │
│ [Search by Root] [Search by Cognate]    │ ← Tabs
│ ┌─────────────────────────────────────┐ │
│ │ Search Input + Button               │ │
│ │ [Transliteration Table toggle]      │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Results (when query provided):          │
│ ┌─────────────────────────────────────┐ │
│ │ Root Header: ܟܬܒ K-TH-B "write"    │ │
│ ├─────────────────────────────────────┤ │
│ │ Peshitta Panel (word forms table)   │ │
│ │ Hebrew Cognates Panel               │ │
│ │ Arabic Cognates Panel               │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ Footer                                  │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ [Verse Modal - overlay]                 │
│ ┌─────────────────────────────────────┐ │
│ │ ↑ Previous verse arrow              │ │
│ │ Reference: Mateo 1:1 · Root: K-TH-B│ │
│ │ Syriac text (RTL, highlighted word) │ │
│ │ Academic transliteration            │ │
│ │ Simple transliteration              │ │
│ │ English translation                 │ │
│ │ Spanish translation                 │ │
│ │ ↓ Next verse arrow                  │ │
│ │ [⧉ Copy]                           │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
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
| Script switching | settings dropdown | Saves to localStorage, reloads page with `script` param |
| Dark mode | theme toggle | Saves to localStorage, respects `prefers-color-scheme` |
| Book name translation | `translate_ref()` | Replaces English book names with localized names in references |

**Transliteration Table:**
A toggleable reference grid showing all 22 Syriac consonants with their Latin equivalents. Hidden by default, toggled by clicking the "show/hide" link.

---

### browse.html (Browse All Roots)

**URL:** `GET /browse`

**Layout:**

```
┌─────────────────────────────────────────┐
│ [Sticky Header] (same as index)         │
├─────────────────────────────────────────┤
│ Title: Browse Roots                     │
│ ← Back to Search                       │
│                                         │
│ Pagination: ← Prev | Page X of Y | →   │
│ ┌─────────────────────────────────────┐ │
│ │ Root | Translit | Meaning | Forms | │ │
│ │ ─────┼──────────┼─────────┼───────┤ │
│ │ ܐܡܪ  | A-M-R    | say     | 42   │ │
│ │ ܗܘܐ  | H-W-A    | be      | 38   │ │
│ │ ...  | ...      | ...     | ...   │ │
│ └─────────────────────────────────────┘ │
│ Pagination (bottom)                     │
│ Footer                                  │
└─────────────────────────────────────────┘
```

Each root row links to `/?q=<root>&lang=<lang>#results`.

---

## CSS (style.css)

### Theme System

Uses CSS custom properties with `[data-theme]` attribute on `<html>`:

```css
:root {
  --bg-page: #f5f0eb;        /* Light theme */
  --text-primary: #2c1810;
  --accent-gold: #8b6914;
  ...
}

[data-theme="dark"] {
  --bg-page: #1a1510;        /* Dark theme */
  --text-primary: #e8ddd0;
  --accent-gold: #d4a832;
  ...
}
```

### Key Components

| Class | Purpose |
|-------|---------|
| `.sticky-header` | Fixed top bar (z-index: 200) |
| `.container` | Main content wrapper (max-width: 900px) |
| `.search-section` | Search form area |
| `.panel` | Card container for results |
| `.panel-header` | Card header with title |
| `.panel-body` | Card content area |
| `.peshitta-table` | Results table (responsive) |
| `.modal-overlay` | Full-screen verse modal backdrop |
| `.modal-content` | Modal card |
| `.autocomplete-list` | Search suggestions dropdown |
| `.count-badge` | Occurrence count pill |
| `.stem-badge` | Verb stem label pill |
| `.stat-item` | Stats bar item with tooltip |
| `.settings-dropdown` | Script selection dropdown |
| `.translit-table` | Alphabet reference grid |

### Responsive Breakpoints

| Breakpoint | Changes |
|------------|---------|
| ≤768px | Table → card layout, reduced padding, full-width buttons |
| ≤480px | Smaller fonts, compact layout |

### Font Families

| Class | Font | Use |
|-------|------|-----|
| `.syriac` | 'Noto Sans Syriac', serif | Syriac text |
| `.hebrew` | 'Noto Sans Hebrew', serif | Hebrew transliteration |
| `.arabic` | 'Noto Sans Arabic', serif | Arabic transliteration |
| `.ac-translit` | monospace | Latin/academic transliteration |

### RTL Support

Hebrew and Arabic transliteration elements get `direction: rtl` and appropriate `font-family` when the script setting is active. Applied both in results tables and verse modal.
