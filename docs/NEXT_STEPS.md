# Next Steps

This file defines the current next steps for FOFO Arena Lab.

## Current project phase

Parser-output exploration phase.

The project is still not ready for fixed architecture, final data contracts, analysis modules, viewer integration, or machine-learning work.

The first technical milestone is complete:

- subtr-actor is available as an external submodule.
- Python .venv is working with Python 3.13.
- subtr_actor imports successfully.
- The built-in 2v2 replay fixture was parsed successfully.
- First output shapes and counts were documented.

## Immediate next steps

1. Create a temporary local probe script for repeatable parser-output inspection.
2. Keep the script focused on inspection only.
3. Inspect nested structures from:
   - get_replay_meta
   - get_replay_frames_data
   - parse_replay
4. Print only:
   - keys
   - field names
   - value types
   - counts
   - small samples
5. Do not dump full frame arrays or large JSON outputs.
6. Document the discovered nested fields.
7. Only after that derive the first internal FOFO data structure.

## Suggested next file

scripts/probes/inspect_subtr_output.py

## Suggested next branch

Continue on:

codex/parser-output-exploration

## Do not do yet

- Do not create final FOFO data contracts.
- Do not build analysis modules.
- Do not build viewer integration.
- Do not start machine-learning work.
- Do not commit replay files.
- Do not commit generated full parser dumps.
- Do not modify external/subtr-actor.
- Do not treat heuristic stats as absolute truth.

## Next likely agent task

Ask Codex App to create a minimal temporary probe script that inspects subtr_actor output shapes from the built-in 2v2 fixture.

The script should be for exploration only and must not define FOFO-owned stable data models yet.
