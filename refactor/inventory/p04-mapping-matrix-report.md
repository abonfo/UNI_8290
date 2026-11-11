# P04 — Draft exhaustive UNI-to-IFC mapping matrix

This is a semantic-review draft, not an approved mapping set. All 117 records remain `pending` for P05 branch review.

## Totals

- UNI decisions: **117** (levels {1: 8, 2: 30, 3: 79})
- Current mapping assignments dispositioned: **3603**
- Proposed mapping assignments: **231**
- UNI decisions with an intentionally empty proposal: **4**
- Unique selected IFC entities: **73**
- IFC entities screened: **876**

## Confidence

- `domain_review_required`: 7
- `high`: 88
- `medium`: 22

## IFC inverse screening

- `SCR_NOT_APPLICABLE`: 152
- `SCR_SELECTED`: 73
- `SCR_TECHNICALLY_INELIGIBLE`: 651

## Most frequent proposed IFC entities

| IFC entity | UNI decisions |
|---|---:|
| `IfcSlab` | 16 |
| `IfcDistributionSystem` | 15 |
| `IfcPipeSegment` | 15 |
| `IfcCableSegment` | 14 |
| `IfcPipeFitting` | 14 |
| `IfcWall` | 9 |
| `IfcDoor` | 8 |
| `IfcValve` | 6 |
| `IfcCableFitting` | 6 |
| `IfcRailing` | 5 |
| `IfcFlowMeter` | 5 |
| `IfcJunctionBox` | 5 |
| `IfcBuildingSystem` | 4 |
| `IfcWindow` | 4 |
| `IfcStair` | 4 |
| `IfcRamp` | 4 |
| `IfcDuctSegment` | 4 |
| `IfcWasteTerminal` | 4 |
| `IfcStackTerminal` | 3 |
| `IfcSanitaryTerminal` | 3 |

## Automated validation

| Check | Result | Detail |
|---|---|---|
| `proposal_code_coverage` | **pass** | {'missing': [], 'extra': []} |
| `decision_record_count` | **pass** | 117 |
| `unique_decision_codes` | **pass** | 117 |
| `selected_entities_exist` | **pass** | [] |
| `selected_entities_technically_eligible` | **pass** | [] |
| `selected_decisions_have_rationales` | **pass** | [] |
| `all_current_mappings_dispositioned` | **pass** | [] |
| `confidence_values_valid` | **pass** | [] |
| `ifc_coverage_count` | **pass** | 876 |
| `ifc_coverage_unique` | **pass** | 876 |
| `mapping_cardinality_review` | **pass** | [] |

## Review warning

Schema validity and exhaustive disposition do not constitute semantic approval. P05 must explicitly review each UNI branch, especially all `medium` and `domain_review_required` records.
