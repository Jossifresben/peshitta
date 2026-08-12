#!/usr/bin/env python3
"""Apply the verdicts from docs/outlier-flag-audit.md to data/cognates.json.

Deterministic and offline: it reads the report that
`scripts/audit_outlier_flags.py` already produced rather than re-running the
audit. Re-running would cost another API pass and could return slightly
different verdicts than the ones that were reviewed, so the reviewed report
is the source of truth.

Only clears flags — never sets them. A cognate whose flag the audit confirmed
is left exactly as it is.

Usage:
    python scripts/apply_outlier_audit.py                 # dry run (default)
    python scripts/apply_outlier_audit.py --apply         # write
    python scripts/apply_outlier_audit.py --apply --min-confidence medium
"""

import argparse
import json
import os
import re

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COGNATES_PATH = os.path.join(REPO_ROOT, 'data', 'cognates.json')
REPORT_PATH = os.path.join(REPO_ROOT, 'docs', 'outlier-flag-audit.md')

# Heading of the section listing flags the audit judged to be false positives.
CLEAR_SECTION = 'Cambios propuestos'
CONF_RANK = {'high': 3, 'medium': 2, 'low': 1}


def parse_clears(report_path):
    """Return [(root, lang_short, translit, confidence)] from the clears section."""
    text = open(report_path, encoding='utf-8').read()
    lines = text.split('\n')

    # Slice out just the "flags to remove" section — the report also contains a
    # confirmed-outliers table and an uncertain-verdicts table, and rows from
    # those must not be treated as clears.
    start = end = None
    for i, ln in enumerate(lines):
        if ln.startswith('##') and CLEAR_SECTION in ln:
            start = i
        elif start is not None and ln.startswith('## '):
            end = i
            break
    if start is None:
        raise SystemExit(f'Could not find a "{CLEAR_SECTION}" section in {report_path}')
    section = lines[start:end if end else len(lines)]

    clears = []
    for ln in section:
        if not ln.startswith('|') or '`' not in ln:
            continue
        cells = [c.strip().strip('`') for c in ln.strip('|').split('|')]
        # root | gloss | lang | translit | meaning | confidence | justification
        if len(cells) < 6:
            continue
        conf = cells[5].lower()
        if conf not in CONF_RANK:
            continue  # header/separator row
        lang = 'hebrew' if cells[2].lower().startswith('heb') else 'arabic'
        clears.append((cells[0], lang, cells[3].lower().strip(), conf))
    return clears


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true',
                    help='Write changes. Without this the script only reports.')
    ap.add_argument('--min-confidence', default='high', choices=['high', 'medium', 'low'],
                    help='Only clear flags at or above this confidence (default: high)')
    ap.add_argument('--report', default=REPORT_PATH)
    args = ap.parse_args()

    threshold = CONF_RANK[args.min_confidence]
    clears = parse_clears(args.report)
    eligible = [c for c in clears if CONF_RANK[c[3]] >= threshold]

    with open(COGNATES_PATH, encoding='utf-8') as f:
        data = json.load(f)
    roots = data['roots']

    cleared = 0
    already = 0
    unmatched = []
    for root, lang, translit, conf in eligible:
        entry = roots.get(root)
        if entry is None:
            unmatched.append((root, lang, translit, 'root not found'))
            continue
        hit = None
        for c in entry.get(lang) or []:
            if (c.get('transliteration') or '').lower().strip() == translit:
                hit = c
                break
        if hit is None:
            unmatched.append((root, lang, translit, 'cognate not found'))
            continue
        if hit.get('outlier'):
            # Remove the key rather than setting it False — absent is how an
            # ordinary cognate is represented everywhere else in this file.
            hit.pop('outlier', None)
            cleared += 1
        else:
            already += 1

    print(f'Report            : {args.report}')
    print(f'Clears in report  : {len(clears)}')
    print(f'At >= {args.min_confidence:<6}      : {len(eligible)}')
    print(f'Flags cleared     : {cleared}')
    print(f'Already clear     : {already}')
    print(f'Unmatched         : {len(unmatched)}')
    for u in unmatched[:10]:
        print(f'    {u[0]:12} {u[1][:3]} {u[2][:20]:20} {u[3]}')

    remaining = sum(1 for e in roots.values() for l in ('hebrew', 'arabic')
                    for c in (e.get(l) or []) if c.get('outlier'))
    print(f'Outlier flags remaining in file: {remaining}')

    if args.apply:
        with open(COGNATES_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        print(f'\nWrote {COGNATES_PATH}')
    else:
        print('\nDry run — nothing written. Pass --apply to write.')


if __name__ == '__main__':
    main()
