"""Packaged FFBB API discovery artefacts."""

from __future__ import annotations

import json
from importlib import resources
from typing import Any, Literal

DiscoveryArtefactName = Literal[
    "collections.json",
    "endpoint_discovery.json",
    "indexes.json",
    "openapi.json",
    "openapi_full.json",
]


def load_discovery_artefact(name: DiscoveryArtefactName) -> dict[str, Any]:
    """Load a packaged FFBB API discovery artefact as JSON."""
    return json.loads(
        resources.files(__package__).joinpath(name).read_text(encoding="utf-8")
    )


__all__ = ["DiscoveryArtefactName", "load_discovery_artefact"]
