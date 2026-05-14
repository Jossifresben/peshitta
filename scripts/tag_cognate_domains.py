#!/usr/bin/env python3
"""Tag each cognate in cognates.json with a `domain` field via the Claude API.

Operationalizes the editorial preference for concrete material vocabulary
over religious glosses. See docs/superpowers/plans/2026-05-14-domain-tagging-pilot.md
for the full methodology.

Usage:
    python scripts/tag_cognate_domains.py                    # All pilot roots
    python scripts/tag_cognate_domains.py --root h-m-n       # Single root
    python scripts/tag_cognate_domains.py --dry-run          # Preview, no API call
    python scripts/tag_cognate_domains.py --batch-size 10    # Process N then stop

Requires ANTHROPIC_API_KEY in env. Uses claude-opus-4-5 for editorial accuracy
on the nuanced material-vs-religious distinction (a slower / pricier model
than `expand_cognates.py`'s haiku, justified by the one-shot pilot scale).

VALID_DOMAINS is imported from `peshitta_roots.domain_tags` so the script
stays in lock-step with the canonical schema used elsewhere in the codebase.
"""

import argparse
import json
import os
import re
import sys
import time

import anthropic

# Make the package importable when running as a script from the repo root.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from peshitta_roots.domain_tags import VALID_DOMAINS  # noqa: E402

COGNATES_PATH = os.path.join(REPO_ROOT, 'data', 'cognates.json')
PILOT_PATH = os.path.join(REPO_ROOT, 'data', 'pilot_roots.json')

MODEL = "claude-opus-4-5"

SYSTEM_PROMPT = """\
You are a Semitic linguistics expert. For each cognate word in a triliteral \
root family, you assign exactly one DOMAIN tag from this fixed set:

  material  - concrete everyday material life: agriculture, livestock, fishing,
              commerce, household utensils, tools, food, building, body parts.
  religious - devotional, cultic, theological, liturgical, ritual.
  nature    - natural phenomena: weather, geography, non-pastoral animals,
              plants, celestial bodies.
  kinship   - family relations and social bonds: father, mother, sibling, tribe.
  abstract  - mental/moral abstractions used in a NON-religious sense.
  neutral   - catch-all when no other category fits cleanly. Use sparingly.

Editorial principle: prefer the material domain when a word has both a
material and a religious sense, AND the material sense is historically
or etymologically prior. Example: Arabic 'amin' is BOTH a religious "amen"
AND a material "trustworthy person / safe-conduct holder" - tag it MATERIAL,
because the safe-conduct sense preserves the underlying root meaning that
the religious application later abstracts.

But: if a word's PRIMARY lexicographic sense is unambiguously religious
(e.g., 'tefillah' = "prayer", 'qorban' = "sacrifice"), tag it RELIGIOUS.
Don't force material when material is genuinely absent.

Respond with ONLY valid JSON. No prose. Schema:

{
  "hebrew": [
    {"transliteration": "word_translit_as_in_input", "domain": "material"}
  ],
  "arabic": [
    {"transliteration": "word_translit_as_in_input", "domain": "religious"}
  ]
}

Include EVERY cognate from the input. Do not omit, add, or rename.

Copy the `transliteration` field VERBATIM from the input - do not re-transliterate, normalize, or correct it. The downstream code matches by exact string equality.
"""


def build_user_message(root_key: str, root_entry: dict) -> str:
    """Format one root family for the model."""
    lines = [
        f"Root key: {root_key}",
        f"Syriac: {root_entry.get('root_syriac', '')}",
        f"Gloss (en): {root_entry.get('gloss_en', '')}",
        f"Gloss (es): {root_entry.get('gloss_es', '')}",
        f"Sabor raiz (en): {root_entry.get('sabor_raiz_en', '')}",
        "",
        "Hebrew cognates:",
    ]
    for c in root_entry.get('hebrew', []):
        lines.append(
            f"  - {c.get('transliteration', '')} ({c.get('word', '')}): "
            f"{c.get('meaning_en', c.get('meaning_es', ''))}"
        )
    lines.append("Arabic cognates:")
    for c in root_entry.get('arabic', []):
        lines.append(
            f"  - {c.get('transliteration', '')} ({c.get('word', '')}): "
            f"{c.get('meaning_en', c.get('meaning_es', ''))}"
        )
    lines.append("")
    lines.append("Tag every cognate. Return JSON.")
    return "\n".join(lines)


