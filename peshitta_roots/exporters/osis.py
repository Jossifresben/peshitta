"""OSIS 2.1.1 XML exporter for Peshitta corpus."""

from datetime import date
from xml.etree import ElementTree as ET
from .. import citations

# OSIS book IDs
BOOK_IDS = {
    'Matthew': 'Matt', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
    'Acts': 'Acts', 'Romans': 'Rom',
    '1 Corinthians': '1Cor', '2 Corinthians': '2Cor',
    'Galatians': 'Gal', 'Ephesians': 'Eph',
    'Philippians': 'Phil', 'Colossians': 'Col',
    '1 Thessalonians': '1Thess', '2 Thessalonians': '2Thess',
    '1 Timothy': '1Tim', '2 Timothy': '2Tim',
    'Titus': 'Titus', 'Philemon': 'Phlm',
    'Hebrews': 'Heb', 'James': 'Jas',
    '1 Peter': '1Pet', '1 John': '1John',
    'Psalms': 'Ps', 'Isaiah': 'Isa',
    'Ezekiel': 'Ezek', 'Proverbs': 'Prov',
}


def export_book(corpus, book: str | None = None) -> bytes:
    """Generate OSIS XML for a book or full corpus. Returns bytes."""
    today = date.today().isoformat()

    osis = ET.Element('osis', {
        'xmlns': 'http://www.bibletechnologies.net/2003/OSIS/namespace',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xsi:schemaLocation': 'http://www.bibletechnologies.net/2003/OSIS/namespace osisCore.2.1.1.xsd',
    })

    osis_text = ET.SubElement(osis, 'osisText', {
        'osisIDWork': 'PeshittaConstellations',
        'osisRefWork': 'Bible',
        'xml:lang': 'syr',
    })

    header = ET.SubElement(osis_text, 'header')
    work = ET.SubElement(header, 'work', {'osisWork': 'PeshittaConstellations'})
    ET.SubElement(work, 'title').text = citations.APP_TITLE
    creator = ET.SubElement(work, 'creator', {'role': 'aut'})
    creator.text = citations.AUTHOR_FULL
    ET.SubElement(work, 'identifier', {'type': 'DOI'}).text = citations.DOI
    ET.SubElement(work, 'date').text = str(citations.YEAR)
    ET.SubElement(work, 'rights').text = 'Apache 2.0'
    desc = ET.SubElement(work, 'description')
    desc.text = f'Syriac Peshitta corpus. Author ORCID: {citations.ORCID}. Version {citations.VERSION}. Generated {today}.'

    books_to_export = [book] if book else [b for b, _ in corpus.get_books()]

    for b_name in books_to_export:
        osis_id = BOOK_IDS.get(b_name, b_name.replace(' ', ''))
        book_div = ET.SubElement(osis_text, 'div', {'type': 'book', 'osisID': osis_id})
        ET.SubElement(book_div, 'title', {'type': 'main'}).text = b_name

        # Find max chapter for this book
        books = corpus.get_books()
        max_ch = 1
        for b, ch in books:
            if b == b_name:
                max_ch = ch
                break

        for ch_num in range(1, max_ch + 1):
            verses = corpus.get_chapter_verses(b_name, ch_num)
            if not verses:
                continue
            ch_elem = ET.SubElement(book_div, 'chapter', {'osisID': f'{osis_id}.{ch_num}'})
            for v_num, ref, syriac in verses:
                v_elem = ET.SubElement(ch_elem, 'verse', {'osisID': f'{osis_id}.{ch_num}.{v_num}'})
                v_elem.text = syriac

    ET.indent(osis, space='  ')
    return ET.tostring(osis, encoding='utf-8', xml_declaration=True)
