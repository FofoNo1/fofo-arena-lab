# subtr-actor Fixture Variance Report

## Purpose

This report documents bounded parser-output variance across the built-in
`external/subtr-actor/assets/*.replay` fixtures before FOFO creates any
normalized replay model.

It is an exploration report only. It does not define FOFO-owned data contracts,
parser adapters, exporters, resolver classes, or analysis logic.

All counts below are fixture-observed runtime results, not universal parser
guarantees.

## Fixtures Compared

All available fixture replays were listed and included in the shallow pass:

| Fixture | Shallow pass | Deeper pass |
| --- | --- | --- |
| `air-dribble-goal-mouth-2026-05-24.replay` | yes | no |
| `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay` | yes | yes |
| `colonelpanic8-double-tap-third-goal-2026-05-24.replay` | yes | no |
| `old-ballchasing-midfield-car.replay` | yes | no |
| `post-eac-private-2026-04-28.replay` | yes | no |
| `post-eac-ranked-doubles-2026-04-28.replay` | yes | yes |
| `post-eac-ranked-duel-2026-04-28-a.replay` | yes | no |
| `post-eac-ranked-duel-2026-04-28-b.replay` | yes | no |
| `post-eac-ranked-standard-2026-04-28.replay` | yes | no |
| `problematic-private-duel-2026-03-20.replay` | yes | no |
| `recent-ranked-doubles-2026-03-10.replay` | yes | yes |
| `recent-ranked-standard-2026-03-10-a.replay` | yes | no |
| `recent-ranked-standard-2026-03-10-b.replay` | yes | no |
| `replay-format-2016-07-21-v868-12-net-none-lan.replay` | yes | no |
| `replay-format-2016-11-09-v868-14-net-none-rlcs-lan.replay` | yes | no |
| `replay-format-2017-03-16-v868-17-net-none-online.replay` | yes | yes |
| `replay-format-2017-11-22-v868-20-net2-legacy-vectors.replay` | yes | no |
| `replay-format-2018-03-15-v868-20-net5-modern-vectors-legacy-rotation.replay` | yes | no |
| `replay-format-2018-05-17-v868-22-net7-modern-rigidbody.replay` | yes | no |
| `replay-format-2019-04-19-v868-24-net10-modern-rigidbody.replay` | yes | no |
| `replay-format-2020-09-25-v868-29-net10-tournament.replay` | yes | no |
| `replay-format-2022-09-29-v868-32-net10-legacy-boost.replay` | yes | no |
| `replay-format-2025-06-10-v868-32-net10-replicated-boost.replay` | yes | no |
| `replay-format-2026-01-14-v868-32-net10-demolish-extended.replay` | yes | no |
| `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay` | yes | yes |
| `rlcs-2025-worlds-grand-final-flcn-nrg-g5.replay` | yes | no |

Fixtures recommended for deeper bounded inspection after the shallow pass:

| Fixture | Reason |
| --- | --- |
| `recent-ranked-doubles-2026-03-10.replay` | Current 2v2 baseline already used by FOFO. |
| `post-eac-ranked-doubles-2026-04-28.replay` | Newer ranked doubles sample with non-empty dodge refreshes. |
| `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay` | Explicit dodge-refresh counter fixture. |
| `replay-format-2017-03-16-v868-17-net-none-online.replay` | Older replay format with no boost pad events and nullable boost pad ids. |
| `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay` | 3v3 fixture with high touch/demo/boost-pad-event counts. |

## Method

The runtime exploration used bounded stdout-only Python snippets from the repo
root with the existing `.venv`.

Shallow pass for all fixtures:

- listed every `.replay` fixture under `external/subtr-actor/assets`
- called `parse_replay(path.read_bytes())`
- called `get_replay_meta(str(path))`
- called `get_replay_frames_data(str(path))`
- recorded only keys, counts, frame lengths, variant names/counts, and null
  field counts

Deeper pass for selected fixtures:

