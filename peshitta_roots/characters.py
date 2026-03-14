"""Syriac, Hebrew, and Arabic character constants and transliteration maps."""

# --- Syriac Consonants (Estrangela/Eastern) ---
# 22 letters, Unicode range U+0710-U+072C

SYRIAC_CONSONANTS = frozenset([
    '\u0710',  # ܐ Alaph
    '\u0712',  # ܒ Beth
    '\u0713',  # ܓ Gamal
    '\u0715',  # ܕ Dalath
    '\u0717',  # ܗ He
    '\u0718',  # ܘ Waw
    '\u0719',  # ܙ Zain
    '\u071A',  # ܚ Heth
    '\u071B',  # ܛ Teth
    '\u071D',  # ܝ Yudh
    '\u071F',  # ܟ Kaph
    '\u0720',  # ܠ Lamadh
    '\u0721',  # ܡ Mim
    '\u0722',  # ܢ Nun
    '\u0723',  # ܣ Semkath
    '\u0725',  # ܥ E (Ayin)
    '\u0726',  # ܦ Pe
    '\u0728',  # ܨ Sadhe
    '\u0729',  # ܩ Qaph
    '\u072A',  # ܪ Rish
    '\u072B',  # ܫ Shin
    '\u072C',  # ܬ Taw
])

# Weak letters (matres lectionis) - can be root consonants or vowel markers
WEAK_LETTERS = frozenset(['\u0710', '\u0718', '\u071D'])  # ܐ ܘ ܝ

# Proclitic letters - single-letter particles that attach to words
PROCLITIC_LETTERS = frozenset(['\u0715', '\u0718', '\u0712', '\u0720'])  # ܕ ܘ ܒ ܠ

# --- Syriac -> Latin transliteration ---
SYRIAC_TO_LATIN = {
    '\u0710': 'a',    # ܐ Alaph
    '\u0712': 'b',    # ܒ Beth
    '\u0713': 'g',    # ܓ Gamal
    '\u0715': 'd',    # ܕ Dalath
    '\u0717': 'h',    # ܗ He
    '\u0718': 'w',    # ܘ Waw
    '\u0719': 'z',    # ܙ Zain
    '\u071A': 'kh',   # ܚ Heth
    '\u071B': 'T',    # ܛ Teth (capital to distinguish from ܬ)
    '\u071D': 'y',    # ܝ Yudh
    '\u071F': 'k',    # ܟ Kaph
    '\u0720': 'l',    # ܠ Lamadh
    '\u0721': 'm',    # ܡ Mim
    '\u0722': 'n',    # ܢ Nun
    '\u0723': 's',    # ܣ Semkath
    '\u0725': 'e',    # ܥ E (Ayin)
    '\u0726': 'p',    # ܦ Pe
    '\u0728': 'ts',   # ܨ Sadhe
    '\u0729': 'q',    # ܩ Qaph
    '\u072A': 'r',    # ܪ Rish
    '\u072B': 'sh',   # ܫ Shin
    '\u072C': 'th',   # ܬ Taw
}

# --- Latin -> Syriac (reverse map for user input parsing) ---
# Handles both upper and lower case input
LATIN_TO_SYRIAC = {
    'a':  '\u0710',  # ܐ
    'b':  '\u0712',  # ܒ
    'g':  '\u0713',  # ܓ
    'd':  '\u0715',  # ܕ
    'h':  '\u0717',  # ܗ
    'w':  '\u0718',  # ܘ
    'z':  '\u0719',  # ܙ
    'kh': '\u071A',  # ܚ
    'T':  '\u071B',  # ܛ
    'y':  '\u071D',  # ܝ
    'k':  '\u071F',  # ܟ
    'l':  '\u0720',  # ܠ
    'm':  '\u0721',  # ܡ
    'n':  '\u0722',  # ܢ
    's':  '\u0723',  # ܣ
    'e':  '\u0725',  # ܥ E (Ayin)
    "'":  '\u0725',  # ܥ (alternate input)
    'o':  '\u0725',  # ܥ (alternate input for Hebrew-familiar users)
    'p':  '\u0726',  # ܦ
    'ts': '\u0728',  # ܨ
    'q':  '\u0729',  # ܩ
    'r':  '\u072A',  # ܪ
    'sh': '\u072B',  # ܫ
    'th': '\u072C',  # ܬ
}

