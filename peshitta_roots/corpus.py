"""CSV parser and word index builder for the Peshitta corpus."""

import csv
import json
import os
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class WordOccurrence:
    word: str
    reference: str
    book: str
    chapter: int
    verse: int
    position: int  # 0-based word position within the verse


class PeshittaCorpus:
    """Loads the Peshitta NT CSV and builds searchable word indexes."""

    def __init__(self, csv_path: str | None = None):
        if csv_path is None:
            csv_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'syriac_nt_traditional22_unicode.csv'
            )
        self.csv_path = csv_path
        self._occurrences: dict[str, list[WordOccurrence]] = {}
        self._total_words: int = 0
        self._verses: dict[str, str] = {}  # reference -> syriac text
        self._verse_order: list[str] = []  # ordered references for book iteration
        self._translations: dict[str, dict] = {}  # lang -> {ref: text}, lazy-loaded per language
        self._loaded = False

    def load(self) -> None:
        """Parse the CSV and build the word index."""
        if self._loaded:
            return

        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                syriac_text = row['syriac'].strip()
                if not syriac_text:
                    continue

                book = row['book']
                chapter = int(row['chapter'])
                verse = int(row['verse'])
                reference = row['reference']

                self._verses[reference] = syriac_text
                self._verse_order.append(reference)

                words = syriac_text.split()
                for pos, word in enumerate(words):
                    clean_word = word.strip()
                    if not clean_word:
                        continue

                    occ = WordOccurrence(
                        word=clean_word,
                        reference=reference,
                        book=book,
                        chapter=chapter,
                        verse=verse,
                        position=pos,
                    )
                    self._total_words += 1

                    if clean_word not in self._occurrences:
                        self._occurrences[clean_word] = []
                    self._occurrences[clean_word].append(occ)

        self._loaded = True

    def get_unique_words(self) -> set[str]:
        """Return all unique surface forms in the corpus."""
        self.load()
        return set(self._occurrences.keys())

    def get_occurrences(self, word: str) -> list[WordOccurrence]:
        """Return all occurrences of a specific surface form."""
        self.load()
        return self._occurrences.get(word, [])

    def word_frequency(self) -> Counter:
        """Return word frequency counts across the entire corpus."""
        self.load()
        return Counter({word: len(occs) for word, occs in self._occurrences.items()})

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
