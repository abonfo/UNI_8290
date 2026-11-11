#!/usr/bin/env python3
"""Validate the P03 mapping policy against the normalized UNI and IFC catalogues."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RULES_PATH = ROOT / "refactor" / "mapping-rules.json"
UNI_PATH = ROOT / "refactor" / "inventory" / "uni8290-classes.csv"
IFC_PATH = ROOT / "refactor" / "inventory" / "ifc432-entities.csv"
OUTPUT_PATH = ROOT / "refactor" / "tests" / "p03-mapping-rules-tests.json"


def test(test_id: str, passed: bool, detail: object) -> dict[str, str]:
    return {"id": test_id, "status": "pass" if passed else "fail", "detail": str(detail)}


def main() -> None:
    rules = json.loads(RULES_PATH.read_text(encoding="utf-8"))
    with UNI_PATH.open(encoding="utf-8-sig", newline="") as stream:
        uni_rows = list(csv.DictReader(stream))
    with IFC_PATH.open(encoding="utf-8-sig", newline="") as stream:
        ifc_rows = list(csv.DictReader(stream))

    roots = {row["code"] for row in uni_rows if row["level"] == "1"}
    branch_roots = [branch["uni_root"] for branch in rules["branch_rules"]]
    ifc_names = {row["name"] for row in ifc_rows}
    preferred = {
        name
        for branch in rules["branch_rules"]
        for name in branch["preferred_families"]
    }
    unknown_preferred = sorted(preferred - ifc_names)

    all_reasons = [
        reason["code"]
        for group in rules["reason_codes"].values()
        for reason in group
    ]
    gate_ids = [gate["id"] for gate in rules["selection_gates"]]
    required_inputs = set(rules["required_inputs"])
    required_decision_fields = set(rules["decision_record_requirements"]["required_fields"])

    tests = [
        test("eight_selection_gates", len(gate_ids) == 8 and len(gate_ids) == len(set(gate_ids)), gate_ids),
        test("full_path_is_required", "full_it_name_path" in required_inputs, sorted(required_inputs)),
        test("all_uni_roots_have_one_branch_rule", set(branch_roots) == roots and len(branch_roots) == len(set(branch_roots)), branch_roots),
        test("preferred_ifc_entities_exist", not unknown_preferred, unknown_preferred),
        test("reason_codes_unique", len(all_reasons) == len(set(all_reasons)), all_reasons),
        test("selection_and_rejection_codes_exist", bool(rules["reason_codes"]["selected"]) and bool(rules["reason_codes"]["rejected"]), "present"),
        test("screening_outcomes_complete", {r["code"] for r in rules["reason_codes"]["screening"]} == {"SCR_SELECTED", "SCR_NOT_APPLICABLE", "SCR_TECHNICALLY_INELIGIBLE"}, [r["code"] for r in rules["reason_codes"]["screening"]]),
        test("decision_matrix_fields_complete", required_decision_fields == {"uni_code", "full_hierarchy", "functional_interpretation", "current_ifc_mappings", "candidate_ifc_entities", "selected_ifc_entities", "ifc_conditions", "rejected_current_mappings", "decision_rationale", "confidence", "review_state"}, sorted(required_decision_fields)),
        test("empty_selection_permitted", rules["decision_record_requirements"]["empty_selection_allowed"] is True, rules["decision_record_requirements"]["empty_selection_rule"]),
    ]

    hard_failures = [item for item in tests if item["status"] == "fail"]
    result = {
        "metadata": {
            "policy_version": rules["policy_version"],
            "uni_root_count": len(roots),
            "ifc_entity_count_checked": len(ifc_rows),
            "reason_code_count": len(all_reasons),
            "hard_failure_count": len(hard_failures),
        },
        "tests": tests,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Tests={len(tests)} HardFailures={len(hard_failures)}")
    if hard_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
