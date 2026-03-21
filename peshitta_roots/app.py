"""Flask web app for the Peshitta Triliteral Root Finder."""

import json
import os
import threading

import hashlib
import time
from datetime import date

from flask import Flask, render_template, request, jsonify, Response

from .characters import (parse_root_input, transliterate_syriac, transliterate_syriac_academic,
                         transliterate_syriac_to_hebrew, transliterate_syriac_to_arabic,
                         semitic_root_variants)
from .corpus import PeshittaCorpus
from .extractor import RootExtractor
from .cognates import CognateLookup
from .glosser import WordGlosser

app = Flask(__name__)


def _detect_lang():
    """Detect UI language from query param or browser Accept-Language header."""
    lang = request.args.get('lang', '').strip()
    if lang in ('es', 'en', 'he', 'ar'):
        return lang
    # Sniff browser Accept-Language
    best = request.accept_languages.best_match(['es', 'en', 'he', 'ar'], default='en')
    return best


# --- Global state (initialized on first request) ---
_corpus: PeshittaCorpus | None = None
_extractor: RootExtractor | None = None
_cognate_lookup: CognateLookup | None = None
_glosser: WordGlosser | None = None
_i18n: dict = {}
_initialized = False
_init_lock = threading.Lock()


def _get_data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def _get_csv_path():
    return os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'syriac_nt_traditional22_unicode.csv'
    )


def _init():
    global _corpus, _extractor, _cognate_lookup, _glosser, _i18n, _initialized
    if _initialized:
        return

    with _init_lock:
        if _initialized:
            return

        data_dir = _get_data_dir()

        # Load i18n
        i18n_path = os.path.join(data_dir, 'i18n.json')
        with open(i18n_path, 'r', encoding='utf-8') as f:
            _i18n = json.load(f)

        # Load corpus
        _corpus = PeshittaCorpus(_get_csv_path())
        _corpus.load()

        # Build root index
        _extractor = RootExtractor(_corpus, data_dir)
        _extractor.build_index()

        # Load cognates
        _cognate_lookup = CognateLookup(data_dir)
        _cognate_lookup.load()

        # Initialize word glosser
        _glosser = WordGlosser(_cognate_lookup, _extractor, data_dir)

        _initialized = True


def _get_translit_fn(script: str):
    """Return the transliteration function for the given script preference."""
    if script == 'hebrew':
        return transliterate_syriac_to_hebrew
    elif script == 'arabic':
        return transliterate_syriac_to_arabic
    elif script == 'syriac':
        return transliterate_syriac_academic
    return transliterate_syriac


def _translit_to_dash(root_syriac: str) -> str:
    """Convert a Syriac root to dash-separated Latin form (e.g., K-TH-B).

    Alef (ܐ) is rendered as "'" (glottal stop), not "A".
    """
    translit = transliterate_syriac(root_syriac)
    parts = []
    i = 0
    while i < len(translit):
        ch = translit[i]
        if ch == "'":
            parts.append("'")
            i += 1
        elif i + 1 < len(translit) and translit[i:i+2].upper() in ('SH', 'KH', 'TH', 'TS'):
            parts.append(translit[i:i+2].upper())
            i += 2
        else:
            parts.append(ch.upper())
            i += 1
    return '-'.join(parts)


class _Namespace:
    """Simple namespace to pass translations to templates."""
    def __init__(self, d):
        self.__dict__.update(d)



@app.route('/robots.txt')
def robots_txt():
    content = "User-agent: *\nAllow: /\n\nSitemap: https://peshitta.onrender.com/sitemap.xml\n"
    return Response(content, mimetype='text/plain')


_sitemap_cache = {'xml': None, 'ts': 0}


