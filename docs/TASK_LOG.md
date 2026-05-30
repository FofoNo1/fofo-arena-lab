# Task Log

This file records important project steps, decisions, and completed setup work for FOFO Arena Lab.

## 2026-05-28

### Repository initialized

- Created GitHub repository: FofoNo1/fofo-arena-lab
- Added public English README
- Added German and English project definition documents in docs/
- Confirmed repository is connected to local Git

### Project direction

- Project name: FOFO Arena Lab
- Claim: Replay Intelligence by Kapautz
- Goal: .replay in -> context-aware analysis out
- Initial focus: 2v2 replay analysis
- Long-term direction: expandable context-aware analysis for 2v2 and 3v3

### Important working principle

- Do not overdesign upfront.
- First parse real replay data.
- Then inspect and document parser output.
- Only after that derive internal data structures and analysis modules.

### Agent setup

- Added AGENTS.md for Codex, Gemini, and other agents.
- Added handoff and next-step documentation to make the project resilient against chat/context loss.

### Environment setup

- Added subtr-actor as external Git submodule under external/subtr-actor.
- Submodule points to subtr-actor v0.12.0.
- Added .gitattributes for stable line endings.
- Added .gitignore rules for local Codex app config and external dependency handling.
- Prepared local .venv with Python 3.13.
- Installed subtr-actor-py from external/subtr-actor/python in editable mode.
- Verified that subtr_actor imports successfully.

### subtr-actor exploration

- Added docs/SUBTR_ACTOR_EXPLORATION.md.
- Added docs/SUBTR_ACTOR_FIRST_PROBE_PLAN.md.
- Added docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md.
- Ran the first local probe against the built-in 2v2 fixture:
  external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay
- Added docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md.

### First probe result summary

The first local probe confirmed:

- subtr_actor can be imported locally.
- get_replay_meta works.
- parse_replay exposes low-level replay structure.
- get_replay_frames_data exposes structured replay/frame/event data.
- The built-in ranked doubles fixture is usable for FOFO's first 2v2 exploration.

Observed output included:

- 4 players
- 9530 metadata frames
- 113 touch events
- 5 goal events
- 2 demolish events
- 34 boost pads
- 1581 boost pad events
- 45 stat module names

## 2026-05-29

### Parser-output variance exploration

- Added repeatable parser-output probes under scripts/probes/ for bounded inspection only.
- Documented subtr-actor output shapes in docs/SUBTR_ACTOR_OUTPUT_FIELD_REFERENCE.md.
- Compared fixture variance in docs/SUBTR_ACTOR_FIXTURE_VARIANCE_REPORT.md.
- Explored modern/local 2v2 replay variance through ignored local_data inputs and reports.
- Confirmed that local_data/ remains ignored and must not be committed.

### Team identity correction

- Corrected the exploratory variance probe to derive team counts from get_replay_frames_data()["meta"]["team_zero"] and ["team_one"].
- Kept team_zero and team_one as list-shaped parser metadata, with safe fallback when missing.
- Added player-name display to generated local summaries when available, without committing those local reports.

### Current evidence

- get_replay_frames_data top-level shape has been stable in inspected samples.
- metadata_frames, ball_data.frames, and player frame arrays aligned in tested samples.
- meta.team_zero and meta.team_one are important team/player identity anchors.
- PlayerFrame.Data.team is unreliable/null in current tested modern replays.
- PlayerFrame.Data.is_team_0 is more useful for team-side information.
- touch_events.player and boost_pad_events.player can be null.
- BallFrame and PlayerFrame can use Data and Empty variants.

### Boundaries preserved

- No FOFO data contracts were created.
- No parser adapters or resolver classes were created.
- No analysis logic, viewer logic, or machine-learning logic was created.
- external/subtr-actor was not modified.
- Local replay files, local summaries, generated dumps, secrets, and tokens remain out of Git.

## 2026-05-30

### Issue #3: Normalized Replay V0 source boundary

- Added `docs/FOFO_NORMALIZED_REPLAY_V0_SOURCE_BOUNDARY.md` as a short decision note.
- Decided `get_replay_frames_data` is the initial primary V0 parser source boundary, with `get_replay_meta` as supporting evidence and `parse_replay` as audit/debug evidence only.
- Kept ndarray outputs, stats timelines, JS viewer models, heuristic analysis outputs, schemas, adapters, resolvers, parser logic, viewer logic, ML logic, replay files, generated dumps, `local_data/`, and `external/subtr-actor` out of scope.
