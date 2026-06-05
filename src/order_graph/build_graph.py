"""Deterministic local builder skeleton for Order Graph GTM fixtures.

This module proves only this spine:

    local fake fixtures -> deterministic local output files

It does not perform real identity resolution, signal attachment, state
computation, enrichment, API access, LLM calls, database writes, or autonomous
actions.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import BuildPaths, BuildSummary, FixtureBundle, JsonObject

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "examples" / "order-graph" / "gtm"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "outputs" / "order-graph" / "gtm"

INPUT_FILES = {
    "source_records": "source-records.json",
    "signals": "signals.json",
    "expected_entities": "expected-entities.json",
    "expected_signal_links": "expected-signal-links.json",
    "expected_entity_states": "expected-entity-states.json",
}

OUTPUT_FILES = {
    "entities": "entities.json",
    "signal_links": "signal-links.json",
    "entity_states": "entity-states.json",
    "build_summary": "build-summary.json",
}

SKELETON_WARNINGS = [
    "Skeleton mode projects expected fixture files into local outputs.",
    "No real identity resolution is performed.",
    "No signal attachment logic is performed.",
    "No entity state computation is performed.",
    "No external APIs, LLMs, databases, credentials, integrations, UI, agents, or deployment work are used.",
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
    """Load the fake GTM fixture bundle required by this skeleton."""

    return FixtureBundle(
        source_records=load_json(input_dir / INPUT_FILES["source_records"]),
        signals=load_json(input_dir / INPUT_FILES["signals"]),
        expected_entities=load_json(input_dir / INPUT_FILES["expected_entities"]),
        expected_signal_links=load_json(input_dir / INPUT_FILES["expected_signal_links"]),
        expected_entity_states=load_json(input_dir / INPUT_FILES["expected_entity_states"]),
    )


def project_entities(expected_entities: JsonObject) -> JsonObject:
    """Project expected entity fixture data into skeleton output shape."""

    return {
        "builder_mode": "skeleton",
        "source_fixture": INPUT_FILES["expected_entities"],
        "warning": "Projected expected entities only; no identity resolution was performed.",
        "fixture_set": expected_entities.get("fixture_set"),
        "canonical_entities": expected_entities.get("canonical_entities", []),
        "unresolved_source_records": expected_entities.get("unresolved_source_records", []),
        "explicit_non_merges": expected_entities.get("explicit_non_merges", []),
    }


def project_signal_links(expected_signal_links: JsonObject) -> JsonObject:
    """Project expected signal-link fixture data into skeleton output shape."""

    return {
        "builder_mode": "skeleton",
        "source_fixture": INPUT_FILES["expected_signal_links"],
        "warning": "Projected expected signal links only; no signal attachment logic was performed.",
        "fixture_set": expected_signal_links.get("fixture_set"),
        "storage_model_principle": expected_signal_links.get("storage_model_principle", []),
        "expected_signal_links": expected_signal_links.get("expected_signal_links", []),
        "expected_no_duplicate_signals": expected_signal_links.get("expected_no_duplicate_signals", []),
    }


def project_entity_states(expected_entity_states: JsonObject) -> JsonObject:
    """Project expected entity-state fixture data into skeleton output shape."""

    return {
        "builder_mode": "skeleton",
        "source_fixture": INPUT_FILES["expected_entity_states"],
        "warning": "Projected expected entity states only; no state computation was performed.",
        "fixture_set": expected_entity_states.get("fixture_set"),
        "expected_entity_states": expected_entity_states.get("expected_entity_states", []),
        "expected_top_10_fixture_preview": expected_entity_states.get("expected_top_10_fixture_preview", []),
        "explicit_state_guardrails": expected_entity_states.get("explicit_state_guardrails", []),
    }


def count_unresolved_records(expected_entities: JsonObject) -> int:
    """Count unresolved source record identifiers from expected fixture data."""

    unresolved_cases = expected_entities.get("unresolved_source_records", [])
    count = 0
    for unresolved_case in unresolved_cases:
        if isinstance(unresolved_case, dict):
            source_record_ids = unresolved_case.get("source_record_ids", [])
            if isinstance(source_record_ids, list):
                count += len(source_record_ids)
    return count


def make_build_summary(paths: BuildPaths, fixtures: FixtureBundle) -> BuildSummary:
    """Create a deterministic skeleton build summary."""

    return BuildSummary(
        builder_mode="skeleton",
        source_record_count=len(fixtures.source_records.get("source_records", [])),
        signal_count=len(fixtures.signals.get("signals", [])),
        expected_entity_count=len(fixtures.expected_entities.get("canonical_entities", [])),
        expected_signal_link_count=len(fixtures.expected_signal_links.get("expected_signal_links", [])),
        expected_entity_state_count=len(fixtures.expected_entity_states.get("expected_entity_states", [])),
        unresolved_record_count=count_unresolved_records(fixtures.expected_entities),
        input_dir=str(paths.input_dir.as_posix()),
        output_dir=str(paths.output_dir.as_posix()),
        output_files=[
            OUTPUT_FILES["entities"],
            OUTPUT_FILES["signal_links"],
            OUTPUT_FILES["entity_states"],
            OUTPUT_FILES["build_summary"],
        ],
        warnings=SKELETON_WARNINGS,
    )


def build_graph_from_fixtures(
    input_dir: Path = DEFAULT_INPUT_DIR,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> BuildSummary:
    """Read fake fixtures and write deterministic local skeleton outputs."""

    paths = BuildPaths(input_dir=input_dir, output_dir=output_dir)
    fixtures = load_fixture_bundle(paths.input_dir)

    write_json(
        paths.output_dir / OUTPUT_FILES["entities"],
        project_entities(fixtures.expected_entities),
    )
    write_json(
        paths.output_dir / OUTPUT_FILES["signal_links"],
        project_signal_links(fixtures.expected_signal_links),
    )
    write_json(
        paths.output_dir / OUTPUT_FILES["entity_states"],
        project_entity_states(fixtures.expected_entity_states),
    )

    summary = make_build_summary(paths, fixtures)
    write_json(paths.output_dir / OUTPUT_FILES["build_summary"], asdict(summary))
    return summary


def main() -> None:
    """Run the skeleton builder from the repository root."""

    summary = build_graph_from_fixtures()
    print(json.dumps(asdict(summary), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
