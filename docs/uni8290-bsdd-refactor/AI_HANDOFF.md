---
project: UNI 8290 bSDD to IFC 4.3.2 refactoring
status: implementation_in_progress
last_updated: 2026-11-11
authoritative_plan: REFACTOR_PLAN.md
source_json_it: ../../UNI-8290-PBS.json
source_json_en: ../../UNI-8290-PBS-en-GB.json
source_files_are_immutable: true
next_phase: P05_targeted_owner_domain_review_in_progress
---

# AI handoff and execution status

## Mandatory rules for every future agent

1. Read this entire file and `REFACTOR_PLAN.md` before doing project work.
2. Treat the two original JSON files as immutable. Never edit, rename, move, or overwrite them.
3. Do not begin implementation until the user explicitly authorizes the refactor. Planning authorization alone is not implementation authorization.
4. Before starting work, inspect the current workspace and this status file. Do not repeat a phase marked `completed` unless its recorded evidence is missing or invalid.
5. Work on the earliest authorized phase whose state is `pending` or `in_progress`.
6. After every material unit of work, update this file in the same change:
   - phase state;
   - artifacts created or modified;
   - checks executed and their results;
   - decisions and assumptions;
   - unresolved questions;
   - exact next action.
7. A phase may be marked `completed` only when its acceptance criteria in `REFACTOR_PLAN.md` are satisfied and evidence is recorded here.
8. If work stops partway through a phase, mark it `in_progress` and record the precise continuation point. Do not summarize it merely as “unfinished.”
9. Never force all IFC schema entities into UNI mappings. The full IFC 4.3.2 schema must be screened exhaustively, but only semantically appropriate entities may be selected.
10. Interpret generic UNI labels through their full hierarchy. For example, `Rete`, `Alimentazione`, `Macchine`, and `Allacciamenti` have different meanings under HVAC, electrical, gas, fire-safety, and anti-intrusion parents.
11. Do not treat parent mappings as the automatic union of all descendant mappings.
12. Keep factual source text, newly authored definitions, translations, and mapping judgments distinguishable, particularly because UNI content is copyrighted.
13. Do not claim that automated validation guarantees the buildingSMART verified badge. Human semantic, ownership, and licensing review remains necessary.

## Current checkpoint

Implementation is authorized. P01 through P04 are complete. The normalized UNI inventory,
exhaustive IFC 4.3.2 catalogue, mapping policy, draft decision matrix, inverse IFC screening,
reproducible generators, and machine-readable tests exist under `refactor/`. P05 review material
is complete. AI assessed all 29 non-high-confidence decisions on 2026-11-11, resolved 17 at
proposal level, and left 12 for the owner/domain expert. No branch has human approval. No
refactored JSON has yet been created.

Protected-source SHA-256 hashes at the planning checkpoint:

- `UNI-8290-PBS.json`: `C8A79D7EC9A0F5DCBC289E0DC7B9FE07A4E8900F6B9FD803B7EFE356C42BCE85`
- `UNI-8290-PBS-en-GB.json`: `EE49386F56CA523FDC43C1102287001E79FDC16270147F36A41BE99939E4AB8B`

Future agents must compare these hashes before creating working copies and again before declaring the refactor complete.

The conversation has completed:

- preliminary audit of both local JSON files;
- review of the current buildingSMART verification checklist;
- conceptual comparison between UNI 8290 and IFC 4.3.2;
- agreement on a hierarchy-aware, selective mapping strategy;
- preparation of the execution plan.

The user explicitly authorized implementation on 2026-08-10. Phase P05 is now in progress.

## Confirmed preliminary findings

- The Italian and English files each contain 117 UNI classes.
- The hierarchy contains 8 first-level classes, 30 second-level classes, and 79 third-level classes.
- There are no duplicate class codes.
- The earlier preliminary audit reported `5.1.2 Gruppi termici` under `5.0.0`, but the protected planning baseline and P01 inventory already contain the correct parent `5.1.0`; no refactor correction is currently required.
- Seventy-nine third-level classes lack definitions.
- The English file is largely untranslated: only 4 names and 2 non-empty definitions differ from the Italian source.
- Current mappings contain 3,603 assignments to 120 unique IFC entity names.
- Mapping breadth does not narrow with the UNI hierarchy:

| UNI level | Classes | Average mappings | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|
| 1 | 8 | 31.2 | 16 | 13 | 91 |
| 2 | 30 | 31.7 | 17 | 6 | 85 |
| 3 | 79 | 30.4 | 34 | 6 | 67 |

