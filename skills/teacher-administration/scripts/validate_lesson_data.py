#!/usr/bin/env python3
"""Validate a GuruAssist lesson JSON record without changing the source file."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_STRINGS = ("subject", "education_level", "topic")
OPTIONAL_STRINGS = (
    "school_name", "grade", "phase", "semester", "curriculum", "duration",
    "student_context", "learning_mode",
)
STRING_LISTS = (
    "learning_outcomes", "learning_objectives", "materials", "learning_method",
    "references", "needs_confirmation",
)
NESTED_LISTS = {
    "activities": ("opening", "core", "closing"),
    "assessment": ("formative", "summative", "criteria"),
}


def validate(data: Any) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for a parsed lesson record."""
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Top-level JSON value must be an object."], []

    for key in REQUIRED_STRINGS:
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"'{key}' must be a non-empty string.")

    for key in OPTIONAL_STRINGS:
        if key in data and data[key] is not None and not isinstance(data[key], str):
            errors.append(f"'{key}' must be a string when provided.")

    for key in STRING_LISTS:
        if key in data:
            value = data[key]
            if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                errors.append(f"'{key}' must be a list of strings.")

    for object_key, child_keys in NESTED_LISTS.items():
        if object_key not in data:
            continue
        obj = data[object_key]
        if not isinstance(obj, dict):
            errors.append(f"'{object_key}' must be an object.")
            continue
        for child_key in child_keys:
            if child_key in obj:
                value = obj[child_key]
                if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
                    errors.append(f"'{object_key}.{child_key}' must be a list of strings.")

    recommended = ("grade", "curriculum", "duration", "learning_objectives", "needs_confirmation")
    for key in recommended:
        if key not in data or data[key] in (None, "", []):
            warnings.append(f"Consider completing '{key}'.")

    if not data.get("references"):
        warnings.append("No references are listed; add the sources used or state that none were supplied.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to lesson JSON")
    args = parser.parse_args()

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: cannot read input: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    if errors:
        print("ERROR: lesson data is invalid:", file=sys.stderr)
        for item in errors:
            print(f" - {item}", file=sys.stderr)
        return 1

    print("OK: lesson JSON structure is valid.")
    for item in warnings:
        print(f"WARNING: {item}")
    if data.get("needs_confirmation"):
        print("REVIEW: items requiring teacher confirmation:")
        for item in data["needs_confirmation"]:
            print(f" - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
