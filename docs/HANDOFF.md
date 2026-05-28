# Handoff

This file is the compact handoff for continuing FOFO Arena Lab in a new chat or with another agent.

## Project identity

Project name: FOFO Arena Lab

Claim: Replay Intelligence by Kapautz

Repository: FofoNo1/fofo-arena-lab

## Core goal

.replay in -> context-aware Rocket League analysis out

The project should not judge isolated statistics. It should evaluate gameplay decisions in the context of the full game situation.

## Current project phase

Parser-output exploration phase.

The repository contains the initial README, German/English project definitions, agent instructions, handoff files, subtr-actor exploration docs, and first parser probe results.

The project intentionally avoids fixed data structures, classes, or modules until real parser output has been inspected.

## Current guiding principle

Understand the data first.
Build structure second.
Develop analysis third.
Visualize and expand afterwards.

## Initial focus

- First visible analysis focus: 2v2 replay analysis
- Long-term direction: expandable context-aware analysis for 2v2 and 3v3
- Positive gameplay decisions should be identified alongside mistakes

## Current technical state

- Branch: codex/parser-output-exploration
- external/subtr-actor is added as a Git submodule.
- Submodule version observed: v0.12.0
- Local .venv with Python 3.13 works.
- subtr-actor-py was installed from external/subtr-actor/python.
- subtr_actor imports successfully.
- First parser probe against the built-in ranked doubles fixture succeeded.

## Important probe result

Fixture:

external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay

Observed output summary:

- get_replay_meta returned column_headers and replay_meta.
- parse_replay returned low-level replay keys.
- get_replay_frames_data returned structured replay data.
- frame_data contains ball_data, metadata_frames, and players.
- metadata_frames: 9530
- players: 4
- touch_events: 113
- goal_events: 5
- demolish_infos: 2
- boost_pads: 34
- boost_pad_events: 1581
- get_stats_module_names returned 45 stat module names.

## Current setup files

- README.md
- AGENTS.md
- docs/HANDOFF.md
- docs/NEXT_STEPS.md
- docs/TASK_LOG.md
- docs/SUBTR_ACTOR_EXPLORATION.md
- docs/SUBTR_ACTOR_FIRST_PROBE_PLAN.md
- docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md
- docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md

## Important constraints

- Do not overdesign upfront.
- Do not invent fixed data models before parser output is known.
- Do not commit private replay files or heavy generated parser outputs.
- Do not commit secrets, tokens, company data, or personal data.
- Do not modify external/subtr-actor.
- Keep changes small and reviewable.

## Next recommended step

Create a temporary local probe script:

scripts/probes/inspect_subtr_output.py

Purpose:

- inspect nested field structures
- print keys, counts, value types, and small samples
- avoid full dumps
- keep it exploratory
- do not define FOFO data contracts yet

## How to continue in a new chat

Tell the assistant:

We are working on FOFO Arena Lab. Please use the GitHub repository FofoNo1/fofo-arena-lab and follow README.md, AGENTS.md, docs/HANDOFF.md, and docs/NEXT_STEPS.md. Continue from the parser-output exploration phase and do not overdesign before parser output has been fully inspected.