def _parse_json(text: str) -> dict | None:
    """Try to extract a JSON object from a model response.

    Mirrors the multi-strategy parser in expand_cognates.py.
    """
    # Direct parse
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # Markdown code fence
    if '```' in text:
        inner = text.split('```')[1]
        if inner.startswith('json'):
            inner = inner[4:]
        inner = inner.strip()
        try:
            obj = json.loads(inner)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    # Find an object embedded in prose
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    return None


def tag_root(client, root_key: str, root_entry: dict, dry_run: bool = False) -> dict | None:
    """Call Claude for one root. Returns the parsed tag dict or None on failure."""
    user_msg = build_user_message(root_key, root_entry)
    if dry_run:
        print(f"\n--- DRY RUN: {root_key} ---")
        print(user_msg)
        return None

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = response.content[0].text.strip()
    parsed = _parse_json(text)
    if parsed is None:
        print(f"  WARNING: could not parse response for {root_key}: {text[:120]}")
    return parsed


def apply_tags(root_entry: dict, tags: dict) -> int:
    """Merge the model's tags back into root_entry. Returns the count of cognates tagged."""
    count = 0
    for lang in ("hebrew", "arabic"):
        proposed = {
            t["transliteration"]: t["domain"]
            for t in tags.get(lang, [])
            if isinstance(t, dict)
            and t.get("transliteration")
            and t.get("domain") in VALID_DOMAINS
        }
        for c in root_entry.get(lang, []):
            tr = c.get("transliteration")
            if tr in proposed:
                c["domain"] = proposed[tr]
                count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description='Tag cognate domains in cognates.json')
    parser.add_argument("--root", help="Single root key to tag (e.g., h-m-n)")
    parser.add_argument("--dry-run", action="store_true", help="Preview prompt, no API call")
    parser.add_argument("--batch-size", type=int, default=None, help="Process N roots then stop")
    args = parser.parse_args()

    with open(COGNATES_PATH, 'r', encoding='utf-8') as f:
        cognates = json.load(f)
    with open(PILOT_PATH, 'r', encoding='utf-8') as f:
        pilot = json.load(f)
    pilot_keys = [r["key"] for r in pilot["roots"]]

    if args.root:
        targets = [args.root]
    else:
        targets = pilot_keys
    if args.batch_size:
        targets = targets[: args.batch_size]

    client = None if args.dry_run else anthropic.Anthropic()

    total_tagged = 0
    for i, key in enumerate(targets, 1):
        if key not in cognates["roots"]:
            print(f"  [{i}/{len(targets)}] {key} - SKIP (not in cognates.json)")
            continue
        try:
            tags = tag_root(client, key, cognates["roots"][key], dry_run=args.dry_run)
        except Exception as e:
            print(f"  [{i}/{len(targets)}] {key} - ERROR: {e}")
            continue
        if not args.dry_run and tags:
            n = apply_tags(cognates["roots"][key], tags)
            total_tagged += n
            print(f"  [{i}/{len(targets)}] {key} - tagged {n} cognates")
            if n > 0:
                # Checkpoint immediately so a crash mid-batch doesn't lose paid work.
                with open(COGNATES_PATH, 'w', encoding='utf-8') as f:
                    json.dump(cognates, f, indent=2, ensure_ascii=False)
        if not args.dry_run:
            time.sleep(0.5)  # mild rate-limit (also gates failed/unparsed roots)

    if not args.dry_run:
        print(f"\nWrote {COGNATES_PATH}; {total_tagged} cognates tagged total.")


if __name__ == "__main__":
    main()