@app.route('/sitemap.xml')
def sitemap():
    _init()
    now = time.time()
    if _sitemap_cache['xml'] and now - _sitemap_cache['ts'] < 86400:
        return Response(_sitemap_cache['xml'], mimetype='application/xml')

    base = 'https://peshitta.onrender.com'
    langs = ['es', 'en', 'he', 'ar']
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']

    def _add_url(path, priority='0.5', changefreq='weekly'):
        lines.append('  <url>')
        lines.append(f'    <loc>{base}{path}</loc>')
        lines.append(f'    <changefreq>{changefreq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        for lg in langs:
            sep = '&amp;' if '?' in path else '?'
            lines.append(f'    <xhtml:link rel="alternate" hreflang="{lg}" href="{base}{path}{sep}lang={lg}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{base}{path}"/>')
        lines.append('  </url>')

    # Static pages
    _add_url('/', '1.0', 'weekly')
    _add_url('/browse', '0.8', 'weekly')
    _add_url('/read', '0.8', 'daily')
    _add_url('/help', '0.5', 'monthly')
    _add_url('/about', '0.5', 'monthly')
    _add_url('/methodology', '0.6', 'monthly')
    _add_url('/constellation', '0.7', 'weekly')

    # Dynamic root pages
    all_roots = _extractor.get_all_roots()
    for entry in all_roots:
        dash_form = _translit_to_dash(entry.root)
        _add_url(f'/visualize/{dash_form}', '0.6', 'monthly')

    lines.append('</urlset>')
    xml = '\n'.join(lines)
    _sitemap_cache['xml'] = xml
    _sitemap_cache['ts'] = now
    return Response(xml, mimetype='application/xml')


@app.route('/llms.txt')
def llms_txt():
    content = """# Peshitta Constellations
> Explore the New Testament from its Aramaic roots

## What this tool does
- Searches triliteral and biliteral Aramaic (Syriac) roots in the Peshitta New Testament
- Shows Hebrew (via BDB lexicon) and Arabic (via Lane's lexicon) cognates for each root
- Provides an interlinear reader with Syriac text, transliteration, and translation
- Visualizes root families as interactive constellation graphs
- Maps passage constellations showing root connections within a Bible passage
- Full text search across verse translations in all supported languages

## API Endpoints
- GET /?q=K-TH-B — Search for a root (returns HTML page with results)
- GET /api/verse?ref=Matthew+1:1&script=latin&trans=en — Get verse data (JSON)
- GET /api/text-search?q=love&lang=en — Search verse translations (JSON)
- GET /api/suggest?q=ktb — Root autocomplete suggestions (JSON)
- GET /api/roots?page=1&per_page=50 — Paginated root list (JSON)
- GET /api/root-family?root=K-TH-B&lang=en — Full root family with cognates (JSON)
- GET /api/word-root?form=ܟܬܒ — Look up root for a Syriac word form (JSON)
- GET /api/passage-constellation?book=Matthew&chapter=1&v_start=1&v_end=5 — Passage root map (JSON)

## Languages
UI available in: Spanish (es), English (en), Hebrew (he), Arabic (ar).
Use ?lang=XX query parameter on any page or API endpoint.

## Data Sources
- Text corpus: ETCBC syrnt (Peshitta New Testament, traditional 22-book canon)
- Hebrew cognates: Brown-Driver-Briggs (BDB) lexicon
- Arabic cognates: Lane's Arabic-English Lexicon
- Syriac lexicon: Payne Smith's Compendious Syriac Dictionary

## Coverage
- Full Peshitta New Testament (27 books)
- 1400+ triliteral and biliteral roots indexed
- Hebrew and Arabic cognate mappings for each root

## Author
Jossi Fresco — https://peshitta.onrender.com/about
Inspired by the Semitic exegesis methodology of Vicente Haya.

## License
Apache 2.0 with attribution requirement — see LICENSE file.
Source: https://github.com/Jossifresben/peshitta
"""
    return Response(content, mimetype='text/plain; charset=utf-8')


_rotd_cache: dict = {}


def _root_of_the_day(lang):
    """Pick a deterministic 'root of the day' based on today's date."""
    _init()
    today = str(date.today())
    cache_key = f'{today}:{lang}'
    if cache_key in _rotd_cache:
        return _rotd_cache[cache_key]

    # Load raw cognates JSON
    cog_path = os.path.join(_get_data_dir(), 'cognates.json')
    with open(cog_path, 'r', encoding='utf-8') as f:
        cog_data = json.load(f)
    roots = cog_data.get('roots', {})
    # Filter to roots with rich data (sabor_raiz + greek_parallel)
    rich = [(k, v) for k, v in roots.items()
            if v.get('sabor_raiz_en') and v.get('greek_parallel')]
    if not rich:
        return None
    # Deterministic pick based on date
    day_hash = int(hashlib.md5(str(date.today()).encode()).hexdigest(), 16)
    key, data = rich[day_hash % len(rich)]
    gloss_key = 'gloss_es' if lang == 'es' else 'gloss_en'
    sabor_key = f'sabor_raiz_{lang}' if lang in ('es', 'en') else 'sabor_raiz_en'
    lost_key = f'lost_{lang}' if lang in ('es', 'en') else 'lost_en'
    gp = data.get('greek_parallel', {})
    result = _Namespace({
        'key': key.upper(),
        'syriac': data.get('root_syriac', ''),
        'gloss': data.get(gloss_key, data.get('gloss_en', '')),
        'sabor': data.get(sabor_key, data.get('sabor_raiz_en', '')),
        'hebrew': data.get('hebrew', [])[:3],
        'arabic': data.get('arabic', [])[:3],
        'lost': gp.get(lost_key, gp.get('lost_en', ''))[:200],
        'greek_word': gp.get('word', ''),
        'greek_meaning': gp.get(f'meaning_{lang}' if lang in ('es', 'en') else 'meaning_en',
                                gp.get('meaning_en', '')),
    })
    _rotd_cache[cache_key] = result
    return result


@app.route('/')
def index():
    _init()

    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    book_names = _i18n[lang].get('book_names', {})

    query = request.args.get('q', '').strip()
    cognate_word = request.args.get('cw', '').strip()
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    translit_fn = _get_translit_fn(script)
    error = None
    result = None
    disambiguation = None

    # Stats
    stats = _Namespace({
        'roots': _extractor.get_root_count(),
        'words': _corpus.total_words(),
        'unique': _corpus.total_unique(),
    })

    # Root of the day
    rotd = _root_of_the_day(lang)

    # Handle cognate word lookup
    if cognate_word and not query:
        cw_results = _cognate_lookup.lookup_by_cognate_word(cognate_word)
        if len(cw_results) == 1:
            # Single match — redirect to root search
            query = _translit_to_dash(cw_results[0].root_syriac)
        elif len(cw_results) > 1:
            # Multiple matches — show disambiguation
            disambiguation = []
            for entry in cw_results:
                dash_form = _translit_to_dash(entry.root_syriac)
                gloss = entry.gloss_es if lang == 'es' else entry.gloss_en
                disambiguation.append({
                    'root_syriac': entry.root_syriac,
                    'root_translit': dash_form,
                    'gloss': gloss,
                })
        else:
            error = t.cognate_no_results

    if query:
        # Parse user input
        root_syriac = parse_root_input(query)
        if root_syriac is None:
            error = t.invalid_input
        else:
            # Look up in Peshitta
            root_entry = _extractor.lookup_root(root_syriac)

            # Look up cognates
            cognate_entry = _cognate_lookup.lookup(root_syriac)

            # Semitic sound correspondence fallback (e.g., s-l-m → sh-l-m)
            if not root_entry and not cognate_entry:
                for variant in semitic_root_variants(root_syriac):
                    v_root = _extractor.lookup_root(variant)
                    v_cognate = _cognate_lookup.lookup(variant)
                    if v_root or v_cognate:
                        root_syriac = variant
                        root_entry = v_root
                        cognate_entry = v_cognate
                        break

            # Get gloss from cognates or known roots
            gloss = ''
            if cognate_entry:
                gloss = cognate_entry.gloss_es if lang == 'es' else cognate_entry.gloss_en
            if not gloss:
                gloss = _extractor.get_root_gloss(root_syriac)

            # Build result
            matches = []
            if root_entry:
                for m in root_entry.matches:
                    # Use script-specific transliteration
                    if script == 'latin':
                        translit_display = m.transliteration
                    else:
                        translit_display = translit_fn(m.form)
                    matches.append({
                        'form': m.form,
                        'transliteration_academic': transliterate_syriac_academic(m.form),
                        'transliteration': translit_display,
                        'gloss': _glosser.gloss(m.form, root_syriac, lang),
                        'stem': _glosser.get_stem(m.form, root_syriac),
                        'count': m.count,
                        'references': m.references,
                    })

            hebrew = []
            arabic = []
            if cognate_entry:
                for hw in cognate_entry.hebrew:
                    hebrew.append({
                        'word': hw.word,
                        'transliteration': hw.transliteration,
                        'meaning': hw.meaning_es if lang == 'es' else hw.meaning_en,
                    })
                for aw in cognate_entry.arabic:
                    arabic.append({
                        'word': aw.word,
                        'transliteration': aw.transliteration,
                        'meaning': aw.meaning_es if lang == 'es' else aw.meaning_en,
                    })

            result = {
                'root': root_syriac,
                'root_translit': _translit_to_dash(root_syriac),
                'gloss': gloss,
                'matches': matches,
                'hebrew': hebrew,
                'arabic': arabic,
            }

    def translate_ref(ref):
        """Translate book names in references."""
        for en_name, local_name in book_names.items():
            if ref.startswith(en_name):
                return ref.replace(en_name, local_name, 1)
        return ref

    return render_template('index.html',
                           t=t, lang=lang, query=query,
                           error=error, result=result, stats=stats,
                           translate_ref=translate_ref,
                           cognate_word=cognate_word,
                           disambiguation=disambiguation,
                           script=script, trans=trans, rotd=rotd,
                           meta_description=_i18n[lang].get('meta_index', ''),
                           canonical_path='/')


@app.route('/api/verse')
def api_verse():
    """Return verse text in Syriac and transliteration for a given reference."""
    _init()
    ref = request.args.get('ref', '').strip()
    if not ref:
        return jsonify({'error': 'Missing ref parameter'}), 400

    syriac_text = _corpus.get_verse_text(ref)
    if syriac_text is None:
        return jsonify({'error': 'Verse not found'}), 404

    # Build word-level arrays for highlighting
    words = syriac_text.split()
    words_translit_academic = [transliterate_syriac_academic(w) for w in words]

    # Script-specific transliteration
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)
    words_translit = [translit_fn(w) for w in words]

    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    translation_en = _corpus.get_verse_translation(ref, 'en')
    translation_es = _corpus.get_verse_translation(ref, 'es')
    translation_he = _corpus.get_verse_translation(ref, 'he')
    translation_ar = _corpus.get_verse_translation(ref, 'ar')

    # Adjacent verse references for modal navigation
    prev_ref = _corpus.get_adjacent_ref(ref, -1)
    next_ref = _corpus.get_adjacent_ref(ref, +1)

    # Translate book name for display
    book_names = _i18n[lang].get('book_names', {})
    ref_display = ref
    for en_name, local_name in book_names.items():
        if ref.startswith(en_name):
            ref_display = ref.replace(en_name, local_name, 1)
            break

    return jsonify({
        'reference': ref,
        'reference_display': ref_display,
        'syriac': syriac_text,
        'transliteration': ' '.join(words_translit),
        'words': words,
        'words_translit': words_translit,
        'words_translit_academic': words_translit_academic,
        'translation_en': translation_en,
        'translation_es': translation_es,
        'translation_he': translation_he,
        'translation_ar': translation_ar,
        'prev_ref': prev_ref,
        'next_ref': next_ref,
        'script': script,
    })


