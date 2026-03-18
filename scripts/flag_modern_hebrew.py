#!/usr/bin/env python3
"""Flag and remove modern Israeli Hebrew forms not attested in BDB."""

import json

# Modern Hebrew words/meanings not in BDB (biblical Hebrew lexicon)
MODERN_MEANINGS = {
    'address', 'technology', 'computer', 'startup', 'internet', 'phone',
    'electricity', 'television', 'radio', 'newspaper', 'photography',
    'airplane', 'airport', 'bus', 'train station', 'parking',
    'apartment', 'balcony', 'elevator', 'refrigerator',
    'university', 'college', 'diploma', 'academic',
    'democracy', 'parliament', 'election', 'vote',
    'police', 'army (modern)', 'soldier (modern)',
    'immigrant', 'immigration',
}

# Modern Hebrew transliterations that are post-biblical coinages
MODERN_FORMS = {
    'ktovet',       # address (modern coinage from K-TH-B)
    'itonut',       # journalism
    'tikshoret',    # communication
    'taksir',       # summary
    'makhshev',     # computer
    'tochnit',      # program/plan (modern sense)
    'misrad',       # office (modern sense)
}

with open('data/cognates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

removed_count = 0
flagged = []

for key, root in data['roots'].items():
    heb = root.get('hebrew', [])
    clean = []
    for h in heb:
        translit = h.get('transliteration', '').lower()
        meaning = h.get('meaning_en', '').lower()

        is_modern = False
        # Check against modern forms
        for mf in MODERN_FORMS:
            if mf in translit:
                is_modern = True
                break
        # Check against modern meanings
        for mm in MODERN_MEANINGS:
            if mm in meaning:
                is_modern = True
                break

        if is_modern:
            flagged.append((key, h['transliteration'], h.get('meaning_en', '')))
            removed_count += 1
        else:
            clean.append(h)

    if len(clean) < len(heb):
        root['hebrew'] = clean

# Also flag roots with excessive entries (>6) for manual review
excessive = []
for key, root in data['roots'].items():
    heb_count = len(root.get('hebrew', []))
    if heb_count > 6:
        excessive.append((key, heb_count))

print(f'=== Modern Hebrew forms removed: {removed_count} ===')
for f in flagged:
    print(f'  {f[0]}: {f[1]} ({f[2]})')

print(f'\n=== Roots with >6 Hebrew entries (review for bloat): {len(excessive)} ===')
for e in sorted(excessive, key=lambda x: -x[1]):
    print(f'  {e[0]}: {e[1]} entries')

with open('data/cognates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nSaved.')
