"""Flask web app for the Peshitta Triliteral Root Finder."""

import json
import os

from flask import Flask, render_template, request, jsonify

from .characters import parse_root_input, transliterate_syriac, transliterate_syriac_academic
from .corpus import PeshittaCorpus
from .extractor import RootExtractor
from .cognates import CognateLookup

app = Flask(__name__)

# --- Global state (initialized on first request) ---
_corpus: PeshittaCorpus | None = None
_extractor: RootExtractor | None = None
_cognate_lookup: CognateLookup | None = None
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
    global _corpus, _extractor, _cognate_lookup, _i18n, _initialized
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

    _initialized = True


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
    error = None
    result = None

    # Stats
    stats = _Namespace({
        'roots': _extractor.get_root_count(),
        'words': _corpus.total_words(),
        'unique': _corpus.total_unique(),
    })

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
                    matches.append({
                        'form': m.form,
                        'transliteration_academic': transliterate_syriac_academic(m.form),
                        'transliteration': m.transliteration,
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
                           translate_ref=translate_ref)


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
    words_translit = [transliterate_syriac(w) for w in words]
    words_translit_academic = [transliterate_syriac_academic(w) for w in words]

    lang = request.args.get('lang', 'es')
    translation_en = _corpus.get_verse_translation(ref, 'en')
    translation_es = _corpus.get_verse_translation(ref, 'es')

    return jsonify({
        'reference': ref,
        'syriac': syriac_text,
        'transliteration': transliterate_syriac(syriac_text),
        'words': words,
        'words_translit': words_translit,
        'words_translit_academic': words_translit_academic,
        'translation_en': translation_en,
        'translation_es': translation_es,
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


def create_app():
    """Factory function for the Flask app."""
    return app