@app.route('/api/text-search')
def api_text_search():
    """Search verse translations (or Syriac text) for a substring."""
    _init()
    query = request.args.get('q', '').strip()
    lang = request.args.get('lang', 'en')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    if not query or len(query) < 2:
        return jsonify({'query': query, 'total': 0, 'results': []})

    # Auto-detect query language from script
    if lang == 'auto':
        # Check for Syriac, Hebrew, Arabic scripts; default to trying all Latin languages
        if any('\u0710' <= ch <= '\u074f' for ch in query):
            lang = 'syriac'  # will be handled by search_text
        elif any('\u0590' <= ch <= '\u05ff' for ch in query):
            lang = 'he'
        elif any('\u0600' <= ch <= '\u06ff' for ch in query):
            lang = 'ar'
        else:
            # Latin script — search all Latin-script languages, return first with results
            lang = None

    if lang is None:
        # Search en and es, merge results by verse order
        all_results = []
        for try_lang in ('en', 'es'):
            results = _corpus.search_text(query, try_lang)
            if results:
                all_results = results
                lang = try_lang
                break
        if not all_results:
            lang = 'en'
    else:
        all_results = _corpus.search_text(query, lang)

    # Use detected lang for UI (book names)
    ui_lang = _detect_lang()
    lang_section = _i18n.get(ui_lang, _i18n.get('en', {}))
    book_names = lang_section.get('book_names', {})

    def translate_ref(ref):
        for en_name, local_name in book_names.items():
            if ref.startswith(en_name):
                return ref.replace(en_name, local_name, 1)
        return ref

    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)

    all_results = _corpus.search_text(query, lang)
    total = len(all_results)

    # Paginate
    start = (page - 1) * per_page
    end = start + per_page
    page_results = all_results[start:end]

    # For translation searches, find which Syriac words match the query
    # by checking their glosses
    query_lower = query.lower()

    # Parse references for reader links
    out = []
    for r in page_results:
        ref = r['reference']
        last_space = ref.rfind(' ')
        book = ref[:last_space] if last_space != -1 else ref
        ch_v = ref[last_space + 1:] if last_space != -1 else ''
        chapter = ch_v.split(':')[0] if ':' in ch_v else ''
        verse = ch_v.split(':')[1] if ':' in ch_v else ''

        # Build per-word data with transliteration and gloss-based highlighting
        syriac_words = r['syriac'].split()
        translit_words = [translit_fn(w) for w in syriac_words]
        highlight_indices = []

        if r['match_type'] == 'translation':
            for i, w in enumerate(syriac_words):
                root = _extractor.lookup_word_root(w)
                if root:
                    gloss = _glosser.gloss(w, root, 'en').lower()
                    if query_lower in gloss:
                        highlight_indices.append(i)

        out.append({
            'reference': ref,
            'reference_display': translate_ref(ref),
            'syriac': r['syriac'],
            'translation': r['translation'],
            'match_positions': r['match_positions'],
            'match_type': r['match_type'],
            'book': book,
            'chapter': chapter,
            'verse': verse,
            'words': syriac_words,
            'words_translit': translit_words,
            'highlight_indices': highlight_indices,
        })

    return jsonify({
        'query': query,
        'search_lang': lang,
        'total': total,
        'page': page,
        'per_page': per_page,
        'results': out,
    })


