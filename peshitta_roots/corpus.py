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
        self._all_words: list[WordOccurrence] = []
        self._verses: dict[str, str] = {}  # reference -> syriac text
        self._translations: dict | None = None  # lazy-loaded from translations.json
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

                words = syriac_text.split()
                for pos, word in enumerate(words):
                    # Skip hyphenated compound words (proper nouns like ܒܝܬ-ܠܚܡ)
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
                    self._all_words.append(occ)

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
        return len(self._all_words)

    def total_unique(self) -> int:
        """Return number of unique surface forms."""
        self.load()
        return len(self._occurrences)

    def get_verse_text(self, reference: str) -> str | None:
        """Return the Syriac text for a given verse reference."""
        self.load()
        return self._verses.get(reference)

    def get_verse_translation(self, reference: str, lang: str) -> str:
        """Return a verse translation (en or es) from translations.json."""
        if self._translations is None:
            translations_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data', 'translations.json'
            )
            if os.path.exists(translations_path):
                with open(translations_path, 'r', encoding='utf-8') as f:
                    self._translations = json.load(f)
            else:
                self._translations = {}
        entry = self._translations.get(reference, {})
        return entry.get(lang, '')
