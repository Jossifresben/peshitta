"""Hebrew & Arabic cognate lookup for Semitic triliteral roots."""

import json
import os
from dataclasses import dataclass, field

from .characters import transliterate_syriac


@dataclass
class CognateWord:
    word: str
    transliteration: str
    meaning_es: str
    meaning_en: str


@dataclass
class CognateEntry:
    root_syriac: str
    gloss_es: str
    gloss_en: str
    hebrew: list[CognateWord] = field(default_factory=list)
    arabic: list[CognateWord] = field(default_factory=list)


class CognateLookup:
    """Looks up Hebrew and Arabic cognates for a given Semitic root."""

    def __init__(self, data_dir: str | None = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.data_dir = data_dir
        self._cognates: dict[str, CognateEntry] = {}
        self._syriac_to_key: dict[str, str] = {}
        self._loaded = False

    def load(self) -> None:
        """Load the cognates dictionary from JSON."""
        if self._loaded:
            return

        cognates_path = os.path.join(self.data_dir, 'cognates.json')
        if not os.path.exists(cognates_path):
            self._loaded = True
            return

        with open(cognates_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for key, entry_data in data.get('roots', {}).items():
            root_syriac = entry_data.get('root_syriac', '')

            hebrew_words = []
            for hw in entry_data.get('hebrew', []):
                hebrew_words.append(CognateWord(
                    word=hw['word'],
                    transliteration=hw['transliteration'],
                    meaning_es=hw.get('meaning_es', ''),
                    meaning_en=hw.get('meaning_en', ''),
                ))

            arabic_words = []
            for aw in entry_data.get('arabic', []):
                arabic_words.append(CognateWord(
                    word=aw['word'],
                    transliteration=aw['transliteration'],
                    meaning_es=aw.get('meaning_es', ''),
                    meaning_en=aw.get('meaning_en', ''),
                ))

            entry = CognateEntry(
                root_syriac=root_syriac,
                gloss_es=entry_data.get('gloss_es', ''),
                gloss_en=entry_data.get('gloss_en', ''),
                hebrew=hebrew_words,
                arabic=arabic_words,
            )

            self._cognates[key] = entry
            if root_syriac:
                self._syriac_to_key[root_syriac] = key

        self._loaded = True

    def lookup(self, root_syriac: str) -> CognateEntry | None:
        """Look up cognates by Syriac root string (e.g., ܟܬܒ).

        Returns CognateEntry or None if not found.
        """
        self.load()

        # Try direct Syriac lookup
        key = self._syriac_to_key.get(root_syriac)
        if key and key in self._cognates:
            return self._cognates[key]

        # Try transliterated key
        translit = transliterate_syriac(root_syriac)
        # Convert transliteration to key format: k-th-b
        if len(root_syriac) >= 3:
            parts = []
            i = 0
            for ch in root_syriac:
                from .characters import SYRIAC_TO_LATIN
                if ch in SYRIAC_TO_LATIN:
                    parts.append(SYRIAC_TO_LATIN[ch])
            if len(parts) == 3:
                key = '-'.join(parts)
                if key in self._cognates:
                    return self._cognates[key]

        return None

    def has_cognates(self, root_syriac: str) -> bool:
        """Check if cognates exist for a given root."""
        return self.lookup(root_syriac) is not None
