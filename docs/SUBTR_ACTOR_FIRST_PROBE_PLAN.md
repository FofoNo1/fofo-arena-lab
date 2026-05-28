# subtr-actor First Probe Plan

## Purpose

Prepare the first FOFO parser-output experiment without creating FOFO-owned data
structures yet. The goal is to parse one Rocket League 2v2 replay, inspect raw
and structured parser output, and document shape/counts/small samples only.

`external/subtr-actor` remains a read-only external dependency.

## Files Inspected

- `README.md`
- `AGENTS.md`
- `docs/HANDOFF.md`
- `docs/NEXT_STEPS.md`
- `docs/SUBTR_ACTOR_EXPLORATION.md`
- `external/subtr-actor/README.md`
- `external/subtr-actor/python/PYTHON-README.md`
- `external/subtr-actor/python/pyproject.toml`
- `external/subtr-actor/python/Cargo.toml`
- `external/subtr-actor/python/build-requirements.txt`
- `external/subtr-actor/python/subtr_actor/__init__.py`
- `external/subtr-actor/python/src/lib.rs`
- `external/subtr-actor/assets/README.md`
- `external/subtr-actor/src/collector/replay_data.rs`
- `external/subtr-actor/src/replay_types.rs`
- `external/subtr-actor/src/collector/ndarray/collector.rs`
- `external/subtr-actor/src/collector/ndarray/builtins.rs`
- `external/subtr-actor/docs/stat-confidence.md`

## Python API Findings

Python package path:

- package root: `external/subtr-actor/python`
- import package: `external/subtr-actor/python/subtr_actor`
- native binding source: `external/subtr-actor/python/src/lib.rs`
- native module name from `pyproject.toml`: `subtr_actor.subtr_actor`

The package is a maturin/PyO3 extension. `subtr_actor/__init__.py` imports the
native extension and also looks for packaged `subtr_actor*.pyd` or
`subtr_actor*.so` files.

Exported Python functions from `python/src/lib.rs`:

- `parse_replay(data: bytes) -> dict`
- `get_ndarray_with_info_from_replay_filepath(filepath, global_feature_adders=None, player_feature_adders=None, fps=None, dtype=None) -> tuple[dict, numpy.ndarray]`
- `get_replay_meta(filepath, global_feature_adders=None, player_feature_adders=None) -> dict`
- `get_column_headers(global_feature_adders=None, player_feature_adders=None) -> dict`
- `get_replay_frames_data(filepath) -> dict`
- `get_stats_module_names() -> list[str]`
- `get_stats(filepath, module_names=None) -> dict`
- `get_stats_snapshot_data(filepath, module_names=None, frame_step_seconds=None) -> dict`
- `get_stats_timeline(filepath, module_names=None, frame_step_seconds=None) -> dict`
- `get_legacy_stats_timeline(filepath, module_names=None, frame_step_seconds=None) -> dict`

Expected input types:

- `filepath`: Python path-like value or string accepted by PyO3 `PathBuf`
- `data`: replay bytes
- `global_feature_adders` / `player_feature_adders`: optional `list[str]`
- `fps` / `frame_step_seconds`: optional positive float
- `dtype`: optional string; documented values include `float16`, `float32`,
  and `float64`
- `module_names`: optional `list[str]`, except compact `get_stats_timeline`
  rejects filtering and should receive `None`

Best first-inspection functions:

- `parse_replay`: confirms raw parser top-level shape.
- `get_replay_meta`: inspects teams, players, replay headers, and ndarray header
  layout without materializing the full ndarray.
- `get_replay_frames_data`: inspects structured frame data and core event
  streams.
- `get_column_headers`: optional quick check for feature header names.

Avoid stats and full ndarray output in the first pass unless the frame-data
shape is already understood.

## Built-in Replay Fixtures

Replay fixtures currently present under `external/subtr-actor/assets` include:

