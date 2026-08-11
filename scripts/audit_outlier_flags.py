#!/usr/bin/env python3
"""Audit the `outlier` flags in data/cognates.json and report false positives.

`scripts/tag_outliers.py` flagged 620 of 3459 cognates as semantic outliers.
A purely lexical screen found dozens of near-certain false positives: entries
whose meaning literally restates the root gloss ("puerta" under a root glossed
"puerta"), or that are simply the same word in a sister dialect. This script
re-evaluates every currently-flagged cognate against the ORIGINAL outlier
definition, one API call per root, with a prompt hardened against that
observed failure mode.

Report-only by default. Never touches cognates.json without --apply.

Usage:
    python scripts/audit_outlier_flags.py --root th-r-e --dry-run  # prompt shape
    python scripts/audit_outlier_flags.py --root th-r-e            # 1 live call
    python scripts/audit_outlier_flags.py --limit 5                # first 5 roots
    python scripts/audit_outlier_flags.py                          # full report
    python scripts/audit_outlier_flags.py --apply                  # write changes

Requires ANTHROPIC_API_KEY in env:
    set -a && . ./.env && set +a

Uses claude-opus-4-5 (same as scripts/tag_cognate_domains.py) — this is a
judgment call on Semitic semantics, not a mechanical classification.
"""

import argparse
import json
import os
import re
import sys
import time

import anthropic

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COGNATES_PATH = os.path.join(REPO_ROOT, 'data', 'cognates.json')
REPORT_PATH = os.path.join(REPO_ROOT, 'docs', 'outlier-flag-audit.md')

MODEL = "claude-opus-4-5"

# Opus-tier pricing, USD per token.
PRICE_IN = 5.0 / 1_000_000
PRICE_OUT = 25.0 / 1_000_000

SYSTEM_PROMPT = """\
You are a Semitic linguistics expert auditing a dataset of triliteral root families.

Each root has a GLOSS (its core meaning) and a list of Hebrew and Arabic cognates.
Some cognates were previously tagged as semantic OUTLIERS. Many of those tags are
WRONG. Your job is to review each currently-tagged cognate and decide whether the
tag is justified.

DEFINITION (the only one that counts):
A cognate is an OUTLIER if its meaning has genuinely diverged from the root's
semantic field with NO clear metaphorical or etymological bridge to the ROOT GLOSS.

Apply these rules strictly:

1. NOT AN OUTLIER if the cognate's meaning restates, translates, or closely
   paraphrases the root gloss. If the gloss is "puerta" (door) and the cognate
   means "puerta", "puerta grande", "umbral de puerta", or "acto de abrir una
   puerta", it is NOT an outlier. This is the single most common error in the
   existing tags — check for it first.

2. NOT AN OUTLIER on dialect grounds alone. A cognate marked "(arameo)",
   "(Aramaic)", "(arameo bíblico)", "(siríaco)" or similar is the same word in a
   sister dialect. Being in a sister dialect is EVIDENCE OF COGNACY, not evidence
   of divergence. Judge it purely on meaning.

3. NOT AN OUTLIER if it is a metaphorical, figurative, causative, nominal,
   instrumental, agentive, or locative EXTENSION of the gloss. "Library" extends
   "write". "Scent" extends "wind/breath". "Priest" extends "priest/diviner".
   "Place of the earth" extends "earth". Derivational morphology is not divergence.

4. NOT AN OUTLIER if it names a concrete object, place, agent, action, or state
   that plainly belongs to the gloss's domain, even if the wording differs.

5. IS AN OUTLIER only when a reader who knows the gloss would find the meaning
   genuinely unrelated, and you cannot state a plausible semantic bridge in one
   sentence. Example: a root glossed "habitar, morar" (to dwell) with a cognate
   meaning "gavilla / sheaf of grain" — no bridge, genuine outlier.

6. If you CAN state a bridge, it is NOT an outlier — even a slightly strained one.
   Homonymous roots that merged in form but not meaning ARE outliers; strained but
   real semantic development is NOT.

Be willing to clear the majority of tags in a root. Being conservative here means
being conservative about calling something an outlier, NOT about changing the tag.

OUTPUT: respond with ONLY valid JSON, no prose, no markdown fence:

{
  "verdicts": [
    {
      "id": "heb:0",
      "outlier": false,
      "confidence": "high",
      "justification": "one line, <=25 words, in Spanish"
    }
  ]
}

Include EXACTLY one verdict per cognate listed under "CURRENTLY TAGGED AS OUTLIER".
Copy the `id` VERBATIM from the input. Do not add verdicts for untagged cognates.
`confidence` is one of "high", "medium", "low" — use "low" when you are genuinely
unsure whether a bridge exists.
"""