# --- Hebrew consonant transliteration (for display) ---
HEBREW_TO_LATIN = {
    '\u05D0': 'a',    # א Alef
    '\u05D1': 'b',    # ב Bet
    '\u05D2': 'g',    # ג Gimel
    '\u05D3': 'd',    # ד Dalet
    '\u05D4': 'h',    # ה He
    '\u05D5': 'w',    # ו Vav
    '\u05D6': 'z',    # ז Zayin
    '\u05D7': 'kh',   # ח Het
    '\u05D8': 'T',    # ט Tet
    '\u05D9': 'y',    # י Yod
    '\u05DA': 'k',    # ך Kaf final
    '\u05DB': 'k',    # כ Kaf
    '\u05DC': 'l',    # ל Lamed
    '\u05DD': 'm',    # ם Mem final
    '\u05DE': 'm',    # מ Mem
    '\u05DF': 'n',    # ן Nun final
    '\u05E0': 'n',    # נ Nun
    '\u05E1': 's',    # ס Samekh
    '\u05E2': 'e',    # ע Ayin
    '\u05E3': 'p',    # ף Pe final
    '\u05E4': 'p',    # פ Pe
    '\u05E5': 'ts',   # ץ Tsadi final
    '\u05E6': 'ts',   # צ Tsadi
    '\u05E7': 'q',    # ק Qof
    '\u05E8': 'r',    # ר Resh
    '\u05E9': 'sh',   # ש Shin
    '\u05EA': 'th',   # ת Tav
}

# --- Arabic consonant transliteration (for display) ---
ARABIC_TO_LATIN = {
    '\u0627': 'a',    # ا Alif
    '\u0628': 'b',    # ب Ba
    '\u062A': 't',    # ت Ta
    '\u062B': 'th',   # ث Tha
    '\u062C': 'j',    # ج Jim
    '\u062D': 'H',    # ح Ha
    '\u062E': 'kh',   # خ Kha
    '\u062F': 'd',    # د Dal
    '\u0630': 'dh',   # ذ Dhal
    '\u0631': 'r',    # ر Ra
    '\u0632': 'z',    # ز Zay
    '\u0633': 's',    # س Sin
    '\u0634': 'sh',   # ش Shin
    '\u0635': 'S',    # ص Sad
    '\u0636': 'D',    # ض Dad
    '\u0637': 'T',    # ط Ta
    '\u0638': 'Z',    # ظ Za
    '\u0639': 'e',    # ع Ayn
    '\u063A': 'gh',   # غ Ghayn
    '\u0641': 'f',    # ف Fa
    '\u0642': 'q',    # ق Qaf
    '\u0643': 'k',    # ك Kaf
    '\u0644': 'l',    # ل Lam
    '\u0645': 'm',    # م Mim
    '\u0646': 'n',    # ن Nun
    '\u0647': 'h',    # ه Ha
    '\u0648': 'w',    # و Waw
    '\u064A': 'y',    # ي Ya
}


# --- Syriac -> Academic transliteration (scholarly standard) ---
SYRIAC_TO_ACADEMIC = {
    '\u0710': 'ʾ',    # ܐ Alaph
    '\u0712': 'b',    # ܒ Beth
    '\u0713': 'g',    # ܓ Gamal
    '\u0715': 'd',    # ܕ Dalath
    '\u0717': 'h',    # ܗ He
    '\u0718': 'w',    # ܘ Waw
    '\u0719': 'z',    # ܙ Zain
    '\u071A': 'ḥ',    # ܚ Heth
    '\u071B': 'ṭ',    # ܛ Teth
    '\u071D': 'y',    # ܝ Yudh
    '\u071F': 'k',    # ܟ Kaph
    '\u0720': 'l',    # ܠ Lamadh
    '\u0721': 'm',    # ܡ Mim
    '\u0722': 'n',    # ܢ Nun
    '\u0723': 's',    # ܣ Semkath
    '\u0725': 'ʿ',    # ܥ Ayin
    '\u0726': 'p',    # ܦ Pe
    '\u0728': 'ṣ',    # ܨ Sadhe
    '\u0729': 'q',    # ܩ Qaph
    '\u072A': 'r',    # ܪ Rish
    '\u072B': 'š',    # ܫ Shin
    '\u072C': 't',    # ܬ Taw
}


