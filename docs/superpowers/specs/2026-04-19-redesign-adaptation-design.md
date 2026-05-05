# Redesign Adaptation — Designer Output → Flask/Jinja Stack

**Date:** 2026-04-19
**Status:** Proposed
**Source:** Anthropic Designer output at `~/Downloads/peshitta.zip` (`design_handoff_peshitta/`)
**Target:** `/Users/jfresco16/Google Drive/Claude/Peshitta` (Flask + Jinja2 + vanilla JS)
**Branch:** `feature/redesign`

## Goal

Adopt as much of Designer's hifi redesign as practical without breaking the existing Flask/Jinja architecture, all 5 UI languages, the v1.3 API/Swagger surfaces, or the user's investment in the current data layer (cognates, OT integration, Greek concordance, bookmarks, audio-removed reader, etc.).

## What Designer Proposed (in summary)

A single-page React/Next.js app with vanilla-JS router, 6 routes (Home, Reader, Browse, Constellation, Method, Ficha/root card), parchment+ink themes, Spectral serif typography, named top navbar, hero search with inline Syriac preview, feature cards grid, root frequency table, root card with right-rail cognate panels, starmap-style constellation. Full design tokens in `styles.css`.

**The README explicitly says "do not ship the raw HTML to production."** It's a hifi reference, not portable code.

## What We Adopt vs. What We Defer

| Designer feature | Decision | Rationale |
|---|---|---|
| Named top navbar (Home / Reader / Browse / Constellation / Method) | **Adopt** | Solves the "no navbar with menu" complaint directly |
| Brand mark + name in left header | **Adopt** | Replaces icon-only logo |
| Lang toggle EN/ES (segmented) in header | **Adopt** but expand to 5 langs (ES/EN/HE/AR/NL) | Keep our existing langs |
| Theme toggle in header | **Adopt** | Already have it |
| Mobile menu hamburger | **Adopt** | Mobile responsive requirement |
| Parchment + Ink themes (full token set) | **Adopt as v2 theme**, keep existing as fallback | Big visual upgrade; warm parchment palette is premium-academic |
| Spectral serif body + Inter UI + JetBrains Mono | **Adopt** | Fonts already loadable from Google Fonts |
| Hero with eyebrow + headline + deck + inline search | **Adopt** | Replaces current dense feature-showcase + search-tabs stack |
| Inline Syriac preview as user types | **Adopt** | Beautiful UX — typeahead transliteration |
| Suggestion chips below hero search | **Adopt** | Discovery for first-time users |
| "Three ways in" numbered card | **Adopt** | Pedagogical entry point |
| Root of the Day right rail | **Adopt** | We already have ROTD data |
| 6-card "Six tools, one corpus" grid | **Adopt** but adjust to actual 6 features | (Reader, Browse, Visualize, Constellation, KWIC, Greek concordance) |
| Top-cited roots table on home | **Adopt** | New surface, uses existing extractor data |
| Density toggle (Comfy/Compact) | **Defer** | Nice-to-have, not blocking |
| Starmap constellation (D3 force, glow filters, dashed bridges) | **Defer to phase 2** | Big visual upgrade, but our current viz works; treat as separate task |
| Verse modal redesign (Reader) | **Adopt** | Modal exists; restyle |
| Ficha right-rail cognate panels | **Adopt** | Reorganizes existing cognate data |
| Translation shift chain (degradation) styled | **Adopt** | Already have data, just restyle |
| Methodology editorial typography (Spectral, large) | **Adopt** | Existing page restyled |
| Pull quote + numbered sections in Method | **Adopt** | Already structured |
| Designer's static mock data | **Discard** | Wire to real corpus |
| `data-route` SPA router | **Discard** | Use existing Flask routes |
| Six-route surface in HTML/JS | **Discard structure**, **adopt visuals** | Map to our existing 9 page routes |

## Architectural Constraints (Cannot Break)

1. **Flask + Jinja2 server-side rendering** — no SPA router, no React
2. **5 UI languages** — every new visible string needs i18n keys
3. **All v1.3 API endpoints** keep working unchanged
4. **Citation modal, cookie banner, /api docs page** stay intact
5. **All existing data files** (cognates.json, corpus CSV, etc.) drive everything — no rewrites of the data layer
6. **Backwards-compatible URLs** — every existing URL keeps working (people may have bookmarked)
7. **No new build step** — no webpack/vite/postcss; styles stay as plain CSS

## Design Tokens to Migrate

Replace the current olive/cream palette with Designer's parchment palette. Both themes (light "parchment" and dark "ink") become the new defaults; the current dark-mode toggle continues to work.