@app.route('/api/suggest')
def api_suggest():
    """Return roots matching a Latin-letter prefix for autocomplete."""
    _init()
    prefix = request.args.get('prefix', '').strip().upper()
    if not prefix:
        return jsonify([])

    # Normalize alternate inputs: O -> E (both map to Ayin), A -> ' (alef)
    normalized_prefix = prefix.replace('O', 'E')
    # Also try matching A as alef (') for backward compatibility
    alef_prefix = None
    if normalized_prefix.startswith('A'):
        alef_prefix = "'" + normalized_prefix[1:]

    results = []
    for entry in _extractor.get_all_roots():
        dash_form = _translit_to_dash(entry.root)

        if (dash_form.startswith(prefix) or
            dash_form.startswith(normalized_prefix) or
            (alef_prefix and dash_form.startswith(alef_prefix))):
            display_form = dash_form
            results.append({
                'root': entry.root,
                'translit': display_form,
                'count': entry.total_occurrences,
            })
            if len(results) >= 20:
                break

    return jsonify(results)


@app.route('/api/roots')
def api_roots():
    """Return a paginated list of all roots sorted by frequency."""
    _init()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    per_page = min(per_page, 100)  # cap at 100

    all_roots = _extractor.get_all_roots()
    total = len(all_roots)
    total_pages = (total + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    page_roots = all_roots[start:end]

    roots_data = []
    for entry in page_roots:
        dash_form = _translit_to_dash(entry.root)
        gloss = ''
        cognate_entry = _cognate_lookup.lookup(entry.root)
        if cognate_entry:
            gloss = cognate_entry.gloss_en
        if not gloss:
            gloss = _extractor.get_root_gloss(entry.root)
        roots_data.append({
            'root': entry.root,
            'translit': dash_form,
            'forms': len(entry.matches),
            'occurrences': entry.total_occurrences,
            'gloss': gloss,
        })

    return jsonify({
        'page': page,
        'per_page': per_page,
        'total': total,
        'total_pages': total_pages,
        'roots': roots_data,
    })


@app.route('/browse')
def browse():
    """Browse all roots with pagination."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    translit_fn = _get_translit_fn(script)

    page = request.args.get('page', 1, type=int)
    freq = request.args.get('freq', '', type=str)
    per_page = 50

    all_roots = _extractor.get_all_roots()
    # Filter by frequency category
    freq_max = {'hapax': 1, 'dis': 2, 'tris': 3, 'tetrakis': 4}.get(freq)
    if freq_max:
        all_roots = [r for r in all_roots if r.total_occurrences == freq_max]
    total = len(all_roots)
    total_pages = (total + per_page - 1) // per_page
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page
    page_roots = all_roots[start:end]

    roots_data = []
    for entry in page_roots:
        dash_form = _translit_to_dash(entry.root)
        if script != 'latin':
            translit_display = translit_fn(entry.root)
        else:
            translit_display = dash_form
        gloss = ''
        cognate_entry = _cognate_lookup.lookup(entry.root)
        if cognate_entry:
            gloss = cognate_entry.gloss_es if lang == 'es' else cognate_entry.gloss_en
        if not gloss:
            gloss = _extractor.get_root_gloss(entry.root)
        # For rare roots without gloss, show first verse reference + word form
        context_ref = ''
        context_form = ''
        if not gloss and entry.matches:
            m = entry.matches[0]
            context_form = m.form
            if m.references:
                context_ref = m.references[0]

        roots_data.append({
            'root': entry.root,
            'translit': translit_display,
            'translit_key': dash_form,
            'forms': len(entry.matches),
            'occurrences': entry.total_occurrences,
            'gloss': gloss,
            'context_ref': context_ref,
            'context_form': context_form,
        })

    freq_param = f'&freq={freq}' if freq else ''
    cp = f'/browse?page={page}{freq_param}' if page > 1 or freq else '/browse'
    return render_template('browse.html',
                           t=t, lang=lang,
                           roots=roots_data,
                           page=page, total_pages=total_pages,
                           total=total, script=script, trans=trans,
                           freq=freq,
                           meta_description=_i18n[lang].get('meta_browse', ''),
                           canonical_path=cp)


@app.route('/read')
def read():
    """Interlinear chapter reader."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    book_names = _i18n[lang].get('book_names', {})
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang

    books = _corpus.get_books()
    book = request.args.get('book', books[0][0] if books else 'Matthew')
    # Find max chapter for selected book
    max_chapter = 1
    for b_name, b_max in books:
        if b_name == book:
            max_chapter = b_max
            break
    chapter = request.args.get('chapter', 1, type=int)
    chapter = max(1, min(chapter, max_chapter))

    # Get chapter verses
    chapter_verses = _corpus.get_chapter_verses(book, chapter)

    verses_data = []
    for verse_num, ref, syriac_text in chapter_verses:
        words_data = []
        for w in syriac_text.split():
            root = _extractor.lookup_word_root(w)
            root_translit = _translit_to_dash(root) if root else None
            words_data.append({
                'syriac': w,
                'translit': translit_fn(w),
                'has_root': root is not None,
                'root': root,
                'root_translit': root_translit,
            })

        translation = _corpus.get_verse_translation(ref, trans)
        if not translation:
            translation = _corpus.get_verse_translation(ref, 'en')

        verses_data.append({
            'number': verse_num,
            'reference': ref,
            'words': words_data,
            'translation': translation,
        })

    # Build books JSON for JS navigation
    books_json = json.dumps([{'name': b, 'chapters': c} for b, c in books])

    # Prev/next chapter
    prev_chapter = chapter - 1 if chapter > 1 else None
    next_chapter = chapter + 1 if chapter < max_chapter else None

    cp = f'/read?book={book}&chapter={chapter}'
    return render_template('read.html',
                           t=t, lang=lang, script=script, trans=trans,
                           books=books, book=book,
                           chapter=chapter, max_chapter=max_chapter,
                           verses=verses_data,
                           book_names=book_names,
                           books_json=books_json,
                           prev_chapter=prev_chapter,
                           next_chapter=next_chapter,
                           meta_description=_i18n[lang].get('meta_read', ''),
                           canonical_path=cp)


@app.route('/help')
def help_page():
    """Help page with how-to, settings, capabilities, and FAQ."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    return render_template('help.html', t=t, lang=lang, script=script, trans=trans,
                           meta_description=_i18n[lang].get('meta_help', ''),
                           canonical_path='/help')


@app.route('/methodology')
def methodology_page():
    """Methodology page describing the Semitic exegesis method."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    return render_template('methodology.html', t=t, lang=lang, script=script, trans=trans,
                           meta_description=_i18n[lang].get('meta_methodology', ''),
                           canonical_path='/methodology')