- `air-dribble-goal-mouth-2026-05-24.replay`
- `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay`
- `colonelpanic8-double-tap-third-goal-2026-05-24.replay`
- `old-ballchasing-midfield-car.replay`
- `post-eac-private-2026-04-28.replay`
- `post-eac-ranked-doubles-2026-04-28.replay`
- `post-eac-ranked-duel-2026-04-28-a.replay`
- `post-eac-ranked-duel-2026-04-28-b.replay`
- `post-eac-ranked-standard-2026-04-28.replay`
- `problematic-private-duel-2026-03-20.replay`
- `recent-ranked-doubles-2026-03-10.replay`
- `recent-ranked-standard-2026-03-10-a.replay`
- `recent-ranked-standard-2026-03-10-b.replay`
- `replay-format-2016-07-21-v868-12-net-none-lan.replay`
- `replay-format-2016-11-09-v868-14-net-none-rlcs-lan.replay`
- `replay-format-2017-03-16-v868-17-net-none-online.replay`
- `replay-format-2017-11-22-v868-20-net2-legacy-vectors.replay`
- `replay-format-2018-03-15-v868-20-net5-modern-vectors-legacy-rotation.replay`
- `replay-format-2018-05-17-v868-22-net7-modern-rigidbody.replay`
- `replay-format-2019-04-19-v868-24-net10-modern-rigidbody.replay`
- `replay-format-2020-09-25-v868-29-net10-tournament.replay`
- `replay-format-2022-09-29-v868-32-net10-legacy-boost.replay`
- `replay-format-2025-06-10-v868-32-net10-replicated-boost.replay`
- `replay-format-2026-01-14-v868-32-net10-demolish-extended.replay`
- `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay`
- `rlcs-2025-worlds-grand-final-flcn-nrg-g5.replay`

Best first 2v2 fixture:

- `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay`

Reason: it is explicitly documented as `ranked-doubles`, has a matching
Ballchasing JSON and replay id, and aligns with FOFO's initial 2v2 focus. A good
second fixture is `post-eac-ranked-doubles-2026-04-28.replay`, because it is
newer/post-EAC, but it lacks Ballchasing stats JSON in this checkout.

## Recommended First Probe

Use a temporary one-shot probe, not a committed FOFO module.

The probe should inspect:

- import success and exported function names
- `parse_replay` top-level keys only
- `get_replay_meta` top-level keys, replay metadata keys, team sizes, player
  names, and ndarray header counts
- `get_replay_frames_data` top-level keys
- frame counts: metadata frames, ball frames, player tracks, per-player frame
  lengths
- first and last metadata frame only
- team structures from `frames["meta"]["team_zero"]` and
  `frames["meta"]["team_one"]`
- event counts for `touch_events`, `goal_events`, `demolish_infos`,
  `boost_pad_events`, `dodge_refreshed_events`, and `player_stat_events`
- first few touch, goal, boost, and stat events with only time/frame/player/team
  fields
- optional `get_column_headers()` output counts and first few header names

Do not dump full `parse_replay`, full `get_replay_frames_data`, full frame
arrays, full ndarray matrices, or full stats timelines in the first pass.

## Recommended Local Commands

Run these locally from the FOFO repository root after activating `.venv`.

```powershell
.\.venv\Scripts\Activate.ps1
python -V
python -m pip show subtr-actor-py
```

If `subtr-actor-py` is not already importable and local compilation is accepted,
editable install is likely possible because `external/subtr-actor/python` has a
maturin `pyproject.toml` and links the Rust crate via `path = ".."`:

```powershell
python -m pip install -e external\subtr-actor\python
```

Then run a temporary summary probe:

```powershell
$env:FOFO_REPLAY = "external\subtr-actor\assets\recent-ranked-doubles-2026-03-10.replay"
@'
import json
import os
from pathlib import Path

import subtr_actor

path = Path(os.environ["FOFO_REPLAY"])
raw = subtr_actor.parse_replay(path.read_bytes())
meta = subtr_actor.get_replay_meta(path)
frames = subtr_actor.get_replay_frames_data(path)
headers = subtr_actor.get_column_headers(
    global_feature_adders=["BallRigidBody", "SecondsRemaining"],
    player_feature_adders=["PlayerRigidBody", "PlayerBoost", "PlayerAnyJump"],
)

frame_data = frames.get("frame_data", {})
replay_meta = frames.get("meta", {})
metadata_frames = frame_data.get("metadata_frames", [])
players = frame_data.get("players", [])
ball_frames = frame_data.get("ball_data", {}).get("frames", [])

def compact_event(event):
    if not isinstance(event, dict):
        return event
    return {
        key: event.get(key)
        for key in ("time", "frame", "player", "team_is_team_0",
                    "scoring_team_is_team_0", "pad_id", "kind")
        if key in event
    }

summary = {
    "replay_path": str(path),
    "exports": [name for name in dir(subtr_actor) if not name.startswith("_")],
    "raw_top_level_keys": sorted(raw.keys()),
    "meta_top_level_keys": sorted(meta.keys()),
    "frames_top_level_keys": sorted(frames.keys()),
    "team_zero_names": [p.get("name") for p in replay_meta.get("team_zero", [])],
    "team_one_names": [p.get("name") for p in replay_meta.get("team_one", [])],
    "frame_counts": {
        "metadata_frames": len(metadata_frames),
        "ball_frames": len(ball_frames),
        "player_tracks": len(players),
        "player_frame_lengths": [len(track[1].get("frames", [])) for track in players[:8]],
    },
    "metadata_samples": {
        "first": metadata_frames[0] if metadata_frames else None,
        "last": metadata_frames[-1] if metadata_frames else None,
    },
    "event_counts": {
        name: len(frames.get(name, []))
        for name in (
            "touch_events",
            "goal_events",
            "demolish_infos",
            "boost_pad_events",
            "dodge_refreshed_events",
            "player_stat_events",
        )
    },
    "event_samples": {
        name: [compact_event(e) for e in frames.get(name, [])[:3]]
        for name in ("touch_events", "goal_events", "boost_pad_events", "player_stat_events")
    },
    "header_counts": {
        "global": len(headers.get("global_headers", [])),
        "player": len(headers.get("player_headers", [])),
    },
    "header_samples": {
        "global": headers.get("global_headers", [])[:8],
        "player": headers.get("player_headers", [])[:8],
    },
}

print(json.dumps(summary, indent=2, default=str))
'@ | python -
```