def collect_flagged(root_entry: dict) -> list[dict]:
    """Return the currently-flagged cognates of a root, with stable ids."""
    flagged = []
    for lang_key, short in (('hebrew', 'heb'), ('arabic', 'ar')):
        for i, c in enumerate(root_entry.get(lang_key, [])):
            if c.get('outlier'):
                flagged.append({
                    'id': f"{short}:{i}",
                    'lang': lang_key,
                    'index': i,
                    'cognate': c,
                })
    return flagged


def build_user_message(root_key: str, root_entry: dict, flagged: list[dict]) -> str:
    """Format one root family for the model: full field + the tagged subset."""
    lines = [
        f"ROOT: {root_key.upper()}   ({root_entry.get('root_syriac', '')})",
        f"GLOSS (es): {root_entry.get('gloss_es', '')}",
        f"GLOSS (en): {root_entry.get('gloss_en', '')}",
        "",
        "ALL COGNATES IN THIS ROOT FAMILY (for context — judge against the GLOSS, "
        "not against the majority):",
    ]
    for lang_key, short in (('hebrew', 'heb'), ('arabic', 'ar')):
        label = 'Hebrew' if lang_key == 'hebrew' else 'Arabic'
        lines.append(f"  {label}:")
        entries = root_entry.get(lang_key, [])
        if not entries:
            lines.append("    (none)")
        for i, c in enumerate(entries):
            tag = "  [TAGGED OUTLIER]" if c.get('outlier') else ""
            meaning = c.get('meaning_es', '') or c.get('meaning_en', '')
            meaning_en = c.get('meaning_en', '')
            extra = f" / {meaning_en}" if meaning_en and meaning_en != meaning else ""
            lines.append(
                f"    {short}:{i}  {c.get('transliteration', '')} "
                f"({c.get('word', '')}) = {meaning}{extra}{tag}"
            )

    lines.append("")
    lines.append("CURRENTLY TAGGED AS OUTLIER — return exactly one verdict for each:")
    for f in flagged:
        c = f['cognate']
        meaning = c.get('meaning_es', '') or c.get('meaning_en', '')
        lines.append(
            f"  {f['id']}  {c.get('transliteration', '')} = {meaning}"
        )
    lines.append("")
    lines.append(
        "For each, decide: is the tag justified under the definition? "
        "Return JSON only."
    )
    return "\n".join(lines)


def _parse_json(text: str) -> dict | None:
    """Multi-strategy JSON extraction, mirroring the other scripts."""
    try:
        obj = json.loads(text)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    if '```' in text:
        inner = text.split('```')[1]
        if inner.startswith('json'):
            inner = inner[4:]
        try:
            obj = json.loads(inner.strip())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            obj = json.loads(match.group())
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    return None


def audit_root(client, root_key: str, root_entry: dict, flagged: list[dict],
               dry_run: bool = False):
    """Call the model for one root. Returns (verdicts_by_id, usage) or (None, None)."""
    user_msg = build_user_message(root_key, root_entry, flagged)

    if dry_run:
        print(f"\n{'=' * 70}\nDRY RUN — {root_key}\n{'=' * 70}")
        print("--- SYSTEM ---")
        print(SYSTEM_PROMPT)
        print("--- USER ---")
        print(user_msg)
        return None, None

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    usage = response.usage
    text = response.content[0].text.strip()
    parsed = _parse_json(text)
    if parsed is None:
        print(f"  WARNING: could not parse response for {root_key}: {text[:160]}")
        return None, usage

    verdicts = {}
    for v in parsed.get('verdicts', []):
        if not isinstance(v, dict) or 'id' not in v:
            continue
        verdicts[str(v['id']).strip()] = {
            'outlier': bool(v.get('outlier')),
            'confidence': str(v.get('confidence', '')).lower().strip() or 'unknown',
            'justification': str(v.get('justification', '')).strip(),
        }
    return verdicts, usage


def esc(s: str) -> str:
    """Escape a value for a markdown table cell."""
    return str(s).replace('|', r'\|').replace('\n', ' ')


