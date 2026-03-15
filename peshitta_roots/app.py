"""Flask web app for the Peshitta Triliteral Root Finder."""

import json
import os

from flask import Flask, render_template, request, jsonify

from .characters import (parse_root_input, transliterate_syriac, transliterate_syriac_academic,
                         transliterate_syriac_to_hebrew, transliterate_syriac_to_arabic)
from .corpus import PeshittaCorpus
from .extractor import RootExtractor
from .cognates import CognateLookup
from .glosser import WordGlosser

app = Flask(__name__)

# --- Global state (initialized on first request) ---
_corpus: PeshittaCorpus | None = None
_extractor: RootExtractor | None = None
_cognate_lookup: CognateLookup | None = None
_glosser: WordGlosser | None = None
_i18n: dict = {}
_initialized = False


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
    return transliterate_syriac


class _Namespace:
    """Simple namespace to pass translations to templates."""
    def __init__(self, d):
        self.__dict__.update(d)


@app.route('/')
def index():
    _init()

    lang = request.args.get('lang', 'es')
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    book_names = _i18n[lang].get('book_names', {})

    query = request.args.get('q', '').strip()
    cognate_word = request.args.get('cw', '').strip()
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic'):
        script = 'latin'
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

    # Handle cognate word lookup
    if cognate_word and not query:
        cw_results = _cognate_lookup.lookup_by_cognate_word(cognate_word)
        if len(cw_results) == 1:
            # Single match — redirect to root search
            root_syriac = cw_results[0].root_syriac
            root_translit = transliterate_syriac(root_syriac).upper()
            # Build dash-separated form
            parts = []
            i = 0
            while i < len(root_translit):
                if i + 1 < len(root_translit) and root_translit[i:i+2] in ('SH', 'KH', 'TH', 'TS'):
                    parts.append(root_translit[i:i+2])
                    i += 2
                else:
                    parts.append(root_translit[i])
                    i += 1
            query = '-'.join(parts)
        elif len(cw_results) > 1:
            # Multiple matches — show disambiguation
            disambiguation = []
            for entry in cw_results:
                root_translit = transliterate_syriac(entry.root_syriac).upper()
                parts = []
                i = 0
                while i < len(root_translit):
                    if i + 1 < len(root_translit) and root_translit[i:i+2] in ('SH', 'KH', 'TH', 'TS'):
                        parts.append(root_translit[i:i+2])
                        i += 2
                    else:
                        parts.append(root_translit[i])
                        i += 1
                dash_form = '-'.join(parts)
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
                'root_translit': query.upper(),
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
                           script=script)


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
    if script not in ('latin', 'hebrew', 'arabic'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)
    words_translit = [translit_fn(w) for w in words]

    lang = request.args.get('lang', 'es')
    if lang not in _i18n:
        lang = 'es'
    translation_en = _corpus.get_verse_translation(ref, 'en')
    translation_es = _corpus.get_verse_translation(ref, 'es')

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
        'prev_ref': prev_ref,
        'next_ref': next_ref,
        'script': script,
    })


@app.route('/api/suggest')
def api_suggest():
    """Return roots matching a Latin-letter prefix for autocomplete."""
    _init()
    prefix = request.args.get('prefix', '').strip().upper()
    if not prefix:
        return jsonify([])

    # Normalize alternate inputs: O -> E (both map to Ayin)
    normalized_prefix = prefix.replace('O', 'E')

    results = []
    for entry in _extractor.get_all_roots():
        translit = transliterate_syriac(entry.root).upper()
        # Build dash-separated form (e.g. "K-TH-B")
        parts = []
        i = 0
        while i < len(translit):
            if i + 1 < len(translit) and translit[i:i+2] in ('SH', 'KH', 'TH', 'TS'):
                parts.append(translit[i:i+2])
                i += 2
            else:
                parts.append(translit[i])
                i += 1
        dash_form = '-'.join(parts)

        if dash_form.startswith(prefix) or dash_form.startswith(normalized_prefix):
            # Show translit matching user's input style (O vs E for Ayin)
            display_form = dash_form
            if prefix != normalized_prefix:
                display_form = dash_form.replace('E', 'O')
            results.append({
                'root': entry.root,
                'translit': display_form,
                'count': entry.total_occurrences,
            })
            if len(results) >= 20:
                break

    return jsonify(results)


def _translit_to_dash(root_syriac: str) -> str:
    """Convert a Syriac root to dash-separated Latin form (e.g., K-TH-B)."""
    translit = transliterate_syriac(root_syriac).upper()
    parts = []
    i = 0
    while i < len(translit):
        if i + 1 < len(translit) and translit[i:i+2] in ('SH', 'KH', 'TH', 'TS'):
            parts.append(translit[i:i+2])
            i += 2
        else:
            parts.append(translit[i])
            i += 1
    return '-'.join(parts)


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
    lang = request.args.get('lang', 'es')
    if lang not in _i18n:
        lang = 'es'
    t = _Namespace(_i18n[lang])
    script = request.args.get('script', 'latin')
    if script not in ('latin', 'hebrew', 'arabic'):
        script = 'latin'
    translit_fn = _get_translit_fn(script)

    page = request.args.get('page', 1, type=int)
    per_page = 50

    all_roots = _extractor.get_all_roots()
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
        roots_data.append({
            'root': entry.root,
            'translit': translit_display,
            'translit_key': dash_form,
            'forms': len(entry.matches),
            'occurrences': entry.total_occurrences,
            'gloss': gloss,
        })

    return render_template('browse.html',
                           t=t, lang=lang,
                           roots=roots_data,
                           page=page, total_pages=total_pages,
                           total=total, script=script)


def create_app():
    """Factory function for the Flask app."""
    return app
