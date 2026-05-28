# subtr-actor Output Field Reference

## Purpose

This file is a practical reference for parser-visible fields exposed by
`subtr_actor` during the FOFO Arena Lab parser-output exploration phase.

It is not a FOFO data contract, not a stable internal model, and not an
architecture proposal. The purpose is to make the observed parser output easier
to inspect before FOFO derives any project-owned structures.

## Sources

- `docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md`
- `docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md`
- `scripts/probes/inspect_subtr_output.py`

Runtime counts and sample types below are from the first/local probe against:

`external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay`

These counts and samples are observed fixture facts, not universal guarantees.

## API Overview

| Python function | Input shape | Output focus | Usefulness for FOFO exploration |
| --- | --- | --- | --- |
| `parse_replay(data)` | Replay bytes | Low-level boxcars replay structure | Useful for raw parser keys and replay internals. Too large for normal dumping. |
| `get_replay_meta(filepath)` | Replay file path | Replay metadata plus ndarray column headers | Useful for teams, players, replay headers, and feature column names. |
| `get_replay_frames_data(filepath)` | Replay file path | Structured frame, player, ball, and event output | Primary source for context-aware replay state exploration. |
| `get_column_headers(...)` | Optional feature-adder names | NDArray global/player header labels | Useful for later feature inspection without generating arrays. |
| `get_stats_module_names()` | None | Built-in stats module names | Useful inventory, but stats confidence must be handled separately. |
| `get_stats(...)` and timeline APIs | Replay file path | Aggregate or timeline stat outputs | Later exploration. Do not treat heuristic stats as ground truth. |

## Observed First Probe Counts

| Area | Observed count/sample | Notes |
| --- | --- | --- |
| Fixture size | `1131088` bytes | Built-in ranked doubles fixture. |
| Teams | `team_zero: 2`, `team_one: 2` | 2v2 fixture only. |
| Metadata frames | `9530` | Frame count observed in `frame_data.metadata_frames`. |
| Ball frames | `9530` | Observed aligned with metadata frames. Needs verification on more replays. |
| Player tracks | `4` | Each observed player track had `9530` frames. |
| Touch events | `113` | Observed event stream count. |
| Goal events | `5` | Observed event stream count. |
| Demolitions | `2` | Observed event stream count. |
| Boost pads | `34` | Observed resolved pad count. |
| Boost pad events | `1581` | Observed pickup/availability event count. |
| Dodge refresh events | `0` | Observed empty in this fixture. |
| Player stat events | `17` | Observed shots/saves/assists counter events. |
| Stats modules | `45` | First observed module: `core`. |
| Column headers | `12` global, `14` player | Default feature-adder header layout. |

## Context Relevance Overview

| Category | Parser-visible fields | Why it matters later |
| --- | --- | --- |
| Replay timing | `MetadataFrame.time`, `seconds_remaining`, game-state fields | Needed for clock, kickoff/post-goal phases, score-context windows, and event ordering. |
| Team identity | `ReplayMeta.team_zero`, `ReplayMeta.team_one`, `PlayerFrame.Data.is_team_0`, `PlayerStatEvent.is_team_0` | Separates teammates from opponents for 2v2 context. |
| Player identity | `PlayerInfo.name`, `remote_id`, `stats`, player track ids | Connects frame state and events to actual players. |
| Ball state | `BallFrame.Data.rigid_body.location`, `linear_velocity`, `angular_velocity`, `rotation` | Central for threat, possession, challenge, shot, clear, and recovery context. |
| Player state | `PlayerFrame.Data.rigid_body`, `boost_amount`, action flags | Needed for availability, pressure, recovery, boost economy, and challenge feasibility. |
| Touches | `TouchEvent.time`, `frame`, `player`, `team_is_team_0`, `closest_approach_distance`, `dodge_contact` | Candidate anchors for future decision-quality review. |
| Goals | `GoalEvent.time`, `frame`, `player`, score fields | Consequence anchors and scoreline changes. |
| Demos | `DemolishInfo.attacker`, `victim`, velocities, victim location | Availability, pressure, open-net, and rotation context. |
| Boost | `PlayerFrame.Data.boost_amount`, `BoostPadEvent`, `ResolvedBoostPad` | Context for realistic options and resource tradeoffs. |
| Replay headers | `ReplayMeta.all_headers`, `PlayerInfo.stats` | Useful for match/player metadata, but header prop shapes need runtime verification. |
| Stats/timeline outputs | Built-in module names and later stat events | Useful as supporting signals, not primary truth during parser-output exploration. |