If editable install is risky or fails:

- Prefer trying the published local-venv package only if network and wheel use
  are acceptable: `python -m pip install subtr-actor-py`.
- If Python remains blocked, use source inspection and postpone the real parser
  probe until Rust/Python build tooling is available.
- A Rust fallback exists through `cargo run -p subtr-actor-tools --bin replay_probe`,
  but that will compile Rust code and should be treated as a separate approved
  experiment, not this planning step.

## Expected Output Summary

The first probe output should be a small JSON summary containing:

- replay path and binding exports
- raw top-level parser keys from `parse_replay`
- `get_replay_meta` keys and replay metadata keys
- team names and player counts
- metadata frame count, ball frame count, player track count, and per-player
  frame lengths
- first and last metadata frame
- event counts for touches, goals, demolitions, boost pad events, dodge
  refreshes, and player stat events
- first three compact samples for touch, goal, boost, and player-stat events
- ndarray header counts and first few header names, if useful

Full parser output, full frame arrays, and numeric matrices should remain local
and temporary.

## What Not To Commit

Do not commit:

- private/local `.replay` files
- full parser JSON dumps
- full `get_replay_frames_data` output
- full stats timeline output
- generated ndarray files, CSVs, parquet files, or screenshots of private data
- `.venv`, `target`, Python build directories, wheels, `.pyd`, `.so`, or cache
  directories
- Ballchasing API keys, replay-download credentials, tokens, or private player
  data

If a summary is committed later, strip or anonymize private replay/player data
unless the replay is an already-public fixture.

## Risks / Open Questions

- Parser output can be very large. Summaries should use counts, keys, and small
  samples only.
- `PlayerBoost` uses raw replay units (`0-255`), not `0-100` percent.
- `external/subtr-actor/docs/stat-confidence.md` marks many gameplay stats as
  medium-confidence or experimental. Do not treat heuristic stats as ground
  truth.
- `pip install -e external\subtr-actor\python` will likely invoke maturin and
  Rust compilation. On Windows this may require a working Rust toolchain, MSVC
  build tools, compatible Python, and network access for build dependencies.
- `pyproject.toml` requires `maturin>=1.0,<1.11`, while
  `build-requirements.txt` still lists `maturin>=0.14,<0.15`; prefer
  `pyproject.toml` as the active build definition, but treat this mismatch as a
  setup risk.
- Open question: should the first FOFO-owned output document use only the public
  ranked-doubles fixture, or compare it with one private player replay kept
  entirely local?
- Open question: if Python build setup is painful, should FOFO use the published
  Python wheel first, or approve a Rust CLI probe instead?

## Next Recommended Action

Run the temporary Python summary probe against
`external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay`, keep the
output local, and create a small follow-up note documenting observed keys,
counts, player/team shape, frame shape, and event sample shape.

Before creating FOFO internal data structures, inspect these source files
against the actual probe output:

- `external/subtr-actor/src/collector/replay_data.rs`
- `external/subtr-actor/src/replay_types.rs`
- `external/subtr-actor/src/replay_meta.rs`
- `external/subtr-actor/src/processor/bootstrap.rs`
- `external/subtr-actor/src/processor/view.rs`
- `external/subtr-actor/src/collector/ndarray/collector.rs`
- `external/subtr-actor/src/collector/ndarray/builtins.rs`
- `external/subtr-actor/src/stats/timeline/types.rs`
- `external/subtr-actor/docs/stat-confidence.md`
