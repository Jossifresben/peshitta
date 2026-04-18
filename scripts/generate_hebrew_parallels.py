#!/usr/bin/env python3
"""Generate hebrew_parallel (translation shift) for each root in cognates.json.

Uses Claude Opus to generate Hebrew source equivalents and a prose analysis of
what shifts when Hebrew is rendered into its Aramaic sister language (Peshitta OT).

Usage:
    python scripts/generate_hebrew_parallels.py                    # Process all
    python scripts/generate_hebrew_parallels.py --dry-run          # Preview prompt
    python scripts/generate_hebrew_parallels.py --root kh-k-m      # Single root
"""

import argparse
import json
import os
import sys
import time

import anthropic

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cognates.json')

SYSTEM_PROMPT = """\
You are an expert in Semitic linguistics, biblical Hebrew, Syriac/Aramaic, and Peshitta translation history.
You specialize in analyzing how meaning shifts when Hebrew is translated into its Aramaic sister language
in the Peshitta Old Testament.

Context: The Peshitta OT books we are analyzing (Psalms, Proverbs, Isaiah, Ezekiel) are notable because
the Syriac translator consulted both the Hebrew Masoretic text and the Greek Septuagint (LXX),
creating a unique triple-source translation. Proverbs is the most complex, with evidence of
Targum influence alongside Hebrew and Greek sources.

Given a Syriac triliteral root with its gloss, semantic field, and Hebrew/Arabic cognates,
produce a Hebrew→Syriac translation shift analysis.

Rules:
- Output ONLY a JSON object with the exact keys shown below
- "word": the Hebrew source word most commonly rendered by this Syriac root (in Hebrew script, with nikkud)
- "transliteration": standard Latin transliteration of the Hebrew word
- "meaning_es" / "meaning_en": how this Hebrew word is typically translated in modern Spanish/English Bibles
- "hebrew_range_es" / "hebrew_range_en": the FULL semantic range of the Hebrew source word (3-6 meanings, comma-separated). Include physical, abstract, and metaphorical senses.
- "syriac_range_es" / "syriac_range_en": the Syriac root's semantic range AND what it preserved, lost, or shifted from the Hebrew. One phrase.
- "cognate_status": one of exactly three values:
  - "cognate" — the Syriac root is a direct phonological cognate of the Hebrew (same triliteral root with regular sound shifts like Ts→Ayin, Sh→T, Z→D)
  - "substitution" — the Syriac uses a non-cognate root to translate the Hebrew (e.g., Hebrew Y-R-D → Syriac N-KH-T for "descend")
  - "lxx_influenced" — the Syriac rendering follows the Greek LXX reading rather than the Hebrew Masoretic text
- "shift_es" / "shift_en": a prose paragraph (3-5 sentences) narrating the translation shift. Write like a teacher explaining to a student:
  - For "cognate": analyze the subtle semantic drift between these sister-language roots. Where do they overlap? Where have they diverged? Point out any "false friend" danger.
  - For "substitution": explain WHY the Syriac translator chose a different root. What dimensions were lost or gained? Was it a theological, cultural, or linguistic choice?
  - For "lxx_influenced": identify the specific Greek LXX reading that displaced the Hebrew, explain why the translator followed the Greek, and what Hebrew nuance was lost.
- If the root has NO clear Hebrew OT source (purely Aramaic/Christian terms, NT-only roots), return {"skip": true}

Examples:

Root: KH-K-M | Gloss: wisdom / sabiduría
Sabor raíz: wisdom, skill, discernment
Hebrew: ḥokhmah (wisdom), ḥakham (wise)
Arabic: ḥikmah (wisdom), ḥakīm (wise/doctor)
→ {
  "word": "חָכְמָה",
  "transliteration": "ḥokhmah",
  "meaning_es": "sabiduría",
  "meaning_en": "wisdom",
  "hebrew_range_es": "sabiduría, habilidad artesanal, astucia, prudencia práctica, sabiduría cósmica, inteligencia divina",
  "hebrew_range_en": "wisdom, craftsmanship skill, cunning, practical prudence, cosmic wisdom, divine intelligence",
  "syriac_range_es": "sabiduría, discernimiento, habilidad — preserva el campo semántico casi completo del hebreo como cognado directo",
  "syriac_range_en": "wisdom, discernment, skill — preserves nearly the full Hebrew semantic field as a direct cognate",
  "cognate_status": "cognate",
  "shift_es": "En hebreo, חָכְמָה (ḥokhmah) abarca desde la habilidad manual del artesano (Éxodo 31:3) hasta la sabiduría cósmica personificada como mujer (Proverbios 8). El siríaco ܚܟܡܬܐ (ḥekhmta) es cognado directo con correspondencia fonológica regular. Sin embargo, en el contexto de Proverbios, el traductor siríaco a veces sigue la Septuaginta al interpretar la Sabiduría personificada en términos más abstractos y filosóficos, perdiendo el matiz concreto y artesanal del hebreo. La dimensión de 'astucia' (ḥokhmah como estrategia, incluso engaño) también se atenúa en siríaco.",
  "shift_en": "In Hebrew, חָכְמָה (ḥokhmah) spans from the manual skill of a craftsman (Exodus 31:3) to cosmic wisdom personified as a woman (Proverbs 8). Syriac ܚܟܡܬܐ (ḥekhmta) is a direct cognate with regular phonological correspondence. However, in the Proverbs context, the Syriac translator sometimes follows the Septuagint in interpreting personified Wisdom in more abstract, philosophical terms, losing the concrete, artisanal nuance of the Hebrew. The dimension of 'cunning' (ḥokhmah as strategy, even deception) is also muted in Syriac."
}

Root: N-KH-T | Gloss: to descend / descender
Sabor raíz: descenso, bajada, penetración
Hebrew: naḥat (rest/descent)
Arabic: —
→ {
  "word": "יָרַד",
  "transliteration": "yarad",
  "meaning_es": "descender",
  "meaning_en": "to descend",
  "hebrew_range_es": "descender, bajar, caer, hundirse, ir abajo (hacia el Sheol)",
  "hebrew_range_en": "to descend, go down, fall, sink, go down (to Sheol)",
  "syriac_range_es": "descender, penetrar, bajar — sustituye al hebreo Y-R-D con una raíz que enfatiza la penetración vertical",
  "syriac_range_en": "to descend, penetrate, go down — substitutes Hebrew Y-R-D with a root emphasizing vertical penetration",
  "cognate_status": "substitution",
  "shift_es": "El hebreo יָרַד (yarad) es la raíz estándar para 'descender' en todo el AT, desde bajar una montaña hasta descender al Sheol. El siríaco no usa el cognado de Y-R-D sino que sustituye con ܢܚܬ (N-KH-T), que añade un matiz de penetración vertical, de hundirse hacia adentro. Esta sustitución no es casual: en arameo, N-KH-T evoca un descenso más profundo e interiorizado que el movimiento direccional neutro del hebreo. Se gana intensidad pero se pierde la neutralidad geográfica del original.",
  "shift_en": "Hebrew יָרַד (yarad) is the standard root for 'to descend' throughout the OT, from going down a mountain to descending to Sheol. Syriac does not use the cognate of Y-R-D but substitutes with ܢܚܬ (N-KH-T), which adds a nuance of vertical penetration, of sinking inward. This substitution is not accidental: in Aramaic, N-KH-T evokes a deeper, more internalized descent than the directionally neutral movement in Hebrew. Intensity is gained but the geographical neutrality of the original is lost."
}
"""