- `IfcFastener` and `IfcMechanicalFastener` occur in 116 of 117 UNI classes; `IfcPlate` occurs in 114 and `IfcCovering` in 103. These frequencies indicate component-based overmapping.
- All 120 unique current IFC names were found in the IFC schema examined during the preliminary audit; the main issue is semantic applicability, not spelling.
- The live dictionary is reported by the user as Active, while both local JSON files say `Preview`.
- The Italian source lacks `LanguageOnly`; both files omit a top-level empty `Properties` array present in the current import template.
- Copyright, permission to translate and redistribute UNI content, dictionary naming, and the declared `CC BY-SA 4.0` licence require resolution before paid verification.

## Agreed conceptual decision

UNI 8290 and IFC 4.3.2 can be combined, but they are not equivalent taxonomies:

- IFC describes the modelled object, system, or assembly.
- UNI 8290 classifies its function within the building technological system.
- The relationship is controlled many-to-many.
- Level 1 should generally use one or a few broad, defensible IFC concepts.
- Level 2 should generally use a system, assembly, or controlled entity family.
- Level 3 should generally use exact IFC occurrence entities or a small directly applicable family.
- Classes that genuinely combine networks, fittings, terminals, or machines may need several IFC entities, but each selection requires a direct semantic justification.

The acceptance question for every mapping is:

> Can an instance of this IFC entity itself honestly receive this UNI code in the context of the full UNI parent path?

If it is only a possible component, connector, support, or participant in a larger system, it should normally be excluded.

## Phase status

| ID | Phase | State | Evidence / continuation point |
|---|---|---|---|
| P00 | Research, preliminary audit, and plan | completed | This folder, the findings above, and `REFACTOR_PLAN.md` |
| P01 | Normalize and validate all UNI classes | completed | `refactor/inventory/uni8290-classes.csv`, `.json`, `p01-structural-report.md`; `refactor/tests/p01-structural-tests.json`; 117 rows; zero hard failures; source hashes unchanged |
| P02 | Build complete IFC 4.3.2 entity catalogue | completed | `refactor/inventory/ifc432-entities.csv`, `ifc432-types.csv`, `ifc432-catalogue.json`, `p02-ifc432-catalogue-report.md`; `refactor/tests/p02-ifc432-catalogue-tests.json`; 876 entities, 436 types, 225 technically eligible occurrences, zero hard failures |
| P03 | Define and encode mapping rules | completed | `refactor/mapping-rules.json`, `docs/uni8290-bsdd-refactor/decisions.md`, `refactor/tools/validate_mapping_rules.py`, and `refactor/tests/p03-mapping-rules-tests.json`; 9 tests passed, zero hard failures |
| P04 | Produce exhaustive UNI-to-IFC decision matrix | completed | `refactor/mapping-proposals.json`, `mapping-decisions.csv/.json`, `mapping-coverage.csv`, `p04-mapping-matrix-report.md`, and `p04-mapping-matrix-tests.json`; 117 UNI decisions, 876 IFC outcomes, zero hard failures; refreshed after AI assessment |
| P05 | Human review of mapping matrix by functional branch | in_progress | AI assessed 29 non-high-confidence decisions; 17 resolved, 12 require owner/domain input; no branch may be approved solely by automated tests or AI assessment |
| P06 | Create protected versioned working JSON copies | pending | Not started |
| P07 | Apply approved mapping refactor | pending | Not started |
| P08 | Repair definitions and English translation | pending | Not started; permission/source distinction unresolved |
| P09 | Run structural, schema, hierarchy, translation, and mapping tests | pending | Not started |
| P10 | Run full buildingSMART checklist audit | pending | Preliminary audit exists; final refactored audit not started |
| P11 | Optional bSDD Preview dry run | pending | Requires user authorization and access |

## External primary references already identified

- UNI 8290-1 official catalogue summary: <https://conto.uni.com/uni-8290-1-1981-a122-1983>
- Official IFC 4.3.2.0 documentation: <https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/>
- bSDD data structure and `RelatedIfcEntityNamesList`: <https://technical.buildingsmart.org/services/bsdd/data-structure/>
- buildingSMART dictionary guidelines: <https://technical.buildingsmart.org/services/bsdd/guidelines/>
- Detailed verification procedure: <https://github.com/buildingSMART/bSDD/blob/master/Documentation/bSDD%20verification%20procedure.md>
- IFC Classification Association: <https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/concepts/Object_Association/Classification_Association/content.html>

## P02 evidence and decisions

- Generator: `refactor/tools/build_ifc432_catalogue.py`.
- Pinned official release: IFC 4.3.2.0 / IFC4X3_ADD2.
- Pinned repository commit: `3ddf36033cd503acd2f6e06dd3923940a3950914`.
- Parsed EXPRESS schema identifier: `IFC4X3_DEV_60a6175`.
- Parsed totals: 876 entities, 436 types, 48 functions, and 2 rules.
- Every EXPRESS entity has a matching official documentation page and every direct parent resolves.
- Eligibility screening retains 225 occurrence entities for semantic review; abstract entities,
  type entities, relationships, property definitions, contexts, and resource entities are excluded.
