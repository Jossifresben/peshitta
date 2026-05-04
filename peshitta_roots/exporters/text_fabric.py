"""Text-Fabric dataset exporter (ZIP)."""

import io
import json
import zipfile
from datetime import date
from .. import citations


def _tf_header(feature: str, value_type: str = "str") -> str:
    """TF feature file header."""
    today = date.today().isoformat()
    return f"""@node
@valueType={value_type}
@author={citations.AUTHOR_FULL}
@orcid={citations.ORCID}
@doi={citations.DOI}
@version={citations.VERSION}
@dateExported={today}
@feature={feature}
"""


def export_zip(corpus, extractor, book: str | None = None) -> bytes:
    """Generate Text-Fabric dataset ZIP for a book or full corpus.

    Returns bytes of the ZIP. Node types: book, chapter, verse, word.
    """
    books = corpus.get_books()
    books_to_export = [book] if book else [b for b, _ in books]

    # Build node lists
    # Slot type = word (slots are 1-indexed)
    word_slots = []  # list of dicts: {syriac, root, book, chapter, verse}
    verse_nodes = []  # list of (book, chapter, verse, [slot_indices])
    chapter_nodes = []  # list of (book, chapter, [slot_indices])
    book_nodes = []  # list of (book, [slot_indices])

    slot_idx = 0
    for b_name in books_to_export:
        max_ch = 1
        for b, ch in books:
            if b == b_name:
                max_ch = ch
                break
        book_slot_start = slot_idx + 1
        for ch_num in range(1, max_ch + 1):
            verses = corpus.get_chapter_verses(b_name, ch_num)
            if not verses:
                continue
            chapter_slot_start = slot_idx + 1
            for v_num, ref, syriac in verses:
                verse_slot_start = slot_idx + 1
                for word in syriac.split():
                    slot_idx += 1
                    root = extractor.lookup_word_root(word) if extractor else None
                    word_slots.append({
                        'syriac': word,
                        'root': root or '',
                        'book': b_name,
                        'chapter': ch_num,
                        'verse': v_num,
                    })
                if slot_idx >= verse_slot_start:
                    verse_nodes.append((b_name, ch_num, v_num, list(range(verse_slot_start, slot_idx + 1))))
            if slot_idx >= chapter_slot_start:
                chapter_nodes.append((b_name, ch_num, list(range(chapter_slot_start, slot_idx + 1))))
        if slot_idx >= book_slot_start:
            book_nodes.append((b_name, list(range(book_slot_start, slot_idx + 1))))

    total_slots = slot_idx
    n_verses = len(verse_nodes)
    n_chapters = len(chapter_nodes)
    n_books = len(book_nodes)

    # Node numbering: slots 1..total_slots; verses next; chapters next; books last
    verse_node_start = total_slots + 1
    chapter_node_start = verse_node_start + n_verses
    book_node_start = chapter_node_start + n_chapters

    # Build TF feature contents
    # otype.tf: node -> type (only non-slot nodes need lines; slots are implied by maxSlot)
    otype_lines = [_tf_header('otype'), f"@maxSlot={total_slots}", f"@maxNode={book_node_start + n_books - 1}", ""]
    # Per TF format, otype lists types for non-slot nodes
    # Slots default to "word"
    otype_lines.append("word")  # default for slots
    for _ in verse_nodes:
        otype_lines.append("verse")
    for _ in chapter_nodes:
        otype_lines.append("chapter")
    for _ in book_nodes:
        otype_lines.append("book")

    # oslots.tf: only non-slot nodes; lists their slots
    oslots_lines = [_tf_header('oslots')]
    oslots_lines.append("")  # blank line after header
    for _, _, _, slots in verse_nodes:
        oslots_lines.append(','.join(str(s) for s in slots))
    for _, _, slots in chapter_nodes:
        oslots_lines.append(','.join(str(s) for s in slots))
    for _, slots in book_nodes:
        oslots_lines.append(','.join(str(s) for s in slots))

    # text.tf: per-slot Syriac form
    text_lines = [_tf_header('text'), ""]
    for w in word_slots:
        text_lines.append(w['syriac'])

    # root.tf: per-slot extracted root
    root_lines = [_tf_header('root'), ""]
    for w in word_slots:
        root_lines.append(w['root'])

    # book.tf, chapter.tf, verse.tf — per-node features for higher-order nodes
    book_lines = [_tf_header('book'), ""]
    chapter_lines = [_tf_header('chapter', 'int'), ""]
    verse_lines = [_tf_header('verse', 'int'), ""]
    # verse-level
    for b, ch, v, _ in verse_nodes:
        verse_lines.append(str(v))
    for _ in verse_nodes:
        chapter_lines.append("")  # placeholder for verse nodes
        book_lines.append("")
    # chapter-level
    for b, ch, _ in chapter_nodes:
        chapter_lines.append(str(ch))
        book_lines.append(b)
        verse_lines.append("")
    # book-level
    for b, _ in book_nodes:
        book_lines.append(b)
        chapter_lines.append("")
        verse_lines.append("")

    # meta.json with citation
    meta = {
        'name': 'Peshitta Constellations TF Export',
        'version': citations.VERSION,
        'doi': citations.DOI,
        'author': citations.AUTHOR_FULL,
        'orcid': citations.ORCID,
        'license': 'Apache 2.0',
        'source': 'ETCBC/syrnt + syriac_ot_selected_unicode.csv',
        'app_url': citations.APP_URL,
        'exported': date.today().isoformat(),
        'books': books_to_export,
        'features': ['otype', 'oslots', 'text', 'root', 'book', 'chapter', 'verse'],
        'node_counts': {
            'word_slots': total_slots,
            'verses': n_verses,
            'chapters': n_chapters,
            'books': n_books,
        },
    }

    # Build ZIP
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('meta.json', json.dumps(meta, indent=2, ensure_ascii=False))
        z.writestr('otype.tf', '\n'.join(otype_lines) + '\n')
        z.writestr('oslots.tf', '\n'.join(oslots_lines) + '\n')
        z.writestr('text.tf', '\n'.join(text_lines) + '\n')
        z.writestr('root.tf', '\n'.join(root_lines) + '\n')
        z.writestr('book.tf', '\n'.join(book_lines) + '\n')
        z.writestr('chapter.tf', '\n'.join(chapter_lines) + '\n')
        z.writestr('verse.tf', '\n'.join(verse_lines) + '\n')

    return buf.getvalue()