@app.route('/about')
def about_page():
    """About the author page."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    return render_template('about.html', t=t, lang=lang,
                           meta_description=_i18n[lang].get('meta_about', ''),
                           canonical_path='/about')


@app.route('/api/word-root')
def api_word_root():
    """Return root info for a given word form."""
    _init()
    form = request.args.get('form', '').strip()
    if not form:
        return jsonify({'error': 'Missing form parameter'}), 400

    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)

    root = _extractor.lookup_word_root(form)
    if root is None:
        return jsonify({'error': 'No root found'}), 404

    root_entry = _extractor.lookup_root(root)
    cognate_entry = _cognate_lookup.lookup(root)

    gloss = ''
    if cognate_entry:
        gloss = cognate_entry.gloss_es if lang == 'es' else cognate_entry.gloss_en
    if not gloss:
        gloss = _extractor.get_root_gloss(root)

    matches = []
    if root_entry:
        for m in root_entry.matches:
            if script == 'latin':
                translit_display = m.transliteration
            else:
                translit_display = translit_fn(m.form)
            matches.append({
                'form': m.form,
                'transliteration': translit_display,
                'gloss': _glosser.gloss(m.form, root, lang),
                'stem': _glosser.get_stem(m.form, root),
                'count': m.count,
                'references': m.references[:20],
            })

    # Greek parallel — compact degradation for word modal
    degradation = None
    if cognate_entry and cognate_entry.greek_parallel:
        gp = cognate_entry.greek_parallel
        is_es = lang == 'es'
        degradation = {
            'greek_word': gp.word,
            'greek_translit': gp.transliteration,
            'meaning': gp.meaning_es if is_es else gp.meaning_en,
            'aramaic_range': gp.aramaic_range_es if is_es else gp.aramaic_range_en,
            'lost': gp.lost_es if is_es else gp.lost_en,
        }

    return jsonify({
        'form': form,
        'root': root,
        'root_translit': _translit_to_dash(root),
        'gloss': gloss,
        'matches': matches,
        'degradation': degradation,
    })


@app.route('/visualize/<root_key>')
def visualize(root_key):
    """Root family visualizer page."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    display_key = root_key.upper()
    if display_key.startswith('A-'):
        display_key = "'" + display_key[1:]
    return render_template('visualize.html', t=t, lang=lang, script=script,
                           trans=trans, root_key=display_key,
                           meta_description=_i18n[lang].get('meta_visualize', ''),
                           canonical_path=f'/visualize/{root_key}')


