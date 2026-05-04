"""USFM 3.0 exporter for Peshitta corpus.

Outputs a USFM-formatted document for a book or chapter range with
citation metadata in a leading comment block.
"""

from datetime import date
from .. import citations

# USFM 3-letter book codes
BOOK_CODES = {
    'Matthew': 'MAT', 'Mark': 'MRK', 'Luke': 'LUK', 'John': 'JHN',
    'Acts': 'ACT', 'Romans': 'ROM',
    '1 Corinthians': '1CO', '2 Corinthians': '2CO',
    'Galatians': 'GAL', 'Ephesians': 'EPH',
    'Philippians': 'PHP', 'Colossians': 'COL',
    '1 Thessalonians': '1TH', '2 Thessalonians': '2TH',
    '1 Timothy': '1TI', '2 Timothy': '2TI',
    'Titus': 'TIT', 'Philemon': 'PHM',
    'Hebrews': 'HEB', 'James': 'JAS',
    '1 Peter': '1PE', '1 John': '1JN',
    'Psalms': 'PSA', 'Isaiah': 'ISA',
    'Ezekiel': 'EZK', 'Proverbs': 'PRO',
}


def _header_comment(book: str, scope: str) -> str:
    """Return USFM comment block with citation metadata."""
    today = date.today().isoformat()
    return f"""\\rem Peshitta Constellations USFM export
\\rem Book: {book} ({scope})
\\rem Source: ETCBC/syrnt corpus (NT) + syriac_ot_selected_unicode.csv (OT)
\\rem Author: {citations.AUTHOR_FULL}
\\rem ORCID: {citations.ORCID}
\\rem DOI: {citations.DOI}
\\rem Version: {citations.VERSION}
\\rem Generated: {today}
\\rem URL: {citations.APP_URL}
"""


def export_book_or_range(corpus, book: str, chapter: int | None = None,
                         start_verse: int | None = None,
                         end_verse: int | None = None) -> str:
    """Generate USFM text for a book, chapter, or verse range."""
    book_code = BOOK_CODES.get(book, book.upper().replace(' ', '')[:3])

    if chapter and start_verse:
        scope = f"chapter {chapter}, verses {start_verse}-{end_verse or start_verse}"
    elif chapter:
        scope = f"chapter {chapter}"
    else:
        scope = "full book"

    out = []
    out.append(_header_comment(book, scope))
    out.append(f"\\id {book_code} {citations.APP_TITLE} v{citations.VERSION}")
    out.append(f"\\h {book}")
    out.append(f"\\toc1 {book}")
    out.append(f"\\toc2 {book}")
    out.append(f"\\toc3 {book_code}")
    out.append(f"\\mt1 {book}")

    # Determine which chapters to include
    books = corpus.get_books()
    max_ch = 1
    for b_name, b_max in books:
        if b_name == book:
            max_ch = b_max
            break

    chapters_to_export = [chapter] if chapter else list(range(1, max_ch + 1))

    for ch in chapters_to_export:
        verses = corpus.get_chapter_verses(book, ch)
        if not verses:
            continue
        out.append(f"\\c {ch}")
        out.append("\\p")
        for v_num, ref, syriac in verses:
            if start_verse and v_num < start_verse:
                continue
            if end_verse and v_num > end_verse:
                continue
            out.append(f"\\v {v_num} {syriac}")

    return "\n".join(out) + "\n"
