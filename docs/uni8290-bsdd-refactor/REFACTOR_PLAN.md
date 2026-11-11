---
document_type: implementation_plan
project: UNI 8290 bSDD to IFC 4.3.2 refactoring
plan_version: 1.0
created: 2026-08-10
implementation_started: true
status_file: AI_HANDOFF.md
---

# UNI 8290 bSDD refactoring plan

## Objective

Create a new, versioned, verification-ready Italian bSDD dictionary and English translation without modifying the published source JSON files. Reassess every UNI 8290 class against the complete official IFC 4.3.2 schema, replace component-based overmapping with hierarchy-aware direct mappings, and test the result against the current buildingSMART detailed-verification checklist.

## Non-goals and constraints

- Do not modify the original Italian or English JSON files.
- Do not assign every IFC entity to at least one UNI class. Exhaustive review and exhaustive assignment are different requirements.
- Do not flatten or rename the UNI hierarchy merely to make generic labels self-contained.
- Do not invent or reproduce copyrighted UNI definitions without distinguishing their provenance and confirming authorization.
- Do not activate or upload a new dictionary version without explicit user authorization.
- Do not represent a human semantic review as an automated pass.

## Source model interpretation

The official UNI summary describes three levels:

1. classes of technological units;
2. technological units;
3. classes of technical elements.

Generic third-level labels must be interpreted with their parent path. `5.7.2 Allacciamenti`, for example, means electrical-system connections, while `5.6.1 Allacciamenti` means gas-distribution connections.

IFC 4.3.2 is an object, system, assembly, process, and resource schema. UNI 8290 supplies a functional classification that can be associated with IFC objects or object types. The trees therefore support a controlled many-to-many relationship rather than a one-to-one translation.

## Mapping policy

### General rule

Map a UNI class to the closest eligible IFC entity or small entity family that directly represents the class in the context of its complete UNI path.

For every proposed pair, ask:

> Can an instance of this IFC entity itself honestly receive this UNI code?

Exclude an entity when the justification is only that it might be contained in, connected to, support, fasten, monitor, or otherwise participate in the corresponding system.

### Hierarchy strategy

| UNI level | Default strategy |
|---|---|
| Level 1 | One or a few broad, eligible IFC generalisations or system concepts |
| Level 2 | An IFC system, functional grouping, assembly, or controlled family |
| Level 3 | An exact IFC occurrence entity or small set of directly applicable entities |

The strategy is a default, not a numerical limit. A third-level class such as a combined distribution network and terminals may legitimately require several entities.

### Eligibility rules

A selected IFC mapping must:

- exist in the official IFC 4.3.2 schema;
- be semantically applicable to the complete UNI class path;
- not be an abstract entity;
- not be an IFC type entity, relationship, measure, select, enumeration, function, or rule;
- avoid deprecated occurrence entities when supported concrete replacements exist;
- avoid `USERDEFINED`, `NOTDEFINED`, and proxy-style choices when a proper entity exists;
- record necessary `PredefinedType`, property, or system-membership conditions that cannot be expressed in `RelatedIfcEntityNamesList` itself.

### Parent and child mappings

- A parent mapping is not automatically the union of all child mappings.
- A child is expected to be at least as semantically specific as its parent, but need not use a subtype of the parent's selected entity when IFC and UNI organize concepts differently.
- Repeated mappings across different UNI branches are acceptable when the same IFC entity can perform different functions. For example, `IfcWall` may be classified differently when load-bearing, enclosing, retaining, or partitioning.

## Implementation phases

### P01 — Normalize and validate the UNI inventory

Read both original JSON files and generate a normalized inventory for all 117 classes containing:

- code;
- hierarchy level;
- parent code;
- complete code and name path;
- Italian name and definition;
- English name and definition;
- current IFC mappings;
- field-presence flags;
- detected anomalies.

Required checks:

- valid JSON;
- exactly 117 unique codes in each language file;
- identical IT/EN code coverage;
- all parent codes exist;
- no hierarchy cycles;
- expected three-level code pattern;
- identify duplicate names without treating hierarchy-dependent duplicates as errors;
- confirm the proposed correction of `5.1.2`.

Acceptance criteria:

- normalized inventory artifact exists;
- all 117 classes are represented exactly once;
- structural test report exists;
- anomalies are recorded in `AI_HANDOFF.md`.

