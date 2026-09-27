"""Offline repository invariants that do not require GenLayer packages."""

from pathlib import Path
import ast
import json

ROOT = Path(__file__).resolve().parents[1]
contract = ROOT / "contracts" / "venue.py"
source = contract.read_text(encoding="utf-8")
ast.parse(source)

pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
assert pkg["devDependencies"]["genlayer"] == "0.39.1"

config = (ROOT / "gltest.config.yaml").read_text(encoding="utf-8")
assert "https://studio.genlayer.com/api" in config
assert "studionet:" in config
assert "studio-dev" not in config.lower()
assert "61997" not in config

for required in (
    "run_nondet_unsafe",
    "MATCH",
    "NO_MATCH",
    "AMBIGUOUS",
    "ROUTE_MULTI_SCOPE",
    "class Venue(gl.Contract)",
    "route_matter",
):
    assert required in source, required

print("VENUE offline preflight: OK")
print("Pinned CLI: 0.39.1")
print("Target network: stable Studionet / 61999")