def write_report(path: str, results: list[dict], stats: dict) -> None:
    lines = [
        "# Auditoría de flags `outlier` en `data/cognates.json`",
        "",
        f"Generado por `scripts/audit_outlier_flags.py` (modelo `{MODEL}`).",
        "**Informe únicamente — no se ha modificado `data/cognates.json`.**",
        "",
        "## Resumen",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Raíces con ≥1 flag | {stats['roots_in_scope']} |",
        f"| Raíces auditadas | {stats['roots_audited']} |",
        f"| Raíces con error de API/parseo | {stats['roots_failed']} |",
        f"| Flags revisados | {stats['reviewed']} |",
        f"| Flags que deberían **eliminarse** (falsos positivos) | {stats['clear']} |",
        f"| Flags **confirmados** como outliers genuinos | {stats['confirm']} |",
        f"| Veredictos con confianza baja/media | {stats['low_conf']} |",
        f"| Coste real | ${stats['cost']:.2f} |",
        "",
    ]
    if stats['reviewed']:
        pct = 100.0 * stats['clear'] / stats['reviewed']
        lines += [
            f"El {pct:.0f}% de los flags revisados son falsos positivos.",
            "",
        ]

    # --- proposed clears ---
    clears = [r for r in results if not r['verdict']['outlier']]
    lines += [
        "## Cambios propuestos (flags a eliminar)",
        "",
        f"{len(clears)} entradas. Cada una debería perder `\"outlier\": true`.",
        "",
        "| Raíz | Gloss (es) | Lang | Translit | Significado | Conf. | Justificación |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(clears, key=lambda x: (x['root'], x['id'])):
        lines.append(
            f"| `{esc(r['root'])}` | {esc(r['gloss_es'])} | {esc(r['lang'])} | "
            f"{esc(r['transliteration'])} | {esc(r['meaning'])} | "
            f"{esc(r['verdict']['confidence'])} | {esc(r['verdict']['justification'])} |"
        )

    # --- confirmed ---
    confirms = [r for r in results if r['verdict']['outlier']]
    lines += [
        "",
        "## Flags confirmados (outliers genuinos)",
        "",
        f"{len(confirms)} entradas. Sin cambios.",
        "",
        "| Raíz | Gloss (es) | Lang | Translit | Significado | Conf. | Justificación |",
        "|---|---|---|---|---|---|---|",
    ]
    for r in sorted(confirms, key=lambda x: (x['root'], x['id'])):
        lines.append(
            f"| `{esc(r['root'])}` | {esc(r['gloss_es'])} | {esc(r['lang'])} | "
            f"{esc(r['transliteration'])} | {esc(r['meaning'])} | "
            f"{esc(r['verdict']['confidence'])} | {esc(r['verdict']['justification'])} |"
        )

    # --- uncertain ---
    uncertain = [r for r in results if r['verdict']['confidence'] in ('low', 'medium')]
    lines += [
        "",
        "## Veredictos con confianza baja o media (revisión humana recomendada)",
        "",
    ]
    if not uncertain:
        lines.append("Ninguno.")
    else:
        lines += [
            "| Raíz | Gloss (es) | Translit | Significado | Veredicto | Conf. | Justificación |",
            "|---|---|---|---|---|---|---|",
        ]
        for r in sorted(uncertain, key=lambda x: (x['verdict']['confidence'], x['root'])):
            verdict = "outlier" if r['verdict']['outlier'] else "NO outlier"
            lines.append(
                f"| `{esc(r['root'])}` | {esc(r['gloss_es'])} | "
                f"{esc(r['transliteration'])} | {esc(r['meaning'])} | {verdict} | "
                f"{esc(r['verdict']['confidence'])} | {esc(r['verdict']['justification'])} |"
            )

    if stats['failed_roots']:
        lines += [
            "",
            "## Raíces no auditadas (error de API o de parseo)",
            "",
        ]
        for k in stats['failed_roots']:
            lines.append(f"- `{k}`")

    if stats['missing']:
        lines += [
            "",
            "## Flags sin veredicto (el modelo omitió la entrada)",
            "",
        ]
        for k in stats['missing']:
            lines.append(f"- `{k}`")

    lines.append("")
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description='Audit outlier flags in cognates.json (report-only by default)')
    parser.add_argument('--root', help='Audit a single root key (e.g. th-r-e)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print the prompt, make no API call')
    parser.add_argument('--limit', type=int,
                        help='Audit only the first N roots in scope')
    parser.add_argument('--apply', action='store_true',
                        help='WRITE the cleared flags back into cognates.json')
    parser.add_argument('--report', default=REPORT_PATH,
                        help=f'Report output path (default: {REPORT_PATH})')
    args = parser.parse_args()

    with open(COGNATES_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    roots = data.get('roots', {})

    # Scope: roots carrying at least one outlier flag.
    scope = []
    for key, entry in roots.items():
        flagged = collect_flagged(entry)
        if flagged:
            scope.append((key, flagged))

    if args.root:
        scope = [(k, f) for k, f in scope if k == args.root]
        if not scope:
            print(f"Root {args.root!r} has no outlier flags (or does not exist). "
                  "Nothing to audit.")
            return
    if args.limit:
        scope = scope[: args.limit]

    total_flags = sum(len(f) for _, f in scope)
    print(f"Roots with >=1 outlier flag in scope: {len(scope)}  "
          f"({total_flags} flags)")
    if args.dry_run:
        print("(dry run — no API calls)")

    client = None if args.dry_run else anthropic.Anthropic()

    results = []
    failed_roots = []
    missing = []
    cost = 0.0
    tok_in = tok_out = 0

    for i, (key, flagged) in enumerate(scope, 1):
        entry = roots[key]
        try:
            verdicts, usage = audit_root(client, key, entry, flagged,
                                         dry_run=args.dry_run)
        except Exception as e:  # noqa: BLE001 — keep going, record the failure
            print(f"  [{i}/{len(scope)}] {key} - ERROR: {e}")
            failed_roots.append(key)
            if not args.dry_run:
                time.sleep(0.5)
            continue

        if usage is not None:
            tok_in += usage.input_tokens
            tok_out += usage.output_tokens
            cost += usage.input_tokens * PRICE_IN + usage.output_tokens * PRICE_OUT

        if args.dry_run:
            continue

        if verdicts is None:
            failed_roots.append(key)
            time.sleep(0.5)
            continue

        n_clear = 0
        for f in flagged:
            v = verdicts.get(f['id'])
            if v is None:
                missing.append(f"{key} / {f['id']} "
                               f"({f['cognate'].get('transliteration', '')})")
                continue
            c = f['cognate']
            results.append({
                'root': key,
                'id': f['id'],
                'lang': 'heb' if f['lang'] == 'hebrew' else 'ar',
                'gloss_es': entry.get('gloss_es', ''),
                'transliteration': c.get('transliteration', ''),
                'word': c.get('word', ''),
                'meaning': c.get('meaning_es', '') or c.get('meaning_en', ''),
                'verdict': v,
            })
            if not v['outlier']:
                n_clear += 1
                if args.apply:
                    c.pop('outlier', None)

        print(f"  [{i}/{len(scope)}] {key} - {len(flagged)} flags, "
              f"{n_clear} to clear, {len(flagged) - n_clear} confirmed  "
              f"(${cost:.2f} so far)")

        if args.apply and n_clear:
            # Checkpoint per root so a crash mid-run doesn't lose paid work.
            with open(COGNATES_PATH, 'w', encoding='utf-8') as f_out:
                json.dump(data, f_out, indent=2, ensure_ascii=False)

        time.sleep(0.5)  # unconditional mild rate-limit

    if args.dry_run:
        print("\n(dry run complete — no report written, no changes made)")
        return

    stats = {
        'roots_in_scope': len(scope),
        'roots_audited': len(scope) - len(failed_roots),
        'roots_failed': len(failed_roots),
        'failed_roots': failed_roots,
        'missing': missing,
        'reviewed': len(results),
        'clear': sum(1 for r in results if not r['verdict']['outlier']),
        'confirm': sum(1 for r in results if r['verdict']['outlier']),
        'low_conf': sum(1 for r in results
                        if r['verdict']['confidence'] in ('low', 'medium')),
        'cost': cost,
    }

    write_report(args.report, results, stats)

    print(f"\nReviewed {stats['reviewed']} flags across {stats['roots_audited']} roots.")
    print(f"  clear (false positives): {stats['clear']}")
    print(f"  confirmed:               {stats['confirm']}")
    print(f"  low/medium confidence:   {stats['low_conf']}")
    if failed_roots:
        print(f"  FAILED roots:            {len(failed_roots)} -> {failed_roots}")
    if missing:
        print(f"  flags without verdict:   {len(missing)}")
    print(f"Tokens: {tok_in} in / {tok_out} out — cost ${cost:.2f}")
    print(f"Report: {args.report}")
    if args.apply:
        print(f"APPLIED: {COGNATES_PATH} updated ({stats['clear']} flags removed).")
    else:
        print("Report only — data/cognates.json untouched (pass --apply to write).")


if __name__ == '__main__':
    main()