@app.route('/api/root-family')
def api_root_family():
    """Return full root family data for the visualizer."""
    _init()
    root_input = request.args.get('root', '').strip()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)

    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    # For cognate meanings, use trans if es/en; fall back to lang for he/ar (no meanings in those)
    meaning_lang = trans if trans in ('es', 'en') else lang

    if not root_input:
        return jsonify({'error': 'Missing root parameter'}), 400

    root_syriac = parse_root_input(root_input)
    if root_syriac is None:
        return jsonify({'error': 'Invalid root'}), 400

    root_entry = _extractor.lookup_root(root_syriac)
    cognate_entry = _cognate_lookup.lookup(root_syriac)

    # Semitic sound correspondence fallback (e.g., s-l-m → sh-l-m)
    if not root_entry and not cognate_entry:
        for variant in semitic_root_variants(root_syriac):
            v_root = _extractor.lookup_root(variant)
            v_cognate = _cognate_lookup.lookup(variant)
            if v_root or v_cognate:
                root_syriac = variant
                root_entry = v_root
                cognate_entry = v_cognate
                break

    gloss = ''
    sabor_raiz_es = ''
    sabor_raiz_en = ''
    if cognate_entry:
        gloss = cognate_entry.gloss_es if meaning_lang == 'es' else cognate_entry.gloss_en
        sabor_raiz_es = getattr(cognate_entry, 'sabor_raiz_es', '') or ''
        sabor_raiz_en = getattr(cognate_entry, 'sabor_raiz_en', '') or ''
    if not gloss:
        gloss = _extractor.get_root_gloss(root_syriac)

    sabor_raiz = sabor_raiz_es if meaning_lang == 'es' else sabor_raiz_en
    if not sabor_raiz:
        sabor_raiz = gloss

    # Syriac word forms — filter out inflected forms with proclitics
    # for the visualizer (keep only base/unique lexical forms)
    PROCLITICS = {'\u0718', '\u0715', '\u0712', '\u0720'}  # ܘ ܕ ܒ ܠ
    COMPOUND_PROCLITICS = {
        '\u0718\u0712', '\u0718\u0720', '\u0718\u0721', '\u0718\u0715',
        '\u0715\u0712', '\u0715\u0720', '\u0715\u0721', '\u0720\u0721',
    }
    syriac_words = []
    seen_meanings = set()
    if root_entry:
        for m in root_entry.matches:
            # Skip forms starting with proclitics (d-, w-, b-, l- and compounds)
            has_proclitic = False
            if len(m.form) > 1:
                if m.form[:2] in COMPOUND_PROCLITICS:
                    has_proclitic = True
                elif m.form[0] in PROCLITICS:
                    has_proclitic = True
            if has_proclitic:
                continue

            meaning = _glosser.gloss(m.form, root_syriac, meaning_lang)
            # Deduplicate by meaning
            if meaning and meaning in seen_meanings:
                continue
            if meaning:
                seen_meanings.add(meaning)

            if script == 'latin':
                translit_display = m.transliteration
            else:
                translit_display = translit_fn(m.form)
            syriac_words.append({
                'word': m.form,
                'translit': translit_display,
                'meaning': meaning,
                'references': m.references[:5],
            })

    # Cognates
    hebrew = []
    arabic = []
    if cognate_entry:
        for hw in cognate_entry.hebrew:
            h = {
                'word': hw.word,
                'translit': hw.transliteration,
                'meaning': hw.meaning_es if meaning_lang == 'es' else hw.meaning_en,
            }
            if hw.outlier:
                h['outlier'] = True
            hebrew.append(h)
        for aw in cognate_entry.arabic:
            a = {
                'word': aw.word,
                'translit': aw.transliteration,
                'meaning': aw.meaning_es if meaning_lang == 'es' else aw.meaning_en,
            }
            if aw.outlier:
                a['outlier'] = True
            arabic.append(a)

    # Semantic bridges
    bridges = []
    if cognate_entry and cognate_entry.semantic_bridges:
        for b in cognate_entry.semantic_bridges:
            bridges.append({
                'outlier_key': b.outlier_key,
                'target_root': b.target_root,
                'relationship': b.relationship,
                'bridge_concept': b.bridge_concept_es if meaning_lang == 'es' else b.bridge_concept_en,
            })

    # Paradigmatic citation — best verse for this root
    paradigmatic_ref = ''
    paradigmatic_verse = ''
    paradigmatic_syriac = ''
    paradigmatic_translit = ''
    paradigmatic_form = ''

    # Check for manual override in cognates.json
    override_ref = cognate_entry.paradigmatic_ref_override if cognate_entry else ''

    if root_entry and root_entry.matches:
        best_match = max(root_entry.matches, key=lambda m: m.count)
        paradigmatic_form = best_match.form

        # Use override ref if set, otherwise pick the most frequent form's first reference
        if override_ref:
            paradigmatic_ref = override_ref
        elif best_match.references:
            paradigmatic_ref = best_match.references[0]

        if paradigmatic_ref:
            verse_text = _corpus.get_verse_translation(paradigmatic_ref, trans)
            if verse_text:
                paradigmatic_verse = verse_text
            # Original Syriac + transliteration
            syriac_text = _corpus.get_verse_text(paradigmatic_ref)
            if syriac_text:
                paradigmatic_syriac = syriac_text
                words = syriac_text.split()
                paradigmatic_translit = ' '.join(translit_fn(w) for w in words)
            # Translate book name for display
            book_names = _i18n.get(trans, {}).get('book_names', {}) or _i18n.get(meaning_lang, {}).get('book_names', {})
            para_ref_display = paradigmatic_ref
            for en_name, local_name in book_names.items():
                if paradigmatic_ref.startswith(en_name):
                    para_ref_display = paradigmatic_ref.replace(en_name, local_name, 1)
                    break
            paradigmatic_ref = para_ref_display

    # Sister roots — roots sharing 2 of 3 consonants
    sister_roots = []
    root_parts = root_input.lower().split('-')
    if len(root_parts) == 3:
        all_keys = _cognate_lookup.get_all_keys()
        for other_key in all_keys:
            if other_key == root_input.lower():
                continue
            other_parts = other_key.split('-')
            if len(other_parts) == 3:
                shared = sum(1 for a, b in zip(root_parts, other_parts) if a == b)
                if shared >= 2:
                    other_entry = _cognate_lookup.lookup_by_key(other_key)
                    other_gloss = ''
                    other_syriac = ''
                    if other_entry:
                        other_gloss = other_entry.gloss_es if meaning_lang == 'es' else other_entry.gloss_en
                        other_syriac = other_entry.root_syriac
                    sister_roots.append({
                        'root_translit': other_key.upper().replace('A-', "'-", 1) if other_key.startswith('a-') else other_key.upper(),
                        'root_syriac': other_syriac,
                        'gloss': other_gloss,
                        'shared': shared,
                    })

    # Greek parallel — translation degradation data
    greek_parallel = None
    if cognate_entry and cognate_entry.greek_parallel:
        gp = cognate_entry.greek_parallel
        is_es = meaning_lang == 'es'
        greek_parallel = {
            'word': gp.word,
            'transliteration': gp.transliteration,
            'meaning': gp.meaning_es if is_es else gp.meaning_en,
            'aramaic_range': gp.aramaic_range_es if is_es else gp.aramaic_range_en,
            'greek_range': gp.greek_range_es if is_es else gp.greek_range_en,
            'lost': gp.lost_es if is_es else gp.lost_en,
        }

    return jsonify({
        'root': root_syriac,
        'root_translit': _translit_to_dash(root_syriac) if root_syriac else root_input.upper(),
        'gloss': gloss,
        'sabor_raiz': sabor_raiz,
        'syriac_words': syriac_words,
        'hebrew': hebrew,
        'arabic': arabic,
        'semantic_bridges': bridges,
        'paradigmatic_ref': paradigmatic_ref,
        'paradigmatic_verse': paradigmatic_verse,
        'paradigmatic_syriac': paradigmatic_syriac,
        'paradigmatic_translit': paradigmatic_translit,
        'paradigmatic_form': paradigmatic_form,
        'paradigmatic_form_translit': translit_fn(paradigmatic_form) if paradigmatic_form else '',
        'paradigmatic_note': (cognate_entry.paradigmatic_note_es if meaning_lang == 'es' else cognate_entry.paradigmatic_note_en) if cognate_entry else '',
        'sister_roots': sister_roots,
        'greek_parallel': greek_parallel,
    })


