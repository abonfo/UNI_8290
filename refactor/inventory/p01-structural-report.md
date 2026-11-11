# P01 — UNI 8290 normalized inventory and structural report

This report is generated from the two protected source JSON files. It does not modify them.

## Source integrity

- `UNI-8290-PBS.json`: `C8A79D7EC9A0F5DCBC289E0DC7B9FE07A4E8900F6B9FD803B7EFE356C42BCE85`
- `UNI-8290-PBS-en-GB.json`: `EE49386F56CA523FDC43C1102287001E79FDC16270147F36A41BE99939E4AB8B`

## Inventory summary

- Normalized classes: **117**
- Level 1: **8**
- Level 2: **30**
- Level 3: **79**
- Italian definitions missing: **79**
- English definitions missing: **79**
- English names identical to Italian: **113**
- Non-empty English definitions identical to Italian: **36**

## Structural checks

| Check | Result | Detail |
|---|---|---|
| `source_hash_UNI-8290-PBS.json` | **pass** | SHA-256 C8A79D7EC9A0F5DCBC289E0DC7B9FE07A4E8900F6B9FD803B7EFE356C42BCE85 |
| `source_hash_UNI-8290-PBS-en-GB.json` | **pass** | SHA-256 EE49386F56CA523FDC43C1102287001E79FDC16270147F36A41BE99939E4AB8B |
| `json_parse` | **pass** | Both protected source files parsed as JSON objects with Classes lists |
| `it_class_count` | **pass** | 117 |
| `en_class_count` | **pass** | 117 |
| `it_unique_codes` | **pass** | [] |
| `en_unique_codes` | **pass** | [] |
| `language_code_coverage` | **pass** | IT-only=[]; EN-only=[] |
| `parent_existence` | **pass** | [] |
| `hierarchy_cycles` | **pass** | [] |
| `code_pattern` | **pass** | [] |
| `level_counts` | **pass** | {1: 8, 2: 30, 3: 79} |
| `parent_code_convention` | **pass** | [] |
| `italian_definitions` | **warning** | Missing 79: ['1.1.1', '1.1.2', '1.2.1', '1.2.2', '1.2.3', '1.3.1', '1.3.2', '2.1.1', '2.1.2', '2.2.1', '2.2.2', '2.3.1', '2.4.1', '2.4.2', '3.1.1', '3.1.2', '3.1.3', '3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.3.2', '4.1.1... |
| `english_definitions` | **warning** | Missing 79: ['1.1.1', '1.1.2', '1.2.1', '1.2.2', '1.2.3', '1.3.1', '1.3.2', '2.1.1', '2.1.2', '2.2.1', '2.2.2', '2.3.1', '2.4.1', '2.4.2', '3.1.1', '3.1.2', '3.1.3', '3.2.1', '3.2.2', '3.2.3', '3.3.1', '3.3.2', '4.1.1... |
| `english_translation_names` | **warning** | Identical to Italian 113: ['1.2.0', '1.2.1', '1.2.2', '1.2.3', '1.3.0', '1.3.1', '1.3.2', '2.0.0', '2.1.0', '2.1.1', '2.1.2', '2.2.0', '2.2.1', '2.2.2', '2.3.0', '2.3.1', '2.4.0', '2.4.1', '2.4.2', '3.0.0', '3.1.0', '... |
| `english_translation_definitions` | **warning** | Identical non-empty definitions 36: ['1.2.0', '1.3.0', '2.0.0', '2.1.0', '2.2.0', '2.3.0', '2.4.0', '3.0.0', '3.1.0', '3.2.0', '3.3.0', '4.0.0', '4.1.0', '4.2.0', '4.3.0', '5.0.0', '5.1.0', '5.2.0', '5.3.0', '5.4.0', ... |
| `duplicate_ifc_mappings_within_class` | **pass** | [] |

## Parent-path anomaly

No parent-path anomaly detected.

## Hierarchy-dependent duplicate names

Duplicate labels are recorded for context-aware interpretation and are not treated as structural errors.

| Italian name | Codes |
|---|---|
| Alimentazione | `5.1.1`, `5.4.1`, `5.7.1`, `5.8.1`, `5.9.1`, `6.4.1` |
| Allacciamenti | `5.2.1`, `5.6.1`, `5.7.2`, `6.1.1` |
| Allarmi | `6.1.4`, `6.4.4` |
| Canne di esalazione | `5.1.6`, `5.5.2` |
| Dispersori | `6.2.2`, `6.3.3` |
| Elementi di protezione | `3.1.3`, `4.1.1` |
| Macchine | `5.4.2`, `5.8.2`, `5.9.2` |
| Rete | `6.3.2`, `6.4.3` |
| Reti di distribuzione e terminali | `5.1.4`, `5.6.2`, `5.7.4`, `5.8.3`, `6.1.3` |
| Rilevatori e trasduttori | `6.1.2`, `6.4.2` |

## Missing definitions by first-level branch

- Branch 1: 7 — `1.1.1`, `1.1.2`, `1.2.1`, `1.2.2`, `1.2.3`, `1.3.1`, `1.3.2`
- Branch 2: 7 — `2.1.1`, `2.1.2`, `2.2.1`, `2.2.2`, `2.3.1`, `2.4.1`, `2.4.2`
- Branch 3: 8 — `3.1.1`, `3.1.2`, `3.1.3`, `3.2.1`, `3.2.2`, `3.2.3`, `3.3.1`, `3.3.2`
- Branch 4: 6 — `4.1.1`, `4.1.2`, `4.2.1`, `4.2.2`, `4.3.1`, `4.3.2`
- Branch 5: 35 — `5.1.1`, `5.1.2`, `5.1.3`, `5.1.4`, `5.1.5`, `5.1.6`, `5.2.1`, `5.2.2`, `5.2.3`, `5.2.4`, `5.2.5`, `5.2.6`, `5.2.7`, `5.2.8`, `5.3.1`, `5.3.2`, `5.3.3`, `5.3.4`, `5.4.1`, `5.4.2`, `5.4.3`, `5.5.1`, `5.5.2`, `5.6.1`, `5.6.2`, `5.7.1`, `5.7.2`, `5.7.3`, `5.7.4`, `5.8.1`, `5.8.2`, `5.8.3`, `5.9.1`, `5.9.2`, `5.9.3`
- Branch 6: 13 — `6.1.1`, `6.1.2`, `6.1.3`, `6.1.4`, `6.2.1`, `6.2.2`, `6.3.1`, `6.3.2`, `6.3.3`, `6.4.1`, `6.4.2`, `6.4.3`, `6.4.4`
- Branch 7: 1 — `7.1.1`
- Branch 8: 2 — `8.2.1`, `8.2.2`

## Generated artifacts

- `uni8290-classes.csv` — tabular normalized inventory.
- `uni8290-classes.json` — machine-readable normalized inventory.
- `../tests/p01-structural-tests.json` — machine-readable structural test results.