def build_user_prompt(key: str, entry: dict) -> str:
    """Build the user prompt for a single root."""
    gloss_combined = f"{entry.get('gloss_en', '')} / {entry.get('gloss_es', '')}"
    sabor = entry.get('sabor_raiz_en', '') or entry.get('gloss_en', '')

    cognate_words = []
    for hw in entry.get('hebrew', []):
        if not hw.get('outlier', False):
            cognate_words.append(f"{hw['transliteration']} ({hw.get('meaning_en', '')})")
    for aw in entry.get('arabic', []):
        if not aw.get('outlier', False):
            cognate_words.append(f"{aw['transliteration']} ({aw.get('meaning_en', '')})")

    cognates_str = ', '.join(cognate_words[:12]) if cognate_words else 'none'

    root_syriac = entry.get('root_syriac', '')
    syriac_part = f" ({root_syriac})" if root_syriac else ''

    return (
        f"Root: {key.upper()}{syriac_part} | Gloss: {gloss_combined}\n"
        f"Sabor raíz: {sabor}\n"
        f"Cognates: {cognates_str}"
    )


def generate_hebrew_parallel(client: anthropic.Anthropic, key: str, entry: dict,
                             model: str = "claude-opus-4-6") -> dict | None:
    """Call Claude to generate hebrew_parallel for one root."""
    user_prompt = build_user_prompt(key, entry)

    try:
        response = client.messages.create(
            model=model,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text.strip()
        # Strip markdown code blocks if present
        if text.startswith('```'):
            text = text.split('\n', 1)[1] if '\n' in text else text[3:]
            if text.endswith('```'):
                text = text[:-3].strip()
        result = json.loads(text)

        # Check for skip signal
        if result.get('skip'):
            print("⊘ no Hebrew equivalent")
            return None

        required = ['word', 'transliteration', 'meaning_es', 'meaning_en',
                     'hebrew_range_es', 'hebrew_range_en',
                     'syriac_range_es', 'syriac_range_en',
                     'cognate_status',
                     'shift_es', 'shift_en']
        if all(k in result for k in required):
            # Validate cognate_status
            if result['cognate_status'] not in ('cognate', 'substitution', 'lxx_influenced'):
                print(f"  WARNING: Invalid cognate_status for {key}: {result['cognate_status']}", file=sys.stderr)
                result['cognate_status'] = 'cognate'  # fallback
            return result
        missing = [k for k in required if k not in result]
        print(f"  WARNING: Missing keys for {key}: {missing}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        print(f"  WARNING: Invalid JSON for {key}: {text[:200]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ERROR for {key}: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description='Generate hebrew_parallel fields')
    parser.add_argument('--dry-run', action='store_true', help='Preview without calling API')
    parser.add_argument('--root', type=str, help='Process a single root (e.g., kh-k-m)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing hebrew_parallel')
    args = parser.parse_args()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    roots = data.get('roots', {})
    client = None if args.dry_run else anthropic.Anthropic()

    if args.root:
        keys_to_process = [args.root.lower()]
    else:
        keys_to_process = list(roots.keys())

    skipped = 0
    processed = 0
    failed = 0

    for i, key in enumerate(keys_to_process):
        if key not in roots:
            print(f"Root '{key}' not found in cognates.json", file=sys.stderr)
            continue

        entry = roots[key]

        # Skip if already has hebrew_parallel (unless --overwrite)
        if not args.overwrite and entry.get('hebrew_parallel'):
            skipped += 1
            continue

        prompt = build_user_prompt(key, entry)

        if args.dry_run:
            print(f"\n--- {key} ---")
            print(prompt)
            continue

        print(f"[{i+1}/{len(keys_to_process)}] {key}...", end=' ', flush=True)
        result = generate_hebrew_parallel(client, key, entry)

        if result:
            entry['hebrew_parallel'] = result
            word = result['word']
            translit = result['transliteration']
            status = result['cognate_status']
            print(f"✓ {word} ({translit}) [{status}]")
            processed += 1
        else:
            failed += 1

        # Rate limiting
        if not args.dry_run and i < len(keys_to_process) - 1:
            time.sleep(1.0)

        # Save every 10 roots
        if processed > 0 and processed % 10 == 0:
            with open(DATA_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  [Saved checkpoint at {processed} roots]")

    if not args.dry_run and processed > 0:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {processed} generated, {skipped} skipped, {failed} failed")


if __name__ == '__main__':
    main()
