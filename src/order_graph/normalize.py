"""Tiny normalization helpers for future deterministic Order Graph logic.

These helpers are intentionally small. They must not become identity resolution,
fuzzy matching, enrichment, or vendor-specific business logic in this PR.
"""

from __future__ import annotations

import re
from urllib.parse import urlparse

_COMPANY_SUFFIXES = (
    "corporation",
    "corp",
    "incorporated",
    "inc",
    "limited",
    "ltd",
    "llc",
)


def normalize_domain(value: str | None) -> str | None:
    """Return a lower-case host without protocol, path, port, or leading www."""

    if not value:
        return None

    candidate = value.strip().lower()
    if not candidate:
        return None

    if "://" not in candidate:
        candidate = f"//{candidate}"

    parsed = urlparse(candidate)
    host = parsed.netloc or parsed.path.split("/", 1)[0]
    host = host.split(":", 1)[0].strip(".")

    if host.startswith("www."):
        host = host[4:]

    return host or None


def normalize_email(value: str | None) -> str | None:
    """Return a lower-case email string, or None for blank input."""

    if not value:
        return None

    normalized = value.strip().lower()
    return normalized or None


def normalize_company_name(value: str | None) -> str | None:
    """Return a simple normalized company name for fixture readability only."""

    if not value:
        return None

    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9\s]", " ", normalized)
    words = [word for word in normalized.split() if word not in _COMPANY_SUFFIXES]
    return " ".join(words) or None
