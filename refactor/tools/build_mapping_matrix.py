#!/usr/bin/env python3
"""Build the exhaustive P04 UNI-to-IFC draft decision matrix and inverse IFC screening."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
UNI_CSV = ROOT / "refactor" / "inventory" / "uni8290-classes.csv"
IFC_CSV = ROOT / "refactor" / "inventory" / "ifc432-entities.csv"
RULES_JSON = ROOT / "refactor" / "mapping-rules.json"
PROPOSALS_JSON = ROOT / "refactor" / "mapping-proposals.json"
MATRIX_CSV = ROOT / "refactor" / "inventory" / "mapping-decisions.csv"
MATRIX_JSON = ROOT / "refactor" / "inventory" / "mapping-decisions.json"
COVERAGE_CSV = ROOT / "refactor" / "inventory" / "mapping-coverage.csv"
REPORT_MD = ROOT / "refactor" / "inventory" / "p04-mapping-matrix-report.md"
TESTS_JSON = ROOT / "refactor" / "tests" / "p04-mapping-matrix-tests.json"

SUSPECT_COMPONENTS = {
    "IfcFastener",
    "IfcMechanicalFastener",
    "IfcPlate",
    "IfcReinforcingBar",
    "IfcReinforcingMesh",
    "IfcTendon",
    "IfcTendonAnchor",
    "IfcTendonConduit",
    "IfcBearing",
    "IfcVibrationDamper",
    "IfcCovering",
    "IfcSign",
    "IfcSignal",
}


def split_pipe(value: str) -> list[str]:
    return [item.strip() for item in value.split("|") if item.strip()]


def compact_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def selection_reason(entity: str, conditions: list[str], level: int) -> str:
    joined = " ".join(conditions)
    if entity in {"IfcDistributionSystem", "IfcBuildingSystem", "IfcBuiltSystem"}:
        return "SEL_SYSTEM_CONTEXT" if entity == "IfcDistributionSystem" else "SEL_BROAD_PARENT"
    if "PredefinedType=" in joined:
        return "SEL_PREDEFINED_TYPE"
    if conditions:
        return "SEL_PROPERTY_CONTEXT"
    return "SEL_DIRECT" if level == 3 else "SEL_CONTROLLED_FAMILY"


def rejection_reason(name: str, ifc: dict[str, dict[str, str]]) -> tuple[str, str]:
    if name not in ifc:
        return "REJ_NOT_IN_SCHEMA", "The current name is not an entity in the pinned IFC 4.3.2 catalogue."
    row = ifc[name]
    if row["related_ifc_mapping_eligible"] != "True":
        reason = row["eligibility_reason"]
        if reason == "ineligible_abstract":
            return "REJ_ABSTRACT", "The entity is abstract and cannot classify an occurrence directly."
        if reason == "ineligible_ifc_type_entity":
            return "REJ_TYPE_ENTITY", "The entity is a type object rather than an occurrence."
        return "REJ_RELATIONSHIP_OR_RESOURCE", f"Technically ineligible catalogue category: {reason}."
    if name in SUSPECT_COMPONENTS:
        return "REJ_COMPONENT_ONLY", "Possible component or participant, but not directly classifiable by this complete UNI path."
    return "REJ_UNRELATED", "The eligible occurrence does not directly embody this UNI function in its complete hierarchy context."


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def check(test_id: str, passed: bool, detail: object, warning: bool = False) -> dict[str, str]:
    status = "pass" if passed else ("warning" if warning else "fail")
    return {"id": test_id, "status": status, "detail": str(detail)}


def main() -> None:
    with UNI_CSV.open(encoding="utf-8-sig", newline="") as stream:
        uni_rows = list(csv.DictReader(stream))
    with IFC_CSV.open(encoding="utf-8-sig", newline="") as stream:
        ifc_rows = list(csv.DictReader(stream))
    rules = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    proposals_document = json.loads(PROPOSALS_JSON.read_text(encoding="utf-8"))
    proposals = proposals_document["records"]
    ifc = {row["name"]: row for row in ifc_rows}

    selected_by: dict[str, list[str]] = defaultdict(list)
    candidate_for: dict[str, list[str]] = defaultdict(list)
    decisions: list[dict[str, object]] = []

    for uni in uni_rows:
        code = uni["code"]
        proposal = proposals.get(code, {})
        selected = proposal.get("entities", [])
        conditions = proposal.get("conditions", [])
        level = int(uni["level"])
        current = split_pipe(uni["current_ifc_mappings"])
        candidates = sorted(set(current) | set(selected))
        for name in candidates:
            candidate_for[name].append(code)
        for name in selected:
            selected_by[name].append(code)

        selected_decisions = [
            {
                "entity": name,
                "reason_code": selection_reason(name, conditions, level),
                "rationale": f"{name} directly represents this function when the recorded hierarchy and conditions are satisfied.",
            }
            for name in selected
        ]
        rejected = []
        for name in current:
            if name in selected:
                continue
            reason_code, rationale = rejection_reason(name, ifc)
            rejected.append({"entity": name, "reason_code": reason_code, "rationale": rationale})

        parent_context = uni["it_name_path"].rsplit(" > ", 1)[0] if " > " in uni["it_name_path"] else "the UNI 8290 technological system"
        interpretation = proposal.get(
            "interpretation",
            f"Interpret “{uni['it_name']}” as the functional class within {parent_context}, using the full hierarchy rather than the leaf label alone.",
        )
        if selected:
            rationale = (
                "Draft selective mapping: each selected occurrence is directly classifiable only in the stated UNI hierarchy and conditions; "
                "the remaining current broad/component mappings are removed."
            )
        else:
            rationale = (
                "No reliable direct IFC 4.3.2 occurrence is proposed. An empty mapping is preferred to a proxy or a union of possible components."
            )

        decisions.append(
            {
                "uni_code": code,
                "uni_level": level,
                "full_hierarchy": uni["it_name_path"],
                "english_hierarchy_baseline": uni["en_name_path"],
                "functional_interpretation": interpretation,
                "current_ifc_mappings": current,
                "candidate_ifc_entities": candidates,
                "selected_ifc_entities": selected,
                "selected_decisions": selected_decisions,
                "ifc_conditions": conditions,
                "rejected_current_mappings": rejected,
                "decision_rationale": rationale,
                "confidence": proposal.get("confidence", "domain_review_required"),
                "review_state": proposals_document["default_review_state"],
            }
        )

    coverage: list[dict[str, object]] = []
    for row in ifc_rows:
        name = row["name"]
        if selected_by[name]:
            outcome = "SCR_SELECTED"
            detail = "Selected by one or more draft UNI decisions."
        elif row["related_ifc_mapping_eligible"] == "True":
            outcome = "SCR_NOT_APPLICABLE"
            detail = "Technically eligible occurrence screened against the UNI inventory but not directly selected."
        else:
            outcome = "SCR_TECHNICALLY_INELIGIBLE"
            detail = row["eligibility_reason"]
        coverage.append(
            {
                "ifc_entity": name,
                "entity_kind": row["entity_kind"],
                "abstract": row["abstract"],
                "deprecated": row["deprecated"],
                "technical_eligibility": row["related_ifc_mapping_eligible"],
                "screening_outcome": outcome,
                "screening_detail": detail,
                "selected_by_uni_codes": selected_by[name],
                "candidate_for_uni_codes": candidate_for[name],
            }
        )

    uni_codes = {row["code"] for row in uni_rows}
    proposal_codes = set(proposals)
    selected_names = {name for decision in decisions for name in decision["selected_ifc_entities"]}
    unknown_selected = sorted(selected_names - set(ifc))
    ineligible_selected = sorted(name for name in selected_names if name in ifc and ifc[name]["related_ifc_mapping_eligible"] != "True")
    incomplete_current_dispositions = []
    for decision in decisions:
        dispositioned = set(decision["selected_ifc_entities"]) | {r["entity"] for r in decision["rejected_current_mappings"]}
        missing = set(decision["current_ifc_mappings"]) - dispositioned
        if missing:
            incomplete_current_dispositions.append({decision["uni_code"]: sorted(missing)})
    invalid_confidence = sorted(
        decision["uni_code"]
        for decision in decisions
        if decision["confidence"] not in rules["decision_record_requirements"]["confidence_values"]
    )
    missing_rationales = sorted(
        decision["uni_code"]
        for decision in decisions
        if any(not item["rationale"] or not item["reason_code"] for item in decision["selected_decisions"])
    )
    broad_warnings = [
        {"uni_code": d["uni_code"], "level": d["uni_level"], "selected_count": len(d["selected_ifc_entities"])}
        for d in decisions
        if len(d["selected_ifc_entities"]) > {1: 8, 2: 12, 3: 8}[d["uni_level"]]
    ]

    tests = [
        check("proposal_code_coverage", proposal_codes == uni_codes, {"missing": sorted(uni_codes - proposal_codes), "extra": sorted(proposal_codes - uni_codes)}),
        check("decision_record_count", len(decisions) == 117, len(decisions)),
        check("unique_decision_codes", len({d["uni_code"] for d in decisions}) == len(decisions), len(decisions)),
        check("selected_entities_exist", not unknown_selected, unknown_selected),
        check("selected_entities_technically_eligible", not ineligible_selected, ineligible_selected),
        check("selected_decisions_have_rationales", not missing_rationales, missing_rationales),
        check("all_current_mappings_dispositioned", not incomplete_current_dispositions, incomplete_current_dispositions),
        check("confidence_values_valid", not invalid_confidence, invalid_confidence),
        check("ifc_coverage_count", len(coverage) == 876, len(coverage)),
        check("ifc_coverage_unique", len({row["ifc_entity"] for row in coverage}) == len(coverage), len(coverage)),
        check("mapping_cardinality_review", not broad_warnings, broad_warnings, warning=True),
    ]
    hard_failures = [item for item in tests if item["status"] == "fail"]

    matrix_csv_rows = []
    for decision in decisions:
        matrix_csv_rows.append(
            {
                key: compact_json(value) if isinstance(value, (list, dict)) else value
                for key, value in decision.items()
            }
        )
    coverage_csv_rows = []
    for row in coverage:
        coverage_csv_rows.append(
            {
                key: " | ".join(value) if isinstance(value, list) else value
                for key, value in row.items()
            }
        )

    write_csv(MATRIX_CSV, matrix_csv_rows, list(matrix_csv_rows[0]))
    write_csv(COVERAGE_CSV, coverage_csv_rows, list(coverage_csv_rows[0]))
    MATRIX_JSON.write_text(
        json.dumps(
            {
                "metadata": {
                    "proposal_version": proposals_document["proposal_version"],
                    "policy_version": rules["policy_version"],
                    "review_state": "draft_pending_branch_review",
                    "uni_record_count": len(decisions),
                    "ifc_entity_screening_count": len(coverage),
                },
                "decisions": decisions,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    TESTS_JSON.write_text(
        json.dumps(
            {
                "metadata": {
                    "hard_failure_count": len(hard_failures),
                    "warning_count": sum(item["status"] == "warning" for item in tests),
                },
                "tests": tests,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    selected_frequency = Counter(name for d in decisions for name in d["selected_ifc_entities"])
    confidence_counts = Counter(d["confidence"] for d in decisions)
    level_counts = Counter(d["uni_level"] for d in decisions)
    empty_count = sum(not d["selected_ifc_entities"] for d in decisions)
    screening_counts = Counter(row["screening_outcome"] for row in coverage)
    total_current = sum(len(d["current_ifc_mappings"]) for d in decisions)
    total_selected = sum(len(d["selected_ifc_entities"]) for d in decisions)
    lines = [
        "# P04 — Draft exhaustive UNI-to-IFC mapping matrix",
        "",
        "This is a semantic-review draft, not an approved mapping set. All 117 records remain `pending` for P05 branch review.",
        "",
        "## Totals",
        "",
        f"- UNI decisions: **{len(decisions)}** (levels {dict(sorted(level_counts.items()))})",
        f"- Current mapping assignments dispositioned: **{total_current}**",
        f"- Proposed mapping assignments: **{total_selected}**",
        f"- UNI decisions with an intentionally empty proposal: **{empty_count}**",
        f"- Unique selected IFC entities: **{len(selected_names)}**",
        f"- IFC entities screened: **{len(coverage)}**",
        "",
        "## Confidence",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(confidence_counts.items())],
        "",
        "## IFC inverse screening",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(screening_counts.items())],
        "",
        "## Most frequent proposed IFC entities",
        "",
        "| IFC entity | UNI decisions |",
        "|---|---:|",
        *[f"| `{name}` | {count} |" for name, count in selected_frequency.most_common(20)],
        "",
        "## Automated validation",
        "",
        "| Check | Result | Detail |",
        "|---|---|---|",
        *[f"| `{item['id']}` | **{item['status']}** | {item['detail']} |" for item in tests],
        "",
        "## Review warning",
        "",
        "Schema validity and exhaustive disposition do not constitute semantic approval. P05 must explicitly review each UNI branch, especially all `medium` and `domain_review_required` records.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {MATRIX_CSV.relative_to(ROOT)}")
    print(f"Wrote {MATRIX_JSON.relative_to(ROOT)}")
    print(f"Wrote {COVERAGE_CSV.relative_to(ROOT)}")
    print(f"Wrote {REPORT_MD.relative_to(ROOT)}")
    print(f"Wrote {TESTS_JSON.relative_to(ROOT)}")
    print(f"Decisions={len(decisions)} IFCscreened={len(coverage)} SelectedAssignments={total_selected} HardFailures={len(hard_failures)}")
    if hard_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
