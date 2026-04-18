# OT Integration + Greek-Syriac Concordance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Merge 4 OT books into the corpus and add a Greek-Syriac translation concordance search tab.

**Architecture:** Extend PeshittaCorpus to load a second CSV alongside the NT, tagged by testament. Add testament filter to browse/search. Build a reverse Greek→Syriac index from existing cognates.json greek_parallel data and expose as a new search tab + API endpoint.

**Tech Stack:** Python/Flask, Jinja2 templates, vanilla JS, JSON data files

---

## File Structure

| File | Action | Responsibility |
|------|--------|---------------|
| `peshitta_roots/corpus.py` | Modify | Load OT CSV, add testament metadata, `get_testament()` method |
| `peshitta_roots/app.py` | Modify | Pass testament info to templates, testament filter on browse, `_build_greek_index()`, `/api/greek-concordance` route |
| `peshitta_roots/templates/browse.html` | Modify | Add testament toggle (All/NT/OT) |
| `peshitta_roots/templates/read.html` | Modify | OT books in selector with optgroup |
| `peshitta_roots/templates/index.html` | Modify | New "By Greek" search tab + results panel + JS |
| `peshitta_roots/static/style.css` | Modify | Greek concordance result cards, testament badges |
| `data/i18n.json` | Modify | New keys: testament names, OT book names, Greek tab labels |

---

### Task 1: Extend PeshittaCorpus to load OT

**Files:**
- Modify: `peshitta_roots/corpus.py`

- [ ] **Step 1: Add OT CSV loading to `__init__` and `load()`**

In `corpus.py`, change `__init__` to accept an optional list of additional CSV paths, and change `load()` to load all of them:

```python
class PeshittaCorpus:
    """Loads the Peshitta corpus (NT + optional OT) and builds searchable word indexes."""

    # NT books in canonical order
    _NT_BOOKS = {
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
        '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
        'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
        'James', '1 Peter', '1 John',
    }

    def __init__(self, csv_path: str | None = None, extra_csv_paths: list[str] | None = None):
        if csv_path is None:
            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'syriac_nt_traditional22_unicode.csv'
            )
        self.csv_path = csv_path
        self._extra_csv_paths = extra_csv_paths or []
        self._occurrences: dict[str, list[str]] = {}
        self._total_words: int = 0
        self._verses: dict[str, str] = {}
        self._verse_order: list[str] = []
        self._testament: dict[str, str] = {}  # book_name -> 'nt' or 'ot'
        self._translations: dict[str, dict] = {}
        self._loaded = False
```

Change `load()` to iterate over all CSV files and tag testament:

```python
def load(self) -> None:
    """Parse the CSV(s) and build the word index."""
    if self._loaded:
        return

    all_paths = [self.csv_path] + self._extra_csv_paths
    for csv_path in all_paths:
        if not os.path.exists(csv_path):
            continue
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                syriac_text = row['syriac'].strip()
                if not syriac_text:
                    continue

                reference = row['reference']
                self._verses[reference] = syriac_text
                self._verse_order.append(reference)

                # Tag testament
                book = reference[:reference.rfind(' ')]
                if book not in self._testament:
                    self._testament[book] = 'nt' if book in self._NT_BOOKS else 'ot'

                words = syriac_text.split()
                for word in words:
                    clean_word = word.strip()
                    if not clean_word:
                        continue
                    self._total_words += 1
                    if clean_word not in self._occurrences:
                        self._occurrences[clean_word] = []
                    self._occurrences[clean_word].append(reference)

    self._loaded = True
```

- [ ] **Step 2: Add `get_testament()` method**

```python
def get_testament(self, book: str) -> str:
    """Return 'nt' or 'ot' for a book name."""
    self.load()
    return self._testament.get(book, 'nt')
```

- [ ] **Step 3: Invalidate `_books_cache` so it rebuilds with OT books**

