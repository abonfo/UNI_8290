# P02 — IFC 4.3.2 exhaustive entity catalogue

Release: **IFC 4.3.2.0 (IFC4X3_ADD2) official**

## Reproducible provenance

- Official documentation: <https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/>
- Normative Annex A: <https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/annex-a.html>
- Official output repository: <https://github.com/buildingSMART/IFC4.3.x-output-2>
- Repository commit: `3ddf36033cd503acd2f6e06dd3923940a3950914`
- EXPRESS repository path: `IFC/RELEASE/IFC4_3/IFC4X3_DEV_60a6175.exp`
- EXPRESS blob SHA: `67f77d54c39aa6889918483268feaf892b44af0a`
- EXPRESS schema identifier: `IFC4X3_DEV_60a6175`
- Local EXPRESS SHA-256: `E1524D66A7BE3FBBE2D1AF58588A0E15C3898E9633F095B9AAA7D55DD6052E1D`
- Documentation archive SHA-256: `9F0E928ACB8BE9BAAD4DC33F5AAE0C12ADBAB9C92BAD28A6EB20D38EF503BB0A`

The official static documentation labels the release IFC 4.3.2.0 / IFC4X3_ADD2. Its generated EXPRESS schema retains the internal identifier `IFC4X3_DEV_60a6175`; both identifiers are recorded to avoid silently conflating release labels.

## Parsed schema totals

- Entities: **876**
- Types: **436**
- Functions: **48**
- Rules: **2**

## Entity categories

| Category | Count |
|---|---:|
| `context` | 3 |
| `object_occurrence` | 253 |
| `object_type` | 158 |
| `property_definition` | 17 |
| `relationship` | 51 |
| `resource_or_other` | 392 |
| `root_other` | 2 |

## Mapping eligibility screening

| Result | Count |
|---|---:|
| `eligible_occurrence_or_system` | 221 |
| `eligible_with_deprecation_warning` | 4 |
| `ineligible_abstract` | 133 |
| `ineligible_context` | 2 |
| `ineligible_ifc_type_entity` | 139 |
| `ineligible_property_definition` | 11 |
| `ineligible_relationship` | 45 |
| `ineligible_resource_or_other` | 321 |

Eligibility means technically suitable for further UNI semantic review. It does not mean the entity must be mapped.

## Source domains

| IFC schema/domain | Entity count |
|---|---:|
| `IfcActorResource` | 8 |
| `IfcApprovalResource` | 3 |
| `IfcArchitectureDomain` | 5 |
| `IfcBuildingControlsDomain` | 12 |
| `IfcConstraintResource` | 5 |
| `IfcConstructionMgmtDomain` | 14 |
| `IfcControlExtension` | 3 |
| `IfcCostResource` | 3 |
| `IfcDateTimeResource` | 14 |
| `IfcElectricalDomain` | 50 |
| `IfcExternalReferenceResource` | 11 |
| `IfcGeometricConstraintResource` | 16 |
| `IfcGeometricModelResource` | 48 |
| `IfcGeometryResource` | 75 |
| `IfcHvacDomain` | 66 |
| `IfcKernel` | 49 |
| `IfcMaterialResource` | 18 |
| `IfcMeasureResource` | 11 |
| `IfcPlumbingFireProtectionDomain` | 10 |
| `IfcPortsAndWaterwaysDomain` | 10 |
| `IfcPresentationAppearanceResource` | 46 |
| `IfcPresentationDefinitionResource` | 6 |
| `IfcPresentationOrganizationResource` | 10 |
| `IfcProcessExtension` | 11 |
| `IfcProductExtension` | 82 |
| `IfcProfileResource` | 28 |
| `IfcPropertyResource` | 14 |
| `IfcQuantityResource` | 10 |
| `IfcRailDomain` | 6 |
| `IfcRepresentationResource` | 21 |
| `IfcRoadDomain` | 4 |
| `IfcSharedBldgElements` | 45 |
| `IfcSharedBldgServiceElements` | 26 |
| `IfcSharedComponentElements` | 10 |
| `IfcSharedFacilitiesElements` | 7 |
| `IfcSharedInfrastructureElements` | 18 |
| `IfcSharedMgmtElements` | 5 |
| `IfcStructuralAnalysisDomain` | 28 |
| `IfcStructuralElementsDomain` | 23 |
| `IfcStructuralLoadResource` | 20 |
| `IfcTopologyResource` | 20 |
| `IfcUtilityResource` | 5 |

## Catalogue validation

| Check | Result | Detail |
|---|---|---|
| `express_sha256` | **pass** | E1524D66A7BE3FBBE2D1AF58588A0E15C3898E9633F095B9AAA7D55DD6052E1D |
| `documentation_archive_sha256` | **pass** | 9F0E928ACB8BE9BAAD4DC33F5AAE0C12ADBAB9C92BAD28A6EB20D38EF503BB0A |
| `schema_identifier` | **pass** | IFC4X3_DEV_60a6175 |
| `entity_count` | **pass** | 876 |
| `type_count` | **pass** | 436 |
| `unique_entity_names` | **pass** | [] |
| `unique_type_names` | **pass** | [] |
| `parent_resolution` | **pass** | [] |
| `documentation_page_coverage` | **pass** | [] |
| `short_definition_coverage` | **warning** | Missing 1: ['IfcGridPlacement'] |
| `predefined_enum_resolution` | **pass** | [] |
| `documentation_non_entity_pages` | **info** | Lexical IFC pages not declared as ENTITY: 486 |

## Missing short semantic definitions

The following official entity pages did not expose a parseable short-definition block and require manual review: `IfcGridPlacement`

## Generated artifacts

- `ifc432-entities.csv` — exhaustive entity catalogue and eligibility screening.
- `ifc432-types.csv` — exhaustive EXPRESS type catalogue, including enumerations.
- `ifc432-catalogue.json` — combined machine-readable catalogue and provenance.
- `../tests/p02-ifc432-catalogue-tests.json` — machine-readable tests.
