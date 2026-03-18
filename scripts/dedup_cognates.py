#!/usr/bin/env python3
"""Remove duplicate Hebrew/Arabic entries from cognates.json."""

import json

def normalize_translit(t):
    t = t.lower().strip()
    replacements = {
        'ā': 'a', 'ē': 'e', 'ī': 'i', 'ō': 'o', 'ū': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'ḥ': 'kh', 'ṣ': 'ts', 'ṭ': 't', 'ḍ': 'd',
        'š': 'sh', 'ś': 's', 'ž': 'z',
        "'": '', "'": '', '`': '', 'ʿ': '', 'ʾ': '',
    }
    for old, new in replacements.items():
        t = t.replace(old, new)
    return t

def dedup_entries(entries):
    seen = {}
    unique = []
    removed = 0
    for entry in entries:
        norm = normalize_translit(entry['transliteration'])
        if norm not in seen:
            seen[norm] = entry
            unique.append(entry)
        else:
            existing = seen[norm]
            if len(entry.get('meaning_en', '')) > len(existing.get('meaning_en', '')):
                unique.remove(existing)
                unique.append(entry)
                seen[norm] = entry
            removed += 1
    return unique, removed

with open('data/cognates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_heb = 0
total_arb = 0
affected = []

for key, root in data['roots'].items():
    heb, rh = dedup_entries(root.get('hebrew', []))
    arb, ra = dedup_entries(root.get('arabic', []))
    if rh > 0:
        root['hebrew'] = heb
        total_heb += rh
    if ra > 0:
        root['arabic'] = arb
        total_arb += ra
    if rh + ra > 0:
        affected.append(key)

print(f'Removed {total_heb} duplicate Hebrew entries')
print(f'Removed {total_arb} duplicate Arabic entries')
print(f'Roots affected: {len(affected)}')

with open('data/cognates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved.')