### P02 — Build the complete IFC 4.3.2 catalogue

Parse the official IFC 4.3.2.0 computer-interpretable schema and associated official semantic documentation.

For every entity, record:

- name;
- parent and inheritance chain;
- abstract status;
- deprecated status;
- schema/domain grouping;
- occurrence/type/relation/resource classification;
- `PredefinedType` enumeration where applicable;
- short official semantic definition;
- eligibility for `RelatedIfcEntityNamesList`;
- reason if ineligible.

Acceptance criteria:

- every IFC 4.3.2 entity appears once in the catalogue;
- entity count is reconciled with the parsed official schema;
- abstract, deprecated, type, relationship, measure, and other ineligible categories are testable;
- source URL and schema version are recorded.

### P03 — Encode the mapping rules

Create a documented, testable mapping policy based on the rules above. Include branch-specific interpretation rules for:

- structural and foundation elements;
- enclosures and partitions;
- building-service distribution systems;
- electrical and communications systems;
- fire, grounding, lightning, and anti-intrusion systems;
- internal and external equipment.

Acceptance criteria:

- mapping rules can be applied consistently by a later agent;
- exclusions and conditional matches have standard reason codes;
- hierarchy context is a required mapping input.

### P04 — Produce the exhaustive mapping decision matrix

Create one record for every UNI class containing:

| Field | Meaning |
|---|---|
| UNI code | Stable identifier |
| Full hierarchy | Context for the term |
| Functional interpretation | Meaning used for mapping |
| Current IFC mappings | Baseline |
| Candidate IFC entities | Candidates from the full catalogue |
| Selected IFC entities | Proposed final list |
| IFC conditions | Predefined type, system, or property context |
| Rejected current mappings | Mappings proposed for removal |
| Decision rationale | Direct match, component-only, unrelated, deprecated, etc. |
| Confidence | High, medium, or domain review required |
| Review state | Pending, approved, or revise |

Also create an inverse IFC coverage view showing every eligible IFC entity as selected or considered-not-applicable.

Acceptance criteria:

- all 117 UNI classes have a decision record;
- every IFC entity has been screened;
- no selected entity lacks a rationale;
- unresolved medium/low-confidence decisions are visible.

### P05 — Review mappings by functional branch

Review the matrix in eight batches:

1. load-bearing structures;
2. enclosures;
3. internal partitions;
4. external partitions;
5. building-service systems;
6. safety systems;
7. internal equipment;
8. external equipment.

Expected mapping patterns include:

- direct foundations → `IfcFooting`, possibly `IfcSlab` with `BASESLAB` context;
- indirect foundations → `IfcDeepFoundation`, `IfcPile`, `IfcCaissonFoundation`;
- HVAC technological unit → primarily `IfcDistributionSystem` with appropriate context;
- service networks → media-specific segments, fittings, and terminals;
- alarms → primarily `IfcAlarm`;
- external pavement → `IfcPavement`, with `IfcCovering` only for dependent finishes.

These are starting hypotheses, not pre-approved final mappings.

Acceptance criteria:

- each branch is explicitly approved or has recorded open decisions;
- no branch is silently accepted through automated similarity alone.

### P06 — Create versioned working copies

After mapping approval, create a separate working area such as:

```text
refactor/
├── UNI-8290-PBS-1.1-it-IT.json
└── UNI-8290-PBS-1.1-en-GB.json
```

Recommended working metadata:

- `DictionaryVersion`: `1.1`;
- `Status`: `Preview`;
- Italian file: `LanguageOnly: false`;
- English file: `LanguageOnly: true`;
- explicit empty `Properties` list if required by the current import model.

The Italian JSON is the authoritative dictionary. The English JSON should be a proper language-only payload containing identifiers and translatable content; non-translatable mappings should not be duplicated unless the current official import model specifically requires them.

Acceptance criteria:

- byte-level or hash evidence confirms originals are unchanged;
- working copies parse successfully;
- working version and translation roles are explicit.

### P07 — Apply the approved mapping refactor

Replace mappings in the authoritative Italian working copy using the approved matrix.

The edit must:

- cover every UNI code exactly once;
- preserve codes and approved hierarchy;
- remove component-based inherited unions;
- retain multiple mappings only where justified;
- keep mapping order deterministic;
- avoid unsupported schema entities.