- compared top-level key sets
- compared frame counts and player/team counts
- sampled frame data shapes without dumping frames
- recorded event stream field names/types and null counts
- inspected ball/player frame variant shapes and rigid-body keys

No replay output files, JSON dumps, exporter output, or parser adapters were
created.

## Top-Level Output Comparison

All 26 fixtures parsed successfully in the shallow pass.

The `parse_replay(...)` top-level key set was stable across all inspected
fixtures:

```text
class_indices, content_crc, content_size, debug_info, game_type, header_crc,
header_size, keyframes, levels, major_version, minor_version, names, net_cache,
net_version, network_frames, objects, packages, properties, tick_marks
```

The `get_replay_frames_data(...)` top-level key set was stable across all
inspected fixtures:

```text
boost_pad_events, boost_pads, demolish_infos, dodge_refreshed_events,
frame_data, goal_events, meta, player_stat_events, touch_events
```

The `frame_data` key set was stable across all inspected fixtures:

```text
ball_data, metadata_frames, players
```

The first observed `metadata_frames[]` key set was stable across all inspected
fixtures:

```text
replicated_game_state_name, replicated_game_state_time_remaining,
seconds_remaining, time
```

## Frame Data Comparison

Observed frame and player counts varied by fixture:

| Fixture | Player tracks | Meta teams | Metadata frames | Ball frames | Player frame lengths |
| --- | ---: | --- | ---: | ---: | --- |
| `air-dribble-goal-mouth-2026-05-24.replay` | 4 | 2+2 | 9199 | 9199 | 9199 |
| `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay` | 6 | 3+3 | 13927 | 13927 | 13927 |
| `colonelpanic8-double-tap-third-goal-2026-05-24.replay` | 2 | 1+1 | 11229 | 11229 | 11229 |
| `old-ballchasing-midfield-car.replay` | 10 | 3+3 | 8322 | 8322 | 8322 |
| `post-eac-private-2026-04-28.replay` | 2 | 1+1 | 23576 | 23576 | 23576 |
| `post-eac-ranked-doubles-2026-04-28.replay` | 4 | 2+2 | 10629 | 10629 | 10629 |
| `post-eac-ranked-duel-2026-04-28-a.replay` | 2 | 1+1 | 2523 | 2523 | 2523 |
| `post-eac-ranked-duel-2026-04-28-b.replay` | 2 | 1+1 | 7802 | 7802 | 7802 |
| `post-eac-ranked-standard-2026-04-28.replay` | 6 | 3+3 | 10127 | 10127 | 10127 |
| `problematic-private-duel-2026-03-20.replay` | 2 | 1+1 | 12029 | 12029 | 12029 |
| `recent-ranked-doubles-2026-03-10.replay` | 4 | 2+2 | 9530 | 9530 | 9530 |
| `recent-ranked-standard-2026-03-10-a.replay` | 6 | 3+3 | 9248 | 9248 | 9248 |
| `recent-ranked-standard-2026-03-10-b.replay` | 6 | 3+3 | 10502 | 10502 | 10502 |
| `replay-format-2016-07-21-v868-12-net-none-lan.replay` | 6 | 3+3 | 7398 | 7398 | 7398 |
| `replay-format-2016-11-09-v868-14-net-none-rlcs-lan.replay` | 6 | 3+3 | 7651 | 7651 | 7651 |
| `replay-format-2017-03-16-v868-17-net-none-online.replay` | 8 | 3+3 | 8136 | 8136 | 8136 |
| `replay-format-2017-11-22-v868-20-net2-legacy-vectors.replay` | 13 | 3+3 | 7901 | 7901 | 7901 |
| `replay-format-2018-03-15-v868-20-net5-modern-vectors-legacy-rotation.replay` | 4 | 2+2 | 9781 | 9781 | 9781 |
| `replay-format-2018-05-17-v868-22-net7-modern-rigidbody.replay` | 6 | 3+3 | 7319 | 7319 | 7319 |
| `replay-format-2019-04-19-v868-24-net10-modern-rigidbody.replay` | 6 | 3+3 | 9574 | 9574 | 9574 |
| `replay-format-2020-09-25-v868-29-net10-tournament.replay` | 6 | 3+3 | 10275 | 10275 | 10275 |
| `replay-format-2022-09-29-v868-32-net10-legacy-boost.replay` | 6 | 3+3 | 11289 | 11289 | 11289 |
| `replay-format-2025-06-10-v868-32-net10-replicated-boost.replay` | 4 | 2+2 | 10921 | 10921 | 10921 |
| `replay-format-2026-01-14-v868-32-net10-demolish-extended.replay` | 6 | 3+3 | 10845 | 10845 | 10845 |
| `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay` | 4 | 2+2 | 9657 | 9657 | 9657 |
| `rlcs-2025-worlds-grand-final-flcn-nrg-g5.replay` | 6 | 3+3 | 8256 | 8256 | 8256 |

