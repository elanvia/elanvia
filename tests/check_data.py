#!/usr/bin/env python3
"""Validate data/services.yaml structure and values."""
import sys
import pathlib

try:
    import yaml
except ImportError:
    print("SKIP: pyyaml not available")
    sys.exit(0)

ROOT = pathlib.Path(__file__).parent.parent
raw = yaml.safe_load((ROOT / "data" / "services.yaml").read_text())

failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


check("services" in raw, "top-level key 'services' missing from services.yaml")
if "services" not in raw:
    print("FAIL:", failures[0])
    sys.exit(1)

services = raw["services"]
check(isinstance(services, list), "'services' must be a list")
check(len(services) == 6, f"expected 6 services, got {len(services)}")

REQUIRED = ["id", "roman", "title", "tagline", "description", "duration", "price", "accent"]
VALID_ACCENTS = {"sage", "plum", "rose", "saffron"}
VALID_ROMANS = {"I", "II", "III", "IV", "V", "VI"}

ids_seen = set()
for i, svc in enumerate(services):
    prefix = f"service[{i}] (id={svc.get('id', '?')})"
    for field in REQUIRED:
        check(field in svc, f"{prefix}: missing field '{field}'")
        check(bool(svc.get(field)), f"{prefix}: field '{field}' is empty or null")
    check(
        svc.get("accent") in VALID_ACCENTS,
        f"{prefix}: accent '{svc.get('accent')}' not in {VALID_ACCENTS}",
    )
    check(
        str(svc.get("roman", "")) in VALID_ROMANS,
        f"{prefix}: roman '{svc.get('roman')}' not in {VALID_ROMANS}",
    )
    sid = svc.get("id")
    check(sid not in ids_seen, f"{prefix}: duplicate id '{sid}'")
    ids_seen.add(sid)

if failures:
    print(f"FAIL: {len(failures)} problem(s) in services.yaml:")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)

print(f"OK: services.yaml valid ({len(services)} services)")
