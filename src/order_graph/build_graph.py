"""Deterministic local builder for Order Graph fixtures.

This module proves this spine:

    local fake fixtures -> deterministic local output files

The default path builds the fake GTM graph fixture. The imported SourceRecord
path consumes adapter-shaped SourceRecords, writes a local handoff output, writes
derived normalization evidence, and validates that boundary; it does not expand
imported records into graph entities yet.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Literal

from .entity_state import compute_entity_states
from .human_feedback_validation import generate_human_feedback_validation_report
from .human_review import generate_human_review_override_model
from .identity import resolve_entities_from_source_records
from .local_real_identity_normalization import normalize_local_real_domain_as_dict
from .local_real_normalization_validation import generate_local_real_normalization_validation_report
from .models import BuildPaths, BuildSummary, FixtureBundle, JsonObject
from .signal_attachment import generate_signal_links
from .top_10_workflow import generate_top_10_account_workflow
from .validation_report import generate_validation_report

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "examples" / "order-graph" / "gtm"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "outputs" / "order-graph" / "gtm"
DEFAULT_LOCAL_REAL_INPUT_DIR = REPO_ROOT / "examples" / "order-graph" / "local-real"
DEFAULT_LOCAL_REAL_OUTPUT_DIR = REPO_ROOT / "outputs" / "order-graph" / "local-real"

BuildMode = Literal["auto", "gtm", "imported-source-records"]

INPUT_FILES = {
    "source_records": "source-records.json",
    "signals": "signals.json",
    "imported_source_records": "expected-source-records.json",
}

OUTPUT_FILES = {
    "source_records": "source-records.json",
    "identity_normalization_evidence": "identity-normalization-evidence.json",
    "identity_normalization_validation": "identity-normalization-validation.json",
    "entities": "entities.json",
    "signal_links": "signal-links.json",
    "entity_states": "entity-states.json",
    "validation_report": "validation-report.json",
    "top_10_accounts": "top-10-accounts.json",
    "human_review_overrides": "human-review-overrides.json",
    "human_feedback_validation": "human-feedback-validation.json",
    "build_summary": "build-summary.json",
}

BUILD_WARNINGS = [
    "Identity resolution uses strong deterministic fixture keys only.",
    "Account-like records merge by canonical domain only.",
    "Contact-like records merge by normalized email only.",
    "Missing-domain account-like records remain unresolved.",
    "Signal links are generated from local signals and resolved entities.",
    "Entity states are generated from resolved entities, signal links, and local fixture evidence.",
    "Validation reports are generated from local outputs only.",
    "Top-10 account recommendations are generated for human review only.",
    "Human review override examples are generated as local feedback records only.",
    "Human feedback validation checks are generated from local review examples only.",
    "No numeric scoring or hidden weighting is used for entity state.",
    "No outreach automation, CRM writes, external APIs, LLMs, databases, credentials, integrations, UI, agents, or deployment work are used.",
]

IMPORTED_SOURCE_RECORD_WARNINGS = [
    "Imported SourceRecords are consumed from local fake or sanitized adapter output only.",
    "Imported SourceRecords are not expanded into entities, signal links, entity states, recommendations, or human review records in this mode.",
    "The local-real fixture has no approved signal fixture or graph expectations yet.",
    "Domain values are preserved exactly as imported; identity normalization evidence is written separately.",
    "Identity normalization evidence does not approve entity merging or account-name-only matching.",
    "No real customer data, live integrations, CRM writes, external APIs, LLMs, databases, credentials, UI, agents, or deployment work are used.",
]


def load_json(path: Path) -> JsonObject:
    """Load one local JSON object from a fixture file."""

    with path.open("r", encoding="utf-8") as handle:
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


def load_fixture_bundle(input_dir: Path) -> FixtureBundle:
    """Load the fake GTM fixture bundle required by the local builder."""

    return FixtureBundle(
        source_records=load_json(input_dir / INPUT_FILES["source_records"]),
        signals=load_json(input_dir / INPUT_FILES["signals"]),
    )


def load_imported_source_records(input_dir: Path) -> JsonObject:
    """Load local adapter-shaped SourceRecords for the import handoff path."""

    imported_output = load_json(input_dir / INPUT_FILES["imported_source_records"])
    source_records = imported_output.get("source_records", [])
    if not isinstance(source_records, list):
        raise ValueError("Imported SourceRecord output must contain source_records as a list")
    return imported_output


def count_unresolved_records(entities_output: JsonObject) -> int:
    """Count unresolved source record identifiers from generated entity output."""

    unresolved_cases = entities_output.get("unresolved_source_records", [])
    count = 0
    for unresolved_case in unresolved_cases:
        if isinstance(unresolved_case, dict):
            source_record_ids = unresolved_case.get("source_record_ids", [])
            if isinstance(source_record_ids, list):
                count += len(source_record_ids)
    return count


def make_build_summary(
    paths: BuildPaths,
    fixtures: FixtureBundle,
    entities_output: JsonObject,
    signal_links_output: JsonObject,
    entity_states_output: JsonObject,
    validation_report_output: JsonObject,
    top_10_output: JsonObject,
    human_review_output: JsonObject,
    human_feedback_validation_output: JsonObject,
) -> BuildSummary:
    """Create a deterministic local build summary."""

    return BuildSummary(
        builder_mode="human_feedback_validation_report",
        source_record_count=len(fixtures.source_records.get("source_records", [])),
        signal_count=len(fixtures.signals.get("signals", [])),
        resolved_entity_count=len(entities_output.get("canonical_entities", [])),
        unresolved_record_count=count_unresolved_records(entities_output),
        generated_signal_link_count=len(signal_links_output.get("generated_signal_links", [])),
        generated_entity_state_count=len(entity_states_output.get("computed_entity_states", [])),
        validation_check_count=int(validation_report_output.get("check_count", 0)),
        failed_validation_check_count=int(validation_report_output.get("failed_check_count", 0)),
        top_10_recommendation_count=int(top_10_output.get("recommendation_count", 0)),
        human_review_example_count=int(human_review_output.get("review_example_count", 0)),
        human_feedback_validation_check_count=int(human_feedback_validation_output.get("check_count", 0)),
        failed_human_feedback_validation_check_count=int(human_feedback_validation_output.get("failed_check_count", 0)),
        input_dir=str(paths.input_dir.as_posix()),
        output_dir=str(paths.output_dir.as_posix()),
        output_files=[
            OUTPUT_FILES["entities"],
            OUTPUT_FILES["signal_links"],
            OUTPUT_FILES["entity_states"],
            OUTPUT_FILES["validation_report"],
            OUTPUT_FILES["top_10_accounts"],
            OUTPUT_FILES["human_review_overrides"],
            OUTPUT_FILES["human_feedback_validation"],
            OUTPUT_FILES["build_summary"],
        ],
        warnings=BUILD_WARNINGS,
    )


def make_imported_source_record_summary(
    paths: BuildPaths,
    imported_source_records_output: JsonObject,
    validation_report_output: JsonObject,
) -> BuildSummary:
    """Create a summary for the imported SourceRecord handoff path."""

    return BuildSummary(
        builder_mode="imported_source_records_build_path",
        source_record_count=len(imported_source_records_output.get("source_records", [])),
        signal_count=0,
        resolved_entity_count=0,
        unresolved_record_count=0,
        generated_signal_link_count=0,
        generated_entity_state_count=0,
        validation_check_count=int(validation_report_output.get("check_count", 0)),
        failed_validation_check_count=int(validation_report_output.get("failed_check_count", 0)),
        top_10_recommendation_count=0,
        human_review_example_count=0,
        human_feedback_validation_check_count=0,
        failed_human_feedback_validation_check_count=0,
        input_dir=str(paths.input_dir.as_posix()),
        output_dir=str(paths.output_dir.as_posix()),
        output_files=[
            OUTPUT_FILES["source_records"],
            OUTPUT_FILES["identity_normalization_evidence"],
            OUTPUT_FILES["identity_normalization_validation"],
            OUTPUT_FILES["build_summary"],
        ],
        warnings=IMPORTED_SOURCE_RECORD_WARNINGS,
    )


def build_graph_from_fixtures(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> BuildSummary:
    """Read fake GTM fixtures and write deterministic local graph outputs."""

    paths = BuildPaths(input_dir=input_dir, output_dir=output_dir)
    fixtures = load_fixture_bundle(paths.input_dir)

    entities_output = resolve_entities_from_source_records(fixtures.source_records)
    signal_links_output = generate_signal_links(
        fixtures.signals,
        entities_output,
        fixtures.source_records,
    )
    entity_states_output = compute_entity_states(
        entities_output,
        signal_links_output,
        fixtures.signals,
        fixtures.source_records,
    )
    validation_report_output = generate_validation_report(
        entities_output,
        signal_links_output,
        entity_states_output,
        fixtures.signals,
    )
    top_10_output = generate_top_10_account_workflow(
        entities_output,
        entity_states_output,
        validation_report_output,
    )
    human_review_output = generate_human_review_override_model(top_10_output)
    human_feedback_validation_output = generate_human_feedback_validation_report(
        top_10_output,
        human_review_output,
    )

    write_json(paths.output_dir / OUTPUT_FILES["entities"], entities_output)
    write_json(paths.output_dir / OUTPUT_FILES["signal_links"], signal_links_output)
    write_json(paths.output_dir / OUTPUT_FILES["entity_states"], entity_states_output)
    write_json(paths.output_dir / OUTPUT_FILES["validation_report"], validation_report_output)
    write_json(paths.output_dir / OUTPUT_FILES["top_10_accounts"], top_10_output)
    write_json(paths.output_dir / OUTPUT_FILES["human_review_overrides"], human_review_output)
    write_json(paths.output_dir / OUTPUT_FILES["human_feedback_validation"], human_feedback_validation_output)

    summary = make_build_summary(
        paths,
        fixtures,
        entities_output,
        signal_links_output,
        entity_states_output,
        validation_report_output,
        top_10_output,
        human_review_output,
        human_feedback_validation_output,
    )
    write_json(paths.output_dir / OUTPUT_FILES["build_summary"], asdict(summary))
    return summary


def _imported_domain_value(source_record: JsonObject) -> str | None:
    """Return the adapter-preserved domain value from one imported SourceRecord."""

    normalized_values = source_record.get("normalized_values", {})
    if not isinstance(normalized_values, dict):
        return None

    domain = normalized_values.get("domain")
    if domain is None:
        return None
    return str(domain)


def generate_identity_normalization_evidence(imported_source_records_output: JsonObject) -> JsonObject:
    """Generate visible normalization evidence without resolving identities."""

    evidence_records: list[JsonObject] = []
    for source_record in imported_source_records_output.get("source_records", []):
        if not isinstance(source_record, dict):
            continue

        imported_domain = _imported_domain_value(source_record)
        evidence = normalize_local_real_domain_as_dict(imported_domain)
        evidence_records.append(
            {
                "source_record_id": source_record.get("source_record_id"),
                "source_system": source_record.get("source_system"),
                "source_object_type": source_record.get("source_object_type"),
                "source_native_id": source_record.get("source_native_id"),
                "imported_domain_value": imported_domain,
                "normalization_evidence": evidence,
            }
        )

    return {
        "builder_mode": "local_real_identity_normalization_evidence",
        "source_record_count": len(imported_source_records_output.get("source_records", [])),
        "evidence_record_count": len(evidence_records),
        "normalizable_record_count": sum(
            1
            for evidence_record in evidence_records
            if evidence_record["normalization_evidence"].get("normalized_domain") is not None
        ),
        "unresolved_candidate_count": sum(
            1
            for evidence_record in evidence_records
            if evidence_record["normalization_evidence"].get("normalized_domain") is None
        ),
        "warning_record_count": sum(
            1
            for evidence_record in evidence_records
            if evidence_record["normalization_evidence"].get("warnings")
        ),
        "evidence_records": evidence_records,
        "boundaries": [
            "This output contains derived normalization evidence only.",
            "This output does not change imported SourceRecord values.",
            "This output does not perform identity resolution.",
            "This output does not create entities, signal links, entity states, recommendations, or review records.",
            "Account-name-only matching remains prohibited.",
        ],
    }


def build_from_imported_source_records(
    input_dir: Path = DEFAULT_LOCAL_REAL_INPUT_DIR,
    output_dir: Path = DEFAULT_LOCAL_REAL_OUTPUT_DIR,
) -> BuildSummary:
    """Read local imported SourceRecords and write deterministic handoff outputs."""

    paths = BuildPaths(input_dir=input_dir, output_dir=output_dir)
    imported_output = load_imported_source_records(paths.input_dir)

    source_records_output: JsonObject = {
        "builder_mode": "imported_source_records_build_path",
        "source_input_file": INPUT_FILES["imported_source_records"],
        "source_record_count": len(imported_output.get("source_records", [])),
        "source_records": imported_output.get("source_records", []),
        "warnings": IMPORTED_SOURCE_RECORD_WARNINGS + list(imported_output.get("warnings", [])),
    }
    normalization_evidence_output = generate_identity_normalization_evidence(source_records_output)
    output_files = [
        OUTPUT_FILES["source_records"],
        OUTPUT_FILES["identity_normalization_evidence"],
        OUTPUT_FILES["identity_normalization_validation"],
        OUTPUT_FILES["build_summary"],
    ]
    validation_report_output = generate_local_real_normalization_validation_report(
        source_records_output,
        normalization_evidence_output,
        output_files,
    )

    write_json(paths.output_dir / OUTPUT_FILES["source_records"], source_records_output)
    write_json(paths.output_dir / OUTPUT_FILES["identity_normalization_evidence"], normalization_evidence_output)
    write_json(paths.output_dir / OUTPUT_FILES["identity_normalization_validation"], validation_report_output)
    summary = make_imported_source_record_summary(paths, source_records_output, validation_report_output)
    write_json(paths.output_dir / OUTPUT_FILES["build_summary"], asdict(summary))
    return summary


def resolve_build_mode(input_dir: Path, requested_mode: BuildMode) -> BuildMode:
    """Resolve auto mode from available local fixture files."""

    if requested_mode != "auto":
        return requested_mode

    if (input_dir / INPUT_FILES["source_records"]).exists() and (input_dir / INPUT_FILES["signals"]).exists():
        return "gtm"

    if (input_dir / INPUT_FILES["imported_source_records"]).exists():
        return "imported-source-records"

    raise ValueError(
        "Could not infer build mode. Expected either source-records.json plus signals.json, "
        "or expected-source-records.json."
    )


def parse_args() -> argparse.Namespace:
    """Parse local builder arguments."""

    parser = argparse.ArgumentParser(description="Run the deterministic local Order Graph builder.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_DIR, help="Local input fixture directory.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_DIR, help="Local output directory.")
    parser.add_argument(
        "--mode",
        choices=["auto", "gtm", "imported-source-records"],
        default="auto",
        help="Build mode. Auto chooses GTM fixtures or imported SourceRecords from local files.",
    )
    return parser.parse_args()


def main() -> None:
    """Run the local builder from the repository root."""

    args = parse_args()
    input_dir = args.input.resolve()
    output_dir = args.output.resolve()
    mode = resolve_build_mode(input_dir, args.mode)

    if mode == "gtm":
        summary = build_graph_from_fixtures(input_dir=input_dir, output_dir=output_dir)
    elif mode == "imported-source-records":
        summary = build_from_imported_source_records(input_dir=input_dir, output_dir=output_dir)
    else:
        raise ValueError(f"Unsupported build mode: {mode}")

    print(json.dumps(asdict(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