The existing `get_books()` uses `hasattr(self, '_books_cache')`. No change needed — the cache builds on first call after `load()`, which now includes OT books. The OT books will appear after NT books because the NT CSV is loaded first.

- [ ] **Step 4: Verify locally**

```bash
cd "/Users/jfresco16/Google Drive/Claude/Peshitta"
python3 -c "
from peshitta_roots.corpus import PeshittaCorpus
c = PeshittaCorpus(extra_csv_paths=['syriac_ot_selected_unicode.csv'])
c.load()
books = c.get_books()
print(f'Total books: {len(books)}')
for b, ch in books:
    print(f'  {b}: {ch} chapters ({c.get_testament(b)})')
print(f'Total verses: {len(c._verses)}')
"
```

Expected: 26 books (22 NT + 4 OT), ~13,400 verses, OT books tagged 'ot'.

- [ ] **Step 5: Commit**

```bash
git add peshitta_roots/corpus.py
git commit -m "feat: extend PeshittaCorpus to load OT CSV with testament tagging"
```

---

### Task 2: Wire OT corpus in app.py init

**Files:**
- Modify: `peshitta_roots/app.py`

- [ ] **Step 1: Pass OT CSV path to PeshittaCorpus in `_init()`**

Find the line (around line 95):
```python
_corpus = PeshittaCorpus(_get_csv_path())
```

Replace with:
```python
ot_csv = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'syriac_ot_selected_unicode.csv')
ot_paths = [ot_csv] if os.path.exists(ot_csv) else []
_corpus = PeshittaCorpus(_get_csv_path(), extra_csv_paths=ot_paths)
```

- [ ] **Step 2: Restart server and verify**

```bash
lsof -ti:5009 | xargs kill 2>/dev/null
cd "/Users/jfresco16/Google Drive/Claude/Peshitta"
FLASK_APP=peshitta_roots.app python3 -m flask run --port 5009 &
sleep 4
curl -s "http://localhost:5009/api/roots?per_page=5" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['total'], 'roots')"
```

Expected: root count should be higher than before (was ~2,532, now more with OT roots).

- [ ] **Step 3: Commit**

```bash
git add peshitta_roots/app.py
git commit -m "feat: load OT corpus alongside NT in app init"
```

---

### Task 3: Add OT book names to i18n

**Files:**
- Modify: `data/i18n.json`

- [ ] **Step 1: Add OT book names and testament labels**

Run this Python script to add the keys:

```python
import json

with open('data/i18n.json', 'r', encoding='utf-8') as f:
    i18n = json.load(f)

ot_keys = {
    'es': {
        'testament_all': 'Todos',
        'testament_nt': 'Nuevo Testamento',
        'testament_ot': 'Antiguo Testamento',
        'search_tab_greek': 'Por griego',
        'greek_search_placeholder': 'Palabra griega (ej. βασιλεύς)',
        'greek_search_help': 'Busca una palabra griega para ver qué raíces siríacas la traducen.',
        'greek_no_results': 'No se encontraron raíces siríacas para esta palabra griega.',
        'greek_browse_all': 'Todas las palabras griegas',
    },
    'en': {
        'testament_all': 'All',
        'testament_nt': 'New Testament',
        'testament_ot': 'Old Testament',
        'search_tab_greek': 'By Greek',
        'greek_search_placeholder': 'Greek word (e.g. βασιλεύς)',
        'greek_search_help': 'Search a Greek word to see which Syriac roots translate it.',
        'greek_no_results': 'No Syriac roots found for this Greek word.',
        'greek_browse_all': 'All Greek words',
    },
    'he': {
        'testament_all': 'הכל',
        'testament_nt': 'הברית החדשה',
        'testament_ot': 'התנ"ך',
        'search_tab_greek': 'ביוונית',
        'greek_search_placeholder': 'מילה יוונית (למשל βασιλεύς)',
        'greek_search_help': 'חפש מילה יוונית כדי לראות אילו שורשים סוריים מתרגמים אותה.',
        'greek_no_results': 'לא נמצאו שורשים סוריים למילה יוונית זו.',
        'greek_browse_all': 'כל המילים היווניות',
    },
    'ar': {
        'testament_all': 'الكل',
        'testament_nt': 'العهد الجديد',
        'testament_ot': 'العهد القديم',
        'search_tab_greek': 'باليونانية',
        'greek_search_placeholder': 'كلمة يونانية (مثل βασιλεύς)',
        'greek_search_help': 'ابحث عن كلمة يونانية لمعرفة أي جذور سريانية تترجمها.',
        'greek_no_results': 'لم يتم العثور على جذور سريانية لهذه الكلمة اليونانية.',
        'greek_browse_all': 'كل الكلمات اليونانية',
    },
    'nl': {
        'testament_all': 'Alles',
        'testament_nt': 'Nieuw Testament',
        'testament_ot': 'Oud Testament',
        'search_tab_greek': 'Op Grieks',
        'greek_search_placeholder': 'Grieks woord (bijv. βασιλεύς)',
        'greek_search_help': 'Zoek een Grieks woord om te zien welke Syrische wortels het vertalen.',
        'greek_no_results': 'Geen Syrische wortels gevonden voor dit Griekse woord.',
        'greek_browse_all': 'Alle Griekse woorden',
    },
}

# Add OT book names
book_names = {
    'es': {'Psalms': 'Salmos', 'Isaiah': 'Isaías', 'Ezekiel': 'Ezequiel', 'Proverbs': 'Proverbios'},
    'en': {'Psalms': 'Psalms', 'Isaiah': 'Isaiah', 'Ezekiel': 'Ezekiel', 'Proverbs': 'Proverbs'},
    'he': {'Psalms': 'תהלים', 'Isaiah': 'ישעיהו', 'Ezekiel': 'יחזקאל', 'Proverbs': 'משלי'},
    'ar': {'Psalms': 'المزامير', 'Isaiah': 'إشعياء', 'Ezekiel': 'حزقيال', 'Proverbs': 'الأمثال'},
    'nl': {'Psalms': 'Psalmen', 'Isaiah': 'Jesaja', 'Ezekiel': 'Ezechiël', 'Proverbs': 'Spreuken'},
}

for lang, keys in ot_keys.items():
    for k, v in keys.items():
        i18n[lang][k] = v

for lang, names in book_names.items():
    if 'book_names' not in i18n[lang]:
        i18n[lang]['book_names'] = {}
    for eng, localized in names.items():
        i18n[lang]['book_names'][eng] = localized

with open('data/i18n.json', 'w', encoding='utf-8') as f:
    json.dump(i18n, f, ensure_ascii=False, indent=2)

print("Done")
```

- [ ] **Step 2: Commit**

```bash
git add data/i18n.json
git commit -m "feat: add i18n keys for testament labels, OT book names, Greek tab"
```

---

### Task 4: Add testament filter to browse page

**Files:**
- Modify: `peshitta_roots/app.py` (browse route)
- Modify: `peshitta_roots/templates/browse.html`

- [ ] **Step 1: Add `testament` query param to browse route in app.py**

Find the browse route. Add `testament` param parsing after `sort`:

```python
testament = request.args.get('testament', '')
if testament not in ('nt', 'ot', ''):
    testament = ''
```

Filter roots before pagination. After the roots list is built, add:

```python
if testament:
    filtered_roots = []
    for root in all_roots_for_page:
        # Check if any of the root's references belong to the requested testament
        has_match = False
        for match in root.matches:
            for ref in match.references:
                book = ref[:ref.rfind(' ')]
                if _corpus.get_testament(book) == testament:
                    has_match = True
                    break
            if has_match:
                break
        if has_match:
            filtered_roots.append(root)
    all_roots_for_page = filtered_roots
```

Pass `testament` to the template:

```python
return render_template('browse.html', ..., testament=testament)
```