## `get_replay_meta` Shape

Observed top-level keys:

```text
get_replay_meta(filepath) -> {
  column_headers: dict,
  replay_meta: dict
}
```

Nested observed/runtime shape:

```text
column_headers: {
  global_headers: list[str],   observed count: 12
  player_headers: list[str]    observed count: 14
}

replay_meta: {
  all_headers: list[[str, HeaderProp-like value]], observed count: 28
  team_zero: list[PlayerInfo-like dict],           observed count: 2
  team_one: list[PlayerInfo-like dict],            observed count: 2
}

PlayerInfo-like dict: {
  name: str,
  remote_id: dict,
  stats: dict
}
```

Observed `PlayerInfo.stats` field names from the first probe:

| Field | Observed Python type | Notes |
| --- | --- | --- |
| `Assists` | `int` | Header-level player stat. |
| `Goals` | `int` | Header-level player stat. |
| `Name` | `str` | May duplicate player name. |
| `OnlineID` | `str` | Identity-related header value. |
| `Platform` | `dict` | Header prop / platform representation. |
| `PlayerID` | `dict` | Header prop / player id representation. |
| `Saves` | `int` | Header-level player stat. |
| `Score` | `int` | Header-level player stat. |
| `Shots` | `int` | Header-level player stat. |
| `Team` | `int` | Team number in header stats. |
| `bBot` | `bool` | Bot flag. |

Observed `remote_id` sample shapes included variant-keyed dictionaries such as
`Epic`, `PlayStation`, and `Xbox`. Exact remote id serialization should still
be verified across replay sources and platforms.

## `parse_replay` Shape

`parse_replay` receives replay bytes, not a path. It exposes the low-level parsed
replay structure and can be large.

Observed top-level keys from the first probe:

```text
parse_replay(data) -> {
  class_indices: list,
  content_crc: int,
  content_size: int,
  debug_info: list,
  game_type: str,
  header_crc: int,
  header_size: int,
  keyframes: list,
  levels: list,
  major_version: int,
  minor_version: int,
  names: list,
  net_cache: list,
  net_version: int,
  network_frames: dict,
  objects: list,
  packages: list,
  properties: list,
  tick_marks: list
}
```

Observed small nested samples:

| Field | Observed sample shape | Context value |
| --- | --- | --- |
| `class_indices[]` | `{ class: str, index: int }` | Object/class inventory. |
| `debug_info[]` | `{ frame: int, text: str, user: str }` | Replay debug annotations. |
| `keyframes[]` | `{ frame: int, position: int, time: float }` | Replay seeking/indexing metadata. |
| `levels[]` | `str` | Map/level packages. |
| `names[]` | `str` | Raw replay name table. |
| `net_cache[]` | `{ cache_id: int, object_ind: int, parent_id: int, properties: list }` | Network class cache. |
| `network_frames` | `{ frames: list }` | Full raw network frames; avoid dumping. |

## `get_replay_frames_data` Shape

Observed top-level keys:

```text
get_replay_frames_data(filepath) -> {
  boost_pad_events: list[BoostPadEvent-like dict],
  boost_pads: list[ResolvedBoostPad-like dict],
  demolish_infos: list[DemolishInfo-like dict],
  dodge_refreshed_events: list[DodgeRefreshedEvent-like dict],
  frame_data: dict,
  goal_events: list[GoalEvent-like dict],
  meta: ReplayMeta-like dict,
  player_stat_events: list[PlayerStatEvent-like dict],
  touch_events: list[TouchEvent-like dict]
}
```

Observed event-stream counts from the first probe:

| Stream | Observed count |
| --- | ---: |
| `boost_pad_events` | 1581 |
| `boost_pads` | 34 |
| `demolish_infos` | 2 |
| `dodge_refreshed_events` | 0 |
| `goal_events` | 5 |
| `player_stat_events` | 17 |
| `touch_events` | 113 |

## `frame_data` Shape

```text
frame_data: {
  ball_data: {
    frames: list[BallFrame]
  },
  metadata_frames: list[MetadataFrame],
  players: list[[PlayerId-like dict, PlayerData-like dict]]
}
```

Observed first-probe counts:

| Field | Observed count | Notes |
| --- | ---: | --- |
| `metadata_frames` | 9530 | Each item was a dict with four timing/state fields. |
| `ball_data.frames` | 9530 | First non-empty sample used `Data`. |
| `players` | 4 | Each track is a two-item list: player id and player data. |
| `players[*][1].frames` | 9530 | Observed for sampled tracks. |

