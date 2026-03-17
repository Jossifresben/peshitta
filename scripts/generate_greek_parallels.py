#!/usr/bin/env python3
"""Generate greek_parallel (translation degradation) for each root in cognates.json.

Uses Claude Haiku to generate Greek NT equivalents and a prose analysis of
what semantic nuance was lost in the Aramaic → Greek → modern translation chain.

Usage:
    python scripts/generate_greek_parallels.py                    # Process all
    python scripts/generate_greek_parallels.py --dry-run          # Preview prompt
    python scripts/generate_greek_parallels.py --root r-w-kh      # Single root
"""

import argparse
import json
import os
import sys
import time

import anthropic

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cognates.json')

SYSTEM_PROMPT = """\
You are an expert in Semitic linguistics, Koine Greek, and biblical translation history.
You specialize in analyzing how meaning shifts when Aramaic/Syriac concepts are translated
through Greek into modern languages.

Given a Syriac triliteral root with its gloss, semantic field, and Hebrew/Arabic cognates,
produce a translation degradation analysis showing what was lost from Aramaic → Greek → modern translation.

Rules:
- Output ONLY a JSON object with the exact keys shown below
- "word": the most common Greek NT equivalent (in Greek script)
- "transliteration": standard Latin transliteration of the Greek word
- "meaning_es" / "meaning_en": how this word is typically translated in modern Spanish/English Bibles
- "aramaic_range_es" / "aramaic_range_en": the FULL semantic range of the Aramaic root (3-6 meanings, comma-separated). Include physical, sensory, and abstract meanings.
- "greek_range_es" / "greek_range_en": the Greek word's semantic range AND what philosophical/cultural influence shaped it (Stoic, Platonic, Aristotelian, Hellenistic, etc.). One phrase.
- "lost_es" / "lost_en": a prose paragraph (3-5 sentences) narrating the journey of semantic reduction. Write like a teacher explaining to a student: what the Aramaic word evoked, how the Greek shifted it, and what the modern translation flattened. Be specific and vivid.
- If the root has NO clear Greek NT equivalent (rare particles, purely Aramaic forms), return {"skip": true}

Examples:

Root: R-W-KH | Gloss: spirit, wind / espíritu, viento
Sabor raíz: aliento vital, movimiento invisible, esencia etérea
Hebrew: ruakh (spirit/wind), reakh (scent/aroma)
Arabic: ruh (spirit/soul), rih (wind), rāʾiḥah (scent, fragrance)
→ {
  "word": "πνεῦμα",
  "transliteration": "pneuma",
  "meaning_es": "espíritu",
  "meaning_en": "spirit",
  "aramaic_range_es": "viento, aliento, espíritu, fuerza vital, aroma, brisa",
  "aramaic_range_en": "wind, breath, spirit, life force, fragrance, breeze",
  "greek_range_es": "espíritu, soplo, aliento — matizado por la filosofía estoica del pneuma como principio cósmico racional",
  "greek_range_en": "spirit, breath, wind — colored by Stoic philosophy of pneuma as rational cosmic principle",
  "lost_es": "En arameo, ܪܘܚܐ (ruḥa) abarca todo el campo del aire en movimiento: el viento que sopla, el aliento que sale de la boca, el aroma que llega por la brisa, y la fuerza vital invisible que anima al ser vivo. Cuando se tradujo al griego como πνεῦμα, el término retuvo 'soplo' y 'espíritu', pero filtrado por la filosofía estoica, donde pneuma es un principio cósmico racional. Al llegar al español como 'espíritu', se perdió por completo la dimensión física y sensorial: ya no se siente el viento, ni se huele el aroma, ni se percibe el aliento. Queda solo lo inmaterial.",
  "lost_en": "In Aramaic, ܪܘܚܐ (ruḥa) spans the entire field of moving air: the wind that blows, the breath leaving the mouth, the fragrance carried on the breeze, and the invisible life force animating living beings. When translated to Greek as πνεῦμα, the term retained 'breath' and 'spirit', but filtered through Stoic philosophy where pneuma is a rational cosmic principle. By the time it reached English as 'spirit', the physical, sensory dimension was entirely lost: no wind, no fragrance, no breath. Only the immaterial remains."
}

Root: K-TH-B | Gloss: write / escribir
Sabor raíz: escritura, inscripción, registro
Hebrew: katav (to write), ketuvim (writings)
Arabic: kataba (to write), kitab (book), maktub (written/destined)
→ {
  "word": "γράφω",
  "transliteration": "graphō",
  "meaning_es": "escribir",
  "meaning_en": "to write",
  "aramaic_range_es": "escribir, inscribir, grabar, registrar, decretar",
  "aramaic_range_en": "to write, inscribe, engrave, record, decree",
  "greek_range_es": "escribir, trazar, grabar — asociado al acto manual de marcar sobre superficie",
  "greek_range_en": "to write, draw, scratch — tied to the physical act of marking a surface",
  "lost_es": "En arameo, ܟܬܒ (ktab) une la acción de escribir con el peso de lo decretado: lo escrito tiene fuerza de destino, como en el árabe maktub ('está escrito', es decir, 'está destinado'). El griego γράφω conserva el acto físico de trazar marcas, pero pierde la dimensión de decreto divino. En español, 'escribir' es un acto neutral y cotidiano — se ha evaporado tanto el peso del destino como la sacralidad de la inscripción.",
  "lost_en": "In Aramaic, ܟܬܒ (ktab) unites the act of writing with the weight of decree: what is written carries the force of destiny, as in Arabic maktub ('it is written', meaning 'it is destined'). Greek γράφω preserves the physical act of tracing marks but loses the dimension of divine decree. In English, 'to write' is a neutral, everyday act — both the weight of destiny and the sacredness of inscription have evaporated."
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


def generate_greek_parallel(client: anthropic.Anthropic, key: str, entry: dict,
                            model: str = "claude-opus-4-6") -> dict | None:
    """Call Claude to generate greek_parallel for one root."""
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
            print("⊘ no Greek equivalent")
            return None

        required = ['word', 'transliteration', 'meaning_es', 'meaning_en',
                     'aramaic_range_es', 'aramaic_range_en',
                     'greek_range_es', 'greek_range_en',
                     'lost_es', 'lost_en']
        if all(k in result for k in required):
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
    parser = argparse.ArgumentParser(description='Generate greek_parallel fields')
    parser.add_argument('--dry-run', action='store_true', help='Preview without calling API')
    parser.add_argument('--root', type=str, help='Process a single root (e.g., r-w-kh)')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing greek_parallel')
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

        # Skip if already has greek_parallel (unless --overwrite)
        if not args.overwrite and entry.get('greek_parallel'):
            skipped += 1
            continue

        prompt = build_user_prompt(key, entry)

        if args.dry_run:
            print(f"\n--- {key} ---")
            print(prompt)
            continue

        print(f"[{i+1}/{len(keys_to_process)}] {key}...", end=' ', flush=True)
        result = generate_greek_parallel(client, key, entry)

        if result:
            entry['greek_parallel'] = result
            word = result['word']
            translit = result['transliteration']
            print(f"✓ {word} ({translit})")
            processed += 1
        else:
            failed += 1

        # Rate limiting — Opus is slower, give it breathing room
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
