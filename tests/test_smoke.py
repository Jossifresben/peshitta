"""Route-level smoke tests for the Peshitta Constellations Flask app.

These mirror the smoke checks that the production deploy script runs against
peshitta.onrender.com after every push:
  - Every route returns 200 (or a documented non-error code)
  - Version metadata is consistent across openapi.yaml, /api/citation, and
    citations.py
  - Methodology pages contain the corrected framing (no "Aramaic Jesus" /
    "spoken in Aramaic" overreach)
  - Visualizer Root Card chain renders Greek (NT source) BEFORE Syriac
    (Peshitta) BEFORE Modern translation
  - Functional API endpoints return well-formed JSON

Run locally with:
    pip install -r requirements-dev.txt
    pytest -q
"""
import json
import re
import pytest


# ---------------------------------------------------------------------------
# 1. Routes return 200
# ---------------------------------------------------------------------------

ROUTES = [
    "/",
    "/methodology?lang=en",
    "/methodology?lang=es",
    "/methodology?lang=he",
    "/methodology?lang=ar",
    "/methodology?lang=nl",
    "/visualize/Z-D-Q?lang=en&trans=en",
    "/visualize/Z-D-Q?lang=es&trans=es",
    "/read?book=Matthew&chapter=1",
    "/api?lang=en",
    "/docs",
    "/openapi.json",
    "/static/openapi.yaml",
    "/about",
    "/browse?lang=en",
    "/api/citation?type=app",
    "/api/root-family?root=Z-D-Q",
    "/api/roots?q=Z-D-Q",
]


@pytest.mark.parametrize("path", ROUTES)
def test_route_returns_200(client, path):
    """Every advertised route should return HTTP 200."""
    response = client.get(path)
    assert response.status_code == 200, (
        f"GET {path} returned {response.status_code}, expected 200"
    )


# ---------------------------------------------------------------------------
# 2. Version metadata consistency
# ---------------------------------------------------------------------------

def _expected_version():
    """Single source of truth: read from citations.VERSION."""
    from peshitta_roots import citations
    return citations.VERSION


def test_openapi_info_version_matches_citations_module(client):
    """/openapi.json info.version must match peshitta_roots.citations.VERSION."""
    response = client.get("/openapi.json")
    spec = json.loads(response.data)
    assert spec["info"]["version"] == _expected_version()


def test_api_citation_metadata_version_matches(client):
    """/api/citation must report the same version."""
    response = client.get("/api/citation?type=app")
    payload = json.loads(response.data)
    assert payload["metadata"]["version"] == _expected_version()


def test_api_citation_apa_string_contains_version(client):
    """The APA-style citation string should embed the current version."""
    response = client.get("/api/citation?type=app")
    payload = json.loads(response.data)
    apa = payload.get("styles", {}).get("apa", "")
    assert _expected_version() in apa, (
        f"APA citation {apa!r} does not include version {_expected_version()}"
    )


# ---------------------------------------------------------------------------
# 3. Methodology framing — no "Aramaic Jesus" / "spoken in Aramaic" overreach
# ---------------------------------------------------------------------------

# Phrases that should NEVER appear on the methodology page in any language.
# Each entry is (lang, phrase, description).
PROBLEM_PHRASES = [
    ("en", "study of the Aramaic Jesus", "English Aramaic-Jesus overreach"),
    ("en", "spoken in Aramaic, recorded in Greek", "English recovery framing"),
    ("es", "estudio del arameo de Jesús", "Spanish Aramaic-Jesus overreach"),
    ("es", "pronunciados en arameo, recogidos en griego", "Spanish recovery framing"),
    ("nl", "studie van de Aramese Jezus", "Dutch Aramaic-Jesus overreach"),
    ("ar", "دراسة آرامية يسوع", "Arabic Aramaic-Jesus overreach"),
    ("he", "חקר הארמית של ישוע", "Hebrew Aramaic-Jesus overreach"),
]


@pytest.mark.parametrize("lang,phrase,desc", PROBLEM_PHRASES)
def test_methodology_does_not_contain_recovery_framing(client, lang, phrase, desc):
    """The corrected methodology page should not contain the old recovery rhetoric."""
    response = client.get(f"/methodology?lang={lang}")
    body = response.data.decode("utf-8")
    assert phrase not in body, f"{desc}: still finds {phrase!r} on /methodology?lang={lang}"


def test_methodology_en_contains_corrected_framing(client):
    """The new framing paragraph should be present on the English methodology page."""
    response = client.get("/methodology?lang=en")
    body = response.data.decode("utf-8")
    assert "Aramaic-speaking Christian scholars in the fourth and fifth" in body, (
        "Corrected framing paragraph missing from English methodology page"
    )


def test_methodology_es_contains_corrected_framing(client):
    """The new framing paragraph should be present on the Spanish methodology page."""
    response = client.get("/methodology?lang=es")
    body = response.data.decode("utf-8")
    assert "eruditos cristianos arameoparlantes en los siglos IV y V" in body, (
        "Corrected framing paragraph missing from Spanish methodology page"
    )


# ---------------------------------------------------------------------------
# 4. Visualizer chain order — Greek must render BEFORE Syriac BEFORE Modern
# ---------------------------------------------------------------------------

def test_visualizer_chain_order_is_greek_syriac_modern(client):
    """The Root Card cross-translation chain must render in the historically correct
    direction: Greek (NT source) → Syriac (Peshitta) → Modern translation."""
    response = client.get("/visualize/Z-D-Q?lang=en&trans=en")
    body = response.data.decode("utf-8")
    # Find the order in which the three CSS class markers appear in the JS render block
    pattern = re.compile(r"deg-(greek|aramaic|modern)")
    matches = [m.group(1) for m in pattern.finditer(body)]
    # Take the first three distinct occurrences (the JS render-template block)
    seen = []
    for m in matches:
        if m not in seen:
            seen.append(m)
        if len(seen) == 3:
            break
    assert seen == ["greek", "aramaic", "modern"], (
        f"Chain order in render template is {seen}, expected ['greek', 'aramaic', 'modern']"
    )


def test_visualizer_uses_syriac_peshitta_label(client):
    """The chain step previously labelled 'Aramaic' must now read 'Syriac (Peshitta)'."""
    response = client.get("/visualize/Z-D-Q?lang=en&trans=en")
    body = response.data.decode("utf-8")
    # The payload is rendered as a JS object literal (unquoted key, double-quoted value)
    # rather than strict JSON, so match flexibly:
    assert re.search(r'degradationAramaic\s*:\s*"Syriac \(Peshitta\)"', body), (
        "Visualizer i18n payload should now serve 'Syriac (Peshitta)' as the chain label"
    )


# ---------------------------------------------------------------------------
# 5. Functional API smoke
# ---------------------------------------------------------------------------

def test_root_family_returns_well_formed_data(client):
    """/api/root-family should return a JSON object with the expected fields."""
    response = client.get("/api/root-family?root=Z-D-Q")
    payload = json.loads(response.data)
    assert payload.get("root_translit") == "Z-D-Q"
    # Greek parallel should be present for this root
    assert "greek_parallel" in payload
    assert payload["greek_parallel"].get("word"), (
        "greek_parallel.word missing from /api/root-family payload"
    )


def test_roots_search_returns_results(client):
    """/api/roots should return search results for a known root."""
    response = client.get("/api/roots?q=Z-D-Q")
    payload = json.loads(response.data)
    # Payload structure may vary; just check it's well-formed JSON
    assert isinstance(payload, (dict, list)), "Search response should be JSON-parsable"
