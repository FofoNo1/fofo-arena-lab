# subtr-actor Exploration

Purpose: compact notes for the first real replay parsing experiment. Treat
`external/subtr-actor` as a read-only external dependency.

## What It Provides

`external/subtr-actor` is a Rust-first Rocket League replay processing
monorepo. It builds on `boxcars` and exposes higher-level replay outputs across
Rust, Python, and JavaScript/WASM.

Relevant outputs appear to include:

- raw replay parsing through `boxcars`
- structured frame data through `ReplayDataCollector`
- replay metadata and player/team info
- event streams for touches, goals, demos, boost pads, dodge refreshes, and
  player stat events
- numeric feature matrices through `NDArrayCollector`
- stat exports and compact stats timelines
- JS replay/player packages for browser playback and stats visualization

## Relevant For Python Parsing

The Python binding lives in `external/subtr-actor/python/`.

Primary files:

- `python/PYTHON-README.md`
- `python/src/lib.rs`
- `python/pyproject.toml`
- `python/subtr_actor/__init__.py`

Useful Python functions exposed by `subtr_actor`:

- `parse_replay(data: bytes)`: parses replay bytes and returns the full parsed
  replay structure as Python data.
- `get_replay_meta(filepath)`: returns replay metadata plus ndarray headers.
- `get_replay_frames_data(filepath)`: returns structured frame-by-frame data
  from `ReplayDataCollector`.
- `get_column_headers(...)`: shows ndarray feature header layout.
- `get_ndarray_with_info_from_replay_filepath(...)`: returns metadata plus a
  sampled numeric matrix.
- `get_stats_module_names()`, `get_stats(...)`, `get_stats_timeline(...)`: useful
  later, but probably secondary for the first parser-output inspection.

The lowest-friction first experiment for FOFO is likely Python, because it can
dump parsed data without creating FOFO modules yet.

## Relevant For JS/WASM And Viewer Usage

The JS/WASM binding lives in `external/subtr-actor/js/`.

Primary files:

- `js/README.md`
- `js/src/lib.rs`
- `js/player/README.md`
- `js/player/src/wasm.ts`
- `js/player/src/replay-data.ts`
- `js/stat-evaluation-player/README.md`

Useful JS/WASM functions include:

- `validate_replay(data)`
- `get_replay_info(data)`
- `parse_replay(data)`
- `get_replay_meta(data)`
- `get_replay_frames_data(data)`
- `get_ndarray_with_info(data, ...)`
- `get_stats_timeline(data)`

Viewer-related packages:

- `@rlrml/player` / `js/player`: normalizes `get_replay_frames_data()` output
  into replay playback tracks, ball samples, boost pad state, and timeline
  events.
- `@rlrml/stats-player` / `js/stat-evaluation-player`: browser UI for replay
  playback, stat panels, overlays, review playlists, and compact stats timeline
  rendering.

This is useful for future viewer work, but the first FOFO parser-output
experiment should probably stay in Python or a direct Rust tool until raw output
shape is documented.

## Useful First Experiment Entry Points

Do not add a project dependency yet. Use an isolated local environment or run
from the external package only.

Candidate Python probe:

```python
import json
import subtr_actor

replay_path = "path/to/example.replay"

with open(replay_path, "rb") as replay_file:
    raw = subtr_actor.parse_replay(replay_file.read())

meta = subtr_actor.get_replay_meta(replay_path)
frames = subtr_actor.get_replay_frames_data(replay_path)

print(json.dumps({
    "raw_top_level_keys": list(raw.keys()),
    "meta_keys": list(meta.keys()),
    "frame_data_keys": list(frames.get("frame_data", {}).keys()),
    "event_counts": {
        "touch_events": len(frames.get("touch_events", [])),
        "goal_events": len(frames.get("goal_events", [])),
        "demolish_infos": len(frames.get("demolish_infos", [])),
        "boost_pad_events": len(frames.get("boost_pad_events", [])),
    },
}, indent=2))
```

Candidate Rust diagnostic commands from the external workspace:

```sh
cargo run -p subtr-actor-tools --bin replay_probe -- metadata path/to/example.replay
cargo run -p subtr-actor-tools --bin replay_probe -- plausibility path/to/example.replay
cargo run -p subtr-actor-tools --bin ndarray_feature_summary -- path/to/example.replay
```

Built-in fixture to inspect if we do not yet have a FOFO replay:

```txt
external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay
```

That fixture is specifically a ranked doubles replay, so it matches FOFO's
initial 2v2 focus better than duel or standard fixtures.

## Inspect Next Before FOFO Data Structures

Inspect actual output before defining FOFO-owned data structures:

- one real 2v2 replay parsed through `parse_replay`
- the same replay through `get_replay_meta`
- the same replay through `get_replay_frames_data`
- `external/subtr-actor/src/collector/replay_data.rs`
- `external/subtr-actor/src/replay_types.rs`
- `external/subtr-actor/src/replay_meta.rs`
- `external/subtr-actor/src/collector/ndarray/builtins.rs`
- `external/subtr-actor/docs/stat-confidence.md`
- `external/subtr-actor/assets/README.md`

For future viewer work, inspect:

- `external/subtr-actor/js/player/src/replay-data.ts`
- `external/subtr-actor/js/player/src/types.ts`
- `external/subtr-actor/js/player/src/wasm.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/statsTimeline.ts`

## Risks, Assumptions, And Open Questions

- Assumption: `subtr-actor-py` can be used in an isolated environment without
  adding a FOFO dependency yet.
- Assumption: `get_replay_frames_data()` is useful for structured inspection,
  but FOFO should still inspect `parse_replay()` output before defining its own
  stable model.
- Risk: parser output may be large. Initial dumps should summarize keys, counts,
  and small samples instead of committing full replay JSON.
- Risk: boost values use raw replay units (`0-255`), not percentage.
- Risk: several gameplay stats are heuristic.
  `external/subtr-actor/docs/stat-confidence.md` should guide how much trust to
  place in each exported stat.
- Open question: should the first FOFO experiment use a local private replay, a
  public 2v2 fixture from `external/subtr-actor/assets/`, or both?
- Open question: should FOFO prefer Python bindings for exploration, or a small
  Rust command that calls `ReplayDataCollector` directly?
