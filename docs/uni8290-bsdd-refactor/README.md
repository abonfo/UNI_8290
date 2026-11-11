# UNI 8290 bSDD refactoring workspace

This folder is the durable project record for the planned refactoring of the UNI 8290 bSDD dictionary against IFC 4.3.2 and the buildingSMART detailed-verification checklist.

## Required reading order

Any person or AI agent continuing the work must read these files before inspecting or modifying the dictionary:

1. [`AI_HANDOFF.md`](AI_HANDOFF.md) — operating rules, current checkpoint, completed work, and next action.
2. [`REFACTOR_PLAN.md`](REFACTOR_PLAN.md) — objectives, mapping policy, implementation phases, tests, and deliverables.
3. [`decisions.md`](decisions.md) — durable semantic mapping decisions and exclusions.
4. [`P05_BRANCH_REVIEW.md`](P05_BRANCH_REVIEW.md) — complete eight-branch semantic review packet.

The handoff file is the authoritative record of execution status. The plan is the authoritative description of the intended workflow.

## Protected source files

The following files are the original published source and must not be edited during the refactoring:

- `../../UNI-8290-PBS.json`
- `../../UNI-8290-PBS-en-GB.json`

All generated inventories, reports, decision matrices, scripts, and refactored JSON files must be created separately.

## Current state

Implementation is authorized. P01 through P04 are complete. P05 AI assessment resolved 17 of 29
non-high-confidence decisions and left 12 questions for the owner/domain expert. All eight
branches still await explicit semantic approval. Do not begin P06 or apply the draft mappings
until that approval and any revisions are recorded in
`../../refactor/review/branch-review-status.json`.
