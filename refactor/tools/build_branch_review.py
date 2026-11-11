#!/usr/bin/env python3
"""Create the P05 human-review packet without claiming semantic approval."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "refactor" / "inventory" / "mapping-decisions.json"
STATUS = ROOT / "refactor" / "review" / "branch-review-status.json"
REPORT = ROOT / "docs" / "uni8290-bsdd-refactor" / "P05_BRANCH_REVIEW.md"
TESTS = ROOT / "refactor" / "tests" / "p05-review-packet-tests.json"
AI_ASSESSMENT = ROOT / "refactor" / "review" / "p05-ai-assessment.json"

BRANCHES = {
    "1": "load-bearing structures",
    "2": "enclosures",
    "3": "internal partitions",
    "4": "external partitions",
    "5": "building-service systems",
    "6": "safety systems",
    "7": "internal equipment",
    "8": "external equipment",
}

TARGETED_QUESTIONS = {
    "2.2.2": "Does this UNI leaf include both glazed horizontal closures and trapdoors, or should one IFC entity be removed?",
    "5.1.1": "Which physical occurrences does Alimentazione denote here: fuel/fluid supply, electrical feed, or both?",
    "5.4.1": "Does Alimentazione mean the electrical feed to extraction machinery, or another supply medium?",
    "6.2.2": "Is modelling an earth electrode as IfcCableSegment/CONDUCTORSEGMENT acceptable in the intended authoring workflows?",
    "6.3.1": "Is an air-termination/capture element represented as IfcCableSegment/CONDUCTORSEGMENT in the intended workflows?",
    "6.3.3": "Is a lightning earth electrode represented as IfcCableSegment/CONDUCTORSEGMENT in the intended workflows?",
    "7.2.0": "Should Blocco servizi remain unmapped, or is there a governed IfcElementAssembly convention that reviewers expect?",
}


def esc(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> None:
    document = json.loads(MATRIX.read_text(encoding="utf-8"))
    assessment = json.loads(AI_ASSESSMENT.read_text(encoding="utf-8"))
    assessed = assessment["decisions"]
    decisions = document["decisions"]
    grouped = {root: [] for root in BRANCHES}
    for decision in decisions:
        grouped[decision["uni_code"].split(".", 1)[0]].append(decision)

    branch_records = []
    for root, name in BRANCHES.items():
        rows = grouped[root]
        reviewed_rows = [row for row in rows if row["confidence"] != "high"]
        open_rows = [row for row in reviewed_rows if assessed.get(row["uni_code"], {}).get("disposition") == "needs_user"]
        branch_records.append(
            {
                "uni_root": f"{root}.0.0",
                "branch": name,
                "state": "awaiting_user_or_domain_expert_approval",
                "decision_count": len(rows),
                "high_confidence_count": sum(row["confidence"] == "high" for row in rows),
                "ai_resolved_decision_codes": [row["uni_code"] for row in reviewed_rows if assessed.get(row["uni_code"], {}).get("disposition") in {"accept", "revise"}],
                "open_decision_codes": [row["uni_code"] for row in open_rows],
                "approval_evidence": None,
                "reviewer": None,
                "review_date": None,
                "review_note": "AI assessment is recorded separately; explicit human semantic approval is not recorded.",
            }
        )

    status_doc = {
        "metadata": {
            "phase": "P05",
            "state": "awaiting_human_review",
            "matrix_proposal_version": document["metadata"]["proposal_version"],
            "ai_assessment_file": str(AI_ASSESSMENT.relative_to(ROOT)).replace("\\", "/"),
            "approval_rule": "A branch may be marked approved only after reviewer, date, evidence, and disposition of every open decision are recorded.",
        },
        "branches": branch_records,
    }
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status_doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# P05 — UNI 8290 to IFC branch review packet",
        "",
        "This packet is ready for explicit owner/domain-expert review. It does **not** record human approval. Automated tests and AI-assisted semantic pre-review cannot satisfy the P05 approval gate by themselves.",
        "",
        "AI assessed all 29 non-high-confidence rows. Its decisions and reasons are in `refactor/review/p05-ai-assessment.json`. The open list below contains only questions that need the owner or a domain expert. Explicit branch approval remains unrecorded.",
        "",
        "## Review summary",
        "",
        "| Root | Branch | Decisions | High | Open | State |",
        "|---|---|---:|---:|---:|---|",
    ]
    for branch in branch_records:
        lines.append(
            f"| `{branch['uni_root']}` | {branch['branch']} | {branch['decision_count']} | "
            f"{branch['high_confidence_count']} | {len(branch['open_decision_codes'])} | `{branch['state']}` |"
        )

    for root, branch_name in BRANCHES.items():
        lines.extend(
            [
                "",
                f"## {root}.0.0 — {branch_name}",
                "",
                "| UNI code and hierarchy | Proposed IFC entities | Conditions | Confidence |",
                "|---|---|---|---|",
            ]
        )
        for row in grouped[root]:
            selected = ", ".join(f"`{name}`" for name in row["selected_ifc_entities"]) or "*(empty)*"
            conditions = "; ".join(row["ifc_conditions"])
            lines.append(
                f"| `{row['uni_code']}` — {esc(row['full_hierarchy'])} | {selected} | {esc(conditions)} | `{row['confidence']}` |"
            )
        open_rows = [row for row in grouped[root] if assessed.get(row["uni_code"], {}).get("disposition") == "needs_user"]
        lines.extend(["", "### Open decisions", ""])
        if not open_rows:
            lines.append("No unresolved AI-assessment question remains in this branch; explicit branch approval is still unrecorded.")
        else:
            for row in open_rows:
                question = TARGETED_QUESTIONS.get(
                    row["uni_code"],
                    "Confirm that the selected family and stated condition match the intended UNI scope; otherwise record the revised entities or an empty mapping.",
                )
                lines.append(f"- `{row['uni_code']}` ({row['confidence']}): {question} AI finding: {assessed[row['uni_code']]['reason']}")
        resolved_rows = [row for row in grouped[root] if assessed.get(row["uni_code"], {}).get("disposition") in {"accept", "revise"}]
        lines.extend(["", "### AI-assessed decisions", ""])
        for row in resolved_rows:
            item = assessed[row["uni_code"]]
            lines.append(f"- `{row['uni_code']}` ({item['disposition']}): {item['reason']}")
        lines.extend(
            [
                "",
                "### Branch approval record",
                "",
                "- Decision: `awaiting_user_or_domain_expert_approval`",
                "- Reviewer: *(not recorded)*",
                "- Date: *(not recorded)*",
                "- Revisions/evidence: *(not recorded)*",
            ]
        )

    lines.extend(
        [
            "",
            "## Approval procedure",
            "",
            "1. Review every row in a branch, including the conditions that cannot be expressed in bSDD's entity-name list.",
            "2. Resolve each open decision as keep, revise, or intentionally empty.",
            "3. Record reviewer identity, review date, evidence/note, and branch state in the status JSON.",
            "4. Regenerate the matrix if selections change and rerun P03/P04 tests.",
            "5. Only after all eight branches are explicitly approved may P06 and P07 treat the mapping set as approved.",
            "",
        ]
    )
    REPORT.write_text("\n".join(lines), encoding="utf-8")

    all_codes = [row["uni_code"] for rows in grouped.values() for row in rows]
    tests = [
        {"id": "eight_review_branches", "status": "pass" if len(branch_records) == 8 else "fail", "detail": str(len(branch_records))},
        {"id": "all_117_decisions_in_packet", "status": "pass" if len(all_codes) == 117 and len(set(all_codes)) == 117 else "fail", "detail": str(len(all_codes))},
        {"id": "no_silent_branch_approval", "status": "pass" if all(branch["state"] == "awaiting_user_or_domain_expert_approval" for branch in branch_records) else "fail", "detail": str(Counter(branch["state"] for branch in branch_records))},
        {"id": "all_29_non_high_confidence_assessed", "status": "pass" if set(assessed) == {row["uni_code"] for row in decisions if row["confidence"] != "high"} and all(item["disposition"] in {"accept", "revise", "needs_user"} for item in assessed.values()) else "fail", "detail": str(len(assessed))},
        {"id": "unresolved_decisions_visible", "status": "pass" if sum(len(branch["open_decision_codes"]) for branch in branch_records) == sum(item["disposition"] == "needs_user" for item in assessed.values()) else "fail", "detail": str(sum(len(branch["open_decision_codes"]) for branch in branch_records))},
    ]
    hard_failures = sum(item["status"] == "fail" for item in tests)
    TESTS.write_text(json.dumps({"metadata": {"hard_failure_count": hard_failures}, "tests": tests}, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {STATUS.relative_to(ROOT)}")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    print(f"Wrote {TESTS.relative_to(ROOT)}")
    print(f"Branches=8 Decisions={len(all_codes)} Open={sum(len(b['open_decision_codes']) for b in branch_records)} HardFailures={hard_failures}")
    if hard_failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