- [ ] **Step 2: Add testament toggle to browse.html**

After the view toggle div and before the frequency filters, add:

```html
<div class="browse-filters" style="margin-bottom: 8px;">
    <a href="{{ url_for('browse', lang=lang, script=script, trans=trans, view=view, sort=sort, freq=freq or '') }}" class="browse-filter{% if not testament %} active{% endif %}">{{ t.testament_all }}</a>
    <a href="{{ url_for('browse', lang=lang, script=script, trans=trans, view=view, sort=sort, freq=freq or '', testament='nt') }}" class="browse-filter{% if testament == 'nt' %} active{% endif %}">{{ t.testament_nt }}</a>
    <a href="{{ url_for('browse', lang=lang, script=script, trans=trans, view=view, sort=sort, freq=freq or '', testament='ot') }}" class="browse-filter{% if testament == 'ot' %} active{% endif %}">{{ t.testament_ot }}</a>
</div>
```

- [ ] **Step 3: Restart server, test browse with `?testament=ot`**

Expected: only roots with OT occurrences shown.

- [ ] **Step 4: Commit**

```bash
git add peshitta_roots/app.py peshitta_roots/templates/browse.html
git commit -m "feat: add testament filter (All/NT/OT) to browse page"
```

---

### Task 5: Add OT books to reader with optgroup

**Files:**
- Modify: `peshitta_roots/templates/read.html`
- Modify: `peshitta_roots/app.py` (read route)

- [ ] **Step 1: Pass testament info to read template**

In the read route, after `books = _corpus.get_books()`, add:

```python
books_by_testament = {'nt': [], 'ot': []}
for b_name, b_max in books:
    t_key = _corpus.get_testament(b_name)
    books_by_testament[t_key].append((b_name, b_max))
```

Pass `books_by_testament` to the template.

- [ ] **Step 2: Update book selector in read.html with optgroup**

Replace the book select dropdown:

```html
<select id="book-select">
    <optgroup label="{{ t.testament_nt }}">
    {% for b_name, b_max in books_by_testament.nt %}
    <option value="{{ b_name }}" data-chapters="{{ b_max }}" {% if b_name == book %}selected{% endif %}>{{ book_names.get(b_name, b_name) }}</option>
    {% endfor %}
    </optgroup>
    {% if books_by_testament.ot %}
    <optgroup label="{{ t.testament_ot }}">
    {% for b_name, b_max in books_by_testament.ot %}
    <option value="{{ b_name }}" data-chapters="{{ b_max }}" {% if b_name == book %}selected{% endif %}>{{ book_names.get(b_name, b_name) }}</option>
    {% endfor %}
    </optgroup>
    {% endif %}
</select>
```

- [ ] **Step 3: Restart server, navigate to Psalms 23 in reader**

```
http://localhost:5009/read?book=Psalms&chapter=23&lang=en
```

Expected: Syriac text + transliteration visible, no translation line (no OT translations yet). Book selector shows NT/OT groups.

- [ ] **Step 4: Commit**

```bash
git add peshitta_roots/app.py peshitta_roots/templates/read.html
git commit -m "feat: add OT books to reader with NT/OT optgroup selector"
```

---

### Task 6: Build Greek reverse index and API endpoint

**Files:**
- Modify: `peshitta_roots/app.py`

- [ ] **Step 1: Add global `_greek_idx` and `_build_greek_index()` function**

Add near the other cache globals (around line 534):

```python
_greek_idx: dict = {}  # greek_word -> [{ key, root_syriac, gloss, transliteration, meaning, occurrences, sabor }]
```

Add the builder function:

```python
def _build_greek_index():
    """Build reverse index: Greek word → Syriac roots that translate it."""
    global _greek_idx
    with _cache_lock:
        if _greek_idx:
            return
    roots = _cognates_raw.get('roots', {})
    idx = {}
    for key, data in roots.items():
        gp = data.get('greek_parallel')
        if not gp or not gp.get('word'):
            continue
        greek_word = gp['word']
        root_syriac = data.get('root_syriac', '')
        occ = 0
        if root_syriac:
            entry = _extractor.lookup_root(root_syriac)
            if entry:
                occ = entry.total_occurrences
        record = {
            'key': key,
            'root_syriac': root_syriac,
            'gloss_en': data.get('gloss_en', ''),
            'gloss_es': data.get('gloss_es', ''),
            'transliteration': gp.get('transliteration', ''),
            'meaning_en': gp.get('meaning_en', gp.get('meaning', '')),
            'meaning_es': gp.get('meaning_es', ''),
            'occurrences': occ,
            'sabor': data.get('sabor_raiz_en', ''),
        }
        if greek_word not in idx:
            idx[greek_word] = []
        idx[greek_word].append(record)

    # Sort entries within each Greek word by occurrences descending
    for gw in idx:
        idx[gw].sort(key=lambda x: -x['occurrences'])

    with _cache_lock:
        _greek_idx.update(idx)
```

- [ ] **Step 2: Add `/api/greek-concordance` route**

```python
@app.route('/api/greek-concordance')
def api_greek_concordance():
    """Return Syriac roots that translate a given Greek word."""
    _init()
    _build_greek_index()
    lang = _detect_lang()

    q = request.args.get('q', '').strip()
    if not q:
        # Return all Greek words for browse mode
        words = []
        for gw, entries in sorted(_greek_idx.items()):
            words.append({
                'word': gw,
                'transliteration': entries[0]['transliteration'] if entries else '',
                'meaning': entries[0].get(f'meaning_{lang}') or entries[0].get('meaning_en', ''),
                'root_count': len(entries),
            })
        return jsonify({'browse': True, 'words': words, 'total': len(words)})

    # Search: exact match first, then prefix/substring
    results = _greek_idx.get(q)
    if not results:
        # Try case-insensitive substring match
        for gw, entries in _greek_idx.items():
            if q.lower() in gw.lower():
                results = entries
                q = gw  # use the actual key
                break

    if not results:
        return jsonify({'query': q, 'roots': [], 'total': 0})

    gloss_key = 'gloss_es' if lang == 'es' else 'gloss_en'
    meaning_key = f'meaning_{lang}' if lang in ('en', 'es') else 'meaning_en'

    out = []
    for r in results:
        out.append({
            'key': r['key'].upper(),
            'root_syriac': r['root_syriac'],
            'gloss': r.get(gloss_key) or r.get('gloss_en', ''),
            'occurrences': r['occurrences'],
            'sabor': r['sabor'],
        })

    return jsonify({
        'query': q,
        'transliteration': results[0]['transliteration'] if results else '',
        'meaning': results[0].get(meaning_key) or results[0].get('meaning_en', ''),
        'roots': out,
        'total': len(out),
    })
```

- [ ] **Step 3: Restart and test the API**

```bash
curl -s "http://localhost:5009/api/greek-concordance?q=βασιλεύς&lang=en" | python3 -m json.tool | head -20
curl -s "http://localhost:5009/api/greek-concordance?lang=en" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['total'], 'Greek words')"
```

Expected: M-L-K returned for βασιλεύς; browse mode returns all Greek words.

- [ ] **Step 4: Commit**

```bash
git add peshitta_roots/app.py
git commit -m "feat: add Greek-Syriac concordance index and /api/greek-concordance endpoint"
```

---

### Task 7: Add "By Greek" search tab to homepage

**Files:**
- Modify: `peshitta_roots/templates/index.html`
- Modify: `peshitta_roots/static/style.css`

- [ ] **Step 1: Add the tab button**

In index.html, after the text search tab button (line ~120), add:

```html
<button class="search-tab" id="tab-greek" onclick="switchTab('greek')">{{ t.search_tab_greek }}</button>
```

- [ ] **Step 2: Add the panel**