Observed notes:

- In all inspected fixtures, `metadata_frames`, `ball_data.frames`, and each
  sampled player track's `frames` length matched.
- Player track count is not always equal to `team_zero + team_one`. Older
  fixtures showed extra player tracks: `old-ballchasing-midfield-car` had 10
  tracks for 3+3 meta teams, and `replay-format-2017-11-22...` had 13 tracks
  for 3+3 meta teams.
- This means FOFO should not assume all player tracks are active in-match
  players without more identity/team verification.

## Event Stream Comparison

Observed event stream counts varied substantially:

| Fixture | Touches | Goals | Demos | Boost pad events | Boost pads | Dodge refreshes | Player stat events |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `air-dribble-goal-mouth-2026-05-24.replay` | 140 | 12 | 5 | 2104 | 34 | 1 | 30 |
| `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay` | 209 | 5 | 10 | 2865 | 34 | 6 | 38 |
| `colonelpanic8-double-tap-third-goal-2026-05-24.replay` | 49 | 7 | 0 | 992 | 34 | 6 | 12 |
| `old-ballchasing-midfield-car.replay` | 88 | 13 | 0 | 243 | 34 | 0 | 26 |
| `post-eac-private-2026-04-28.replay` | 203 | 21 | 8 | 3521 | 34 | 8 | 55 |
| `post-eac-ranked-doubles-2026-04-28.replay` | 137 | 8 | 1 | 1831 | 34 | 4 | 28 |
| `post-eac-ranked-duel-2026-04-28-a.replay` | 27 | 4 | 0 | 325 | 34 | 0 | 7 |
| `post-eac-ranked-duel-2026-04-28-b.replay` | 79 | 8 | 5 | 1378 | 34 | 4 | 17 |
| `post-eac-ranked-standard-2026-04-28.replay` | 127 | 3 | 6 | 1774 | 34 | 1 | 28 |
| `problematic-private-duel-2026-03-20.replay` | 94 | 12 | 1 | 1826 | 34 | 0 | 26 |
| `recent-ranked-doubles-2026-03-10.replay` | 113 | 5 | 2 | 1581 | 34 | 0 | 17 |
| `recent-ranked-standard-2026-03-10-a.replay` | 145 | 1 | 8 | 1787 | 34 | 0 | 24 |
| `recent-ranked-standard-2026-03-10-b.replay` | 126 | 9 | 17 | 2086 | 34 | 0 | 29 |
| `replay-format-2016-07-21-v868-12-net-none-lan.replay` | 125 | 5 | 0 | 592 | 34 | 0 | 26 |
| `replay-format-2016-11-09-v868-14-net-none-rlcs-lan.replay` | 139 | 7 | 0 | 599 | 34 | 0 | 32 |
| `replay-format-2017-03-16-v868-17-net-none-online.replay` | 118 | 3 | 0 | 0 | 34 | 0 | 222 |
| `replay-format-2017-11-22-v868-20-net2-legacy-vectors.replay` | 110 | 8 | 0 | 415 | 34 | 0 | 19 |
| `replay-format-2018-03-15-v868-20-net5-modern-vectors-legacy-rotation.replay` | 130 | 5 | 0 | 333 | 34 | 0 | 19 |
| `replay-format-2018-05-17-v868-22-net7-modern-rigidbody.replay` | 119 | 5 | 0 | 389 | 34 | 0 | 17 |
| `replay-format-2019-04-19-v868-24-net10-modern-rigidbody.replay` | 144 | 5 | 0 | 426 | 34 | 0 | 34 |
| `replay-format-2020-09-25-v868-29-net10-tournament.replay` | 141 | 6 | 3 | 1975 | 34 | 0 | 22 |
| `replay-format-2022-09-29-v868-32-net10-legacy-boost.replay` | 141 | 8 | 3 | 2033 | 34 | 0 | 25 |
| `replay-format-2025-06-10-v868-32-net10-replicated-boost.replay` | 138 | 7 | 2 | 1810 | 34 | 0 | 38 |
| `replay-format-2026-01-14-v868-32-net10-demolish-extended.replay` | 135 | 6 | 10 | 2140 | 34 | 0 | 24 |
| `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay` | 98 | 7 | 3 | 1516 | 34 | 12 | 26 |
| `rlcs-2025-worlds-grand-final-flcn-nrg-g5.replay` | 148 | 5 | 8 | 2212 | 34 | 0 | 29 |

