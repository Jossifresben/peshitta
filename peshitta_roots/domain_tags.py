"""Cognate domain tagging — schema, validation, and display helpers.

A `domain` field on each cognate tags it with one of 6 fixed values that
operationalize the editorial preference for concrete material vocabulary
over religious / abstract glosses (a principle articulated on the
methodology page).

The domain field is OPTIONAL on every cognate dict — older entries that
lack it sort between abstract and religious in the default UI order.
"""

VALID_DOMAINS = {
    "material",   # agriculture, livestock, commerce, utensils, tools, body, food
    "religious",  # devotional, cultic, theological, liturgical
    "nature",     # weather, geography, animals (non-pastoral), plants, celestial
    "kinship",    # family relations, tribe, social bonds
    "abstract",   # mental / moral abstractions when used non-religiously
    "neutral",    # catch-all when no other category fits cleanly
}

# Display order for the Visualizer Root Card cognate tables.
# Material first (most stable across the Semitic field), religious last
# (most theologically distorted). Untagged cognates sort just before
# religious so they remain visible without claiming a domain they may
# not actually have.
_DOMAIN_PRIORITY = {
    "material": 0,
    "nature": 1,
    "kinship": 2,
    "abstract": 3,
    None: 4,        # untagged
    "neutral": 4,   # explicitly neutral sorts with untagged
    "religious": 5,
}


def validate_domain(value) -> bool:
    """Return True if the value is one of the 6 valid domain strings."""
    return isinstance(value, str) and value in VALID_DOMAINS


def domain_priority(domain) -> int:
    """Sort key for a domain value (lower = displayed first)."""
    return _DOMAIN_PRIORITY.get(domain, _DOMAIN_PRIORITY[None])


def sort_cognates_by_domain(cognates):
    """Return cognates sorted by the editorial domain priority.

    Material > nature > kinship > abstract > untagged/neutral > religious.
    Stable within each domain (preserves the input order of equal-priority items).
    """
    return sorted(
        cognates,
        key=lambda c: domain_priority(c.get("domain") if isinstance(c, dict) else None),
    )
