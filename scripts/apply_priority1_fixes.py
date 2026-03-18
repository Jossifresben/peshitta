#!/usr/bin/env python3
"""Apply Priority 1 corrections from BDB/Lane/Payne audits to cognates.json."""

import json

with open('data/cognates.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

roots = data['roots']
changes = []

# ============================================================
# I. HEBREW (BDB) FIXES
# ============================================================

# A. Wrong root assignments — replace with correct BDB cognates or empty
wrong_hebrew_roots = {
    'n-p-q': {'action': 'note', 'note': 'No direct Hebrew cognate. Listed forms are semantic parallels from Y-TS-A.'},
    'd-kh-l': {'action': 'note', 'note': 'No direct Hebrew cognate. Listed forms are semantic parallels from P-KH-D.'},
    'sh-d-r': {'action': 'note', 'note': 'No direct Hebrew cognate. Listed forms are from SH-L-KH.'},
    'a-z-l': {'action': 'replace', 'hebrew': [
        {'word': 'אָזַל', 'transliteration': 'azal', 'meaning_es': 'ir, irse (arameo bíblico)', 'meaning_en': 'to go, depart (biblical Aramaic)'}
    ]},
    'sh-r-r': {'action': 'replace', 'hebrew': [
        {'word': 'שׁוֹרֵר', 'transliteration': 'shorer', 'meaning_es': 'enemigo, opresor', 'meaning_en': 'enemy, oppressor'},
        {'word': 'שָׁרִיר', 'transliteration': 'sharir', 'meaning_es': 'firme, válido', 'meaning_en': 'firm, valid'}
    ]},
    'z-b-n': {'action': 'note', 'note': 'No direct Hebrew cognate from Z-B-N. Listed Z-M-N forms are semantic parallels.'},
    'k-r-z': {'action': 'replace', 'hebrew': [
        {'word': 'כָּרַז', 'transliteration': 'karaz', 'meaning_es': 'proclamar, pregonar', 'meaning_en': 'to proclaim, herald'},
        {'word': 'כָּרוֹז', 'transliteration': 'karoz', 'meaning_es': 'heraldo, pregonero', 'meaning_en': 'herald, crier'}
    ]},
    'q-r-sh': {'action': 'note', 'note': 'Listed forms are from Q-R-KH (ice/bald), not Q-R-SH.'},
    'y-h-b': {'action': 'filter', 'remove_translits': ['monah', 'moná']},
    'n-s-b': {'action': 'note', 'note': 'Listed forms are from N-S-H (to test) and N-S-KH, not N-S-B.'},
    'th-r-e': {'action': 'note', 'note': 'Listed forms are from SH-\'-R (gate). Aramaic tar\'a is correct but not Hebrew.'},
    'd-n-kh': {'action': 'note', 'note': 'No direct Hebrew cognate of D-N-KH (to dawn). Listed forms are from unrelated roots.'},
    's-n-q': {'action': 'note', 'note': 'No direct Hebrew cognate. Listed forms are from TS-R-KH.'},
    'r-m-y': {'action': 'replace', 'hebrew': [
        {'word': 'רָמָה', 'transliteration': 'ramá', 'meaning_es': 'lanzar, arrojar', 'meaning_en': 'to throw, cast'},
        {'word': 'רְמִיָּה', 'transliteration': 'remiyá', 'meaning_es': 'engaño, pereza', 'meaning_en': 'deceit, slackness'}
    ]},
    'z-k-a': {'action': 'replace', 'hebrew': [
        {'word': 'זָכָה', 'transliteration': 'zaká', 'meaning_es': 'ser puro, ser inocente', 'meaning_en': 'to be pure, be innocent'},
        {'word': 'זַךְ', 'transliteration': 'zakh', 'meaning_es': 'puro, limpio', 'meaning_en': 'pure, clean'}
    ]},
}

# E-TH-D: remove K-W-N forms, keep correct ones
if 'e-th-d' in roots:
    heb = roots['e-th-d'].get('hebrew', [])
    roots['e-th-d']['hebrew'] = [h for h in heb if h['transliteration'].lower() not in
        ('hettikhin', 'hettekhin', 'hakhanah', 'hakhaná', 'nakhon', 'nākhōn')]
    changes.append('e-th-d: removed K-W-N forms from Hebrew')

# K-A-P: remove K-B-D forms, keep only kef
if 'k-a-p' in roots:
    heb = roots['k-a-p'].get('hebrew', [])
    roots['k-a-p']['hebrew'] = [h for h in heb if 'kef' in h['transliteration'].lower() or 'kaf' in h['transliteration'].lower() or 'kap' in h['transliteration'].lower()]
    if not roots['k-a-p']['hebrew']:
        roots['k-a-p']['hebrew'] = [{'word': 'כֵּף', 'transliteration': 'kef', 'meaning_es': 'roca, peña', 'meaning_en': 'rock, crag'}]
    changes.append('k-a-p: removed K-B-D forms, kept only kef (rock)')

# SH-KH-KH: note semantic parallels
if 'sh-kh-kh' in roots:
    for h in roots['sh-kh-kh'].get('hebrew', []):
        if h['transliteration'].lower() in ('matsa', 'matsá', 'matzá', 'mishkan', 'mishkān'):
            h['outlier'] = True
    changes.append('sh-kh-kh: marked M-TS-A and SH-K-N forms as outliers')

for key, fix in wrong_hebrew_roots.items():
    if key not in roots:
        changes.append(f'{key}: SKIP (not found)')
        continue
    if fix['action'] == 'replace':
        roots[key]['hebrew'] = fix['hebrew']
        changes.append(f'{key}: replaced Hebrew with correct BDB cognates')
    elif fix['action'] == 'note':
        # Mark all existing as outlier and add note
        for h in roots[key].get('hebrew', []):
            h['outlier'] = True
        changes.append(f'{key}: marked Hebrew as outliers/semantic parallels ({fix["note"][:60]})')
    elif fix['action'] == 'filter':
        heb = roots[key].get('hebrew', [])
        roots[key]['hebrew'] = [h for h in heb if h['transliteration'].lower() not in [t.lower() for t in fix['remove_translits']]]
        changes.append(f'{key}: removed specific wrong Hebrew entries')

# B. Remove remaining modern Hebrew forms
modern_removals = {
    'k-th-b': ['ktiva', 'ktivá', 'כְּתִיבָה'],
    'k-s-p': ['kaspomat', 'כַּסְפּוֹמָט'],
    'sh-l-m': ['mushlam', 'mushlām', 'מוּשְׁלָם'],
    'b-y-th': ['baytanut', 'baytani', "baytha'i", 'בַּיְתָנוּת', 'בַּיְתָנִי', 'בַּיְתָאִי'],
    's-p-r': ['sifriyya', 'sifriyá', 'סִפְרִיָּה'],
    'y-d-e': ['mada', 'madá', 'muda', 'mudá', 'מַדָּע', 'מוּדָע'],
    'y-w-m': ['yoman', 'יֹומַן'],
    'p-l-g': ['miflaga', 'miflagá', 'palganut', 'מִפְלָגָה', 'פַּלְגָּנוּת'],
    'kh-sh-b': ['khashivut', 'חֲשִׁיבוּת'],
    'l-m-d': ['lamadut', 'לַמָּדוּת'],
}

for key, remove_list in modern_removals.items():
    if key not in roots:
        continue
    remove_lower = [r.lower() for r in remove_list]
    heb = roots[key].get('hebrew', [])
    before = len(heb)
    roots[key]['hebrew'] = [h for h in heb if h['transliteration'].lower() not in remove_lower and h.get('word', '') not in remove_list]
    after = len(roots[key]['hebrew'])
    if before > after:
        changes.append(f'{key}: removed {before - after} modern Hebrew forms')

# C. Remove fabricated forms
fabricated = {
    'n-w-n': ['linon', 'na\'on', 'לִנוֹן', 'נַאוֹן'],
    'z-y-n': ['lizon', 'zaniyin', 'לִיזוֹן', 'זָנִיין'],
}
for key, remove_list in fabricated.items():
    if key not in roots:
        continue
    remove_lower = [r.lower() for r in remove_list]
    heb = roots[key].get('hebrew', [])
    before = len(heb)
    roots[key]['hebrew'] = [h for h in heb if h['transliteration'].lower() not in remove_lower and h.get('word', '') not in remove_list]
    after = len(roots[key]['hebrew'])
    if before > after:
        changes.append(f'{key}: removed {before - after} fabricated Hebrew forms')

if 'n-p-l' in roots:
    heb = roots['n-p-l'].get('hebrew', [])
    before = len(heb)
    roots['n-p-l']['hebrew'] = [h for h in heb if h['transliteration'].lower() not in ('mannafel', 'mannáfel')]
    after = len(roots['n-p-l']['hebrew'])
    if before > after:
        changes.append(f'n-p-l: removed {before - after} fabricated form(s)')

# D. Label Aramaic-as-Hebrew
for key in ['s-g-a', 'm-r-y', 'n-h-r']:
    if key in roots:
        for h in roots[key].get('hebrew', []):
            translit = h['transliteration'].lower()
            if translit in ('sagi', 'sagí', 'shgia', 'mari', 'maran', 'mar', 'maryah', 'nahir', 'manhir'):
                h['outlier'] = True
                if 'meaning_en' in h and '(Aramaic)' not in h['meaning_en']:
                    h['meaning_en'] += ' (Aramaic, not Hebrew)'
                if 'meaning_es' in h and '(arameo)' not in h['meaning_es']:
                    h['meaning_es'] += ' (arameo, no hebreo)'
        changes.append(f'{key}: labeled Aramaic forms')


# ============================================================
# II. ARABIC (LANE) FIXES
# ============================================================

# A. Fix 11 critical wrong cognates
# kh-z-a: remove all wrong Arabic
if 'kh-z-a' in roots:
    roots['kh-z-a']['arabic'] = []
    changes.append('kh-z-a: removed all wrong Arabic cognates (no Arabic cognate exists)')

# n-p-q: remove non-cognate kharaja forms
if 'n-p-q' in roots:
    arb = roots['n-p-q'].get('arabic', [])
    roots['n-p-q']['arabic'] = [a for a in arb if 'kharaj' not in a['transliteration'].lower() and 'خَرَج' not in a.get('word', '')]
    changes.append('n-p-q: removed non-cognate خرج forms from Arabic')

# g-b-a: remove ikhtara
if 'g-b-a' in roots:
    arb = roots['g-b-a'].get('arabic', [])
    roots['g-b-a']['arabic'] = [a for a in arb if 'ikhtar' not in a['transliteration'].lower()]
    changes.append('g-b-a: removed اختار (wrong root)')

# m-l-p: mark Arabic as semantic parallel
if 'm-l-p' in roots:
    for a in roots['m-l-p'].get('arabic', []):
        a['outlier'] = True
    changes.append('m-l-p: marked Arabic as semantic parallels (no true cognate)')

# kh-b-sh: remove asir and qayd
if 'kh-b-sh' in roots:
    arb = roots['kh-b-sh'].get('arabic', [])
    roots['kh-b-sh']['arabic'] = [a for a in arb if a['transliteration'].lower() not in ('asir', 'asīr', 'qayd')]
    changes.append('kh-b-sh: removed أسير and قيد (wrong roots)')

# l-b-n: remove abyad
if 'l-b-n' in roots:
    arb = roots['l-b-n'].get('arabic', [])
    roots['l-b-n']['arabic'] = [a for a in arb if 'abya' not in a['transliteration'].lower()]
    changes.append('l-b-n: removed أبيض (semantic equivalent, not cognate)')

# sh-r (biliteral): remove sharra
if 'sh-r' in roots:
    roots['sh-r']['arabic'] = []
    changes.append('sh-r: removed شرّ (false cognate)')

# kh-sh (biliteral): remove ihsas, fix hashsha
if 'kh-sh' in roots:
    arb = roots['kh-sh'].get('arabic', [])
    roots['kh-sh']['arabic'] = [a for a in arb if 'ikhsas' not in a['transliteration'].lower() and 'ihsās' not in a['transliteration'].lower() and 'iḥsās' not in a['transliteration'].lower()]
    changes.append('kh-sh: removed إحساس (wrong root ح-س-س)')

# kh-d-y: remove farih
if 'kh-d-y' in roots:
    arb = roots['kh-d-y'].get('arabic', [])
    roots['kh-d-y']['arabic'] = [a for a in arb if 'farih' not in a['transliteration'].lower() and 'fariḥ' not in a['transliteration'].lower()]
    changes.append('kh-d-y: removed فرح (wrong root)')

# kh-d-r: remove forms from ح-ض-ر
if 'kh-d-r' in roots:
    arb = roots['kh-d-r'].get('arabic', [])
    roots['kh-d-r']['arabic'] = [a for a in arb if 'muhadar' not in a['transliteration'].lower() and 'muḥāḍar' not in a['transliteration'].lower() and 'hidar' not in a['transliteration'].lower() and 'ḥiḍār' not in a['transliteration'].lower()]
    changes.append('kh-d-r: removed ح-ض-ر forms (different root)')

# kh-b-r: note confusion
if 'kh-b-r' in roots:
    for a in roots['kh-b-r'].get('arabic', []):
        if 'habara' in a['transliteration'].lower() or 'ḥabara' in a['transliteration'].lower():
            a['outlier'] = True
    changes.append('kh-b-r: marked ح-ب-ر forms as outliers (may be خ-ب-ر)')

# B. Fix 4 incorrect outlier markings
outlier_fixes = {
    'y-l-d': ['milad', 'milād', 'mīlād', 'mawlud', 'mawlūd'],
    'm-l-k': ['mulk'],
    'e-b-d': ["ma'bud", "maʿbūd", "ma'būd"],
    'kh-r-m': ['hurma', 'ḥurma', 'ḥurmah'],
}
for key, translits in outlier_fixes.items():
    if key not in roots:
        continue
    translits_lower = [t.lower() for t in translits]
    for a in roots[key].get('arabic', []):
        if a['transliteration'].lower() in translits_lower and a.get('outlier'):
            del a['outlier']
            changes.append(f'{key}: unmarked {a["transliteration"]} as outlier (core per Lane)')

# C. Fix 3 wrong glosses
# m-l-k: fix malaka
if 'm-l-k' in roots:
    for a in roots['m-l-k'].get('arabic', []):
        if a['transliteration'].lower() in ('malaka', 'malakah'):
            if 'queen' in a.get('meaning_en', '').lower() or 'reina' in a.get('meaning_es', '').lower():
                a['meaning_en'] = 'faculty, aptitude, natural ability'
                a['meaning_es'] = 'facultad, aptitud, habilidad natural'
                changes.append('m-l-k: fixed malaka meaning (faculty, not queen)')

# q-d-sh: fix vocalization
if 'q-d-sh' in roots:
    for a in roots['q-d-sh'].get('arabic', []):
        if a.get('word') == 'قِدْس':
            a['word'] = 'قُدْس'
            a['transliteration'] = 'quds'
            changes.append('q-d-sh: fixed vocalization to قُدْس (quds)')

# sh-l-m: replace salum with salim
if 'sh-l-m' in roots:
    for a in roots['sh-l-m'].get('arabic', []):
        if a['transliteration'].lower() in ('salum', 'salūm'):
            a['word'] = 'سَالِم'
            a['transliteration'] = 'sālim'
            a['meaning_en'] = 'safe, sound, intact'
            a['meaning_es'] = 'sano, salvo, intacto'
            changes.append('sh-l-m: replaced salūm with sālim (attested in Lane)')


# ============================================================
# III. SYRIAC (PAYNE SMITH) FIXES
# ============================================================

# A. Fix 10 incorrect glosses
gloss_fixes = {
    's-k-l': {'gloss_en': 'be foolish, senseless', 'gloss_es': 'ser necio, insensato'},
    'sh-w-q': {'gloss_en': 'street, market', 'gloss_es': 'calle, mercado'},
    'e-w-l': {'gloss_en': 'iniquity, wrong', 'gloss_es': 'iniquidad, injusticia'},
    'q-l-l': {'gloss_en': 'be light, swift; curse', 'gloss_es': 'ser ligero, veloz; maldecir'},
    'z-d-q': {'gloss_en': 'be right, fitting, proper', 'gloss_es': 'ser correcto, apropiado, justo'},
    'k-m-r': {'gloss_en': 'pagan priest', 'gloss_es': 'sacerdote pagano'},
    'z-q-p': {'gloss_en': 'raise up, erect; crucify', 'gloss_es': 'levantar, erigir; crucificar'},
}
# sh-r biliteral
if 'sh-r' in roots:
    roots['sh-r']['gloss_en'] = 'leap, spring'
    roots['sh-r']['gloss_es'] = 'saltar, brincar'
    changes.append('sh-r: fixed gloss to "leap, spring" (Payne Smith)')

for key, fix in gloss_fixes.items():
    if key in roots:
        old_en = roots[key].get('gloss_en', '')
        roots[key]['gloss_en'] = fix['gloss_en']
        roots[key]['gloss_es'] = fix['gloss_es']
        changes.append(f'{key}: changed gloss from "{old_en}" to "{fix["gloss_en"]}"')

# B. Remove 6 ghost roots (particles/prepositions)
ghost_roots = ['w-m-n', 'm-d-m', 'l-w-th', 'a-y-k', 'a-y-th', 'k-w-l']
for key in ghost_roots:
    if key in roots:
        del roots[key]
        changes.append(f'{key}: DELETED (not a root — grammatical particle)')

# C. Fix 4 root confusions
confusion_roots = ['sh-y-kh', 'p-l-sh', 'd-m-n']
for key in confusion_roots:
    if key in roots:
        del roots[key]
        changes.append(f'{key}: DELETED (not attested / confused with another root)')

# p-r-s: fix gloss, don't delete (it exists but Pharisee meaning belongs to p-r-sh)
if 'p-r-s' in roots:
    if 'fariseo' in roots['p-r-s'].get('gloss_es', '').lower() or 'pharisee' in roots['p-r-s'].get('gloss_en', '').lower():
        roots['p-r-s']['gloss_en'] = 'spread out, stretch'
        roots['p-r-s']['gloss_es'] = 'extender, desplegar'
        changes.append('p-r-s: removed Pharisee reference (belongs to P-R-SH)')


# ============================================================
# SAVE
# ============================================================

with open('data/cognates.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\n=== PRIORITY 1 FIXES APPLIED: {len(changes)} changes ===\n')
for c in changes:
    print(f'  {c}')
print(f'\nTotal roots remaining: {len(roots)}')