### `MetadataFrame`

```text
MetadataFrame: {
  time: float,
  seconds_remaining: int,
  replicated_game_state_name: int,
  replicated_game_state_time_remaining: int
}
```

Context relevance:

- `time` anchors every frame and event in replay time.
- `seconds_remaining` supports scoreline and urgency context.
- replicated game-state fields may help identify kickoff, live play, replay, or
  post-goal phases after further verification.

### `BallFrame`

Source-mapped variants:

```text
BallFrame:
  Empty
  Data: {
    rigid_body: RigidBody
  }
```

Observed sample shape:

```text
{ Data: { rigid_body: dict with 5 keys } }
```

Expected `RigidBody` fields from the schema map:

```text
RigidBody: {
  sleeping: bool,
  location: Vector3,
  rotation: Quaternion,
  linear_velocity: Vector3 | null,
  angular_velocity: Vector3 | null
}

Vector3: {
  x: float,
  y: float,
  z: float
}

Quaternion: {
  x: float,
  y: float,
  z: float,
  w: float
}
```

Context relevance:

- Ball location and velocity are core inputs for shot threat, pressure,
  possession, clears, passes, saves, and challenge timing.
- Optional velocity fields need runtime verification across more replays.

### `PlayerTrack` and `PlayerFrame`

Observed player track shape:

```text
players[]: [
  PlayerId-like dict,
  {
    frames: list[PlayerFrame]
  }
]
```

Source-mapped player frame variants:

```text
PlayerFrame:
  Empty
  Data: {
    rigid_body: RigidBody,
    boost_amount: float,
    boost_active: bool,
    powerslide_active: bool,
    jump_active: bool,
    double_jump_active: bool,
    dodge_active: bool,
    player_name: str | null,
    team: int | null,
    is_team_0: bool | null
  }
```

Observed first non-empty sample:

```text
{ Data: { boost_active: bool, boost_amount: float, ... } }
```

Context relevance:

- `rigid_body.location` and velocity fields describe rotation, spacing,
  challenge distance, recovery, and teammate/opponent options.
- `boost_amount` is source-documented as raw replay units, not necessarily a
  normalized 0-100 value.
- action flags describe jump, dodge, powerslide, and boost usage context.
- `team` and `is_team_0` help bind frame state to teammate/opponent context.

## Event Stream Field Reference

### `touch_events`

Observed field names and types:

```text
TouchEvent: {
  closest_approach_distance: float,
  dodge_contact: bool,
  frame: int,
  player: dict | null,
  team_is_team_0: bool,
  time: float
}
```

Context relevance:

- Touches are likely future decision-review anchors.
- `closest_approach_distance` may help qualify touch attribution/proximity.
- `dodge_contact` may distinguish soft touches from dodge-based contacts.
- `player` presence must be verified across more replays.

### `goal_events`

Observed field names and types:

```text
GoalEvent: {
  frame: int,
  player: dict | null,
  scoring_team_is_team_0: bool,
  team_one_score: int | null,
  team_zero_score: int | null,
  time: float
}
```

Context relevance:

- Goals are consequence anchors.
- Score fields support scoreline-aware evaluation.
- `player` may identify scorer when available; optionality needs verification.

### `demolish_infos`

Observed field names and types:

```text
DemolishInfo: {
  attacker: dict,
  attacker_velocity: Vector3,
  frame: int,
  seconds_remaining: int,
  time: float,
  victim: dict,
  victim_location: Vector3,
  victim_velocity: Vector3
}
```

Context relevance:

- Demos change player availability and pressure.
- Attacker/victim velocities and victim location can help explain whether a
  demo opened space, stopped pressure, or created a rotation gap.

### `boost_pad_events`

Observed field names and types:

```text
BoostPadEvent: {
  frame: int,
  kind: dict,
  pad_id: str,
  player: dict | null,
  time: float
}
```

Observed `kind` sample:

```text
{ PickedUp: { ... } }
```

Source-mapped variants:

```text
BoostPadEvent.kind:
  PickedUp: { sequence: int }
  Available
```

Context relevance:

- Boost pad pickup and availability are important for resource context.
- `player` may identify who collected a pad when available.
- Pad respawn/availability timing can matter for route and rotation decisions.

### `boost_pads`

Observed field names and types:

```text
ResolvedBoostPad: {
  index: int,
  pad_id: str | null,
  position: Vector3,
  size: str
}
```

Observed `size` sample:

```text
Small
```

Source-mapped size variants:

```text
BoostPadSize:
  Small
  Big
```

