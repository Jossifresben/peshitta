# Peshitta Constellations MCP Server

The MCP (Model Context Protocol) server exposes the Peshitta corpus and analytical data to AI agents like Claude Desktop and Claude Code.

## Tools available

- `peshitta_search_root` — search Syriac roots by transliteration or Syriac script
- `peshitta_get_verse` — fetch a single verse with translation
- `peshitta_concordance` — KWIC concordance for any word form
- `peshitta_greek_concordance` — Syriac roots translating a Greek lemma
- `peshitta_passage` — all roots in a passage
- `peshitta_cite` — citation in 5 academic styles

All tool responses include a `_citation` block (author, ORCID, DOI, version).

## Install

```bash
git clone https://github.com/Jossifresben/peshitta.git
cd peshitta
pip install -r requirements.txt
```

## Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "peshitta": {
      "command": "python3",
      "args": ["-m", "peshitta_roots.mcp_server"],
      "cwd": "/path/to/peshitta"
    }
  }
}
```

## Claude Code

Add to `~/.claude/mcp_config.json` (or your project's config):

```json
{
  "mcpServers": {
    "peshitta": {
      "command": "python3",
      "args": ["-m", "peshitta_roots.mcp_server"],
      "cwd": "/path/to/peshitta"
    }
  }
}
```

Restart your client. The 6 tools will appear under the `peshitta` namespace.

## Citation

Fresco, J. (2026). _Peshitta Constellations_ (Version 1.3.0) [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.19358529
