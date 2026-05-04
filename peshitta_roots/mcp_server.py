"""MCP server exposing Peshitta data to AI agents.

Run with: python -m peshitta_roots.mcp_server

Exposes 6 tools:
  - peshitta_search_root
  - peshitta_get_verse
  - peshitta_concordance
  - peshitta_greek_concordance
  - peshitta_passage
  - peshitta_cite

All tool responses include a _citation block.
"""

import asyncio
import json
import os
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from . import citations
from .corpus import PeshittaCorpus
from .extractor import RootExtractor
from .cognates import CognateLookup


# Initialize data once
_BASE = os.path.dirname(os.path.dirname(__file__))
_corpus = PeshittaCorpus(
    os.path.join(_BASE, 'syriac_nt_traditional22_unicode.csv'),
    extra_csv_paths=[os.path.join(_BASE, 'syriac_ot_selected_unicode.csv')]
        if os.path.exists(os.path.join(_BASE, 'syriac_ot_selected_unicode.csv')) else []
)
_corpus.load()
_extractor = RootExtractor(_corpus, os.path.join(_BASE, 'data'))
_extractor.build_index()
_cognates = CognateLookup(os.path.join(_BASE, 'data'))
_cognates.load()


def _with_citation(payload: dict) -> dict:
    """Wrap a payload with citation metadata."""
    return {**payload, '_citation': citations.metadata()}


server = Server("peshitta-constellations")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="peshitta_search_root",
            description="Search Syriac roots by transliteration (e.g. 'M-L-K') or Syriac script. Returns root data with all forms, references, and cognates.",
            inputSchema={
                "type": "object",
                "properties": {
                    "root": {"type": "string", "description": "Root in dash-transliteration like 'M-L-K' or Syriac script"},
                    "lang": {"type": "string", "enum": ["en", "es"], "default": "en"}
                },
                "required": ["root"]
            }
        ),
        types.Tool(
            name="peshitta_get_verse",
            description="Get a single verse with Syriac, transliteration, and translation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reference": {"type": "string", "description": "Verse reference like 'Matthew 1:1'"},
                    "lang": {"type": "string", "enum": ["en", "es", "he", "ar", "nl"], "default": "en"}
                },
                "required": ["reference"]
            }
        ),
        types.Tool(
            name="peshitta_concordance",
            description="Get all occurrences of a Syriac word form with KWIC context.",
            inputSchema={
                "type": "object",
                "properties": {
                    "form": {"type": "string", "description": "Syriac word form (Syriac script)"},
                    "lang": {"type": "string", "default": "en"}
                },
                "required": ["form"]
            }
        ),
        types.Tool(
            name="peshitta_greek_concordance",
            description="Find all Syriac roots used to translate a given Greek lemma.",
            inputSchema={
                "type": "object",
                "properties": {
                    "greek_word": {"type": "string", "description": "Greek lemma like 'βασιλεύς'"},
                    "lang": {"type": "string", "enum": ["en", "es"], "default": "en"}
                },
                "required": ["greek_word"]
            }
        ),
        types.Tool(
            name="peshitta_passage",
            description="Get all roots in a passage with cognates and semantic bridges.",
            inputSchema={
                "type": "object",
                "properties": {
                    "book": {"type": "string"},
                    "chapter": {"type": "integer"},
                    "v_start": {"type": "integer"},
                    "v_end": {"type": "integer"},
                    "lang": {"type": "string", "default": "en"}
                },
                "required": ["book", "chapter", "v_start", "v_end"]
            }
        ),
        types.Tool(
            name="peshitta_cite",
            description="Generate citation in 5 academic styles (BibTeX, Chicago, MLA, APA, SBL).",
            inputSchema={
                "type": "object",
                "properties": {
                    "view": {"type": "string", "enum": ["app", "root", "passage", "search"], "default": "app"},
                    "label": {"type": "string", "description": "Optional label like 'M-L-K' or 'Matthew 1:1'"}
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "peshitta_search_root":
        root = arguments["root"]
        entry = _extractor.lookup_root(root) or _extractor.lookup_root(root.replace('-', ''))
        if not entry:
            result = {"error": f"Root '{root}' not found"}
        else:
            result = {
                "root_syriac": entry.root,
                "root_transliteration": entry.root_transliteration,
                "total_occurrences": entry.total_occurrences,
                "forms_count": len(entry.matches),
                "matches": [
                    {
                        "form": m.form,
                        "count": len(m.references),
                        "references": m.references[:20],
                        "more_references": max(0, len(m.references) - 20),
                    }
                    for m in entry.matches[:50]
                ]
            }
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    if name == "peshitta_get_verse":
        ref = arguments["reference"]
        lang = arguments.get("lang", "en")
        syriac = _corpus.get_verse_text(ref)
        if not syriac:
            result = {"error": f"Verse '{ref}' not found"}
        else:
            result = {
                "reference": ref,
                "syriac": syriac,
                "translation": _corpus.get_verse_translation(ref, lang),
            }
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    if name == "peshitta_concordance":
        form = arguments["form"]
        refs = _corpus.get_occurrences(form)
        contexts = []
        for ref in refs[:30]:
            text = _corpus.get_verse_text(ref) or ""
            contexts.append({"reference": ref, "context": text})
        result = {"form": form, "total_occurrences": len(refs), "contexts": contexts}
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    if name == "peshitta_greek_concordance":
        # Lazy: read cognates JSON for greek_parallel mappings
        cog_path = os.path.join(_BASE, 'data', 'cognates.json')
        with open(cog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        roots = data.get('roots', {})
        gw = arguments["greek_word"]
        lang = arguments.get("lang", "en")
        matches = []
        for key, d in roots.items():
            gp = d.get('greek_parallel') or {}
            if gp.get('word') == gw or gw.lower() in (gp.get('word') or '').lower():
                matches.append({
                    "key": key.upper(),
                    "root_syriac": d.get('root_syriac', ''),
                    "gloss": d.get(f'gloss_{lang}', d.get('gloss_en', '')),
                    "greek_meaning": gp.get(f'meaning_{lang}', gp.get('meaning_en', '')),
                })
        result = {"query": gw, "total": len(matches), "roots": matches}
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    if name == "peshitta_passage":
        book = arguments["book"]
        chapter = arguments["chapter"]
        v_start = arguments["v_start"]
        v_end = arguments["v_end"]
        verses = _corpus.get_chapter_verses(book, chapter)
        out = []
        for v_num, ref, syriac in verses:
            if v_start <= v_num <= v_end:
                roots = []
                for word in syriac.split():
                    r = _extractor.lookup_word_root(word)
                    if r:
                        roots.append(r)
                out.append({
                    "reference": ref,
                    "syriac": syriac,
                    "roots": list(set(roots))
                })
        result = {"book": book, "chapter": chapter, "v_start": v_start, "v_end": v_end, "verses": out}
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    if name == "peshitta_cite":
        view = arguments.get("view", "app")
        label = arguments.get("label")
        result = {"styles": citations.all_styles(view, label, None)}
        return [types.TextContent(type="text", text=json.dumps(_with_citation(result), ensure_ascii=False, indent=2))]

    return [types.TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
