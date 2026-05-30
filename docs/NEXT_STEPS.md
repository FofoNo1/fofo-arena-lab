# Next Steps

This file defines the current next steps for FOFO Arena Lab.

## Current project phase

Parser-output exploration phase.

The project is still not ready for fixed architecture, final FOFO data contracts, parser adapters, resolver classes, analysis modules, viewer integration, or machine-learning work.

The first parser-output milestone is complete and has expanded into variance exploration:

- subtr-actor is available as an external submodule.
- Python .venv is working with Python 3.13.
- subtr_actor imports successfully.
- The built-in 2v2 replay fixture was parsed successfully.
- First output shapes and counts were documented.
- Source/schema and output field references were documented.
- Fixture variance was explored.
- Modern/local 2v2 replay variance was explored through ignored local_data inputs.
- The variance probe now derives team counts from get_replay_frames_data()["meta"]["team_zero"] and ["team_one"].

## Immediate next step

Draft a minimal "FOFO Normalized Replay V0" documentation proposal from the
completed questions document and the Issue #3 source-boundary decision.

This must remain documentation-first. It must cite parser source areas, preserve
raw/nullable/variant parser evidence, and avoid turning observed fields into a
stable FOFO data contract too early.

Use these existing documents as the immediate inputs:

- `docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md`
- `docs/FOFO_NORMALIZED_REPLAY_V0_SOURCE_BOUNDARY.md`

## Suggested next file

docs/FOFO_NORMALIZED_REPLAY_V0.md

## Suggested next branch

Create a new branch for the V0 draft after the source-boundary decision is
merged:

codex/normalized-replay-v0-draft

## Do not do yet

- Do not create final FOFO data contracts.
- Do not create parser adapters.
- Do not create resolver classes.
- Do not build analysis modules.
- Do not build viewer integration.
- Do not start machine-learning work.
- Do not commit replay files.
- Do not commit generated parser dumps, generated local summaries, matrices, or full frame arrays.
- Do not commit local_data/.
- Do not modify external/subtr-actor.
- Do not treat heuristic stats as absolute truth.
- Do not use Ballchasing as a required runtime dependency.

## Next likely agent task

Ask Codex to draft `docs/FOFO_NORMALIZED_REPLAY_V0.md` as a minimal
documentation proposal.

The task must not define a final schema, parser adapter, resolver API, analysis
logic, viewer logic, ML logic, or stable FOFO data contract.