Observed notes:

- `boost_pads` was always 34 in this fixture set, but `boost_pad_events` could
  be zero in an older replay.
- `dodge_refreshed_events` was empty in many fixtures and non-empty in several
  newer or mechanic-focused fixtures.
- `demolish_infos` was empty in multiple older or focused fixtures, but present
  in many modern fixtures.
- `player_stat_events` count can be unexpectedly high relative to goals/touches
  in older fixtures, especially `replay-format-2017-03-16...` with 222 observed
  player stat events.

## Optional / Null Field Observations

Observed nulls in event streams:

| Field location | Observation |
| --- | --- |
| `touch_events[].player` | Some touch events had `player = None` in every inspected fixture. Count matched `closest_approach_distance = None` in the aggregate pass. |
| `touch_events[].closest_approach_distance` | Nullable in every inspected fixture. Observed null counts ranged from 5 to 38 per fixture. |
| `boost_pad_events[].player` | Often null in fixtures with boost pad events. Example: `recent-ranked-doubles...` had 1266 null player fields out of 1581 boost pad events. |
| `boost_pads[].pad_id` | Nullable in some fixtures. `replay-format-2017-03-16...` had all 34 pad ids null. |
| `goal_events[].player` | Usually present in this pass, but `replay-format-2020-09-25...` had 1 null goal player. |
| `PlayerFrame.Data.team` | Sampled as null in deeper fixtures, even when `is_team_0` was present. |
| `BallFrame.Data.rigid_body.linear_velocity` and `angular_velocity` | Sampled as null in early portions of all deeper fixtures. |
| `PlayerFrame.Data.rigid_body.linear_velocity` and `angular_velocity` | Usually present in deeper modern samples, but sampled nulls occurred in the 2017 fixture. |

This confirms that FOFO should treat optional fields as genuinely optional until
more replay types are inspected.

## Variant Shape Observations

Observed frame variant shapes:

| Area | Observation |
| --- | --- |
| Ball frames | Shallow pass observed both `Data` and scalar string variants across fixtures. The string variant likely represents the unit variant such as `Empty`, but this should not be hard-coded yet. |
| Player frames | Shallow pass observed both `Data` and scalar string variants. Older fixtures had many string variant player frames. |
| `BallFrame.Data` | Deeper sampled data contained `rigid_body` only. |
| `PlayerFrame.Data` | Deeper sampled data keys were `rigid_body`, `boost_amount`, `boost_active`, `powerslide_active`, `jump_active`, `double_jump_active`, `dodge_active`, `player_name`, `team`, and `is_team_0`. |
| `RigidBody` | Deeper sampled rigid-body keys were `sleeping`, `location`, `rotation`, `linear_velocity`, and `angular_velocity`. |
| `BoostPadEvent.kind` | First observed sample remained variant-shaped, for example `{ PickedUp: ... }`. |
| `DodgeRefreshedEvent` | Non-empty fixtures used fields `counter_value`, `frame`, `is_team_0`, `player`, and `time`. |