```css
/* Parchment (light) — replaces current --bg, --bg-card, etc. */
--bg: #f4efe4;
--bg-2: #ece5d3;
--bg-card: #fbf7ec;
--bg-elev: #ffffff;
--bg-sunk: #ebe3d0;
--ink: #1a1a17;
--ink-2: #3a3a33;
--ink-3: #6b6a5e;
--ink-4: #9b9787;
--rule: #d8cfb8;
--rule-2: #c8bd9f;
--olive: #4d5a3e;       /* keep — already our brand */
--olive-2: #6b7a5e;
--olive-3: #2c3525;
--gold: #a88536;
--gold-2: #c9a558;
--gold-soft: #e8d49a;
--terracotta: #a8593a;
--lapis: #2e4a6b;
--hl: #f3e6b2;

--serif: "Spectral", Georgia, serif;
--sans: "Inter", system-ui, sans-serif;
--mono: "JetBrains Mono", ui-monospace, monospace;

--r-sm: 6px; --r-md: 10px; --r-lg: 16px; --r-xl: 24px;
```

## Phases (Each is a separate Plan)

### Phase 1 — Navbar + Tokens + Typography (this spec's primary scope)
**Goal:** Make the existing app look and navigate like the Designer mock without changing what each page does.

- New navbar: brand mark + 5 named menu links (Home, Read, Browse, Constellation, Method)
- Move the icon row (Help, Bookmarks, Settings, Theme, Share, API) to a secondary "utility" group on the right of the navbar
- Apply parchment+ink theme tokens (rename existing tokens or add new ones, keep dark-mode toggle working)
- Load Spectral + JetBrains Mono fonts (Inter already loaded)
- Headlines and body switch to serif; UI stays Inter
- Active menu link gets persistent gold underline

**Files modified:**
- `peshitta_roots/templates/base.html` — full navbar restructure
- `peshitta_roots/static/style.css` — token swap, font load, typography rules, navbar styles
- `data/i18n.json` — add `nav_read` (already have `read_title`, can reuse), confirm all 5 menu labels exist

**Files unchanged:** all routes, all other templates, all data, all JS.

### Phase 2 — Homepage Restructure
**Goal:** Replace current `index.html` body with Designer's hero + "three ways in" + ROTD aside + 6-card feature grid + top-cited roots table.

- Hero: eyebrow stat strip + serif headline + deck + inline search with live Syriac preview
- Right column: ROTD card (data already exists)
- Below hero: 6 feature cards (Reader, Browse, Root Card, Constellation, Concordance, Greek)
- Top-cited roots table (queries existing extractor)
- Editorial closing: Methodology lead-in + Luke 24:39 citation card
- Keep existing search tabs (Root/Cognate/Meaning/Co-occurrence/Text/Greek) but move to a `/search` page or below the hero feature cards

**Files modified:**
- `peshitta_roots/templates/index.html` — major restructure
- `peshitta_roots/static/style.css` — hero, feature grid, root table, cite card styles
- `peshitta_roots/app.py` — add top-cited roots data to index route
- `peshitta_roots/static/js/global.js` — live transliteration preview JS

### Phase 3 — Reader / Visualize / Browse / Methodology Restyle
- Reader: toolbar (book/chapter/prev/next/density/settings), serif verse numbers, gold accent, restyled verse modal
- Visualize (Ficha): hero + numbered sections (Sabor, Citation, Translation Shift, Sister roots) + right-rail Hebrew/Arabic panels
- Browse: filter chips row (All / Verbs / Nouns / Particles / With cognates / Outliers), root frequency bars
- Methodology: serif typography, pull quotes, numbered sections

### Phase 4 — Constellation Starmap (Optional / Later)
- D3 force layout with glow + dashed animated bridges
- Bigger surgery; defer

## Phase 1 — Detailed Spec (Approved-then-implemented)

### Navbar HTML structure (replacing current sticky header)

```html
<header class="menubar">
  <div class="menubar-row">
    <a class="brand" href="{{ url_for('index', lang=lang) }}">
      <div class="brand-mark">ܐ</div>
      <div class="brand-text">
        <div class="brand-name">Peshitta</div>
        <div class="brand-sub">{{ t.nav_subtitle|default('Root Constellations') }}</div>
      </div>
    </a>

    <nav class="menu-nav" id="menuNav">
      <a class="menu-link {% if request.endpoint == 'index' %}active{% endif %}"
         href="{{ url_for('index', lang=lang) }}">
        <span class="material-symbols-outlined">cottage</span>{{ t.nav_home }}
      </a>
      <a class="menu-link {% if request.endpoint == 'read' %}active{% endif %}"
         href="{{ url_for('read', lang=lang, book='Matthew', chapter=1) }}">
        <span class="material-symbols-outlined">menu_book</span>{{ t.nav_read|default('Read') }}
      </a>
      <a class="menu-link {% if request.endpoint == 'browse' %}active{% endif %}"
         href="{{ url_for('browse', lang=lang) }}">
        <span class="material-symbols-outlined">view_list</span>{{ t.nav_browse|default('Browse') }}
      </a>
      <a class="menu-link {% if request.endpoint == 'constellation' %}active{% endif %}"
         href="{{ url_for('constellation', lang=lang, book='Luke', chapter=24, v_start=13, v_end=35) }}">
        <span class="material-symbols-outlined">hub</span>{{ t.nav_constellation|default('Constellation') }}
      </a>
      <a class="menu-link {% if request.endpoint == 'methodology_page' %}active{% endif %}"
         href="{{ url_for('methodology_page', lang=lang) }}">
        <span class="material-symbols-outlined">school</span>{{ t.nav_method|default('Method') }}
      </a>
    </nav>

    <div class="menu-spacer"></div>

    <!-- Utility cluster: lang, help, bookmarks, settings, theme, share, API -->
    <div class="menu-utility">
      [existing dropdowns/icons here, slightly compressed]
    </div>

    <button class="icon-btn menu-mobile" id="mobileMenuBtn" aria-label="Menu">
      <span class="material-symbols-outlined">menu</span>
    </button>
  </div>
</header>
```

