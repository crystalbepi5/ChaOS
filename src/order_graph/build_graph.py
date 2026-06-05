"""Deterministic local builder for Order Graph GTM fixtures.

This module proves this spine:

    local fake fixtures -> deterministic local output files

This PR adds the first deterministic top-10 account workflow from generated
entity states and local validation evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .entity_state import compute_entity_states
from .identity import resolve_entities_from_source_records
from .models import BuildPaths, BuildSummary, FixtureBundle, JsonObject
from .signal_attachment import generate_signal_links
from .top_10_workflow import generate_top_10_account_workflow
from .validation_report import generate_validation_report

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "examples" / "order-graph" / "gtm"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "outputs" / "order-graph" / "gtm"

INPUT_FILES = {
    "source_records": "source-records.json",
    "signals": "signals.json",
}

OUTPUT_FILES = {
    "entities": "entities.json",
    "signal_links": "signal-links.json",
    "entity_states": "entity-states.json",
    "validation_report": "validation-report.json",
    "top_10_accounts": "top-10-accounts.json",
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
    "No numeric scoring or hidden weighting is used for entity state.",
    "No outreach automation, CRM writes, external APIs, LLMs, databases, credentials, integrations, UI, agents, or deployment work are used.",
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
) -> BuildSummary:
    """Create a deterministic local build summary."""

    return BuildSummary(
        builder_mode="entity_state_computation",
        source_record_count=len(fixtures.source_records.get("source_records", [])),
        signal_count=len(fixtures.signals.get("signals", [])),
        resolved_entity_count=len(entities_output.get("canonical_entities", [])),
        unresolved_record_count=count_unresolved_records(entities_output),
        generated_signal_link_count=len(signal_links_output.get("generated_signal_links", [])),
        generated_entity_state_count=len(entity_states_output.get("computed_entity_states", [])),
        validation_check_count=int(validation_report_output.get("check_count", 0)),
        failed_validation_check_count=int(validation_report_output.get("failed_check_count", 0)),
        top_10_recommendation_count=int(top_10_output.get("recommendation_count", 0)),
        input_dir=str(paths.input_dir.as_posix()),
        output_dir=str(paths.output_dir.as_posix()),
        output_files=[
            OUTPUT_FILES["entities"],
            OUTPUT_FILES["signal_links"],
            OUTPUT_FILES["entity_states"],
            OUTPUT_FILES["validation_report"],
            OUTPUT_FILES["top_10_accounts"],
            OUTPUT_FILES["build_summary"],
        ],
        warnings=BUILD_WARNINGS,
    )


def build_graph_from_fixtures(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> BuildSummary:
    """Read fake fixtures and write deterministic local outputs."""

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

    write_json(paths.output_dir / OUTPUT_FILES["entities"], entities_output)
    write_json(paths.output_dir / OUTPUT_FILES["signal_links"], signal_links_output)
    write_json(paths.output_dir / OUTPUT_FILES["entity_states"], entity_states_output)
    write_json(paths.output_dir / OUTPUT_FILES["validation_report"], validation_report_output)
    write_json(paths.output_dir / OUTPUT_FILES["top_10_accounts"], top_10_output)

    summary = make_build_summary(
        paths,
        fixtures,
        entities_output,
        signal_links_output,
        entity_states_output,
        validation_report_output,
        top_10_output,
    )
    write_json(paths.output_dir / OUTPUT_FILES["build_summary"], asdict(summary))
    return summary


def main() -> None:
    """Run the local builder from the repository root."""

    summary = build_graph_from_fixtures()
    print(json.dumps(asdict(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