Deep sampled player frame shapes:

| Fixture | Player frame sampled variants | Sampled player nulls |
| --- | --- | --- |
| `recent-ranked-doubles-2026-03-10.replay` | `Data` only in sample | `team` null |
| `post-eac-ranked-doubles-2026-04-28.replay` | `Data` only in sample | `team` null |
| `replay-format-2026-03-03-v868-32-net11-dodge-refresh-counter.replay` | `Data` only in sample | `team` null |
| `replay-format-2017-03-16-v868-17-net-none-online.replay` | `Data` and string variant in sample | `team` null; some rigid-body velocities null |
| `ballchasing-d0a7cdd4-5c9d-42b2-81aa-24ef85da3f8a.replay` | `Data` only in sample | `team` null |

## Stable Fields So Far

Stable across all inspected fixtures:

- `parse_replay` top-level keys were stable.
- `get_replay_frames_data` top-level keys were stable.
- `frame_data` contained `ball_data`, `metadata_frames`, and `players`.
- `metadata_frames[]` contained `time`, `seconds_remaining`,
  `replicated_game_state_name`, and
  `replicated_game_state_time_remaining`.
- `boost_pads` stream was present and had 34 observed items in every fixture.
- Ball/player frame lists aligned with metadata frame count in this fixture set.
- Core event streams were always present as lists, even when empty.

## Unstable Or Needs More Verification

Needs more verification before FOFO models anything:

- Player track count can exceed visible team metadata counts.
- Player tracks may include many string-variant frames in older fixtures.
- `touch_events[].player` and `closest_approach_distance` can be null.
- `boost_pad_events[].player` is often null.
- `boost_pads[].pad_id` can be null in older/focused fixtures.
- `goal_events[].player` can be null.
- `PlayerFrame.Data.team` was sampled as null even when team identity exists
  elsewhere.
- Rigid-body velocity fields can be null.
- Empty event streams are normal and should not be treated as missing parser
  output.
- Event counts vary heavily by fixture type, playlist, replay age, and mechanic
  focus.

## Implications For FOFO Normalized Replay V0

FOFO should not create Normalized Replay V0 from one fixture or from assumptions
about active players only.

When FOFO eventually drafts V0, it should be informed by:

- a clear distinction between parser player tracks and active match players
- optional/null handling for event attribution and rigid-body velocities
- explicit handling of enum/variant shapes such as `Data` vs string variants
- event streams as optional-empty lists, not required non-empty signals
- fixture/version variance in boost pad event availability and pad ids
- team identity from metadata and frame/event fields, not one source only

This report still stops short of defining any FOFO-owned field names, classes,
schemas, or adapters.

## What Not To Assume Yet

- Do not assume player track count equals team size.
- Do not assume all player tracks are active players.
- Do not assume `player` is present on touch, goal, or boost pad events.
- Do not assume every `ResolvedBoostPad` has a `pad_id`.
- Do not assume all frames are `Data`.
- Do not assume rigid-body velocities are always present.
- Do not assume dodge refresh or demo streams are always non-empty.
- Do not assume boost pad event availability is consistent across old replay
  formats.
- Do not assume stats events are analysis judgments.

## Next Recommended Action

Create a narrow follow-up document for "FOFO Normalized Replay V0 questions",
not a schema. It should list the exact unresolved modeling questions revealed by
this variance pass, such as active-player selection, optional attribution,
variant decoding, and event/frame alignment.

After those questions are explicit, FOFO can draft a minimal Normalized Replay
V0 document with clear "observed parser source" notes and no analysis logic.