After the text search panel (after `panel-text` div), add:

```html
<div id="panel-greek" class="search-panel" style="display:none;">
    <form onsubmit="return doGreekSearch()">
        <div class="search-row">
            <input type="text" id="greek-input" placeholder="{{ t.greek_search_placeholder }}" autocomplete="off">
            <button type="submit" class="search-btn">{{ t.search_button }}</button>
        </div>
        <p class="search-help">{{ t.greek_search_help }}</p>
    </form>
    <div id="greek-browse-toggle" style="margin-top:12px;">
        <a href="#" onclick="event.preventDefault(); browseGreekWords();" style="color:var(--accent); font-size:0.9em;">{{ t.greek_browse_all }} &rarr;</a>
    </div>
    <div id="greek-search-results"></div>
</div>
```

- [ ] **Step 3: Update `switchTab()` to include 'greek'**

Find the line:
```javascript
var tabs = ['root', 'cognate', 'meaning', 'proximity', 'text'];
```

Change to:
```javascript
var tabs = ['root', 'cognate', 'meaning', 'proximity', 'text', 'greek'];
```

- [ ] **Step 4: Add `doGreekSearch()` and `browseGreekWords()` JS functions**

Add before the closing `</script>` tag in the main inline script:

```javascript
function doGreekSearch() {
    var q = document.getElementById('greek-input').value.trim();
    var resultsDiv = document.getElementById('greek-search-results');
    if (!q) return false;
    resultsDiv.innerHTML = '<p class="search-loading">Loading...</p>';
    fetch('/api/greek-concordance?q=' + encodeURIComponent(q) + '&lang=' + currentLang)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (!data.roots || !data.roots.length) {
                resultsDiv.innerHTML = '<p class="no-results">{{ t.greek_no_results }}</p>';
                return;
            }
            var html = '<div class="greek-result-header">';
            html += '<span class="greek-word" style="font-size:1.4em;">' + escHtml(data.query) + '</span> ';
            html += '<span class="greek-translit" style="font-style:italic;">' + escHtml(data.transliteration) + '</span> ';
            html += '<span class="greek-meaning" style="color:var(--text-muted);">' + escHtml(data.meaning) + '</span>';
            html += '</div>';
            html += '<p style="margin:8px 0; font-weight:600;">' + data.total + ' {{ t.proximity_root|default("Syriac root") }}' + (data.total > 1 ? 's' : '') + '</p>';
            for (var i = 0; i < data.roots.length; i++) {
                var r = data.roots[i];
                html += '<div class="greek-result-card">';
                html += '<a href="/?q=' + encodeURIComponent(r.key) + '&lang=' + currentLang + '#results" class="greek-root-link">';
                html += '<span class="syriac">' + escHtml(r.root_syriac) + '</span> ';
                html += '<span class="root-key">' + escHtml(r.key) + '</span>';
                html += '</a>';
                html += ' <span class="greek-gloss">' + escHtml(r.gloss) + '</span>';
                html += ' <span class="count-badge">' + r.occurrences + '</span>';
                if (r.sabor) html += '<div class="greek-sabor">' + escHtml(r.sabor) + '</div>';
                html += '<a href="/visualize/' + encodeURIComponent(r.key) + '?lang=' + currentLang + '" class="viz-btn" style="margin-left:8px;" title="Visualize"><span class="material-symbols-outlined">hub</span></a>';
                html += '</div>';
            }
            resultsDiv.innerHTML = html;
        })
        .catch(function() {
            resultsDiv.innerHTML = '<p class="no-results">Error</p>';
        });
    return false;
}

function browseGreekWords() {
    var resultsDiv = document.getElementById('greek-search-results');
    resultsDiv.innerHTML = '<p class="search-loading">Loading...</p>';
    fetch('/api/greek-concordance?lang=' + currentLang)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (!data.words || !data.words.length) {
                resultsDiv.innerHTML = '<p class="no-results">No data</p>';
                return;
            }
            var html = '<p style="margin:8px 0; font-weight:600;">' + data.total + ' Greek words mapped to Syriac roots</p>';
            html += '<div class="greek-browse-list">';
            for (var i = 0; i < data.words.length; i++) {
                var w = data.words[i];
                html += '<a href="#" class="greek-browse-item" onclick="event.preventDefault(); document.getElementById(\'greek-input\').value=\'' + w.word.replace(/'/g, "\\'") + '\'; doGreekSearch();">';
                html += '<span class="greek-word">' + escHtml(w.word) + '</span> ';
                html += '<span class="greek-translit">' + escHtml(w.transliteration) + '</span> ';
                html += '<span class="greek-meaning">' + escHtml(w.meaning) + '</span> ';
                html += '<span class="count-badge">' + w.root_count + '</span>';
                html += '</a>';
            }
            html += '</div>';
            resultsDiv.innerHTML = html;
        })
        .catch(function() {
            resultsDiv.innerHTML = '<p class="no-results">Error</p>';
        });
}
```

