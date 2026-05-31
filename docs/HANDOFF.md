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

The repository has moved past the first parser probe, but it is still intentionally before stable FOFO data contracts, parser adapters, resolver classes, analysis modules, viewer integration, or machine-learning work.

The project intentionally avoids fixed data structures, classes, modules, and long-term architecture until real parser output and replay variance have been inspected.

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

- Current clean base after merge: main
- Current work topic: Normalized Replay V0 source boundary decision
- external/subtr-actor is added as a Git submodule and must stay read-only.
- Submodule version observed: v0.12.0.
- Local .venv with Python 3.13 works.
- subtr-actor-py was installed from external/subtr-actor/python.
- subtr_actor imports successfully.
- The built-in ranked-doubles fixture was parsed successfully.
- Repeatable parser probes exist under scripts/probes/.
- local_data/ is ignored and contains local replay inputs and generated local summaries only.

## Completed parser exploration

Completed work now includes:

- first parser probe against the built-in ranked-doubles fixture
- source/schema mapping of subtr-actor outputs
- output field reference for observed parser structures
- fixture variance exploration across subtr-actor replay fixtures
- modern/local 2v2 replay variance exploration using ignored local_data inputs
- corrected variance probe team counting from get_replay_frames_data()["meta"]["team_zero"] and ["team_one"]
- `docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md`, a questions-only document for unresolved V0 modeling decisions
- Issue #3 source-boundary decision in `docs/FOFO_NORMALIZED_REPLAY_V0_SOURCE_BOUNDARY.md`
- Issue #5 parser evidence summary in `docs/FOFO_NORMALIZED_REPLAY_V0_PARSER_EVIDENCE_SUMMARY.md`
- bounded V0 parser evidence probe in `scripts/probes/summarize_v0_parser_evidence.py`

## Key evidence so far

- get_replay_frames_data top-level keys have been stable in inspected samples.
- frame_data contains ball_data, metadata_frames, and players.
- metadata_frames, ball_data.frames, and player frame arrays aligned in tested samples.
- Replay meta team arrays, meta.team_zero and meta.team_one, are important player/team identity anchors.
- PlayerFrame.Data.team is unreliable/null in current tested modern replays.
- PlayerFrame.Data.is_team_0 is more useful for frame-level team-side information.
- touch_events.player and boost_pad_events.player can be null.
- goal_events.player can be null in some fixture variance.
- BallFrame and PlayerFrame can appear as Data or Empty variants.
- Rigid-body velocity fields can be null.
- Event streams can be empty and should not be treated as missing parser output.

## Current project files to read

- README.md
- AGENTS.md
- docs/HANDOFF.md
- docs/NEXT_STEPS.md
- docs/TASK_LOG.md
- docs/SUBTR_ACTOR_EXPLORATION.md
- docs/SUBTR_ACTOR_FIRST_PROBE_PLAN.md
- docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md
- docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md
- docs/SUBTR_ACTOR_OUTPUT_FIELD_REFERENCE.md
- docs/SUBTR_ACTOR_FIXTURE_VARIANCE_REPORT.md
- docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md
- docs/FOFO_NORMALIZED_REPLAY_V0_SOURCE_BOUNDARY.md
- docs/FOFO_NORMALIZED_REPLAY_V0_PARSER_EVIDENCE_SUMMARY.md
- scripts/probes/inspect_subtr_output.py
- scripts/probes/inspect_modern_replay_variance.py
- scripts/probes/summarize_v0_parser_evidence.py
- scripts/probes/ballchasing_download_recent_2v2_replays.py

## Important constraints

- Do not overdesign upfront.
- Do not invent fixed data models before parser output is understood.
- Do not create FOFO contracts, adapters, resolver classes, analysis logic, viewer logic, or ML logic yet.
- Do not commit private replay files or heavy generated parser outputs.
- Do not commit secrets, tokens, company data, or personal data.
- Do not modify external/subtr-actor.
- Keep changes small and reviewable.

## Next recommended step

Draft a minimal `docs/FOFO_NORMALIZED_REPLAY_V0.md` documentation proposal from
the completed V0 questions document, the Issue #3 source-boundary decision, and
the Issue #5 parser evidence summary.

The draft should use `get_replay_frames_data` as the primary initial parser
source boundary, `get_replay_meta` as supporting evidence, and keep
`parse_replay`, ndarray outputs, stats timelines, JS viewer models, and
heuristic analysis outputs outside the normal initial V0 boundary.

## How to continue in a new chat

Tell the assistant:

We are working on FOFO Arena Lab. Follow README.md, AGENTS.md, docs/HANDOFF.md, docs/NEXT_STEPS.md, and docs/TASK_LOG.md. Continue from the parser-output exploration phase. Do not overdesign before parser output and replay variance are understood. The V0 questions document and Issue #3 source-boundary decision now exist; next, draft a minimal Normalized Replay V0 documentation proposal without creating schemas, adapters, resolvers, analysis logic, viewer logic, or ML logic.
