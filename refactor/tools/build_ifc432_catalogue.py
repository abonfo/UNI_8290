#!/usr/bin/env python3
"""Parse the official IFC 4.3.2 EXPRESS schema and static semantic documentation."""

from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = REPO_ROOT / "refactor" / "sources"
EXPRESS_PATH = SOURCE_DIR / "IFC4X3_ADD2.exp"
DOC_ZIP_PATH = SOURCE_DIR / "IFC4.3.x-output-2-main.zip"
OUT_DIR = REPO_ROOT / "refactor" / "inventory"
TEST_DIR = REPO_ROOT / "refactor" / "tests"

OFFICIAL_RELEASE = "IFC 4.3.2.0 (IFC4X3_ADD2) official"
OFFICIAL_DOC_URL = "https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/"
OFFICIAL_ANNEX_URL = "https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/annex-a.html"
REPOSITORY_URL = "https://github.com/buildingSMART/IFC4.3.x-output-2"
REPOSITORY_COMMIT = "3ddf36033cd503acd2f6e06dd3923940a3950914"
REPOSITORY_EXPRESS_PATH = "IFC/RELEASE/IFC4_3/IFC4X3_DEV_60a6175.exp"
REPOSITORY_EXPRESS_BLOB_SHA = "67f77d54c39aa6889918483268feaf892b44af0a"
EXPECTED_EXPRESS_SHA256 = "E1524D66A7BE3FBBE2D1AF58588A0E15C3898E9633F095B9AAA7D55DD6052E1D"
EXPECTED_DOC_ZIP_SHA256 = "9F0E928ACB8BE9BAAD4DC33F5AAE0C12ADBAB9C92BAD28A6EB20D38EF503BB0A"

ENTITY_RE = re.compile(r"(?ims)^ENTITY\s+(Ifc\w+)\s*(.*?);(.*?)^END_ENTITY\s*;")
TYPE_RE = re.compile(r"(?ims)^TYPE\s+(Ifc\w+)\s*=\s*(.*?);(.*?)^END_TYPE\s*;")
FUNCTION_RE = re.compile(r"(?im)^FUNCTION\s+(Ifc\w+)")
RULE_RE = re.compile(r"(?im)^RULE\s+(Ifc\w+)")
SCHEMA_RE = re.compile(r"(?im)^SCHEMA\s+(\w+)\s*;")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def strip_html(fragment: str) -> str:
    fragment = re.sub(r"(?is)<script\b.*?</script>", " ", fragment)
    fragment = re.sub(r"(?is)<style\b.*?</style>", " ", fragment)
    fragment = re.sub(r"(?i)<br\s*/?>", " ", fragment)
    fragment = re.sub(r"(?i)</p\s*>", " ", fragment)
    fragment = re.sub(r"(?s)<[^>]+>", " ", fragment)
    text = html.unescape(fragment).replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_short_definition(page: str) -> str:
    heading = re.search(r"(?is)<h2[^>]*>.*?Semantic definition.*?</h2>", page)
    if not heading:
        return ""
    start = heading.end()
    end_marker = page.find("<!-- end of short definition -->", start)
    if end_marker >= 0:
        return strip_html(page[start:end_marker])
    first_paragraph = re.search(r"(?is)<p(?:\s[^>]*)?>(.*?)</p>", page[start:])
    return strip_html(first_paragraph.group(1)) if first_paragraph else ""


def parse_domain(page: str) -> str:
    match = re.search(
        r'(?is)<a\s+class="sublink-1 current"[^>]*>\s*([0-9.]+\s+)?(Ifc\w+)\s*</a>',
        page,
    )
    if match:
        return match.group(2)
    return ""


def parse_page_number(page: str, entity_name: str) -> str:
    match = re.search(rf"(?is)<h1[^>]*>\s*([0-9.]+)\s+{re.escape(entity_name)}\b", page)
    return match.group(1) if match else ""


def enum_values(type_expression: str) -> list[str]:
    match = re.search(r"(?is)ENUMERATION\s+OF\s*\((.*?)\)", type_expression)
    if not match:
        return []
    return [value.strip() for value in match.group(1).split(",") if value.strip()]


def type_category(expression: str) -> str:
    upper = expression.upper()
    if "ENUMERATION OF" in upper:
        return "enumeration"
    if re.search(r"\bSELECT\b", upper):
        return "select"
    if re.search(r"\b(ARRAY|BAG|LIST|SET)\b", upper):
        return "aggregation"
    return "defined_type"


