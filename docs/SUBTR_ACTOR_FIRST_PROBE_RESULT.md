# subtr-actor First Probe Result

## Purpose

This document records the first local parser-output probe for FOFO Arena Lab.

The goal was not to define FOFO data structures yet.
The goal was to verify that subtr_actor can be imported locally and to inspect the first real output shapes from the built-in 2v2 replay fixture.

## Environment

- Branch: codex/parser-output-exploration
- Python: .venv with Python 3.13
- Package: subtr-actor-py
- Source: local submodule external/subtr-actor
- Fixture: external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay

## Fixture

- exists: True
- size_mb: 1.08

## Import Result

subtr_actor imported successfully.

Visible exported functions included:

- get_column_headers
- get_legacy_stats_timeline
- get_ndarray_with_info_from_replay_filepath
- get_replay_frames_data
- get_replay_meta
- get_stats
- get_stats_module_names
- get_stats_snapshot_data
- get_stats_timeline
- parse_replay

## get_replay_meta Result

Top-level keys:

- column_headers
- replay_meta

Observed structure:

column_headers:
- global_headers: 12
- player_headers: 14

replay_meta:
- all_headers: 28
- team_one: 2 players
- team_zero: 2 players

## parse_replay Result

Top-level raw parse keys included:

- class_indices
- content_crc
- content_size
- debug_info
- game_type
- header_crc
- header_size
- keyframes
- levels
- major_version
- minor_version
- names
- net_cache
- net_version
- network_frames
- objects
- packages
- properties
- tick_marks

This confirms that parse_replay exposes a low-level replay structure.

## get_replay_frames_data Result

Top-level keys:

- boost_pad_events
- boost_pads
- demolish_infos
- dodge_refreshed_events
- frame_data
- goal_events
- meta
- player_stat_events
- touch_events

Observed counts:

- boost_pad_events: 1581
- boost_pads: 34
- demolish_infos: 2
- dodge_refreshed_events: 0
- goal_events: 5
- touch_events: 113

Observed frame_data keys:

- ball_data
- metadata_frames
- players

Observed frame counts:

- metadata_frames: 9530
- players: 4

## get_stats_module_names Result

Returned 45 stat module names.

The first observed module was:

- core

## get_column_headers Result

Returned:

- global_headers
- player_headers

First observed global header:

- Ball - position x

First observed player header:

- position x

## Important Findings

- Python bindings work locally in .venv.
- The built-in ranked doubles fixture is usable for first 2v2 exploration.
- get_replay_frames_data is the most useful first structured output.
- parse_replay is useful for low-level/raw replay inspection.
- get_replay_meta is useful for metadata, teams, players, and headers.
- Output should be summarized by keys, counts, and samples.
- Full frame dumps should not be committed.

## Next Recommended Action

Create a temporary local probe script that inspects only:

- top-level keys
- field names
- value types
- event counts
- small samples
- frame/player/ball shape

Do not create a stable FOFO data model yet.

The next step is to document the actual nested field structure from:

- get_replay_meta
- get_replay_frames_data
- parse_replay
