"""Small data containers for the Order Graph builder skeleton.

These models are not schemas, ORM models, or production contracts. The plain-
language contracts remain authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class FixtureBundle:
    """Loaded fake GTM fixture files used by the skeleton builder."""

    source_records: JsonObject
    signals: JsonObject
    expected_entities: JsonObject
    expected_signal_links: JsonObject
    expected_entity_states: JsonObject


@dataclass(frozen=True)
class BuildPaths:
    """Local input and output paths for one deterministic skeleton run."""

    input_dir: Path
    output_dir: Path


@dataclass(frozen=True)
class BuildSummary:
    """Inspectable summary of a skeleton build.

    This summary proves file movement and counting only. It does not prove real
    identity resolution, signal attachment, or state computation.
    """

    builder_mode: str
    source_record_count: int
    signal_count: int
    expected_entity_count: int
    expected_signal_link_count: int
    expected_entity_state_count: int
    unresolved_record_count: int
    input_dir: str
    output_dir: str
    output_files: list[str]
    warnings: list[str]