- [ ] **Step 5: Add CSS for Greek concordance results**

In `style.css`, add:

```css
/* Greek concordance */
.greek-result-header {
    padding: 12px 0;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 12px;
}
.greek-result-card {
    padding: 10px 0;
    border-bottom: 1px solid var(--border-light);
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}
.greek-root-link {
    text-decoration: none;
    color: inherit;
    font-weight: 600;
}
.greek-root-link:hover { color: var(--accent); }
.greek-gloss { color: var(--text-muted); font-style: italic; }
.greek-sabor { font-size: 0.85em; color: var(--text-muted); width: 100%; margin-top: 2px; }
.greek-browse-list {
    display: flex;
    flex-direction: column;
    gap: 4px;
    max-height: 500px;
    overflow-y: auto;
}
.greek-browse-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 8px;
    text-decoration: none;
    color: inherit;
    border-radius: 4px;
}
.greek-browse-item:hover { background: var(--bg-highlight); }
.greek-browse-item .greek-word { font-weight: 600; min-width: 100px; }
.greek-browse-item .greek-translit { font-style: italic; color: var(--text-muted); min-width: 80px; }
.greek-browse-item .greek-meaning { flex: 1; }
```

- [ ] **Step 6: Restart server and test**

Navigate to `http://localhost:5009/?lang=en`, click "By Greek" tab, search for βασιλεύς. Click "All Greek words" to browse.

- [ ] **Step 7: Commit**

```bash
git add peshitta_roots/templates/index.html peshitta_roots/static/style.css
git commit -m "feat: add 'By Greek' search tab with concordance results and browse"
```

---

### Task 8: Final integration test and user review

- [ ] **Step 1: Restart server and run full verification**

```bash
lsof -ti:5009 | xargs kill 2>/dev/null
cd "/Users/jfresco16/Google Drive/Claude/Peshitta"
FLASK_APP=peshitta_roots.app python3 -m flask run --port 5009 &
sleep 5
```

Test each feature:

1. `http://localhost:5009/?q=SH-L-M&lang=en` — search results should include both NT and OT references
2. `http://localhost:5009/browse?lang=en&testament=ot` — only OT roots
3. `http://localhost:5009/read?book=Psalms&chapter=23&lang=en` — Syriac + transliteration, no translation
4. `http://localhost:5009/read?book=Isaiah&chapter=1&lang=en` — Isaiah renders
5. Click "By Greek" tab → search βασιλεύς → M-L-K result card
6. Click "All Greek words" → browse list
7. Click a word in OT reader → root modal shows NT + OT occurrences

- [ ] **Step 2: Wait for user review**

Ask user to test locally and confirm everything works before deploying.

- [ ] **Step 3: Commit any fixes, then deploy**

```bash
git push
git checkout main && git merge feature/passage-constellation && git push
git checkout feature/passage-constellation
```