def transliterate_syriac_academic(text: str) -> str:
    """Convert Syriac Unicode text to academic/scholarly transliteration."""
    result = []
    for ch in text:
        if ch in SYRIAC_TO_ACADEMIC:
            result.append(SYRIAC_TO_ACADEMIC[ch])
        elif ch == ' ':
            result.append(' ')
        elif ch == '-':
            result.append('-')
    return ''.join(result)


def transliterate_syriac(text: str) -> str:
    """Convert Syriac Unicode text to simple Latin transliteration."""
    result = []
    for ch in text:
        if ch in SYRIAC_TO_LATIN:
            result.append(SYRIAC_TO_LATIN[ch])
        elif ch == ' ':
            result.append(' ')
        elif ch == '-':
            result.append('-')
    return ''.join(result)


def transliterate_hebrew(text: str) -> str:
    """Convert Hebrew Unicode text to simple Latin transliteration."""
    result = []
    for ch in text:
        if ch in HEBREW_TO_LATIN:
            result.append(HEBREW_TO_LATIN[ch])
        elif ch == ' ':
            result.append(' ')
    return ''.join(result)


def transliterate_arabic(text: str) -> str:
    """Convert Arabic Unicode text to simple Latin transliteration."""
    result = []
    for ch in text:
        if ch in ARABIC_TO_LATIN:
            result.append(ARABIC_TO_LATIN[ch])
        elif ch == ' ':
            result.append(' ')
    return ''.join(result)


def parse_root_input(user_input: str) -> str | None:
    """Parse user input like 'K-T-B' or 'k t b' into Syriac root string.

    Accepts:
      - Dash-separated: K-T-B
      - Space-separated: K T B
      - Digraphs: SH-L-M, KH-T-B, TH-Q-N, TS-L-M
      - Case-insensitive (except T for Teth)

    Returns Syriac root string or None if invalid.
    """
    user_input = user_input.strip()
    if not user_input:
        return None

    # Split by dash or space
    if '-' in user_input:
        parts = [p.strip() for p in user_input.split('-') if p.strip()]
    else:
        parts = user_input.split()

    if len(parts) != 3:
        return None

    syriac_chars = []
    for part in parts:
        low = part.lower()
        # Check digraphs first
        if low in LATIN_TO_SYRIAC:
            syriac_chars.append(LATIN_TO_SYRIAC[low])
        elif part in LATIN_TO_SYRIAC:  # case-sensitive check (T for Teth)
            syriac_chars.append(LATIN_TO_SYRIAC[part])
        else:
            return None

    return ''.join(syriac_chars)


def syriac_consonants_of(word: str) -> str:
    """Extract only the Syriac consonant characters from a word."""
    return ''.join(ch for ch in word if ch in SYRIAC_CONSONANTS)


def detect_script(text: str) -> str:
    """Detect the script of the input text.

    Returns 'hebrew', 'arabic', 'syriac', or 'latin'.
    """
    for ch in text:
        cp = ord(ch)
        if 0x0590 <= cp <= 0x05FF:
            return 'hebrew'
        if 0x0600 <= cp <= 0x06FF or 0xFB50 <= cp <= 0xFDFF or 0xFE70 <= cp <= 0xFEFF:
            return 'arabic'
        if 0x0700 <= cp <= 0x074F:
            return 'syriac'
    return 'latin'


def strip_diacritics(text: str) -> str:
    """Remove Hebrew niqqud and Arabic tashkil diacritics from text.

    Hebrew niqqud: U+0591–U+05BD, U+05BF, U+05C1–U+05C2, U+05C4–U+05C5, U+05C7
    Arabic tashkil: U+064B–U+065F, U+0670, U+06D6–U+06DC, U+06DF–U+06E4, U+06E7–U+06E8
    """
    result = []
    for ch in text:
        cp = ord(ch)
        # Skip Hebrew niqqud
        if 0x0591 <= cp <= 0x05BD or cp == 0x05BF or cp in (0x05C1, 0x05C2, 0x05C4, 0x05C5, 0x05C7):
            continue
        # Skip Arabic tashkil
        if 0x064B <= cp <= 0x065F or cp == 0x0670:
            continue
        result.append(ch)
    return ''.join(result)
