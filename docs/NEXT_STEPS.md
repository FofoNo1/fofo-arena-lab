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

Create a narrow document for "FOFO Normalized Replay V0 questions".

This must be a questions document only. It must not define a FOFO-owned schema, class model, adapter API, resolver API, analysis module, or stable data contract.

The document should capture unresolved modeling questions revealed by parser variance:

- active-player selection versus parser player tracks
- team identity reconciliation between meta.team_zero/team_one, player track ids, PlayerFrame.Data.is_team_0, and event team fields
- optional event attribution when player fields are null
- BallFrame and PlayerFrame Data/Empty variant handling
- frame/event alignment and how events should reference frame indices and time
- nullable rigid-body velocity fields
- boost amount units and boost pad event attribution
- empty event streams as valid parser output
- replay-version and playlist variance

## Suggested next file

docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md

## Suggested next branch

Continue on:

codex/parser-output-exploration

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

Ask Codex to create docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md as a concise unresolved-questions document.

The task should document questions only and must not define FOFO-owned stable field names, schemas, adapters, resolver classes, analysis logic, viewer logic, or ML logic.