- Four eligible occurrences are deprecated and carry an explicit warning.
- `IfcGridPlacement` is the sole entity without a parseable short-definition block in the official
  generated page. It is ineligible as a resource/placement concept, so this warning does not block P02.
- Full provenance, SHA-256 hashes, category counts, and tests are recorded in
  `refactor/inventory/p02-ifc432-catalogue-report.md`.

## P03 evidence and decisions

- Machine-readable policy: `refactor/mapping-rules.json`.
- Human-readable decisions: `docs/uni8290-bsdd-refactor/decisions.md`.
- The policy contains eight mandatory selection gates, 21 unique selection/rejection/screening
  reason codes, level-specific scope guidance, and one branch rule for each of the eight UNI roots.
- Full hierarchy is a required mapping input; empty mappings are explicitly permitted when IFC has
  no honest direct equivalent.
- The first validation run correctly rejected three nonexistent IFC 4.3.2 entity names
  (`IfcCeiling`, `IfcFence`, and `IfcGate`). They were removed and replaced by valid entity plus
  role/PredefinedType guidance.
- Final command: `python refactor/tools/validate_mapping_rules.py`.
- Final result: 9 tests passed, zero hard failures, all preferred IFC family names exist among the
  876 parsed entities.

## P04 evidence and decisions

- Semantic proposal source: `refactor/mapping-proposals.json`.
- Generated decision matrix: `refactor/inventory/mapping-decisions.csv` and `.json`.
- Inverse schema screening: `refactor/inventory/mapping-coverage.csv`.
- Final command: `python refactor/tools/build_mapping_matrix.py`.
- All 117 UNI classes have exactly one draft decision and all 876 IFC entities have exactly one
  screening outcome.
- All 3,603 current assignments were explicitly selected or rejected; the current draft has 231
  assignments to 74 unique eligible IFC occurrences.
- Four aggregate UNI classes intentionally have empty mappings rather than false proxy mappings.
- Confidence distribution: 88 high, 22 medium, and 7 domain-review-required.
- All P04 hard tests pass and no proposal exceeds the mapping-cardinality warning threshold.
- Original-source hashes were rechecked after P04 and remain identical to the protected baseline.

## Next action

Obtain P05 review: the user/domain expert must resolve the 12 open decisions and approve or
revise all eight functional branches. Approval is required
before P06 working copies and P07 mappings may be treated as approved.

## P05 preparation evidence and current gate

- Review packet: `docs/uni8290-bsdd-refactor/P05_BRANCH_REVIEW.md`.
- Machine-readable state: `refactor/review/branch-review-status.json`.
- Generator: `refactor/tools/build_branch_review.py`.
- Tests: `refactor/tests/p05-review-packet-tests.json`; four tests passed, zero hard failures.
- The packet contains all eight branches and all 117 UNI decisions.
- The 2026-11-11 AI assessment in `refactor/review/p05-ai-assessment.json` covers all 29 originally
  non-high-confidence decisions: 13 accepted, 4 revised, and 12 left for the owner/domain expert.
- Revisions: `1.2.3` only `IfcElementAssembly`; `5.5.2` only `IfcDuctSegment`; `7.1.1` only
  `IfcFurniture`; `8.0.0` retained `IfcFurnishingElement` with a narrower, explicit condition.
- The current draft has 231 selected IFC assignments. `build_mapping_matrix.py` and
  `build_branch_review.py` passed with zero hard failures; the packet contains all 117 UNI rows,
  17 AI-assessed resolutions, and 12 open questions.
- Protected-source SHA-256 hashes rechecked on 2026-11-11 and match the planning baseline.
- Each branch state is `awaiting_user_or_domain_expert_approval`; no automated or AI-only approval
  has been recorded.
- P06 and P07 are gated by P05. Do not create working JSON copies or apply the draft mappings until
  the user/domain reviewer approves or revises the branches and that evidence is written to the
  status JSON.

## Exact continuation point

Ask the user/domain reviewer to answer the 12 open questions in `P05_BRANCH_REVIEW.md` and
approve or revise the eight branch tables. Apply revisions to `refactor/mapping-proposals.json`,
rerun `build_mapping_matrix.py` and `build_branch_review.py`, and record reviewer/date/evidence
for approved branches. When all eight branches are explicitly approved and P03–P05 tests still
pass, mark P05 completed and begin P06.
