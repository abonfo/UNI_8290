#!/usr/bin/env python3
"""Build a normalized, read-only inventory of the two protected UNI 8290 JSON files."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
IT_SOURCE = REPO_ROOT / "UNI-8290-PBS.json"
EN_SOURCE = REPO_ROOT / "UNI-8290-PBS-en-GB.json"
OUT_DIR = REPO_ROOT / "refactor" / "inventory"
TEST_DIR = REPO_ROOT / "refactor" / "tests"

EXPECTED_HASHES = {
    IT_SOURCE.name: "C8A79D7EC9A0F5DCBC289E0DC7B9FE07A4E8900F6B9FD803B7EFE356C42BCE85",
    EN_SOURCE.name: "EE49386F56CA523FDC43C1102287001E79FDC16270147F36A41BE99939E4AB8B",
}

CODE_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as stream:
        data = json.load(stream)
    if not isinstance(data, dict):
        raise ValueError(f"Expected an object at the top level of {path}")
    if not isinstance(data.get("Classes"), list):
        raise ValueError(f"Expected a Classes list in {path}")
    return data


def present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return True


def code_level(code: str) -> int | None:
    if not CODE_PATTERN.fullmatch(code):
        return None
    major, middle, leaf = code.split(".")
    if middle == "0" and leaf == "0":
        return 1
    if leaf == "0":
        return 2
    return 3


def expected_parent(code: str) -> str | None:
    level = code_level(code)
    if level is None or level == 1:
        return None
    major, middle, _leaf = code.split(".")
    if level == 2:
        return f"{major}.0.0"
    return f"{major}.{middle}.0"


def index_classes(classes: list[dict[str, Any]]) -> tuple[dict[str, dict[str, Any]], list[str]]:
    index: dict[str, dict[str, Any]] = {}
    duplicates: list[str] = []
    for item in classes:
        code = str(item.get("Code") or "")
        if code in index:
            duplicates.append(code)
        else:
            index[code] = item
    return index, sorted(set(duplicates))


def hierarchy_path(
    code: str,
    index: dict[str, dict[str, Any]],
    field: str,
) -> tuple[list[str], bool]:
    path: list[str] = []
    visited: set[str] = set()
    current = code
    cycle = False
    while current:
        if current in visited:
            cycle = True
            path.append(f"[CYCLE:{current}]")
            break
        visited.add(current)
        item = index.get(current)
        if item is None:
            path.append(f"[MISSING:{current}]")
            break
        value = str(item.get(field) or "").strip()
        path.append(value or f"[{current}]")
        current = str(item.get("ParentClassCode") or "").strip()
    path.reverse()
    return path, cycle


def group_duplicate_names(classes: list[dict[str, Any]]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for item in classes:
        name = str(item.get("Name") or "").strip()
        if name:
            grouped[name].append(str(item.get("Code") or ""))
    return {name: sorted(codes) for name, codes in sorted(grouped.items()) if len(codes) > 1}


def add_test(tests: list[dict[str, Any]], test_id: str, status: str, detail: str) -> None:
    tests.append({"id": test_id, "status": status, "detail": detail})


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    source_hashes = {path.name: sha256(path) for path in (IT_SOURCE, EN_SOURCE)}
    it_data = load_json(IT_SOURCE)
    en_data = load_json(EN_SOURCE)
    it_classes = it_data["Classes"]
    en_classes = en_data["Classes"]
    it_index, duplicate_it_codes = index_classes(it_classes)
    en_index, duplicate_en_codes = index_classes(en_classes)

    it_codes = set(it_index)
    en_codes = set(en_index)
    missing_parents = sorted(
        {
            str(item.get("ParentClassCode"))
            for item in it_classes
            if present(item.get("ParentClassCode"))
            and str(item.get("ParentClassCode")) not in it_index
        }
    )

    rows: list[dict[str, Any]] = []
    cycle_codes: list[str] = []
    parent_convention_mismatches: list[dict[str, str]] = []
    mapping_duplicate_codes: list[str] = []

    for code in sorted(it_codes, key=lambda value: tuple(int(part) for part in value.split("."))):
        it_item = it_index[code]
        en_item = en_index.get(code, {})
        level = code_level(code)
        expected = expected_parent(code)
        actual_parent = str(it_item.get("ParentClassCode") or "").strip() or None
        if actual_parent != expected:
            parent_convention_mismatches.append(
                {
                    "code": code,
                    "actual_parent": actual_parent or "",
                    "expected_parent": expected or "",
                }
            )

        it_name_path, it_cycle = hierarchy_path(code, it_index, "Name")
        en_name_path, en_cycle = hierarchy_path(code, en_index, "Name")
        if it_cycle or en_cycle:
            cycle_codes.append(code)

        mappings = [str(value) for value in (it_item.get("RelatedIfcEntityNamesList") or [])]
        mapping_duplicates = sorted(name for name, count in Counter(mappings).items() if count > 1)
        if mapping_duplicates:
            mapping_duplicate_codes.append(code)

        it_name = str(it_item.get("Name") or "")
        en_name = str(en_item.get("Name") or "")
        it_definition = str(it_item.get("Definition") or "")
        en_definition = str(en_item.get("Definition") or "")
        anomalies: list[str] = []
        if not present(it_definition):
            anomalies.append("missing_it_definition")
        if not present(en_definition):
            anomalies.append("missing_en_definition")
        if present(it_name) and it_name == en_name:
            anomalies.append("en_name_identical_to_it")
        if present(it_definition) and it_definition == en_definition:
            anomalies.append("en_definition_identical_to_it")
        if actual_parent != expected:
            anomalies.append("parent_does_not_match_code_hierarchy")
        if mapping_duplicates:
            anomalies.append("duplicate_ifc_mapping")

        rows.append(
            {
                "code": code,
                "level": level,
                "parent_code": actual_parent or "",
                "expected_parent_code": expected or "",
                "code_path": " > ".join(
                    [
                        path_code
                        for path_code in _code_path(code, it_index)
                    ]
                ),
                "it_name_path": " > ".join(it_name_path),
                "en_name_path": " > ".join(en_name_path),
                "it_name": it_name,
                "it_definition": it_definition,
                "en_name": en_name,
                "en_definition": en_definition,
                "it_name_present": present(it_name),
                "it_definition_present": present(it_definition),
                "en_name_present": present(en_name),
                "en_definition_present": present(en_definition),
                "en_name_identical_to_it": present(it_name) and it_name == en_name,
                "en_definition_identical_to_it": present(it_definition) and it_definition == en_definition,
                "current_ifc_mapping_count": len(mappings),
                "current_ifc_mappings": " | ".join(mappings),
                "duplicate_ifc_mappings": " | ".join(mapping_duplicates),
                "class_type": str(it_item.get("ClassType") or ""),
                "status": str(it_item.get("Status") or ""),
                "it_fields_present": " | ".join(sorted(it_item.keys())),
                "en_fields_present": " | ".join(sorted(en_item.keys())),
                "anomalies": " | ".join(anomalies),
            }
        )

    csv_path = OUT_DIR / "uni8290-classes.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path = OUT_DIR / "uni8290-classes.json"
    json_path.write_text(
        json.dumps(
            {
                "metadata": {
                    "generated_from": [IT_SOURCE.name, EN_SOURCE.name],
                    "source_sha256": source_hashes,
                    "class_count": len(rows),
                },
                "classes": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    duplicate_it_names = group_duplicate_names(it_classes)
    duplicate_en_names = group_duplicate_names(en_classes)
    level_counts = Counter(row["level"] for row in rows)
    missing_it_definitions = [row["code"] for row in rows if not row["it_definition_present"]]
    missing_en_definitions = [row["code"] for row in rows if not row["en_definition_present"]]
    identical_names = [row["code"] for row in rows if row["en_name_identical_to_it"]]
    identical_definitions = [row["code"] for row in rows if row["en_definition_identical_to_it"]]

    tests: list[dict[str, Any]] = []
    for source_name, digest in source_hashes.items():
        add_test(
            tests,
            f"source_hash_{source_name}",
            "pass" if digest == EXPECTED_HASHES[source_name] else "fail",
            f"SHA-256 {digest}",
        )
    add_test(tests, "json_parse", "pass", "Both protected source files parsed as JSON objects with Classes lists")
    add_test(tests, "it_class_count", "pass" if len(it_classes) == 117 else "fail", str(len(it_classes)))
    add_test(tests, "en_class_count", "pass" if len(en_classes) == 117 else "fail", str(len(en_classes)))
    add_test(tests, "it_unique_codes", "pass" if not duplicate_it_codes else "fail", repr(duplicate_it_codes))
    add_test(tests, "en_unique_codes", "pass" if not duplicate_en_codes else "fail", repr(duplicate_en_codes))
    add_test(
        tests,
        "language_code_coverage",
        "pass" if it_codes == en_codes else "fail",
        f"IT-only={sorted(it_codes - en_codes)}; EN-only={sorted(en_codes - it_codes)}",
    )
    add_test(tests, "parent_existence", "pass" if not missing_parents else "fail", repr(missing_parents))
    add_test(tests, "hierarchy_cycles", "pass" if not cycle_codes else "fail", repr(sorted(set(cycle_codes))))
    invalid_codes = sorted(code for code in it_codes | en_codes if not CODE_PATTERN.fullmatch(code))
    add_test(tests, "code_pattern", "pass" if not invalid_codes else "fail", repr(invalid_codes))
    add_test(
        tests,
        "level_counts",
        "pass" if dict(level_counts) == {1: 8, 2: 30, 3: 79} else "fail",
        repr(dict(sorted(level_counts.items()))),
    )
    add_test(
        tests,
        "parent_code_convention",
        "warning" if parent_convention_mismatches else "pass",
        repr(parent_convention_mismatches),
    )
    add_test(
        tests,
        "italian_definitions",
        "warning" if missing_it_definitions else "pass",
        f"Missing {len(missing_it_definitions)}: {missing_it_definitions}",
    )
    add_test(
        tests,
        "english_definitions",
        "warning" if missing_en_definitions else "pass",
        f"Missing {len(missing_en_definitions)}: {missing_en_definitions}",
    )
    add_test(
        tests,
        "english_translation_names",
        "warning" if identical_names else "pass",
        f"Identical to Italian {len(identical_names)}: {identical_names}",
    )
    add_test(
        tests,
        "english_translation_definitions",
        "warning" if identical_definitions else "pass",
        f"Identical non-empty definitions {len(identical_definitions)}: {identical_definitions}",
    )
    add_test(
        tests,
        "duplicate_ifc_mappings_within_class",
        "warning" if mapping_duplicate_codes else "pass",
        repr(mapping_duplicate_codes),
    )

    test_path = TEST_DIR / "p01-structural-tests.json"
    test_path.write_text(json.dumps({"tests": tests}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_path = OUT_DIR / "p01-structural-report.md"
    report_path.write_text(
        _render_report(
            source_hashes=source_hashes,
            rows=rows,
            level_counts=level_counts,
            duplicate_it_names=duplicate_it_names,
            duplicate_en_names=duplicate_en_names,
            parent_convention_mismatches=parent_convention_mismatches,
            missing_it_definitions=missing_it_definitions,
            missing_en_definitions=missing_en_definitions,
            identical_names=identical_names,
            identical_definitions=identical_definitions,
            tests=tests,
        ),
        encoding="utf-8",
    )

    failures = [test for test in tests if test["status"] == "fail"]
    print(f"Wrote {csv_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {json_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {report_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {test_path.relative_to(REPO_ROOT)}")
    print(f"Classes: {len(rows)}; hard failures: {len(failures)}")
    return 1 if failures else 0


def _code_path(code: str, index: dict[str, dict[str, Any]]) -> list[str]:
    result: list[str] = []
    visited: set[str] = set()
    current = code
    while current:
        if current in visited:
            result.append(f"[CYCLE:{current}]")
            break
        visited.add(current)
        result.append(current)
        item = index.get(current)
        if item is None:
            break
        current = str(item.get("ParentClassCode") or "").strip()
    result.reverse()
    return result


def _render_report(**context: Any) -> str:
    rows = context["rows"]
    tests = context["tests"]
    lines = [
        "# P01 — UNI 8290 normalized inventory and structural report",
        "",
        "This report is generated from the two protected source JSON files. It does not modify them.",
        "",
        "## Source integrity",
        "",
    ]
    for name, digest in context["source_hashes"].items():
        lines.append(f"- `{name}`: `{digest}`")
    lines.extend(
        [
            "",
            "## Inventory summary",
            "",
            f"- Normalized classes: **{len(rows)}**",
            f"- Level 1: **{context['level_counts'].get(1, 0)}**",
            f"- Level 2: **{context['level_counts'].get(2, 0)}**",
            f"- Level 3: **{context['level_counts'].get(3, 0)}**",
            f"- Italian definitions missing: **{len(context['missing_it_definitions'])}**",
            f"- English definitions missing: **{len(context['missing_en_definitions'])}**",
            f"- English names identical to Italian: **{len(context['identical_names'])}**",
            f"- Non-empty English definitions identical to Italian: **{len(context['identical_definitions'])}**",
            "",
            "## Structural checks",
            "",
            "| Check | Result | Detail |",
            "|---|---|---|",
        ]
    )
    for test in tests:
        detail = str(test["detail"]).replace("|", "\\|").replace("\n", " ")
        if len(detail) > 220:
            detail = detail[:217] + "..."
        lines.append(f"| `{test['id']}` | **{test['status']}** | {detail} |")

    lines.extend(["", "## Parent-path anomaly", ""])
    if context["parent_convention_mismatches"]:
        lines.extend(["| Code | Actual parent | Expected parent |", "|---|---|---|"])
        for mismatch in context["parent_convention_mismatches"]:
            lines.append(
                f"| `{mismatch['code']}` | `{mismatch['actual_parent']}` | `{mismatch['expected_parent']}` |"
            )
    else:
        lines.append("No parent-path anomaly detected.")

    lines.extend(["", "## Hierarchy-dependent duplicate names", ""])
    lines.append(
        "Duplicate labels are recorded for context-aware interpretation and are not treated as structural errors."
    )
    lines.extend(["", "| Italian name | Codes |", "|---|---|"])
    for name, codes in context["duplicate_it_names"].items():
        lines.append(f"| {name} | {', '.join(f'`{code}`' for code in codes)} |")

    lines.extend(["", "## Missing definitions by first-level branch", ""])
    by_branch: dict[str, list[str]] = defaultdict(list)
    for code in context["missing_it_definitions"]:
        by_branch[code.split(".")[0]].append(code)
    for branch, codes in sorted(by_branch.items(), key=lambda pair: int(pair[0])):
        lines.append(f"- Branch {branch}: {len(codes)} — {', '.join(f'`{code}`' for code in codes)}")

    lines.extend(
        [
            "",
            "## Generated artifacts",
            "",
            "- `uni8290-classes.csv` — tabular normalized inventory.",
            "- `uni8290-classes.json` — machine-readable normalized inventory.",
            "- `../tests/p01-structural-tests.json` — machine-readable structural test results.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