def inheritance_chain(name: str, parents: dict[str, list[str]]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()

    def visit(current: str) -> None:
        for parent in parents.get(current, []):
            if parent in seen:
                continue
            seen.add(parent)
            result.append(parent)
            visit(parent)

    visit(name)
    return result


def entity_kind(name: str, chain: list[str]) -> str:
    lineage = set(chain) | {name}
    if "IfcRelationship" in lineage or name.startswith("IfcRel"):
        return "relationship"
    if "IfcTypeObject" in lineage:
        return "object_type"
    if "IfcObject" in lineage:
        return "object_occurrence"
    if "IfcContext" in lineage:
        return "context"
    if "IfcPropertyDefinition" in lineage:
        return "property_definition"
    if "IfcRoot" in lineage:
        return "root_other"
    return "resource_or_other"


def eligibility(abstract: bool, deprecated: bool, kind: str) -> tuple[bool, str]:
    if abstract:
        return False, "ineligible_abstract"
    if kind == "object_type":
        return False, "ineligible_ifc_type_entity"
    if kind == "relationship":
        return False, "ineligible_relationship"
    if kind != "object_occurrence":
        return False, f"ineligible_{kind}"
    if deprecated:
        return True, "eligible_with_deprecation_warning"
    return True, "eligible_occurrence_or_system"


def docs_lookup(zip_file: zipfile.ZipFile) -> dict[str, str]:
    result: dict[str, str] = {}
    marker = "/IFC/RELEASE/IFC4_3/lexical/"
    for archive_name in zip_file.namelist():
        if marker not in archive_name or not archive_name.endswith(".html"):
            continue
        stem = Path(archive_name).stem
        if stem.startswith("Ifc"):
            result[stem] = archive_name
    return result


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    TEST_DIR.mkdir(parents=True, exist_ok=True)

    express_hash = sha256(EXPRESS_PATH)
    archive_hash = sha256(DOC_ZIP_PATH)
    express_text = EXPRESS_PATH.read_text(encoding="utf-8-sig")
    schema_match = SCHEMA_RE.search(express_text)
    schema_identifier = schema_match.group(1) if schema_match else ""

    type_rows: list[dict[str, Any]] = []
    type_index: dict[str, dict[str, Any]] = {}
    for match in TYPE_RE.finditer(express_text):
        name, expression, constraints = match.groups()
        row = {
            "name": name,
            "category": type_category(expression),
            "base_expression": " ".join(expression.split()),
            "enum_values": " | ".join(enum_values(expression)),
            "has_where_constraints": bool(re.search(r"(?im)^\s*WHERE\b", constraints)),
        }
        type_rows.append(row)
        type_index[name] = row

    raw_entities: dict[str, dict[str, Any]] = {}
    parents: dict[str, list[str]] = {}
    for match in ENTITY_RE.finditer(express_text):
        name, header, body = match.groups()
        parent_match = re.search(r"(?is)SUBTYPE\s+OF\s*\((.*?)\)", header)
        direct_parents = re.findall(r"Ifc\w+", parent_match.group(1)) if parent_match else []
        predefined_match = re.search(
            r"(?im)^\s*PredefinedType\s*:\s*(?:OPTIONAL\s+)?(Ifc\w+)\s*;",
            body,
        )
        raw_entities[name] = {
            "header": header,
            "body": body,
            "abstract": bool(re.search(r"(?i)\bABSTRACT\b", header)),
            "direct_parents": direct_parents,
            "predefined_type_enum": predefined_match.group(1) if predefined_match else "",
        }
        parents[name] = direct_parents

    rows: list[dict[str, Any]] = []
    missing_doc_pages: list[str] = []
    missing_short_definitions: list[str] = []
    docs_not_entities: list[str] = []
    with zipfile.ZipFile(DOC_ZIP_PATH) as archive:
        lookup = docs_lookup(archive)
        docs_not_entities = sorted(set(lookup) - set(raw_entities))
        for name in sorted(raw_entities):
            raw = raw_entities[name]
            archive_name = lookup.get(name)
            page = archive.read(archive_name).decode("utf-8", errors="replace") if archive_name else ""
            if not archive_name:
                missing_doc_pages.append(name)
            definition = parse_short_definition(page) if page else ""
            if not definition:
                missing_short_definitions.append(name)
            deprecated = bool(re.search(r'class="[^"]*\bdeprecation\b', page, re.I))
            chain = inheritance_chain(name, parents)
            kind = entity_kind(name, chain)
            eligible, eligibility_reason = eligibility(raw["abstract"], deprecated, kind)
            predefined_enum = raw["predefined_type_enum"]
            predefined_values = type_index.get(predefined_enum, {}).get("enum_values", "")
            rows.append(
                {
                    "name": name,
                    "domain": parse_domain(page) if page else "",
                    "documentation_number": parse_page_number(page, name) if page else "",
                    "direct_parents": " | ".join(raw["direct_parents"]),
                    "inheritance_chain": " | ".join(chain),
                    "abstract": raw["abstract"],
                    "deprecated": deprecated,
                    "entity_kind": kind,
                    "predefined_type_enum": predefined_enum,
                    "predefined_type_values": predefined_values,
                    "short_semantic_definition": definition,
                    "related_ifc_mapping_eligible": eligible,
                    "eligibility_reason": eligibility_reason,
                    "official_documentation_url": (
                        f"https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/{name}.htm"
                    ),
                }
            )

    entity_csv_path = OUT_DIR / "ifc432-entities.csv"
    with entity_csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    type_csv_path = OUT_DIR / "ifc432-types.csv"
    with type_csv_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(type_rows[0].keys()))
        writer.writeheader()
        writer.writerows(sorted(type_rows, key=lambda row: row["name"]))

    metadata = {
        "official_release": OFFICIAL_RELEASE,
        "official_documentation_url": OFFICIAL_DOC_URL,
        "official_normative_annex_url": OFFICIAL_ANNEX_URL,
        "schema_identifier": schema_identifier,
        "repository_url": REPOSITORY_URL,
        "repository_commit": REPOSITORY_COMMIT,
        "repository_express_path": REPOSITORY_EXPRESS_PATH,
        "repository_express_blob_sha": REPOSITORY_EXPRESS_BLOB_SHA,
        "local_express_sha256": express_hash,
        "local_documentation_archive_sha256": archive_hash,
        "entity_count": len(rows),
        "type_count": len(type_rows),
        "function_count": len(FUNCTION_RE.findall(express_text)),
        "rule_count": len(RULE_RE.findall(express_text)),
    }
    json_path = OUT_DIR / "ifc432-catalogue.json"
    json_path.write_text(
        json.dumps(
            {
                "metadata": metadata,
                "entities": rows,
                "types": sorted(type_rows, key=lambda row: row["name"]),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    entity_names = [row["name"] for row in rows]
    type_names = [row["name"] for row in type_rows]
    duplicate_entity_names = sorted(name for name, count in Counter(entity_names).items() if count > 1)
    duplicate_type_names = sorted(name for name, count in Counter(type_names).items() if count > 1)
    missing_parent_entities = sorted(
        {
            parent
            for row in rows
            for parent in row["direct_parents"].split(" | ")
            if parent and parent not in raw_entities
        }
    )
    invalid_predefined_enums = sorted(
        {
            row["predefined_type_enum"]
            for row in rows
            if row["predefined_type_enum"] and row["predefined_type_enum"] not in type_index
        }
    )
    kind_counts = Counter(row["entity_kind"] for row in rows)
    eligibility_counts = Counter(row["eligibility_reason"] for row in rows)
    domain_counts = Counter(row["domain"] or "[missing]" for row in rows)

    tests: list[dict[str, str]] = []
    add_test(tests, "express_sha256", "pass" if express_hash == EXPECTED_EXPRESS_SHA256 else "fail", express_hash)
    add_test(tests, "documentation_archive_sha256", "pass" if archive_hash == EXPECTED_DOC_ZIP_SHA256 else "fail", archive_hash)
    add_test(tests, "schema_identifier", "pass" if schema_identifier == "IFC4X3_DEV_60a6175" else "fail", schema_identifier)
    add_test(tests, "entity_count", "pass" if len(rows) == 876 else "fail", str(len(rows)))
    add_test(tests, "type_count", "pass" if len(type_rows) == 436 else "fail", str(len(type_rows)))
    add_test(tests, "unique_entity_names", "pass" if not duplicate_entity_names else "fail", repr(duplicate_entity_names))
    add_test(tests, "unique_type_names", "pass" if not duplicate_type_names else "fail", repr(duplicate_type_names))
    add_test(tests, "parent_resolution", "pass" if not missing_parent_entities else "fail", repr(missing_parent_entities))
    add_test(tests, "documentation_page_coverage", "pass" if not missing_doc_pages else "fail", repr(missing_doc_pages))
    add_test(
        tests,
        "short_definition_coverage",
        "warning" if missing_short_definitions else "pass",
        f"Missing {len(missing_short_definitions)}: {missing_short_definitions}",
    )
    add_test(
        tests,
        "predefined_enum_resolution",
        "pass" if not invalid_predefined_enums else "fail",
        repr(invalid_predefined_enums),
    )
    add_test(
        tests,
        "documentation_non_entity_pages",
        "info",
        f"Lexical IFC pages not declared as ENTITY: {len(docs_not_entities)}",
    )

    tests_path = TEST_DIR / "p02-ifc432-catalogue-tests.json"
    tests_path.write_text(json.dumps({"metadata": metadata, "tests": tests}, indent=2) + "\n", encoding="utf-8")

    report_path = OUT_DIR / "p02-ifc432-catalogue-report.md"
    report_path.write_text(
        render_report(
            metadata=metadata,
            tests=tests,
            kind_counts=kind_counts,
            eligibility_counts=eligibility_counts,
            domain_counts=domain_counts,
            missing_short_definitions=missing_short_definitions,
        ),
        encoding="utf-8",
    )

    failures = [test for test in tests if test["status"] == "fail"]
    print(f"Wrote {entity_csv_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {type_csv_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {json_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {report_path.relative_to(REPO_ROOT)}")
    print(f"Wrote {tests_path.relative_to(REPO_ROOT)}")
    print(
        f"Entities={len(rows)} Types={len(type_rows)} "
        f"Eligible={sum(1 for row in rows if row['related_ifc_mapping_eligible'])} "
        f"HardFailures={len(failures)}"
    )
    return 1 if failures else 0


def add_test(tests: list[dict[str, str]], test_id: str, status: str, detail: str) -> None:
    tests.append({"id": test_id, "status": status, "detail": detail})


def render_report(**context: Any) -> str:
    metadata = context["metadata"]
    tests = context["tests"]
    lines = [
        "# P02 — IFC 4.3.2 exhaustive entity catalogue",
        "",
        f"Release: **{metadata['official_release']}**",
        "",
        "## Reproducible provenance",
        "",
        f"- Official documentation: <{metadata['official_documentation_url']}>",
        f"- Normative Annex A: <{metadata['official_normative_annex_url']}>",
        f"- Official output repository: <{metadata['repository_url']}>",
        f"- Repository commit: `{metadata['repository_commit']}`",
        f"- EXPRESS repository path: `{metadata['repository_express_path']}`",
        f"- EXPRESS blob SHA: `{metadata['repository_express_blob_sha']}`",
        f"- EXPRESS schema identifier: `{metadata['schema_identifier']}`",
        f"- Local EXPRESS SHA-256: `{metadata['local_express_sha256']}`",
        f"- Documentation archive SHA-256: `{metadata['local_documentation_archive_sha256']}`",
        "",
        "The official static documentation labels the release IFC 4.3.2.0 / IFC4X3_ADD2. "
        "Its generated EXPRESS schema retains the internal identifier `IFC4X3_DEV_60a6175`; both identifiers are recorded to avoid silently conflating release labels.",
        "",
        "## Parsed schema totals",
        "",
        f"- Entities: **{metadata['entity_count']}**",
        f"- Types: **{metadata['type_count']}**",
        f"- Functions: **{metadata['function_count']}**",
        f"- Rules: **{metadata['rule_count']}**",
        "",
        "## Entity categories",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in sorted(context["kind_counts"].items()):
        lines.append(f"| `{category}` | {count} |")
    lines.extend(["", "## Mapping eligibility screening", "", "| Result | Count |", "|---|---:|"])
    for reason, count in sorted(context["eligibility_counts"].items()):
        lines.append(f"| `{reason}` | {count} |")
    lines.extend(["", "Eligibility means technically suitable for further UNI semantic review. It does not mean the entity must be mapped.", ""])

    lines.extend(["## Source domains", "", "| IFC schema/domain | Entity count |", "|---|---:|"])
    for domain, count in sorted(context["domain_counts"].items()):
        lines.append(f"| `{domain}` | {count} |")

    lines.extend(["", "## Catalogue validation", "", "| Check | Result | Detail |", "|---|---|---|"])
    for test in tests:
        detail = test["detail"].replace("|", "\\|")
        if len(detail) > 240:
            detail = detail[:237] + "..."
        lines.append(f"| `{test['id']}` | **{test['status']}** | {detail} |")

    lines.extend(["", "## Missing short semantic definitions", ""])
    missing = context["missing_short_definitions"]
    if missing:
        lines.append(
            "The following official entity pages did not expose a parseable short-definition block and require manual review: "
            + ", ".join(f"`{name}`" for name in missing)
        )
    else:
        lines.append("All entity pages supplied a parseable short semantic definition.")

    lines.extend(
        [
            "",
            "## Generated artifacts",
            "",
            "- `ifc432-entities.csv` — exhaustive entity catalogue and eligibility screening.",
            "- `ifc432-types.csv` — exhaustive EXPRESS type catalogue, including enumerations.",
            "- `ifc432-catalogue.json` — combined machine-readable catalogue and provenance.",
            "- `../tests/p02-ifc432-catalogue-tests.json` — machine-readable tests.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
