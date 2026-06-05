"""Small data containers for the Order Graph local builder.

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
    """Loaded fake GTM fixture files used by the local builder."""

    source_records: JsonObject
    signals: JsonObject


@dataclass(frozen=True)
class BuildPaths:
    """Local input and output paths for one deterministic run."""

    input_dir: Path
    output_dir: Path


@dataclass(frozen=True)
class BuildSummary:
    """Inspectable summary of a local Order Graph build.

    The summary must name which parts are real local logic and which parts
    remain fixture projections.
    """

    builder_mode: str
    source_record_count: int
    signal_count: int
    resolved_entity_count: int
    unresolved_record_count: int
    generated_signal_link_count: int
    generated_entity_state_count: int
    input_dir: str
    output_dir: str
    output_files: list[str]
    warnings: list[str]