### Mobile behavior
- Hide `.menu-nav` text labels below 768px → show as icon-only with tooltip
- Below 600px → collapse main menu into hamburger drawer; brand stays; utility cluster collapses to settings + lang only
- API icon stays in the rightmost utility position (per recent user request)

### Token migration strategy
- Add new parchment tokens at `:root` level with NEW names (`--bg-parchment`, `--olive-parchment`, etc.)
- Add a CSS feature flag `[data-design="redesign"]` that maps the existing token names to the new ones
- Add a small JS toggle in settings to opt in to redesign during phase 1, then flip default in phase 2 launch
- This lets us ship phase 1 dark, get user feedback, and roll back if needed

OR simpler: just rebrand all tokens in one commit, since both themes (current olive/cream and new parchment) are similar warm palettes.

**Decision: simple swap. We're on a feature branch, easy to revert.**

### Typography migration
- Add Spectral 400/500 weight to existing Google Fonts link
- Add JetBrains Mono 400/500
- Define `--serif`, `--sans`, `--mono` CSS variables
- Apply `font-family: var(--serif)` to `h1, h2, h3, .home-headline, .verse-tr, .editorial *`
- Keep Inter for navbar, buttons, search inputs, badges, body text outside hero

### Navbar CSS (key rules)
```css
.menubar {
  background: var(--bg-card);
  border-bottom: 1px solid var(--rule);
  position: sticky; top: 0; z-index: 100;
}
.menubar-row {
  display: flex; align-items: center; gap: 24px;
  max-width: 1280px; margin: 0 auto; padding: 12px 24px;
}
.brand { display: flex; gap: 12px; text-decoration: none; color: inherit; }
.brand-mark {
  width: 40px; height: 40px; border-radius: 50%;
  background: var(--olive); color: var(--bg-elev);
  display: grid; place-items: center; font-family: var(--syriac); font-size: 22px;
}
.brand-name { font-family: var(--serif); font-weight: 600; font-size: 18px; }
.brand-sub  { font-size: 11px; color: var(--ink-3); letter-spacing: 0.06em; text-transform: uppercase; }
.menu-nav   { display: flex; gap: 8px; }
.menu-link  {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 8px 12px; border-radius: var(--r-sm);
  color: var(--ink-2); text-decoration: none; font-weight: 500;
  border-bottom: 2px solid transparent;
}
.menu-link:hover     { color: var(--olive); border-bottom-color: var(--gold-soft); }
.menu-link.active    { color: var(--olive); border-bottom-color: var(--gold); }
.menu-spacer         { flex: 1; }
.menu-utility        { display: flex; gap: 8px; align-items: center; }
.menu-mobile         { display: none; }
@media (max-width: 768px) {
  .menu-nav .menu-link span:not(.material-symbols-outlined) { display: none; }
  .menu-link { padding: 8px; }
}
@media (max-width: 600px) {
  .menu-nav { display: none; }
  .menu-mobile { display: inline-flex; }
}
```

### i18n keys to add (ES/EN/HE/AR/NL)
- `nav_subtitle` ("Constelaciones de raíces" / "Root Constellations" / etc.)
- `nav_read` ("Leer" / "Read")
- `nav_browse` ("Explorar" / "Browse")
- `nav_constellation` ("Constelación" / "Constellation")
- `nav_method` ("Método" / "Method")

(Note: `nav_home`, `nav_language`, etc. were added in the previous tooltip pass.)

## Verification

1. Every existing page renders without error in all 5 langs
2. Active menu link highlights correctly per current route
3. Mobile breakpoints collapse menu cleanly
4. Existing utility icons (help/bookmarks/settings/theme/share/API) still work
5. Dark mode toggle still flips theme
6. No new console errors
7. /api, /docs, all v1.3 surfaces unaffected
8. Site looks at least 30% closer to Designer mocks

## Out of Scope (Phase 1)

- Replacing the homepage hero / feature grid (Phase 2)
- Restyling Reader, Visualize, Browse, Methodology pages (Phase 3)
- Constellation D3 starmap (Phase 4)
- Density toggle (defer)
- Live transliteration preview (Phase 2)
- Top-cited roots table (Phase 2)
