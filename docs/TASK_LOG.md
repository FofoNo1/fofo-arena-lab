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
