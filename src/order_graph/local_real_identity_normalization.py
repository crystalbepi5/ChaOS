"""Deterministic local-real identity normalization helpers.

These helpers turn imported domain-like values into visible identity evidence for
future local-real resolution work. They do not merge records, create entities, or
modify adapter output.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
from urllib.parse import urlparse

JsonObject = dict[str, Any]


@dataclass(frozen=True)
class DomainNormalizationEvidence:
    """Inspectable normalization result for one imported domain value."""

    input_domain: str | None
    normalized_domain: str | None
    status: str
    warnings: list[str]
    allowed_use: list[str]


def _has_valid_domain_shape(host: str) -> bool:
    """Return True for a simple host shape suitable for local identity evidence."""

    if not host or "." not in host or " " in host:
        return False

    labels = host.split(".")
    if any(not label for label in labels):
        return False

    for label in labels:
        if label.startswith("-") or label.endswith("-"):
            return False
        if not all(character.isalnum() or character == "-" for character in label):
            return False

    return True


def normalize_local_real_domain(input_domain: str | None) -> DomainNormalizationEvidence:
    """Normalize one imported local-real domain value as future identity evidence."""

    if input_domain is None:
        return DomainNormalizationEvidence(
            input_domain=input_domain,
            normalized_domain=None,
            status="missing_domain_unresolved_candidate",
            warnings=["domain_missing"],
            allowed_use=["warning", "human_review"],
        )

    candidate = input_domain.strip()
    if not candidate:
        return DomainNormalizationEvidence(
            input_domain=input_domain,
            normalized_domain=None,
            status="missing_domain_unresolved_candidate",
            warnings=["domain_missing"],
            allowed_use=["warning", "human_review"],
        )

    lowered = candidate.lower()
    if " " in lowered:
        return DomainNormalizationEvidence(
            input_domain=input_domain,
            normalized_domain=None,
            status="malformed_domain_unresolved_candidate",
            warnings=["domain_malformed"],
            allowed_use=["warning", "human_review"],
        )

    parse_candidate = lowered if "://" in lowered else f"//{lowered}"
    parsed = urlparse(parse_candidate)
    host = (parsed.netloc or parsed.path.split("/", 1)[0]).split(":", 1)[0].strip(".")

    if host.startswith("www."):
        host = host[4:]

    if not _has_valid_domain_shape(host):
        status = "not_enough_domain_evidence_unresolved_candidate" if host and "." not in host else "malformed_domain_unresolved_candidate"
        warning = "domain_not_enough_evidence" if status.startswith("not_enough") else "domain_malformed"
        return DomainNormalizationEvidence(
            input_domain=input_domain,
            normalized_domain=None,
            status=status,
            warnings=[warning],
            allowed_use=["warning", "human_review"],
        )

    warnings: list[str] = []
    if parsed.path and parsed.path not in (host, f"www.{host}"):
        warnings.append("domain_path_ignored_for_identity_evidence")

    return DomainNormalizationEvidence(
        input_domain=input_domain,
        normalized_domain=host,
        status="normalizable_with_warning" if warnings else "normalizable",
        warnings=warnings,
        allowed_use=["future_identity_resolution_evidence", *(["warning"] if warnings else [])],
    )


def normalize_local_real_domain_as_dict(input_domain: str | None) -> JsonObject:
    """Return a JSON-friendly normalization result."""

    return asdict(normalize_local_real_domain(input_domain))


def verify_identity_normalization_cases(fixture: JsonObject) -> JsonObject:
    """Verify approved fixture expectations against the deterministic helper."""

    cases = fixture.get("cases", [])
    if not isinstance(cases, list):
        raise ValueError("Identity normalization fixture must contain cases as a list")

    failures: list[JsonObject] = []
    checked_cases: list[JsonObject] = []

    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Identity normalization fixture cases must be objects")

        evidence = normalize_local_real_domain(case.get("input_domain"))
        expected_domain = case.get("expected_normalized_domain")
        expected_status = case.get("expected_status")
        passed = evidence.normalized_domain == expected_domain and evidence.status == expected_status

        checked_case = {
            "case_id": case.get("case_id"),
            "input_domain": case.get("input_domain"),
            "expected_normalized_domain": expected_domain,
            "actual_normalized_domain": evidence.normalized_domain,
            "expected_status": expected_status,
            "actual_status": evidence.status,
            "passed": passed,
        }
        checked_cases.append(checked_case)

        if not passed:
            failures.append(checked_case)

    return {
        "verification": "local_real_identity_normalization_cases",
        "status": "passed" if not failures else "failed",
        "case_count": len(checked_cases),
        "failed_case_count": len(failures),
        "checked_cases": checked_cases,
        "failures": failures,
        "boundaries": [
            "This verification checks normalization expectations only.",
            "This verification does not perform identity resolution.",
            "This verification does not create entities or graph outputs.",
        ],
    }
