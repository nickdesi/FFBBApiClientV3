#!/usr/bin/env python3
"""Check that FFBBAPIClientV3 wrapper exposes all methods from inner clients."""

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS = ROOT / "src" / "ffbb_api_client_v3" / "clients"

# Methods intentionally excluded from the parity check
EXCLUDED = {
    # private / dunder / internal helpers
    "__init__",
    "__repr__",
    "__str__",
}


def get_public_methods(path: Path) -> set[str]:
    """Return all public method names defined in the first class of a file."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    methods: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    name = item.name
                    if not name.startswith("_") and name not in EXCLUDED:
                        methods.add(name)
            break  # only first class
    return methods


def main() -> int:
    api_methods = get_public_methods(CLIENTS / "api_ffbb_app_client.py")
    ms_methods = get_public_methods(CLIENTS / "meilisearch_ffbb_client.py")
    wrapper_methods = get_public_methods(CLIENTS / "ffbb_api_client_v3.py")

    # All inner-client methods that should be reachable through the wrapper
    all_inner = api_methods | ms_methods

    missing = sorted(all_inner - wrapper_methods)

    if not missing:
        print("✅ Wrapper parity OK — all methods are exposed.")
        return 0

    # Build markdown report (written to disk so the GH Actions step can read it)
    lines = [
        "## ⚠️ Wrapper parity check failed",
        "",
        "The following methods exist in inner clients but are **not exposed** "
        "in `FFBBAPIClientV3`:",
        "",
        "| Method | Source client |",
        "|---|---|",
    ]
    for m in missing:
        source = []
        if m in api_methods:
            source.append("`ApiFFBBAppClient`")
        if m in ms_methods:
            source.append("`MeilisearchFFBBClient`")
        lines.append(f"| `{m}` | {', '.join(source)} |")

    lines += [
        "",
        "### How to fix",
        "Add the missing method(s) to "
        "`src/ffbb_api_client_v3/clients/ffbb_api_client_v3.py` "
        "so they delegate to the appropriate inner client.",
    ]

    report = "\n".join(lines)
    Path("parity_report.md").write_text(report, encoding="utf-8")

    print(report)
    print(f"\n❌ {len(missing)} missing method(s) found — failing build.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
