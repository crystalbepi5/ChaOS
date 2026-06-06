"""Mapping helpers for local CSV export adapter skeleton.

These helpers interpret local mapping and classification examples. They must not
connect to source systems, classify fields with an LLM, or ingest restricted,
excluded, or unknown field values.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .models import JsonObject

INGESTIBLE_REVIEW_STATUS = "approved_for_local_ingestion"
BLOCKED_CLASSIFICATIONS = {
    "restricted",
    "excluded",
    "unknown_needs_review",
}


@dataclass(frozen=True)
class FieldDecision:
    """Resolved classification and mapping decision for one source field."""

    field_name: str
    classification: str
    review_status: str
    target_path: str | None
    value_handling: str
    warning_type: str | None
    reason: str


def field_classifications_by_name(classification_config: JsonObject) -> dict[str, JsonObject]:
    """Return classification entries keyed by source field name."""

    classifications = {}
    for entry in classification_config.get("field_classifications", []):
        if isinstance(entry, dict) and entry.get("field_name"):
            classifications[str(entry["field_name"])] = entry
    return classifications


def field_mappings_by_name(mapping_config: JsonObject) -> dict[str, JsonObject]:
    """Return mapping entries keyed by source field name."""

    mappings = {}
    for entry in mapping_config.get("field_mappings", []):
        if isinstance(entry, dict) and entry.get("source_field"):
            mappings[str(entry["source_field"])] = entry
    return mappings


def decide_field(
    field_name: str,
    classification_config: JsonObject,
    mapping_config: JsonObject,
) -> FieldDecision:
    """Decide whether a field value may be mapped into a SourceRecord."""

    classifications = field_classifications_by_name(classification_config)
    mappings = field_mappings_by_name(mapping_config)
    classification_entry = classifications.get(field_name)
    mapping_entry = mappings.get(field_name)

    if classification_entry is None:
        return FieldDecision(
            field_name=field_name,
            classification="unknown_needs_review",
            review_status="blocked_pending_review",
            target_path=None,
            value_handling="do_not_ingest_value",
            warning_type="unknown_field_not_classified",
            reason="Field is not present in the classification config.",
        )

    classification = str(classification_entry.get("primary_classification", "unknown_needs_review"))
    review_status = str(classification_entry.get("review_status", "blocked_pending_review"))

    if classification in BLOCKED_CLASSIFICATIONS:
        return FieldDecision(
            field_name=field_name,
            classification=classification,
            review_status=review_status,
            target_path=None,
            value_handling="do_not_ingest_value",
            warning_type=f"{classification}_field_blocked",
            reason="Field classification prohibits value ingestion.",
        )

    if review_status != INGESTIBLE_REVIEW_STATUS:
        return FieldDecision(
            field_name=field_name,
            classification=classification,
            review_status=review_status,
            target_path=None,
            value_handling="do_not_ingest_value",
            warning_type="field_not_approved_for_ingestion",
            reason="Field review status is not approved for local ingestion.",
        )

    if mapping_entry is None:
        return FieldDecision(
            field_name=field_name,
            classification=classification,
            review_status=review_status,
            target_path=None,
            value_handling="do_not_ingest_value",
            warning_type="classified_field_has_no_mapping",
            reason="Field is classified but has no target mapping.",
        )

    return FieldDecision(
        field_name=field_name,
        classification=classification,
        review_status=review_status,
        target_path=str(mapping_entry.get("target_path")),
        value_handling="ingest_value",
        warning_type=None,
        reason="Field is classified, approved, and mapped.",
    )


def required_mapping_fields(mapping_config: JsonObject) -> list[str]:
    """Return source fields marked required by the mapping example."""

    fields = []
    for entry in mapping_config.get("field_mappings", []):
        if isinstance(entry, dict) and entry.get("required") is True and entry.get("source_field"):
            fields.append(str(entry["source_field"]))
    return fields


def source_metadata(mapping_config: JsonObject, classification_config: JsonObject) -> JsonObject:
    """Return source metadata with mapping config taking precedence."""

    return {
        "source_system": mapping_config.get("source_system") or classification_config.get("source_system"),
        "source_object_type": mapping_config.get("source_object_type") or classification_config.get("source_object_type"),
        "target_object": mapping_config.get("target_object", "SourceRecord"),
        "mapping_status": mapping_config.get("status"),
        "classification_status": classification_config.get("status"),
    }


def set_target_value(target: JsonObject, target_path: str, value: Any) -> None:
    """Set a dotted target path in a SourceRecord-shaped object."""

    if not target_path.startswith("source_record."):
        return

    path_parts = target_path.split(".")[1:]
    current = target
    for part in path_parts[:-1]:
        existing = current.get(part)
        if not isinstance(existing, dict):
            existing = {}
            current[part] = existing
        current = existing
    current[path_parts[-1]] = value
