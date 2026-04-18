"""CSV parser and word index builder for the Peshitta corpus."""

import csv
import json
import os
from collections import Counter


class PeshittaCorpus:
    """Loads the Peshitta NT/OT CSV files and builds searchable word indexes."""

    _NT_BOOKS: set[str] = {
        'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
        '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
        'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
        '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
        'James', '1 Peter', '1 John',
    }

    def __init__(self, csv_path: str | None = None,
                 extra_csv_paths: list[str] | None = None):
        if csv_path is None:
            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'syriac_nt_traditional22_unicode.csv'
            )
        self.csv_path = csv_path
        self._extra_csv_paths = extra_csv_paths or []
        self._occurrences: dict[str, list[str]] = {}  # word -> [reference, ...]
        self._total_words: int = 0
        self._verses: dict[str, str] = {}  # reference -> syriac text
        self._verse_order: list[str] = []  # ordered references for book iteration
        self._translations: dict[str, dict] = {}  # lang -> {ref: text}, lazy-loaded per language
        self._testament: dict[str, str] = {}  # book name -> 'nt' or 'ot'
        self._loaded = False

    def load(self) -> None:
        """Parse the CSV file(s) and build the word index."""
        if self._loaded:
            return

        all_paths = [self.csv_path] + self._extra_csv_paths
        for path in all_paths:
            if not os.path.exists(path):
                continue

            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    syriac_text = row['syriac'].strip()
                    if not syriac_text:
                        continue

                    reference = row['reference']

                    # Extract book name and tag testament
                    last_space = reference.rfind(' ')
                    book = reference[:last_space] if last_space != -1 else reference
                    self._testament[book] = 'nt' if book in self._NT_BOOKS else 'ot'

                    self._verses[reference] = syriac_text
                    self._verse_order.append(reference)

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

    def get_unique_words(self) -> set[str]:
        """Return all unique surface forms in the corpus."""
        self.load()
        return set(self._occurrences.keys())

    def get_occurrences(self, word: str) -> list[str]:
        """Return all reference strings where this word appears."""
        self.load()
        return self._occurrences.get(word, [])

    def word_frequency(self) -> Counter:
        """Return word frequency counts across the entire corpus."""
        self.load()
        return Counter({word: len(refs) for word, refs in self._occurrences.items()})

    def total_words(self) -> int:
        """Return total number of word tokens."""
        self.load()
        return self._total_words

    def total_unique(self) -> int:
        """Return number of unique surface forms."""
        self.load()
        return len(self._occurrences)

    def get_books(self) -> list[tuple[str, int]]:
        """Return ordered list of (book_name, max_chapter) tuples."""
        self.load()
        if not hasattr(self, '_books_cache'):
            books_max_ch: dict[str, int] = {}
            book_list: list[tuple[str, int]] = []
            for ref in self._verse_order:
                # Parse "Book chapter:verse"
                last_space = ref.rfind(' ')
                book = ref[:last_space]
                ch = int(ref[last_space + 1:].split(':')[0])
                if book not in books_max_ch:
                    books_max_ch[book] = ch
                    book_list.append((book, ch))  # placeholder max_ch
                elif ch > books_max_ch[book]:
                    books_max_ch[book] = ch
            # Update max chapters
            self._books_cache = [(b, books_max_ch[b]) for b, _ in book_list]
        return self._books_cache

    def get_testament(self, book: str) -> str:
        """Return 'nt' or 'ot' for the given book name."""
        return self._testament.get(book, 'nt')

    def get_chapter_verses(self, book: str, chapter: int) -> list[tuple[int, str, str]]:
        """Return list of (verse_number, reference, syriac_text) for a chapter."""
        self.load()
        results = []
        for ref, text in self._verses.items():
            # Parse reference: "Book Chapter:Verse"
            last_space = ref.rfind(' ')
            if last_space == -1:
                continue
            book_part = ref[:last_space]
            if book_part != book:
                continue
            chv = ref[last_space + 1:]
            if ':' not in chv:
                continue
            ch_str, v_str = chv.split(':', 1)
            try:
                ch = int(ch_str)
                v = int(v_str)
            except ValueError:
                continue
            if ch == chapter:
                results.append((v, ref, text))
        results.sort(key=lambda x: x[0])
        return results

    def get_verse_text(self, reference: str) -> str | None:
        """Return the Syriac text for a given verse reference."""
        self.load()
        return self._verses.get(reference)

    def get_adjacent_ref(self, reference: str, direction: int) -> str | None:
        """Return the reference for an adjacent verse (direction: -1 or +1).

        Returns None if the adjacent verse doesn't exist or would cross
        chapter boundaries.
        """
        self.load()
        # Parse "Book Chapter:Verse" — book may contain spaces (e.g., "1 Corinthians")
        last_space = reference.rfind(' ')
        if last_space == -1:
            return None
        book_part = reference[:last_space]
        chv_part = reference[last_space + 1:]
        if ':' not in chv_part:
            return None
        ch_str, v_str = chv_part.split(':', 1)
        try:
            chapter = int(ch_str)
            verse = int(v_str)
        except ValueError:
            return None
        new_verse = verse + direction
        if new_verse < 1:
            return None  # don't cross chapter boundaries
        new_ref = f"{book_part} {chapter}:{new_verse}"
        if new_ref in self._verses:
            return new_ref
        return None

    def get_verse_translation(self, reference: str, lang: str) -> str:
        """Return a verse translation from per-language translation files."""
        if lang not in self._translations:
            lang_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data', f'translations_{lang}.json'
            )
            if os.path.exists(lang_path):
                with open(lang_path, 'r', encoding='utf-8') as f:
                    self._translations[lang] = json.load(f)
            else:
                self._translations[lang] = {}
        return self._translations.get(lang, {}).get(reference, '')

    def _ensure_translations(self, lang: str) -> dict:
        """Load and return the translations dict for a language."""
        if lang not in self._translations:
            lang_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data', f'translations_{lang}.json'
            )
            if os.path.exists(lang_path):
                with open(lang_path, 'r', encoding='utf-8') as f:
                    self._translations[lang] = json.load(f)
            else:
                self._translations[lang] = {}
        return self._translations.get(lang, {})

    def search_text(self, query: str, lang: str = 'en') -> list[dict]:
        """Search verse translations (or Syriac corpus) for a substring.

        Returns list of {reference, syriac, translation, match_positions}.
        Detects Syriac script automatically; otherwise searches the
        translation file for the given language.
        """
        self.load()
        results = []
        query_lower = query.lower()

        # Detect Syriac script (U+0710-U+074F)
        is_syriac = any('\u0710' <= ch <= '\u074f' for ch in query)

        if is_syriac:
            # Search Syriac corpus directly
            for ref in self._verse_order:
                text = self._verses[ref]
                pos = text.find(query)
                if pos != -1:
                    positions = []
                    start = 0
                    while True:
                        idx = text.find(query, start)
                        if idx == -1:
                            break
                        positions.append([idx, idx + len(query)])
                        start = idx + 1
                    results.append({
                        'reference': ref,
                        'syriac': text,
                        'translation': '',
                        'match_positions': positions,
                        'match_type': 'syriac'
                    })
                    if len(results) >= 100:
                        break
        else:
            # Search translations for the given language
            translations = self._ensure_translations(lang)
            for ref in self._verse_order:
                trans_text = translations.get(ref, '')
                if not trans_text:
                    continue
                trans_lower = trans_text.lower()
                pos = trans_lower.find(query_lower)
                if pos != -1:
                    positions = []
                    start = 0
                    while True:
                        idx = trans_lower.find(query_lower, start)
                        if idx == -1:
                            break
                        positions.append([idx, idx + len(query_lower)])
                        start = idx + 1
                    results.append({
                        'reference': ref,
                        'syriac': self._verses.get(ref, ''),
                        'translation': trans_text,
                        'match_positions': positions,
                        'match_type': 'translation'
                    })
                    if len(results) >= 100:
                        break

        return results