Acceptance criteria:

- JSON mappings equal the approved decision matrix;
- no UNI class is lost;
- no selected IFC entity is missing or added without a matrix decision;
- mapping-frequency and outlier reports have been reviewed.

### P08 — Repair definitions and English translation

For every UNI class:

- preserve the official Italian name;
- use the full hierarchy when interpreting generic labels;
- add a definition when absent;
- distinguish official/authorized text from newly authored non-normative text;
- translate all names, definitions, descriptions, and synonyms faithfully;
- do not expand an English translation beyond the Italian source meaning.

Generic names may remain short because hierarchy supplies context. Their definitions must make that context explicit.

This phase is blocked from final completion until the provenance and permitted use of UNI definitions and translations are resolved.

Acceptance criteria:

- every Italian class has a definition;
- every translatable Italian field has an English counterpart;
- untranslated Italian text in the English file is either zero or explicitly justified;
- bilingual review findings are recorded.

### P09 — Automated validation

Run tests for:

- JSON syntax and current import-model structure;
- required dictionary and class fields;
- code uniqueness and format;
- IT/EN code-set equality;
- parent existence and absence of cycles;
- intended hierarchy depth and code pattern;
- complete definitions and translations;
- accidental Italian text in the English payload;
- mapping existence in IFC 4.3.2;
- abstract/type/relation/measure exclusion;
- deprecated-entity warnings;
- duplicate mappings within classes;
- selected mappings matching the decision matrix;
- mapping-count outliers by level;
- high-frequency entities across unrelated branches;
- suspicious generic components such as fasteners, plates, coverings, signs, and signals.

Mapping cardinality is a warning metric, not a hard quality rule.

Acceptance criteria:

- all hard tests pass;
- all warnings are either corrected or documented with rationale;
- test commands and results are recorded in `AI_HANDOFF.md`.

### P10 — Full detailed-verification audit

Assess the refactored version against:

- `GEN-01` through `GEN-12`;
- `DCT-01` and `DCT-02`;
- `CLS-01` through `CLS-05`;
- property, allowed-value, class-property, and explicit-relation controls as not applicable unless such objects are introduced.

The final report must separately identify:

- automated passes;
- semantic reviewer judgments;
- ownership and licensing evidence;
- unresolved risks;
- items requiring buildingSMART confirmation.

Acceptance criteria:

- checklist report exists with evidence per applicable control;
- no open blocker is described as passed;
- readiness recommendation is explicit.

### P11 — Optional bSDD Preview dry run

Only with explicit user authorization:

1. upload version 1.1 as Preview;
2. review import validation results;
3. inspect rendered hierarchy and translations;
4. test IFC-entity filtering and representative tool workflows;
5. correct only documented issues;
6. freeze the Preview submission;
7. request detailed verification;
8. activate only after a positive review.

## Planned artifacts

Exact formats may be adjusted before implementation, but the project should eventually contain:

```text
docs/uni8290-bsdd-refactor/
├── README.md
├── AI_HANDOFF.md
├── REFACTOR_PLAN.md
├── verification-report.md
└── decisions.md

refactor/
├── inventory/
│   ├── uni8290-classes.csv
│   ├── ifc432-entities.csv
│   ├── mapping-decisions.csv
│   └── mapping-coverage.csv
├── tests/
├── UNI-8290-PBS-1.1-it-IT.json
└── UNI-8290-PBS-1.1-en-GB.json
```

## Verification and legal gates

Before paid review, obtain or document:

- authority to reproduce the UNI hierarchy and definitions;
- authority to create and publish English translations;
- authority to redistribute the content through bSDD;
- permission or conditions for using `UNI 8290` as the dictionary name;
- an accurate content licence;
- a meaningful QA and governance procedure;
- a responsive professional change-request address.

These gates are independent of technical JSON validity.

## Definition of completion

The refactor is complete only when:

- originals remain unchanged;
- every UNI class has been reviewed and retained;
- the full IFC 4.3.2 entity catalogue has been screened;
- every selected mapping has a documented direct semantic justification;
- Italian definitions and English translations are complete and provenance-aware;
- all hard automated tests pass;
- the detailed-verification report contains no undisclosed blocker;
- `AI_HANDOFF.md` accurately records the final state and artifacts.