@app.route('/constellation')
def constellation():
    """Passage constellation visualizer page."""
    _init()
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    book = request.args.get('book', 'Matthew')
    chapter = request.args.get('chapter', 1, type=int)
    v_start = request.args.get('v_start', 1, type=int)
    v_end = request.args.get('v_end', v_start, type=int)
    book_names = _i18n[lang].get('book_names', {})
    cp = f'/constellation?book={book}&chapter={chapter}&v_start={v_start}&v_end={v_end}'
    return render_template('constellation.html', t=t, lang=lang, script=script,
                           trans=trans, book=book, chapter=chapter,
                           v_start=v_start, v_end=v_end,
                           book_names=book_names,
                           meta_description=_i18n[lang].get('meta_constellation', ''),
                           canonical_path=cp)


@app.route('/api/passage-constellation')
def api_passage_constellation():
    """Return constellation data for a passage: roots, cognates, and inter-root connections."""
    _init()
    book = request.args.get('book', '').strip()
    chapter = request.args.get('chapter', 0, type=int)
    v_start = request.args.get('v_start', 0, type=int)
    v_end = request.args.get('v_end', v_start, type=int)
    # Validate book against known books
    valid_books = {b[0] for b in _corpus.get_books()}
    if book not in valid_books:
        return jsonify({'error': 'Invalid book name', 'roots': [], 'connections': []}), 400
    lang = _detect_lang()
    if lang not in _i18n:
        lang = 'es'
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic', 'syriac'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)
    trans = request.args.get('trans', lang)
    if trans not in ('en', 'es', 'he', 'ar'):
        trans = lang
    meaning_lang = trans if trans in ('es', 'en') else lang

    if not book or not chapter or not v_start:
        return jsonify({'error': 'Missing book, chapter, or v_start'}), 400

    # Collect verses
    verses = []
    for v_num in range(v_start, v_end + 1):
        ref = f"{book} {chapter}:{v_num}"
        syriac_text = _corpus.get_verse_text(ref)
        if syriac_text is None:
            continue
        words = syriac_text.split()
        verse_words = []
        for w in words:
            root = _extractor.lookup_word_root(w)
            root_translit = _translit_to_dash(root) if root else None
            verse_words.append({
                'syriac': w,
                'translit': translit_fn(w),
                'root': root_translit,
                'root_syriac': root,
            })
        # Get translation
        translation = _corpus.get_verse_translation(ref, trans)
        if not translation:
            translation = _corpus.get_verse_translation(ref, 'en')

        verses.append({
            'ref': ref,
            'verse_num': v_num,
            'words': verse_words,
            'translation': translation or '',
        })

    if not verses:
        return jsonify({'error': 'No verses found'}), 404

    # Collect unique roots with frequency and word forms
    root_map = {}  # root_translit -> { root_syriac, word_forms, count }
    for v in verses:
        for w in v['words']:
            rt = w['root']
            if not rt:
                continue
            if rt not in root_map:
                root_map[rt] = {
                    'root_syriac': w['root_syriac'],
                    'root_translit': rt,
                    'word_forms': [],
                    'count': 0,
                }
            root_map[rt]['count'] += 1
            # Track unique word forms
            form_key = w['syriac']
            existing = [f for f in root_map[rt]['word_forms'] if f['syriac'] == form_key]
            if not existing:
                root_map[rt]['word_forms'].append({
                    'syriac': w['syriac'],
                    'translit': w['translit'],
                    'verse_ref': v['ref'],
                })

    # Build root data with cognates
    roots_data = []
    root_keys_in_passage = set()  # cognate.json keys for bridge detection
    for rt, info in root_map.items():
        root_syriac = info['root_syriac']
        cognate_entry = _cognate_lookup.lookup(root_syriac)

        gloss = ''
        if cognate_entry:
            gloss = cognate_entry.gloss_es if meaning_lang == 'es' else cognate_entry.gloss_en
        if not gloss:
            gloss = _extractor.get_root_gloss(root_syriac)

        # Cognates
        hebrew = []
        arabic = []
        bridges_raw = []
        if cognate_entry:
            for hw in cognate_entry.hebrew:
                hebrew.append({
                    'word': hw.word,
                    'translit': hw.transliteration,
                    'meaning': hw.meaning_es if meaning_lang == 'es' else hw.meaning_en,
                    'outlier': hw.outlier,
                })
            for aw in cognate_entry.arabic:
                arabic.append({
                    'word': aw.word,
                    'translit': aw.transliteration,
                    'meaning': aw.meaning_es if meaning_lang == 'es' else aw.meaning_en,
                    'outlier': aw.outlier,
                })
            if cognate_entry.semantic_bridges:
                for b in cognate_entry.semantic_bridges:
                    bridges_raw.append({
                        'target_root': b.target_root,
                        'bridge_concept': b.bridge_concept_es if meaning_lang == 'es' else b.bridge_concept_en,
                    })
            # Track the cognate key for this root
            key = _cognate_lookup._syriac_to_key.get(root_syriac)
            if key:
                root_keys_in_passage.add(key)

        roots_data.append({
            'root_translit': rt,
            'root_syriac': root_syriac,
            'gloss': gloss,
            'frequency': info['count'],
            'word_forms': info['word_forms'],
            'hebrew': hebrew,
            'arabic': arabic,
            'bridges': bridges_raw,
        })

    # Sort by frequency (most common roots first)
    roots_data.sort(key=lambda r: -r['frequency'])

    # Detect inter-root connections (bridges between roots in the passage)
    connections = []
    passage_root_translits = {r['root_translit'] for r in roots_data}
    seen_connections = set()
    for rd in roots_data:
        for b in rd.get('bridges', []):
            target_key = b['target_root']
            # Check if target root is also in this passage
            # The target_root in bridges is a cognates.json key (e.g., "n-w-kh")
            # Convert to translit format: uppercase, but Alef 'a-' → "'-"
            target_translit = target_key.upper().replace('A-', "'-", 1) if target_key.startswith('a-') else target_key.upper()
            if target_translit in passage_root_translits:
                conn_key = tuple(sorted([rd['root_translit'], target_translit]))
                if conn_key not in seen_connections:
                    seen_connections.add(conn_key)
                    connections.append({
                        'source': rd['root_translit'],
                        'target': target_translit,
                        'concept': b['bridge_concept'],
                    })

    # Also check for shared consonants (2 of 3)
    root_translits = list(passage_root_translits)
    for i in range(len(root_translits)):
        for j in range(i + 1, len(root_translits)):
            r1_parts = root_translits[i].split('-')
            r2_parts = root_translits[j].split('-')
            if len(r1_parts) >= 2 and len(r2_parts) >= 2:
                shared = sum(1 for a, b in zip(r1_parts, r2_parts) if a == b)
                max_len = max(len(r1_parts), len(r2_parts))
                if shared >= 2:
                    conn_key = tuple(sorted([root_translits[i], root_translits[j]]))
                    if conn_key not in seen_connections:
                        seen_connections.add(conn_key)
                        label = (meaning_lang == 'es' and 'Raíces hermanas' or 'Sister roots') + \
                                f' ({shared}/{max_len})'
                        connections.append({
                            'source': root_translits[i],
                            'target': root_translits[j],
                            'concept': label,
                            'type': 'sister',
                        })

    # Build display reference
    book_names = _i18n[lang].get('book_names', {})
    book_display = book_names.get(book, book)
    if v_start == v_end:
        ref_display = f"{book_display} {chapter}:{v_start}"
    else:
        ref_display = f"{book_display} {chapter}:{v_start}-{v_end}"

    return jsonify({
        'reference': ref_display,
        'verses': verses,
        'roots': roots_data,
        'connections': connections,
        'total_roots': len(roots_data),
    })


def create_app():
    """Factory function for the Flask app."""
    return app