Context relevance:

- Pad positions and sizes support later boost route and resource availability
  analysis.

### `dodge_refreshed_events`

Observed first-probe stream:

```text
dodge_refreshed_events: []
```

Source-mapped expected fields when present:

```text
DodgeRefreshedEvent: {
  time: float,
  frame: int,
  player: dict,
  is_team_0: bool,
  counter_value: int
}
```

Context relevance:

- May support later flip-reset or dodge-reset interpretation.
- Empty in the first fixture, so runtime shape still needs direct observation.

### `player_stat_events`

Observed field names and types:

```text
PlayerStatEvent: {
  frame: int,
  is_team_0: bool,
  kind: str,
  player: dict,
  shot: ShotEventMetadata | null,
  time: float
}
```

Observed `kind` sample:

```text
Shot
```

Source-mapped stat kinds:

```text
PlayerStatEvent.kind:
  Shot
  Save
  Assist
```

Observed `shot` metadata field names and types:

```text
ShotEventMetadata: {
  ball_goal_alignment: float | null,
  ball_position: Vector3,
  ball_speed: float | null,
  ball_speed_toward_goal: float | null,
  ball_velocity: Vector3 | null,
  distance_to_goal_center: float,
  distance_to_goal_line: float,
  player_distance_to_ball: float | null,
  player_position: Vector3 | null,
  player_speed: float | null,
  player_velocity: Vector3 | null,
  target_goal_position: Vector3
}
```

Context relevance:

- Shot metadata is already context-rich, especially ball speed, player distance,
  target goal position, and alignment.
- It should still be treated as parser/stat output, not FOFO judgement logic.
- `shot` may be absent for non-shot stat events.

## Header and NDArray Field Reference

`get_column_headers()` and `get_replay_meta(...).column_headers` returned:

```text
column_headers: {
  global_headers: list[str],
  player_headers: list[str]
}
```

Observed first-probe samples:

| Header list | Observed count | First observed sample |
| --- | ---: | --- |
| `global_headers` | 12 | `Ball - position x` |
| `player_headers` | 14 | `position x` |

Context relevance:

- Headers are useful for future feature exploration.
- They should not replace source-level frame/event inspection during the
  current parser-output phase.
- Generating full ndarrays is out of scope for this reference.

## Fields Most Relevant For Future Context-Aware Analysis

| Future question | Parser-visible fields to inspect first |
| --- | --- |
| Where was the ball and how dangerous was it? | `BallFrame.Data.rigid_body.location`, `linear_velocity`, `ShotEventMetadata.ball_position`, `ball_speed`, `ball_speed_toward_goal` |
| Which players were available? | `PlayerFrame.Data.rigid_body.location`, `linear_velocity`, `boost_amount`, action flags, demo events |
| Was this teammate or opponent context? | `ReplayMeta.team_zero/team_one`, player ids, `is_team_0`, `team_is_team_0`, `scoring_team_is_team_0` |
| What was the score and time pressure? | `MetadataFrame.seconds_remaining`, `GoalEvent.team_zero_score`, `GoalEvent.team_one_score` |
| What action anchors exist? | `touch_events`, `goal_events`, `player_stat_events`, `demolish_infos`, `boost_pad_events` |
| What resources were available? | `PlayerFrame.Data.boost_amount`, `boost_active`, `boost_pads`, `boost_pad_events` |
| What happened after a decision? | Event `frame`/`time` ordering plus subsequent ball/player frames |

## Open Verification Items

- Exact Python serialization shape for `RemoteId`, `HeaderProp`, `BallFrame`,
  `PlayerFrame`, and enum variants across more replays.
- Whether optional fields are omitted, present as `None`, or present as variant
  objects across replay versions.
- Whether all ball/player frame arrays always align with `metadata_frames`.
- Whether `TouchEvent.player` and `GoalEvent.player` are consistently populated.
- Whether `ShotEventMetadata` is available only for `Shot` events or appears in
  other stat-event variants in some cases.
- Whether boost values are consistently raw replay units in every output path.
- How reliable team/player identity is for bots, duplicate ids, substitutions,
  and late player discovery.

## Usage Guidance

- Prefer `get_replay_frames_data` for structured runtime exploration.
- Use `get_replay_meta` for team/player identity and replay headers.
- Use `parse_replay` only for bounded raw-key inspection.
- Print summaries, counts, field names, and small samples only.
- Do not write full parser dumps, frame arrays, matrices, or generated JSON.
- Do not turn this reference into a FOFO data model without broader runtime
  verification.
