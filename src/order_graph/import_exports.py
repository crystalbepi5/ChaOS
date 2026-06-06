"""Local CSV-to-SourceRecord adapter skeleton.

This module reads a local CSV file plus local mapping/classification examples
and writes adapter-shaped JSON outputs. It must not read real source systems,
call external APIs, use LLM classification, or ingest restricted, excluded, or
unknown field values.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from .export_mapping import (
    decide_field,
    required_mapping_fields,
    set_target_value,
    source_metadata,
)
from .models import JsonObject

OUTPUT_FILES = {
    "source_records": "source-records.json",
    "import_summary": "import-summary.json",
    "mapping_warnings": "mapping-warnings.json",
}

ADAPTER_WARNINGS = [
    "This adapter reads local CSV files only.",
    "This adapter is a skeleton for fake or sanitized local exports.",
    "This adapter must not be used with real customer data committed to the repository.",
    "This adapter does not call external APIs, LLMs, databases, live integrations, UI, agents, CRM writes, outreach actions, or deployment systems.",
]


def load_json(path: Path) -> JsonObject:
    """Load a local JSON object."""

    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object at {path}")
    return data


def write_json(path: Path, data: Any) -> None:
    """Write deterministic, human-readable JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> list[JsonObject]:
    """Read local CSV rows as dictionaries."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def import_csv_exports(
    csv_path: Path,
    mapping_path: Path,
    classification_path: Path,
    output_dir: Path,
) -> JsonObject:
    """Read local export CSV and write SourceRecord-shaped outputs."""

    mapping_config = load_json(mapping_path)
    classification_config = load_json(classification_path)
    rows = read_csv_rows(csv_path)

    source_records, warnings = build_source_records(
        rows=rows,
        csv_path=csv_path,
        mapping_config=mapping_config,
        classification_config=classification_config,
    )
    summary = build_import_summary(
        csv_path=csv_path,
        mapping_path=mapping_path,
        classification_path=classification_path,
        output_dir=output_dir,
        mapping_config=mapping_config,
        classification_config=classification_config,
        source_records=source_records,
        warnings=warnings,
        row_count=len(rows),
    )
    warning_output = build_mapping_warnings(warnings)

    write_json(output_dir / OUTPUT_FILES["source_records"], source_records)
    write_json(output_dir / OUTPUT_FILES["import_summary"], summary)
    write_json(output_dir / OUTPUT_FILES["mapping_warnings"], warning_output)

    return summary


def build_source_records(
    rows: list[JsonObject],
    csv_path: Path,
    mapping_config: JsonObject,
    classification_config: JsonObject,
) -> tuple[JsonObject, list[JsonObject]]:
    """Build SourceRecord-shaped output and warning records."""

    metadata = source_metadata(mapping_config, classification_config)
    required_fields = required_mapping_fields(mapping_config)
    source_records = []
    warnings = []

    for row_index, row in enumerate(rows, start=1):
        source_record: JsonObject = {
            "source_record_id": _source_record_id(metadata, row_index, row),
            "source_system": metadata.get("source_system"),
            "source_object_type": metadata.get("source_object_type"),
            "source_native_id": None,
            "raw_values": {},
            "normalized_values": {},
            "derived_values": {},
            "context_values": {},
            "source_reference": {
                "source_file": csv_path.as_posix(),
                "row_number": row_index,
            },
            "status": "mapped_from_local_csv",
            "adapter_boundary": "local_csv_skeleton_no_external_systems",
        }

        for field in required_fields:
            if not _has_value(row.get(field)):
                warnings.append(_warning(row_index, "required_field_missing", field))
                if field == "AccountId":
                    source_record["status"] = "incomplete_required_field_missing"

        for field_name, value in row.items():
            if not _has_value(value):
                continue
            decision = decide_field(field_name, classification_config, mapping_config)
            if decision.value_handling != "ingest_value":
                warnings.append(_warning(row_index, decision.warning_type or "field_blocked", field_name))
                continue
            if decision.target_path:
                set_target_value(source_record, decision.target_path, value)

        native_id = source_record.get("native_id")
        if native_id:
            source_record["source_native_id"] = native_id
            del source_record["native_id"]

        source_record["field_classification_summary"] = _field_classification_summary(
            row,
            classification_config,
            mapping_config,
        )
        source_records.append(source_record)

    return (
        {
            "builder_mode": "csv_to_source_record_adapter_skeleton",
            "source_records": source_records,
            "record_count": len(source_records),
            "warnings": ADAPTER_WARNINGS,
        },
        warnings,
    )


def build_import_summary(
    csv_path: Path,
    mapping_path: Path,
    classification_path: Path,
    output_dir: Path,
    mapping_config: JsonObject,
    classification_config: JsonObject,
    source_records: JsonObject,
    warnings: list[JsonObject],
    row_count: int,
) -> JsonObject:
    """Build deterministic import summary output."""

    metadata = source_metadata(mapping_config, classification_config)
    warning_types = sorted({str(warning.get("warning_type")) for warning in warnings})
    return {
        "builder_mode": "csv_to_source_record_adapter_skeleton",
        "adapter_status": "completed_local_skeleton_run",
        "source_csv": csv_path.as_posix(),
        "mapping_config": mapping_path.as_posix(),
        "classification_config": classification_path.as_posix(),
        "output_dir": output_dir.as_posix(),
        "source_system": metadata.get("source_system"),
        "source_object_type": metadata.get("source_object_type"),
        "target_object": metadata.get("target_object"),
        "row_count": row_count,
        "source_record_count": int(source_records.get("record_count", 0)),
        "mapping_warning_count": len(warnings),
        "mapping_warning_types": warning_types,
        "output_files": [
            OUTPUT_FILES["source_records"],
            OUTPUT_FILES["import_summary"],
            OUTPUT_FILES["mapping_warnings"],
        ],
        "boundaries": [
            "local_csv_only",
            "fake_or_sanitized_exports_only",
            "no_live_integrations",
            "no_real_customer_data_committed",
            "no_llm_classification",
            "no_agents",
            "no_ui",
            "no_crm_writes",
            "no_outreach_actions",
        ],
        "warnings": ADAPTER_WARNINGS,
    }


def build_mapping_warnings(warnings: list[JsonObject]) -> JsonObject:
    """Build mapping warning output without restricted or excluded values."""

    return {
        "builder_mode": "csv_to_source_record_adapter_skeleton",
        "warning_count": len(warnings),
        "warnings": sorted(
            warnings,
            key=lambda item: (
                int(item.get("row_number", 0)),
                str(item.get("field_name")),
                str(item.get("warning_type")),
            ),
        ),
        "value_policy": [
            "Warnings may include safe field names.",
            "Warnings must not include restricted, excluded, or unknown field values.",
            "SourceRecords must not include excluded field values.",
        ],
    }


def _source_record_id(metadata: JsonObject, row_index: int, row: JsonObject) -> str:
    native_id = str(row.get("AccountId") or row.get("source_native_id") or row_index)
    source_system = _slug(str(metadata.get("source_system") or "unknown_source"))
    source_object = _slug(str(metadata.get("source_object_type") or "unknown_object"))
    return f"sr_import_{source_system}_{source_object}_{_slug(native_id)}"


def _field_classification_summary(
    row: JsonObject,
    classification_config: JsonObject,
    mapping_config: JsonObject,
) -> JsonObject:
    """Summarize only fields whose values were approved for ingestion."""

    summary: JsonObject = {}
    for field_name, value in row.items():
        if not _has_value(value):
            continue
        decision = decide_field(field_name, classification_config, mapping_config)
        if decision.value_handling == "ingest_value":
            summary[field_name] = decision.classification
    return summary


def _warning(row_number: int, warning_type: str, field_name: str) -> JsonObject:
    return {
        "row_number": row_number,
        "warning_type": warning_type,
        "field_name": field_name,
        "value_included": False,
    }


def _has_value(value: object) -> bool:
    return value is not None and str(value).strip() != ""


def _slug(value: str) -> str:
    chars = []
    for char in value.lower():
        if char.isalnum():
            chars.append(char)
        elif chars and chars[-1] != "_":
            chars.append("_")
    return "".join(chars).strip("_") or "unknown"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Local CSV-to-SourceRecord adapter skeleton.")
    parser.add_argument("--csv", required=True, type=Path, help="Local fake or sanitized CSV export path.")
    parser.add_argument("--mapping", required=True, type=Path, help="Local field mapping JSON path.")
    parser.add_argument("--classification", required=True, type=Path, help="Local field classification JSON path.")
    parser.add_argument("--output", required=True, type=Path, help="Output directory for adapter-shaped JSON files.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary = import_csv_exports(
        csv_path=args.csv,
        mapping_path=args.mapping,
        classification_path=args.classification,
        output_dir=args.output,
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
