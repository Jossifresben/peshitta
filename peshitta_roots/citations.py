"""Citation formatters for academic export.

Generates citation strings in BibTeX, Chicago, MLA, APA, and SBL styles.
All citations include author Jossi Fresco with ORCID 0009-0000-2026-0836
and Zenodo concept DOI 10.5281/zenodo.19358529.
"""

from datetime import date

# Citation metadata baseline
AUTHOR_FAMILY = "Fresco"
AUTHOR_GIVEN = "Jossi"
AUTHOR_FULL = "Jossi Fresco"
ORCID = "0009-0000-2026-0836"
ORCID_URL = "https://orcid.org/0009-0000-2026-0836"
DOI = "10.5281/zenodo.19358529"
DOI_URL = "https://doi.org/10.5281/zenodo.19358529"
APP_TITLE = "Peshitta Constellations"
APP_URL = "https://peshitta.onrender.com"
REPO_URL = "https://github.com/Jossifresben/peshitta"
VERSION = "1.4.1"
YEAR = 2026


def _resource_label(view_type: str, label: str | None) -> str:
    """Format the resource label for a citation (e.g., 'root M-L-K')."""
    if not label:
        return ""
    if view_type == "root":
        return f", root {label}"
    if view_type == "passage":
        return f", passage {label}"
    if view_type == "search":
        return f", search results for '{label}'"
    return f", {label}"


def bibtex(view_type: str = "app", label: str | None = None, url: str | None = None) -> str:
    """Generate BibTeX citation. view_type in {'app','root','passage','search'}."""
    key = f"fresco{YEAR}peshitta"
    if label:
        slug = label.lower().replace(" ", "_").replace(":", "_").replace("-", "")
        key = f"fresco{YEAR}peshitta_{slug}"
    full_url = url or APP_URL
    note_parts = [f"ORCID: {ORCID}"]
    if label:
        note_parts.append(f"{view_type}: {label}")
    note = "; ".join(note_parts)
    return f"""@misc{{{key},
  author       = {{Fresco, Jossi}},
  title        = {{{APP_TITLE}{_resource_label(view_type, label)}}},
  year         = {{{YEAR}}},
  version      = {{{VERSION}}},
  doi          = {{{DOI}}},
  url          = {{{full_url}}},
  note         = {{{note}}}
}}"""


def chicago(view_type: str = "app", label: str | None = None, url: str | None = None) -> str:
    """Chicago author-date style."""
    full_url = url or APP_URL
    accessed = date.today().strftime("%B %d, %Y")
    return (
        f"Fresco, Jossi. {YEAR}. \"{APP_TITLE}{_resource_label(view_type, label)}.\" "
        f"Version {VERSION}. https://doi.org/{DOI}. Accessed {accessed}. {full_url}."
    )


def mla(view_type: str = "app", label: str | None = None, url: str | None = None) -> str:
    """MLA 9th edition."""
    full_url = url or APP_URL
    accessed = date.today().strftime("%d %b %Y")
    return (
        f"Fresco, Jossi. \"{APP_TITLE}{_resource_label(view_type, label)}.\" "
        f"Version {VERSION}, {YEAR}, doi.org/{DOI}. Accessed {accessed}."
    )


def apa(view_type: str = "app", label: str | None = None, url: str | None = None) -> str:
    """APA 7th edition."""
    return (
        f"Fresco, J. ({YEAR}). {APP_TITLE}{_resource_label(view_type, label)} "
        f"(Version {VERSION}) [Computer software]. Zenodo. https://doi.org/{DOI}"
    )


def sbl(view_type: str = "app", label: str | None = None, url: str | None = None) -> str:
    """Society of Biblical Literature style."""
    accessed = date.today().strftime("%B %d, %Y")
    return (
        f"Fresco, Jossi. {APP_TITLE}{_resource_label(view_type, label)}. "
        f"Version {VERSION}. {YEAR}. https://doi.org/{DOI}. Accessed {accessed}."
    )


def all_styles(view_type: str = "app", label: str | None = None, url: str | None = None) -> dict:
    """Return all 5 citation styles for the given view."""
    return {
        "bibtex": bibtex(view_type, label, url),
        "chicago": chicago(view_type, label, url),
        "mla": mla(view_type, label, url),
        "apa": apa(view_type, label, url),
        "sbl": sbl(view_type, label, url),
    }


def metadata() -> dict:
    """Return the citation metadata baseline as a dict (used in API responses)."""
    return {
        "author": AUTHOR_FULL,
        "orcid": ORCID,
        "orcid_url": ORCID_URL,
        "doi": DOI,
        "doi_url": DOI_URL,
        "title": APP_TITLE,
        "version": VERSION,
        "year": YEAR,
        "url": APP_URL,
        "repo": REPO_URL,
    }
