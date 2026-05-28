# subtr-actor Output Schema Map

## Purpose

This document maps subtr-actor's existing parser-visible output structures before FOFO Arena Lab creates its own internal replay model.

It is a source-based inventory of what subtr-actor already exposes through Rust, Python, and JavaScript/WASM. It should help the first FOFO parser probe ask better questions without inventing FOFO-owned data contracts too early.

## Scope

- This maps replay/parser-visible structures exposed by subtr-actor.
- This does not define FOFO-owned data contracts yet.
- This does not recommend architecture, parser modules, or application code.
- This may need runtime verification after the first probe, especially for exact Python dict keys, enum serialization, optional fields, output sizes, and fixture-specific counts.

## Files Inspected

- `README.md`
- `AGENTS.md`
- `docs/HANDOFF.md`
- `docs/NEXT_STEPS.md`
- `docs/SUBTR_ACTOR_EXPLORATION.md`
- `docs/SUBTR_ACTOR_FIRST_PROBE_PLAN.md`
- `external/subtr-actor/README.md`
- `external/subtr-actor/assets/README.md`
- `external/subtr-actor/docs/stat-confidence.md`
- `external/subtr-actor/python/src/lib.rs`
- `external/subtr-actor/python/subtr_actor/__init__.py`
- `external/subtr-actor/python/PYTHON-README.md`
- `external/subtr-actor/python/pyproject.toml`
- `external/subtr-actor/src/lib.rs`
- `external/subtr-actor/src/replay_meta.rs`
- `external/subtr-actor/src/replay_types.rs`
- `external/subtr-actor/src/ts_bindings.rs`
- `external/subtr-actor/src/processor/bootstrap.rs`
- `external/subtr-actor/src/processor/mod.rs`
- `external/subtr-actor/src/processor/queries.rs`
- `external/subtr-actor/src/processor/view.rs`
- `external/subtr-actor/src/collector/replay_data.rs`
- `external/subtr-actor/src/collector/ndarray/collector.rs`
- `external/subtr-actor/src/collector/ndarray/builtins.rs`
- `external/subtr-actor/src/collector/ndarray/traits.rs`
- `external/subtr-actor/src/collector/ndarray/mod.rs`
- `external/subtr-actor/src/collector/stats/types.rs`
- `external/subtr-actor/src/collector/stats/collector.rs`
- `external/subtr-actor/src/collector/stats/playback.rs`
- `external/subtr-actor/src/collector/stats/builtins.rs`
- `external/subtr-actor/src/collector/frame_resolution.rs`
- `external/subtr-actor/src/stats/timeline/types.rs`
- `external/subtr-actor/src/stats/timeline/collector.rs`
- `external/subtr-actor/src/stats/calculators/frame_components.rs`
- `external/subtr-actor/src/stats/calculators/frame_input.rs`
- `external/subtr-actor/src/stats/calculators/live_play.rs`
- `external/subtr-actor/src/stats/calculators/samples.rs`
- `external/subtr-actor/src/stats/calculators/flip_reset.rs`
- `external/subtr-actor/js/src/lib.rs`
- `external/subtr-actor/js/README.md`
- `external/subtr-actor/js/player/src/types.ts`
- `external/subtr-actor/js/player/src/raw-types.ts`
- `external/subtr-actor/js/player/src/replay-data.ts`
- `external/subtr-actor/js/player/src/wasm.ts`
- `external/subtr-actor/js/player/src/generated/ReplayData.ts`
- `external/subtr-actor/js/player/src/generated/FrameData.ts`
- `external/subtr-actor/js/player/src/generated/BallData.ts`
- `external/subtr-actor/js/player/src/generated/BallFrame.ts`
- `external/subtr-actor/js/player/src/generated/PlayerData.ts`
- `external/subtr-actor/js/player/src/generated/PlayerFrame.ts`
- `external/subtr-actor/js/player/src/generated/MetadataFrame.ts`
- `external/subtr-actor/js/player/src/generated/ReplayMeta.ts`
- `external/subtr-actor/js/player/src/generated/PlayerInfo.ts`
- `external/subtr-actor/js/player/src/generated/RigidBodyTs.ts`
- `external/subtr-actor/js/player/src/generated/Vector3fTs.ts`
- `external/subtr-actor/js/player/src/generated/QuaternionTs.ts`
- `external/subtr-actor/js/player/src/generated/RemoteIdTs.ts`
- `external/subtr-actor/js/player/src/generated/HeaderPropTs.ts`
- `external/subtr-actor/js/player/src/generated/BoostPadEvent.ts`
- `external/subtr-actor/js/player/src/generated/BoostPadEventKind.ts`
- `external/subtr-actor/js/player/src/generated/ResolvedBoostPad.ts`
- `external/subtr-actor/js/player/src/generated/GoalEvent.ts`
- `external/subtr-actor/js/player/src/generated/TouchEvent.ts`
- `external/subtr-actor/js/player/src/generated/DemolishInfo.ts`
- `external/subtr-actor/js/player/src/generated/DodgeRefreshedEvent.ts`
- `external/subtr-actor/js/player/src/generated/PlayerStatEvent.ts`
- `external/subtr-actor/js/player/src/generated/PlayerStatEventKind.ts`
- `external/subtr-actor/js/player/src/generated/ShotEventMetadata.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsTimeline.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsTimelineScaffold.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsTimelineEvents.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsFrame.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsFrameScaffold.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/ReplayStatsPlayerIdentity.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/StatsTimelineConfig.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BackboardBounceEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BallCarryEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BoostLedgerEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BoostPadEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BoostPickupComparisonEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BoostStateEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/BumpEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/CeilingShotEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/CenterEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/CorePlayerStatsEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/CoreTeamStatsEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/DodgeRefreshedEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/DodgeResetEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/DoubleTapEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/FiftyFiftyEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/FlickEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/FlipResetEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/FlipResetFollowupDodgeEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/GoalContextEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/GoalEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/GoalTagEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/HalfFlipEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/HalfVolleyEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/MechanicEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/MovementEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/MustyFlickEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/OneTimerEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PassEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PassLastCompletedEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PlayerStatEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PositioningEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PossessionEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PostWallDodgeEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PowerslideEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/PressureEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/RotationPlayerEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/RotationTeamEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/RushEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/SpeedFlipEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TerritorialPressureEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TimelineEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TouchBallMovementEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TouchEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TouchLastTouchEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/TouchStatsEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/WallAerialEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/WallAerialShotEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/WavedashEvent.ts`
- `external/subtr-actor/js/stat-evaluation-player/src/generated/WhiffEvent.ts`

## Public Python API

| Function | Source file | Input | Output / Return Shape | Useful For First Probe | Notes |
| --- | --- | --- | --- | --- | --- |
| `parse_replay` | `external/subtr-actor/python/src/lib.rs` | `data: bytes` | Python data converted from `serde_json::to_value(boxcars::Replay)`. Expected shape is nested dict/list/scalar data for the full parsed replay. | Yes | Rawest API. Likely very large. Use only top-level keys and small samples at first. |
| `get_ndarray_with_info_from_replay_filepath` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, optional `global_feature_adders`, optional `player_feature_adders`, optional `fps`, optional `dtype` | Python tuple `(meta_dict, numpy.ndarray)`. `meta_dict` is `ReplayMetaWithHeaders`; ndarray is 2D `(sampled_frames, feature_columns)`. | Later / small header check only | Defaults: global `["BallRigidBody"]`, player `["PlayerRigidBody", "PlayerBoost", "PlayerAnyJump"]`, `fps=10.0`, `dtype=float32`. Do not dump full ndarray in first probe. |
| `get_replay_meta` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, optional feature adder lists | Dict converted from `ReplayMetaWithHeaders`: `{ replay_meta, column_headers }`. | Yes | Low-cost way to inspect teams, players, all replay headers, and ndarray header layout without matrix data. |
| `get_column_headers` | `external/subtr-actor/python/src/lib.rs` | Optional `global_feature_adders`, optional `player_feature_adders` | Dict converted from `NDArrayColumnHeaders`: `{ global_headers, player_headers }`. | Yes | Good for confirming feature names and column counts before generating arrays. |
| `get_replay_frames_data` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf` | Dict converted from `ReplayData`: frame data, replay metadata, boost pads, touches, goals, demos, dodge refreshes, player stat events. | Yes | Primary structured output for first FOFO schema probe. No FPS resampling. |
| `get_stats_module_names` | `external/subtr-actor/python/src/lib.rs` | None | `list[str]` of builtin stats modules. | Optional | Useful to list available stat outputs, but stats should be secondary to replay/frame output in first probe. |
| `get_stats` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, optional `module_names: list[str]` | Dict converted from `CollectedStats`: `{ replay_meta, modules }`, where `modules` is module-name keyed JSON values. | Later | Aggregate stats, not raw frame shape. Many modules are heuristic. |
| `get_stats_snapshot_data` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, optional `module_names`, optional `frame_step_seconds` | Dict converted from `StatsSnapshotData`: `{ replay_meta, config, modules, frames }`; each frame has timing/gameplay scaffold plus module snapshots. | Later | Can be large because frames include module snapshots. `frame_step_seconds` defaults to every frame. |
| `get_stats_timeline` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, `module_names=None`, optional `frame_step_seconds` | Dict converted from `ReplayStatsTimelineScaffold`: `{ config, replay_meta, events, frames }`. Frames are scaffolds; stat deltas live under `events`. | Later | Compact event-backed timeline. Passing `module_names` raises `ValueError`. |
| `get_legacy_stats_timeline` | `external/subtr-actor/python/src/lib.rs` | `filepath: PathBuf`, optional `module_names`, optional `frame_step_seconds` | Dict/JSON value for legacy full snapshot timeline: `{ config, replay_meta, events, frames }`, where frames include team/player stat snapshots. | No for first probe | Compatibility path. Likely larger than compact timeline. |

Python package loading:

- `external/subtr-actor/python/subtr_actor/__init__.py` imports native module `subtr_actor.subtr_actor`.
- If normal import fails, it searches packaged `subtr_actor*.so` and `subtr_actor*.pyd` files in the package directory.
- `external/subtr-actor/python/pyproject.toml` declares a maturin/PyO3 package named `subtr-actor-py` with native module `subtr_actor.subtr_actor`.

## Rust Structures Relevant To Replay Output

| Struct / Enum | Source file | Fields | Field Types | Purpose | Appears In Which Output |
| --- | --- | --- | --- | --- | --- |
| `ReplayData` | `external/subtr-actor/src/collector/replay_data.rs` | `frame_data`, `meta`, `demolish_infos`, `boost_pad_events`, `boost_pads`, `touch_events`, `dodge_refreshed_events`, `player_stat_events`, `goal_events` | `FrameData`, `ReplayMeta`, `Vec<DemolishInfo>`, `Vec<BoostPadEvent>`, `Vec<ResolvedBoostPad>`, `Vec<TouchEvent>`, `Vec<DodgeRefreshedEvent>`, `Vec<PlayerStatEvent>`, `Vec<GoalEvent>` | Top-level structured replay payload. | Python `get_replay_frames_data`; JS `get_replay_frames_data`; JS bundle raw replay data. |
| `FrameData` | `external/subtr-actor/src/collector/replay_data.rs` | `ball_data`, `players`, `metadata_frames` | `BallData`, `Vec<(PlayerId, PlayerData)>`, `Vec<MetadataFrame>` | Frame-by-frame state grouped by ball, player tracks, and match metadata. | `ReplayData.frame_data`. |
| `MetadataFrame` | `external/subtr-actor/src/collector/replay_data.rs` | `time`, `seconds_remaining`, `replicated_game_state_name`, `replicated_game_state_time_remaining` | `f32`, `i32`, `i32`, `i32` | Per-frame replay clock and game-state metadata. | `FrameData.metadata_frames`. |
| `BallData` | `external/subtr-actor/src/collector/replay_data.rs` | `frames` | `Vec<BallFrame>` | Chronological ball frames. | `FrameData.ball_data`. |
| `BallFrame` | `external/subtr-actor/src/collector/replay_data.rs` | Variants: `Empty`; `Data { rigid_body }` | `rigid_body: boxcars::RigidBody` | Ball position, rotation, and velocities, or missing ball state. | `BallData.frames`. |
| `PlayerData` | `external/subtr-actor/src/collector/replay_data.rs` | `frames` | `Vec<PlayerFrame>` | Chronological per-player car/input frames. | `FrameData.players[*][1]`. |
| `PlayerFrame` | `external/subtr-actor/src/collector/replay_data.rs` | Variants: `Empty`; `Data { rigid_body, boost_amount, boost_active, powerslide_active, jump_active, double_jump_active, dodge_active, player_name, team, is_team_0 }` | `boxcars::RigidBody`, `f32`, `bool`, `bool`, `bool`, `bool`, `bool`, `Option<String>`, `Option<i32>`, `Option<bool>` | Player/car state for one frame. Boost amount is raw replay units. | `PlayerData.frames`. |
| `ReplayMeta` | `external/subtr-actor/src/replay_types.rs`; built in `external/subtr-actor/src/processor/bootstrap.rs` | `team_zero`, `team_one`, `all_headers` | `Vec<PlayerInfo>`, `Vec<PlayerInfo>`, `Vec<(String, HeaderProp)>` | Replay metadata, player ordering, and replay header properties. | `ReplayData.meta`; `ReplayMetaWithHeaders.replay_meta`; stats timelines. |
| `PlayerInfo` | `external/subtr-actor/src/replay_types.rs` | `remote_id`, `stats`, `name` | `boxcars::RemoteId`, `Option<HashMap<String, HeaderProp>>`, `String` | Player identity plus optional header-level player stats/settings. | `ReplayMeta.team_zero`, `ReplayMeta.team_one`; JS player camera settings extraction. |
| `DemolishInfo` | `external/subtr-actor/src/replay_types.rs` | `time`, `seconds_remaining`, `frame`, `attacker`, `victim`, `attacker_velocity`, `victim_velocity`, `victim_location` | `f32`, `i32`, `usize`, `PlayerId`, `PlayerId`, `Vector3f`, `Vector3f`, `Vector3f` | Demo event with participants and physical context. | `ReplayData.demolish_infos`; stats frame events; viewer timeline demos. |
| `DemolishFormat` / `DemolishAttribute` | `external/subtr-actor/src/replay_types.rs` | `DemolishFormat`: `Fx`, `Extended`; `DemolishAttribute`: `Fx(boxcars::DemolishFx)`, `Extended(boxcars::DemolishExtended)` | Enum variants | Handles old and new Rocket League demolition attributes. | Internal processor event extraction; not directly serialized in `ReplayData`. |
| `BoostPadEventKind` | `external/subtr-actor/src/replay_types.rs` | `PickedUp { sequence }`, `Available` | `sequence: u8` | Pickup vs respawn/availability state. | `BoostPadEvent.kind`. |
| `BoostPadSize` | `external/subtr-actor/src/replay_types.rs` | `Big`, `Small` | Enum variants | Standard boost pad size. | `ResolvedBoostPad.size`. |
| `BoostPadEvent` | `external/subtr-actor/src/replay_types.rs` | `time`, `frame`, `pad_id`, `player`, `kind` | `f32`, `usize`, `String`, `Option<PlayerId>`, `BoostPadEventKind` | Observed boost pad pickup and availability events. | `ReplayData.boost_pad_events`; stats frame events; JS player boost pad event tracks. |
| `ResolvedBoostPad` | `external/subtr-actor/src/replay_types.rs` | `index`, `pad_id`, `size`, `position` | `usize`, `Option<String>`, `BoostPadSize`, `Vector3f` | Resolved standard boost pad layout plus replay pad id where known. | `ReplayData.boost_pads`; JS player boost pad model. |
| `GoalEvent` | `external/subtr-actor/src/replay_types.rs` | `time`, `frame`, `scoring_team_is_team_0`, `player`, `team_zero_score`, `team_one_score` | `f32`, `usize`, `bool`, `Option<PlayerId>`, `Option<i32>`, `Option<i32>` | Goal event with scorer and cumulative score when available. | `ReplayData.goal_events`; stats timeline; viewer timeline goals. |
| `PlayerStatEventKind` | `external/subtr-actor/src/replay_types.rs` | `Shot`, `Save`, `Assist` | Enum variants | Replay counter event classification. | `PlayerStatEvent.kind`. |
| `ShotEventMetadata` | `external/subtr-actor/src/replay_types.rs` | `ball_position`, `ball_velocity`, `ball_speed`, `player_position`, `player_velocity`, `player_speed`, `player_distance_to_ball`, `target_goal_position`, `distance_to_goal_center`, `distance_to_goal_line`, `ball_goal_alignment`, `ball_speed_toward_goal` | `Vector3f`, `Option<Vector3f>`, `Option<f32>`, `Option<Vector3f>`, `Option<Vector3f>`, `Option<f32>`, `Option<f32>`, `Vector3f`, `f32`, `f32`, `Option<f32>`, `Option<f32>` | Context attached to shot events when rigid bodies are available. | `PlayerStatEvent.shot`; JS viewer timeline shot location/metadata. |
| `PlayerStatEvent` | `external/subtr-actor/src/replay_types.rs` | `time`, `frame`, `player`, `is_team_0`, `kind`, `shot` | `f32`, `usize`, `PlayerId`, `bool`, `PlayerStatEventKind`, `Option<ShotEventMetadata>` | Shot/save/assist counter increment event. | `ReplayData.player_stat_events`; viewer timeline shots/saves/assists. |
| `TouchEvent` | `external/subtr-actor/src/replay_types.rs` | `time`, `frame`, `team_is_team_0`, `player`, `closest_approach_distance`, `dodge_contact` | `f32`, `usize`, `bool`, `Option<PlayerId>`, `Option<f32>`, `bool` | Ball-touch event with team, optional player attribution, proximity, and dodge-contact flag. | `ReplayData.touch_events`; stats touch/fifty-fifty/pass/possession logic. |
| `DodgeRefreshedEvent` | `external/subtr-actor/src/stats/calculators/flip_reset.rs` | `time`, `frame`, `player`, `is_team_0`, `counter_value` | `f32`, `usize`, `PlayerId`, `bool`, `i32` | Replay counter-derived dodge refresh event. | `ReplayData.dodge_refreshed_events`; dodge reset stats. |
| `Vector3fTs` | `external/subtr-actor/src/ts_bindings.rs` | `x`, `y`, `z` | `f32`, `f32`, `f32` | TypeScript-visible vector shape for `boxcars::Vector3f`. | Generated JS types. |
| `QuaternionTs` | `external/subtr-actor/src/ts_bindings.rs` | `x`, `y`, `z`, `w` | `f32`, `f32`, `f32`, `f32` | TypeScript-visible quaternion shape. | Generated JS types. |
| `RigidBodyTs` | `external/subtr-actor/src/ts_bindings.rs` | `sleeping`, `location`, `rotation`, `linear_velocity`, `angular_velocity` | `bool`, `Vector3fTs`, `QuaternionTs`, `Option<Vector3fTs>`, `Option<Vector3fTs>` | Serialized rigid-body shape used by ball/player frames. | Generated JS `BallFrame` and `PlayerFrame`. |
| `RemoteIdTs` | `external/subtr-actor/src/ts_bindings.rs` | Variants: `PlayStation`, `PsyNet`, `SplitScreen`, `Steam`, `Switch`, `Xbox`, `QQ`, `Epic` | Platform-specific IDs, usually string/u64-like payloads or structs | TypeScript-visible player id shape. | Generated JS types and serialized player ids. |
| `HeaderPropTs` | `external/subtr-actor/src/ts_bindings.rs` | Variants: `Array`, `Bool`, `Byte`, `Float`, `Int`, `Name`, `QWord`, `Str`, `Struct` | Recursive replay header property values | TypeScript-visible replay header stats/settings shape. | `ReplayMeta.all_headers`, `PlayerInfo.stats`. |
| `NDArrayColumnHeaders` | `external/subtr-actor/src/collector/ndarray/collector.rs` | `global_headers`, `player_headers` | `Vec<String>`, `Vec<String>` | Column labels for dense feature matrix. | Python/JS `get_column_headers`; `ReplayMetaWithHeaders.column_headers`. |
| `ReplayMetaWithHeaders` | `external/subtr-actor/src/collector/ndarray/collector.rs` | `replay_meta`, `column_headers` | `ReplayMeta`, `NDArrayColumnHeaders` | Metadata bundled with ndarray layout. | Python/JS `get_replay_meta`; ndarray metadata. |
| `NDArrayCollector<F>` | `external/subtr-actor/src/collector/ndarray/collector.rs` | Internal: feature adders, player feature adders, data, replay meta, frame count | Generic numeric feature collection | Builds dense 2D arrays by frame and player order. | Python `get_ndarray_with_info_from_replay_filepath`; JS `get_ndarray_with_info`. |
| `StatsFrameResolution` | `external/subtr-actor/src/collector/frame_resolution.rs` | `EveryFrame`, `TimeStep { seconds }` | `f32` for timestep | Controls stats snapshot/timeline sampling. | Python stats functions via `frame_step_seconds`. |
| `CollectedStats` | `external/subtr-actor/src/collector/stats/types.rs` | `replay_meta`, `modules` | `ReplayMeta`, module-name keyed JSON values | Aggregate stats output. | Python `get_stats`. |
| `CapturedStatsFrame<Modules>` | `external/subtr-actor/src/collector/stats/playback.rs` | `frame_number`, `time`, `dt`, `seconds_remaining`, `game_state`, `ball_has_been_hit`, `kickoff_countdown_time`, `gameplay_phase`, `is_live_play`, `modules` | `usize`, `f32`, `f32`, `Option<i32>`, `Option<i32>`, `Option<bool>`, `Option<i32>`, `GameplayPhase`, `bool`, generic module payload | Per-sample stats snapshot frame. | Python `get_stats_snapshot_data`. |
| `CapturedStatsData<Frame>` | `external/subtr-actor/src/collector/stats/playback.rs` | `replay_meta`, `config`, `modules`, `frames` | `ReplayMeta`, `Map<String, Value>`, `Map<String, Value>`, `Vec<Frame>` | Captured stats payload with configs, aggregate modules, and sampled frames. | Python `get_stats_snapshot_data`. |
| `StatsTimelineConfig` | `external/subtr-actor/src/stats/timeline/types.rs` | Threshold/config fields for positioning, pressure, territorial pressure, rotation, rush, aerial/goal/mechanic detectors, half volley | All `f32` | Documents thresholds used by exported timeline/stats events. | `ReplayStatsTimeline`, `ReplayStatsTimelineScaffold`. |
| `ReplayStatsTimelineScaffold` | `external/subtr-actor/src/stats/timeline/types.rs` | `config`, `replay_meta`, `events`, `frames` | `StatsTimelineConfig`, `ReplayMeta`, `ReplayStatsTimelineEvents`, `Vec<ReplayStatsFrameScaffold>` | Compact event-backed stats timeline. | Python `get_stats_timeline`; JS `get_stats_timeline`; bundle stats timeline. |
| `ReplayStatsFrameScaffold` | `external/subtr-actor/src/stats/timeline/types.rs` | `frame_number`, `time`, `dt`, `seconds_remaining`, `game_state`, `ball_has_been_hit`, `kickoff_countdown_time`, `gameplay_phase`, `is_live_play`, `team_zero`, `team_one`, `players` | `usize`, `f32`, `f32`, optional gameplay fields, `GameplayPhase`, `bool`, empty/dynamic maps, `Vec<ReplayStatsPlayerIdentity>` | Lightweight sampled frame scaffold. | Compact stats timeline `frames`. |
| `ReplayStatsPlayerIdentity` | `external/subtr-actor/src/stats/timeline/types.rs` | `player_id`, `name`, `is_team_0` | `PlayerId`, `String`, `bool` | Player identity repeated in compact frame scaffolds. | `ReplayStatsFrameScaffold.players`. |
| `ReplayStatsTimelineEvents` | `external/subtr-actor/src/stats/timeline/types.rs` | Event arrays: `timeline`, `core_player`, `core_team`, `possession`, `pressure`, `territorial_pressure`, `movement`, `positioning`, `rotation_player`, `rotation_team`, `mechanics`, `goal_context`, `backboard`, `ceiling_shot`, `wall_aerial`, `wall_aerial_shot`, `center`, `flick`, `musty_flick`, `dodge_reset`, `double_tap`, `fifty_fifty`, `one_timer`, `pass`, `pass_last_completed`, `ball_carry`, `goal_tags`, `rush`, `speed_flip`, `half_flip`, `half_volley`, `wavedash`, `whiff`, `powerslide`, `touch`, `touch_ball_movement`, `touch_last_touch`, `boost_pickups`, `boost_ledger`, `boost_state`, `bump` | `Vec<...Event>` for each event type | Timeline event transfer object for stats and mechanics. | Compact and legacy stats timeline outputs. |
| `ReplayStatsTimeline` | `external/subtr-actor/src/stats/timeline/types.rs` | `config`, `replay_meta`, `events`, `frames` | `StatsTimelineConfig`, `ReplayMeta`, `ReplayStatsTimelineEvents`, `Vec<ReplayStatsFrame>` | Legacy/full typed stats timeline. | Python `get_legacy_stats_timeline`; JS `get_legacy_stats_timeline_json`. |
| `ReplayStatsFrame` | `external/subtr-actor/src/stats/timeline/types.rs` | Same scaffold timing/gameplay fields plus `team_zero`, `team_one`, `players` | `TeamStatsSnapshot`, `TeamStatsSnapshot`, `Vec<PlayerStatsSnapshot>` | Full per-frame typed stat snapshot. | Legacy timeline frames. |
| `TeamStatsSnapshot` | `external/subtr-actor/src/stats/timeline/types.rs` | Stat groups: `fifty_fifty`, `possession`, `pressure`, `territorial_pressure`, `rotation`, `rush`, `core`, `backboard`, `double_tap`, `one_timer`, `pass`, `ball_carry`, `air_dribble`, `boost`, `bump`, `half_volley`, `movement`, `powerslide`, `demo` | Module-specific stats structs | Full team stat state at a sample. | `ReplayStatsFrame.team_zero/team_one`. |
| `PlayerStatsSnapshot` | `external/subtr-actor/src/stats/timeline/types.rs` | `player_id`, `name`, `is_team_0`, then player stat groups for core, backboard, ceiling shot, wall aerial, wall aerial shot, double tap, one timer, pass, fifty-fifty, speed flip, half flip, half volley, wavedash, touch, whiff, flick, musty flick, dodge reset, ball carry, air dribble, boost, bump, movement, positioning, rotation, powerslide, demo | Player id/name/team plus module-specific stats structs | Full player stat state at a sample. | `ReplayStatsFrame.players`. |
| `FrameInfo` | `external/subtr-actor/src/stats/calculators/frame_components.rs` | `frame_number`, `time`, `dt`, `seconds_remaining` | `usize`, `f32`, `f32`, `Option<i32>` | Internal sampled frame state used by stats graph. | Stats snapshot/timeline frame scaffolds. |
| `GameplayState` | `external/subtr-actor/src/stats/calculators/frame_components.rs` | `game_state`, `ball_has_been_hit`, `kickoff_countdown_time`, `team_zero_score`, `team_one_score`, `possession_team_is_team_0`, `scored_on_team_is_team_0`, `current_in_game_team_player_counts` | Optional ints/bools plus `[usize; 2]` | Internal game context used by stats graph. | Stats timeline frame fields and many derived stats. |
| `FrameEventsState` | `external/subtr-actor/src/stats/calculators/frame_components.rs` | `active_demos`, `demo_events`, `boost_pad_events`, `touch_events`, `dodge_refreshed_events`, `player_stat_events`, `goal_events` | Vectors of event structs | Current-frame or since-last-sample event bundle for stats. | Internal stats graph inputs. |
| `GameplayPhase` | `external/subtr-actor/src/stats/calculators/live_play.rs` | `Unknown`, `KickoffCountdown`, `KickoffWaitingForTouch`, `ActivePlay`, `PostGoal` | Enum variants serialized as snake_case | Live-play classification for filtering stats. | Stats frames: `gameplay_phase`; JS generated `GameplayPhase`. |
| `LivePlayState` | `external/subtr-actor/src/stats/calculators/live_play.rs` | `gameplay_phase`, `is_live_play` | `GameplayPhase`, `bool` | Whether a frame counts as active gameplay. | Stats frames and internal calculators. |
| `BallSample` | `external/subtr-actor/src/stats/calculators/samples.rs` | `rigid_body` | `boxcars::RigidBody` | Internal stats graph ball sample. | Internal frame input. |
| `PlayerSample` | `external/subtr-actor/src/stats/calculators/samples.rs` | `player_id`, `is_team_0`, `rigid_body`, `boost_amount`, `last_boost_amount`, `boost_active`, `dodge_active`, `powerslide_active`, `match_goals`, `match_assists`, `match_saves`, `match_shots`, `match_score` | `PlayerId`, `bool`, `Option<RigidBody>`, optional stat/boost values, bools | Internal stats graph player sample. | Internal frame input. |

### Stats Timeline Event Streams

The compact stats timeline exposes many event arrays through `ReplayStatsTimelineEvents`. These are not FOFO data contracts. They are subtr-actor event shapes that may be useful later.

| Event Type | Source file | Key Fields / Shape | Purpose |
| --- | --- | --- | --- |
| `TimelineEvent` | `external/subtr-actor/src/stats/calculators/match_stats.rs` | `time`, optional `frame`, `kind`, optional `player_id`, optional `is_team_0` | Generic goals/demos/stat timeline markers. |
| `CorePlayerStatsEvent` / `CoreTeamStatsEvent` | `external/subtr-actor/src/stats/calculators/match_stats.rs` | `time`, `frame`, player/team identity, `delta` stats | Core stat deltas. |
| `GoalContextEvent` | `external/subtr-actor/src/stats/calculators/match_stats.rs` | `time`, `frame`, `scoring_team_is_team_0`, optional `scorer`, most-back players, ball position, ball air time, buildup kind, last touch, per-player contexts | Goal context reconstruction. |
| `GoalTagEvent` | `external/subtr-actor/src/stats/calculators/goal_tags.rs` | `goal_index`, `time`, `frame`, `kind`, scoring team, optional scorer, `confidence`, modifiers, evidence | Goal tag classifiers. |
| `PossessionEvent` | `external/subtr-actor/src/stats/calculators/possession.rs` | `time`, `frame`, `active`, `possession_state`, optional `field_third` | Possession timeline state. |
| `PressureEvent` | `external/subtr-actor/src/stats/calculators/pressure.rs` | `time`, `frame`, `active`, `field_half` | Pressure zone state. |
| `TerritorialPressureEvent` | `external/subtr-actor/src/stats/calculators/territorial_pressure.rs` | start/end time/frame, `team_is_team_0`, duration, offensive half/third time, end reason | Sustained territorial pressure sessions. |
| `PositioningEvent` | `external/subtr-actor/src/stats/calculators/positioning.rs` | time/frame/player/team, tracked time, distance sums, possession/no-possession splits, role/third/half/ball-relative time, caught-ahead count | Positioning/role deltas. |
| `MovementEvent` | `external/subtr-actor/src/stats/calculators/movement.rs` | time/frame/player/team, `dt`, speed, distance, speed band, height band | Movement stat deltas. |
| `RotationPlayerEvent` / `RotationTeamEvent` | `external/subtr-actor/src/stats/calculators/rotation.rs` | player role/depth changes, first-man change counts, team rotation count | Rotation role tracking. |
| `TouchStatsEvent`, `TouchBallMovementEvent`, `TouchLastTouchEvent` | `external/subtr-actor/src/stats/calculators/touch.rs` | touch sample time/frame, player/team, labels, ball speed change, travel/advance/retreat, last-touch player | Touch-derived stat events. |
| `FiftyFiftyEvent` | `external/subtr-actor/src/stats/calculators/fifty_fifty.rs` | start/resolve time/frame, kickoff flag, team players, touch times, dodge contacts, positions, midpoint, plane normal, winning/possession team | Contested ball event. |
| `PassEvent`, `PassLastCompletedEvent` | `external/subtr-actor/src/stats/calculators/pass.rs` | passer, receiver, timing, duration, travel/advance distance, pass kind; last completed player | Passing event detection. |
| `OneTimerEvent` | `external/subtr-actor/src/stats/calculators/one_timer.rs` | shooter, passer, pass timing, duration, travel/advance distance, ball speed, goal alignment | One-timer detection. |
| `BackboardBounceEvent`, `CenterEvent`, `DoubleTapEvent`, `BallCarryEvent`, `RushEvent` | Calculator files under `external/subtr-actor/src/stats/calculators/` | Event-specific timing, player/team, distances, counts, and ball movement fields | Higher-level offensive sequence detection. |
| `CeilingShotEvent`, `WallAerialEvent`, `WallAerialShotEvent`, `FlickEvent`, `MustyFlickEvent`, `DodgeResetEvent`, `SpeedFlipEvent`, `HalfFlipEvent`, `HalfVolleyEvent`, `WavedashEvent`, `WhiffEvent`, `PowerslideEvent` | Calculator files under `external/subtr-actor/src/stats/calculators/` | Mechanic-specific timing, player/team, positions, speeds, alignments, confidence/quality fields | Mechanic and mistake/recovery detectors. Many are heuristic. |
| `BoostPickupComparisonEvent`, `BoostLedgerEvent`, `BoostStateEvent` | `external/subtr-actor/src/stats/calculators/boost.rs` | boost pickup comparison, transaction kind, amount/count/labels, boost before/after, boost state changes | Boost collection/use/ledger timeline. |
| `BumpEvent` | `external/subtr-actor/src/stats/calculators/bump.rs` | initiator/victim, teams, team-bump flag, strength, confidence, distance/speed/impulse, positions | Non-demo collision inference. Experimental/heuristic. |
| `MechanicEvent` | `external/subtr-actor/src/stats/timeline/types.rs` | `id`, `kind`, `player_id`, `is_team_0`, `timing`, optional properties | Generic viewer-friendly mechanics event wrapper built from selected mechanic detectors. |

## JS/WASM / Viewer-Facing Types

| Type / Function | Source file | Fields / Shape | Purpose | Relevance For FOFO Viewer Later |
| --- | --- | --- | --- | --- |
| `validate_replay(data)` | `external/subtr-actor/js/src/lib.rs`; documented in `external/subtr-actor/js/README.md` | Returns `{ valid: true, message }` or `{ valid: false, error }` | Check replay parseability in browser/WASM. | Useful upload validation path. |
| `get_replay_info(data)` | `external/subtr-actor/js/src/lib.rs` | `{ header_size, major_version, minor_version, net_version, properties_count }` | Lightweight replay version/property summary. | Useful before loading large frame payloads. |
| `parse_replay(data)` | `external/subtr-actor/js/src/lib.rs` | Full `boxcars::Replay` converted to JS value | Raw parsed replay. | Usually too large for viewer; useful for probe only if summarized. |
| `get_replay_meta(data, globalFeatureAdders?, playerFeatureAdders?)` | `external/subtr-actor/js/src/lib.rs` | `ReplayMetaWithHeaders` | Metadata and ndarray headers without full matrix. | Useful for preflight/player info. |
| `get_column_headers(globalFeatureAdders?, playerFeatureAdders?)` | `external/subtr-actor/js/src/lib.rs` | `{ global_headers, player_headers }` | Header layout for feature matrix. | Useful for ML/debug views. |
| `get_ndarray_with_info(data, globalFeatureAdders?, playerFeatureAdders?, fps?)` | `external/subtr-actor/js/src/lib.rs` | `{ metadata, array_data, shape }`, where `array_data` is `number[][]` | JS-friendly ndarray-like output. | Potential later ML/prototype path; too big for normal viewer load. |
| `get_replay_frames_data(data)` | `external/subtr-actor/js/src/lib.rs` | `ReplayData` JS value | Structured frame and event output. | Main raw viewer input. |
| `get_replay_frames_data_with_progress` | `external/subtr-actor/js/src/lib.rs` | `ReplayData` plus progress callback payloads `{ stage, processedFrames, totalFrames, progress }` | Long replay load progress. | Important for browser UX. |
| `get_replay_frames_data_json_with_progress` | `external/subtr-actor/js/src/lib.rs` | JSON bytes for `ReplayData` plus progress | Avoids costly JS object transfer in some paths. | Useful worker/bundle optimization. |
| `get_replay_bundle_json_with_progress` | `external/subtr-actor/js/src/lib.rs` | JS object with `rawReplayData: Uint8Array`, `statsTimeline: Uint8Array` | One pass for replay data plus stats timeline. | Useful when viewer needs playback and stats. |
| `get_replay_bundle_json_parts_with_progress` | `external/subtr-actor/js/src/lib.rs` | `rawReplayData: Uint8Array`, `statsTimelineParts: { config, replayMeta, events, frameChunks }` as JSON bytes/chunks | Chunks large stats timeline frames. | Relevant for large replay memory/performance. |
| `get_stats_timeline(data)` / `get_stats_timeline_json(data)` | `external/subtr-actor/js/src/lib.rs` | `ReplayStatsTimelineScaffold` as JS value or JSON bytes | Compact stats timeline. | Future stats overlays/review panels. |
| `get_stats_timeline_json_parts(data, maxFrameChunkBytes?)` | `external/subtr-actor/js/src/lib.rs` | `{ config, replayMeta, events, frameChunks }` as JSON byte chunks | Chunked compact stats timeline transfer. | Relevant for performance. |
| `get_legacy_stats_timeline_json(data)` | `external/subtr-actor/js/src/lib.rs` | JSON bytes for full `ReplayStatsTimeline` | Legacy full snapshot stats timeline. | Avoid unless needed for parity/debug. |
| `RawReplayFramesData` and related `Raw*` aliases | `external/subtr-actor/js/player/src/raw-types.ts` | Aliases to generated TS types such as `ReplayData`, `FrameData`, `PlayerFrame`, `GoalEvent` | Raw generated Rust output in TS. | Confirms raw viewer boundary shape. |
| `normalizeReplayData(raw)` / `normalizeReplayDataAsync(raw)` | `external/subtr-actor/js/player/src/replay-data.ts` | Converts `RawReplayFramesData` to `ReplayModel` | Normalizes raw output for playback. | Direct model for future FOFO viewer research, but not FOFO backend schema. |
| `loadReplayFromBytes(data, options)` | `external/subtr-actor/js/player/src/wasm.ts` | Returns `{ raw, replay }`; may use worker; validates, parses, normalizes | Browser entry point for replay loading. | Useful if FOFO builds a web viewer on top of existing player. |
| `Vec3` / `Quaternion` | `external/subtr-actor/js/player/src/types.ts` | `{ x, y, z }`; `{ x, y, z, w }` | Viewer math primitives. | Same shape as generated vectors/quaternions. |
| `PlaybackFrame` | `external/subtr-actor/js/player/src/types.ts` | `time`, `secondsRemaining`, `gameState`, `kickoffCountdown` | Viewer frame scaffold from `MetadataFrame`. | Useful timeline/playback clock. |
| `BallSample` | `external/subtr-actor/js/player/src/types.ts` | nullable `position`, `linearVelocity`, `angularVelocity`, `rotation` | Viewer ball state. | Ball context for analysis overlays. |
| `PlayerSample` | `external/subtr-actor/js/player/src/types.ts` | presence, nullable position/velocities/rotation/forward/up, boost amount/fraction, boost/powerslide/jump/double-jump/dodge flags | Viewer-normalized player frame. | Strong later viewer signal for context-aware analysis. |
| `ReplayPlayerTrack` | `external/subtr-actor/js/player/src/types.ts` | `id`, `name`, `isTeamZero`, `cameraSettings`, `frames` | Per-player playback track. | Team/player identity and frame alignment. |
| `ReplayBoostPad` / `ReplayBoostPadEvent` | `external/subtr-actor/js/player/src/types.ts` | pad index/id/size/position/events; events have time/frame/available/player id/name | Viewer boost pad state. | Boost context overlays. |
| `ReplayTimelineEvent` | `external/subtr-actor/js/player/src/types.ts`; built in `external/subtr-actor/js/player/src/replay-data.ts` | id/time/seek/frame/kind/label/player fields/location/shot/team/color | Viewer timeline events for goals, shots, saves, assists, demos, and custom overlays. | Natural viewer event marker shape. |
| `ReplayModel` | `external/subtr-actor/js/player/src/types.ts` | `frameCount`, `duration`, `frames`, `ballFrames`, `boostPads`, `players`, `timelineEvents`, `teamZeroNames`, `teamOneNames` | Viewer-ready playback model. | Possible reference for FOFO viewer, not a FOFO parser contract. |

## Output Categories For FOFO Analysis

### Match / Replay Metadata

- Available fields:
  - `ReplayMeta.team_zero`, `ReplayMeta.team_one`: arrays of `PlayerInfo`.
  - `ReplayMeta.all_headers`: replay property list as `(String, HeaderProp)`.
  - `MetadataFrame.time`, `seconds_remaining`, `replicated_game_state_name`, `replicated_game_state_time_remaining`.
  - `GameplayState.team_zero_score`, `team_one_score`, `game_state`, `ball_has_been_hit`, `possession_team_is_team_0`, `scored_on_team_is_team_0`.
  - JS `get_replay_info`: version and property counts.
- Likely value type:
  - Numeric seconds/frames/score integers, enum-like ints, recursive header props.
- Source structure/function:
  - `ReplayMeta`, `MetadataFrame`, `GameplayState`, JS `get_replay_info`.
- Why it may matter:
  - Scoreline, kickoff/post-goal filtering, replay version compatibility, and player/team ordering are core context inputs.

### Teams

- Available fields:
  - `ReplayMeta.team_zero`, `ReplayMeta.team_one`.
  - `PlayerFrame.Data.team`, `PlayerFrame.Data.is_team_0`.
  - `ReplayStatsPlayerIdentity.is_team_0`.
  - `ReplayModel.teamZeroNames`, `ReplayModel.teamOneNames`.
- Likely value type:
  - Arrays of players, optional integer team id, booleans for team zero.
- Source structure/function:
  - `ReplayMeta`, `PlayerFrame`, stats timeline frames, JS `ReplayModel`.
- Why it may matter:
  - Needed to distinguish teammate/opponent context for 2v2 and future 3v3.

### Players

- Available fields:
  - `PlayerInfo.remote_id`, `name`, `stats`.
  - `PlayerData.frames`.
  - `PlayerFrame.Data.player_name`, `team`, `is_team_0`.
  - `PlayerSample.player_id`, `boost_amount`, `match_goals`, `match_assists`, `match_saves`, `match_shots`, `match_score`.
  - JS `ReplayPlayerTrack.id`, `name`, `isTeamZero`, `cameraSettings`.
- Likely value type:
  - Remote id variant object, strings, optional header props, vectors of frames.
- Source structure/function:
  - `PlayerInfo`, `PlayerData`, `PlayerFrame`, `PlayerSample`, JS normalization.
- Why it may matter:
  - Player identity, team assignment, player-specific frame alignment, and context around scoreboard counters.

### Ball State

- Available fields:
  - `BallFrame.Empty` or `BallFrame.Data.rigid_body`.
  - `RigidBody.location`, `rotation`, `linear_velocity`, `angular_velocity`, `sleeping`.
  - `BallSample.position()`, `velocity()`.
  - JS `BallSample.position`, `linearVelocity`, `angularVelocity`, `rotation`.
- Likely value type:
  - Vector/quaternion numeric fields, optional velocities.
- Source structure/function:
  - `BallFrame`, `RigidBodyTs`, `BallSample`, JS `parseBallFrame`.
- Why it may matter:
  - Ball position, speed, direction, height, and goal threat context.

### Player Frame State

- Available fields:
  - `PlayerFrame.Data.rigid_body`.
  - `boost_amount`, `boost_active`, `powerslide_active`, `jump_active`, `double_jump_active`, `dodge_active`.
  - `player_name`, `team`, `is_team_0`.
  - Internal `PlayerSample`: boost, last boost, active flags, match counters.
  - JS `PlayerSample`: position, linear/angular velocity, rotation, forward/up, boost fraction, input/action flags.
- Likely value type:
  - Numeric vectors, optional vectors, raw boost `f32`, booleans, optional identity fields.
- Source structure/function:
  - `PlayerFrame`, `PlayerSample`, JS `parsePlayerFrame`.
- Why it may matter:
  - Core context for rotation, recovery, challenge quality, pressure, boost economy, and teammate/opponent availability.

### Events

- Available fields:
  - `ReplayData` event streams: demos, boost pad events, touches, dodge refreshes, player stat events, goals.
  - `FrameEventsState`: current-frame or since-last-sample event groups.
  - `ReplayStatsTimelineEvents`: higher-level stat/mechanic event arrays.
- Likely value type:
  - Arrays of typed event structs with time/frame/player/team and event-specific fields.
- Source structure/function:
  - `ReplayData`, `FrameEventsState`, `ReplayStatsTimelineEvents`.
- Why it may matter:
  - Events anchor the moments where FOFO may later explain decisions and consequences.

### Goals

- Available fields:
  - `GoalEvent.time`, `frame`, `scoring_team_is_team_0`, optional `player`, optional score fields.
  - `GoalContextEvent`: scorer, most-back players, ball position, ball air time, buildup, last touch, player contexts.
  - `GoalTagEvent`: kind, modifiers, evidence, confidence.
- Likely value type:
  - Numeric time/frame, booleans, optional player IDs, optional vectors/context objects.
- Source structure/function:
  - `GoalEvent`, `GoalContextEvent`, `GoalTagEvent`.
- Why it may matter:
  - Consequence evaluation, scoreline shifts, kickoff/post-goal filtering, and mistake/positive-decision analysis.

### Touches

- Available fields:
  - `TouchEvent.time`, `frame`, `team_is_team_0`, optional `player`, `closest_approach_distance`, `dodge_contact`.
  - `TouchStatsEvent`: player, labels, ball speed change.
  - `TouchBallMovementEvent`: travel/advance/retreat distance.
  - `TouchLastTouchEvent`: last-touch sample.
- Likely value type:
  - Numeric time/frame, player IDs, booleans, floats, string labels.
- Source structure/function:
  - `TouchEvent`, touch calculator event structs.
- Why it may matter:
  - Touch attribution and touch quality are central to context-aware replay analysis.

### Demos

- Available fields:
  - `DemolishInfo`: attacker, victim, time/frame, seconds remaining, attacker/victim velocity, victim location.
  - Stats demo outputs and `BumpEvent` for non-demo collisions.
- Likely value type:
  - Player IDs, vectors, floats, integers.
- Source structure/function:
  - `DemolishInfo`, demo/bump calculators.
- Why it may matter:
  - Player availability, pressure, rotations, open-net context, and whether a decision created or solved pressure.

### Boost / Boost Pads

- Available fields:
  - `PlayerFrame.Data.boost_amount`, `boost_active`.
  - `PlayerSample.boost_amount`, `last_boost_amount`, `boost_active`.
  - `BoostPadEvent.time`, `frame`, `pad_id`, optional `player`, `kind`.
  - `ResolvedBoostPad.index`, `pad_id`, `size`, `position`.
  - `BoostLedgerEvent`, `BoostStateEvent`, `BoostPickupComparisonEvent`.
  - NDArray `PlayerBoost` header: `boost level (raw replay units)`.
- Likely value type:
  - Raw replay boost amount `0.0..255.0` per docs/source, booleans, pad ids, vector positions.
- Source structure/function:
  - `PlayerFrame`, `BoostPadEvent`, `ResolvedBoostPad`, boost stats events, ndarray builtins.
- Why it may matter:
  - Boost context changes whether challenges, rotations, saves, and follow-ups are realistic.

### Stats / Timeline

- Available fields:
  - `ReplayStatsTimelineScaffold.config`, `replay_meta`, `events`, `frames`.
  - Frame scaffold timing/gameplay/player identity fields.
  - Event-backed stat deltas under `ReplayStatsTimelineEvents`.
  - Legacy `ReplayStatsTimeline.frames` with full team/player snapshots.
- Likely value type:
  - Typed event arrays, numeric thresholds, optional gameplay fields, player identity arrays.
- Source structure/function:
  - `StatsTimelineEventCollector`, `StatsTimelineCollector`, `ReplayStatsTimeline*`.
- Why it may matter:
  - Later analysis may use timeline events as supporting signals, but heuristic confidence must be respected.

### NDArray / ML Features

- Available fields:
  - Column headers: `global_headers`, `player_headers`.
  - Matrix rows: global features once per sampled frame, player features repeated by replay player order.
  - Registered global feature names: `BallRigidBody`, `BallRigidBodyNoVelocities`, `BallRigidBodyQuaternions`, `BallRigidBodyQuaternionVelocities`, `BallRigidBodyBasis`, `VelocityAddedBallRigidBodyNoVelocities`, `InterpolatedBallRigidBodyNoVelocities`, `SecondsRemaining`, `CurrentTime`, `FrameTime`, `ReplicatedStateName`, `ReplicatedGameStateTimeRemaining`, `BallHasBeenHit`.
  - Registered player feature names: `PlayerRigidBody`, `PlayerRigidBodyNoVelocities`, `PlayerRigidBodyQuaternions`, `PlayerRigidBodyQuaternionVelocities`, `PlayerRigidBodyBasis`, `PlayerRelativeBallPosition`, `PlayerRelativeBallVelocity`, `PlayerLocalRelativeBallPosition`, `PlayerLocalRelativeBallVelocity`, `VelocityAddedPlayerRigidBodyNoVelocities`, `InterpolatedPlayerRigidBodyNoVelocities`, `PlayerBallDistance` / `PlayerDistanceToBall`, `PlayerBoost`, `PlayerJump`, `PlayerAnyJump`, `PlayerDodgeRefreshed`, `PlayerDemolishedBy`.
- Likely value type:
  - Numeric arrays of `float16`, `float32`, or `float64` in Python; `number[][]` in JS; Rust generic `Array2<F>`.
- Source structure/function:
  - `NDArrayCollector`, `NDArrayColumnHeaders`, `ReplayMetaWithHeaders`, ndarray builtins.
- Why it may matter:
  - Useful later for ML/feature exploration, but should not replace source-level frame inspection.

### Viewer / Playback Data

- Available fields:
  - `ReplayModel.frameCount`, `duration`, `frames`, `ballFrames`, `boostPads`, `players`, `timelineEvents`, team names.
  - `PlaybackFrame.time`, `secondsRemaining`, `gameState`, `kickoffCountdown`.
  - `ReplayPlayerTrack` and `PlayerSample`.
  - `ReplayTimelineEvent` for goals, shots, saves, assists, demos.
- Likely value type:
  - JS objects normalized from raw generated TS types.
- Source structure/function:
  - `external/subtr-actor/js/player/src/types.ts`, `replay-data.ts`, `wasm.ts`.
- Why it may matter:
  - This is useful for a future FOFO viewer, but it is a viewer-normalized shape, not FOFO backend schema.

## Fields Likely Important For Context Analysis

- Player position: `PlayerFrame.Data.rigid_body.location`, JS `PlayerSample.position`, internal `PlayerSample.position()`.
- Ball position: `BallFrame.Data.rigid_body.location`, JS `BallSample.position`, `ShotEventMetadata.ball_position`.
- Velocity/speed: rigid-body `linear_velocity`, `angular_velocity`, `ShotEventMetadata.ball_speed/player_speed`, movement event `speed`, JS velocity fields.
- Boost: `PlayerFrame.Data.boost_amount`, `PlayerSample.boost_amount`, `PlayerBoost` ndarray feature, `BoostStateEvent.boost_amount`, boost ledger before/after.
- Teammate/opponent context: `ReplayMeta.team_zero/team_one`, `PlayerFrame.Data.is_team_0`, `ReplayStatsPlayerIdentity.is_team_0`, `current_in_game_team_player_counts`.
- Pressure: `PressureEvent`, `TerritorialPressureEvent`, `GameplayState.possession_team_is_team_0`, ball/player positions.
- Scoreline: `GoalEvent.team_zero_score/team_one_score`, `GameplayState.team_zero_score/team_one_score`, `MetadataFrame.seconds_remaining`.
- Goals: `GoalEvent`, `GoalContextEvent`, `GoalTagEvent`.
- Touches: `TouchEvent`, `TouchStatsEvent`, `TouchBallMovementEvent`, `TouchLastTouchEvent`.
- Events: `demolish_infos`, `boost_pad_events`, `dodge_refreshed_events`, `player_stat_events`, `goal_events`, stats timeline event arrays.
- Replay timing: `MetadataFrame.time`, `ReplayStatsFrameScaffold.time`, `frame_number`, `dt`, `seconds_remaining`.
- Player identity/team identity: `PlayerInfo.remote_id`, `PlayerInfo.name`, `PlayerFrame.Data.player_name`, `ReplayPlayerTrack.id/name/isTeamZero`.

## Needs Runtime Verification

- Exact Python dict keys after `convert_to_py`, especially enum variant serialization from `serde_json`.
- Exact JSON serialization shape for `RemoteId`, `HeaderProp`, `BallFrame`, `PlayerFrame`, and event enum variants.
- Whether optional fields are present, omitted, or present as `None`/`null` in Python and JS for each fixture.
- Whether boost values in every exposed path are raw `0..255`, normalized, or mixed. Source/docs say `PlayerBoost` and `PlayerFrame.boost_amount` are raw replay units, while JS viewer derives `boostFraction = boost_amount / 255`.
- Frame count and whether all per-player and ball frame arrays align exactly with `metadata_frames`.
- Frame sampling differences between `get_replay_frames_data` and ndarray/stats functions using FPS or `frame_step_seconds`.
- Event counts and event naming for a real 2v2 fixture.
- Whether `TouchEvent.player` is consistently populated or often `None`.
- Whether `GoalEvent.player`, score fields, and `ShotEventMetadata` are present across replay versions.
- Which player header stats appear under `PlayerInfo.stats` for the selected fixture.
- Coordinate normalization and orientation for old replay versions.
- Size of `parse_replay`, `get_replay_frames_data`, compact timeline JSON, and legacy timeline JSON on a 2v2 replay.
- Exact ndarray shape and header ordering for default and custom feature adders.
- Whether generated TypeScript types exactly match the installed/published WASM package in the local environment.

## Risks / Open Questions

- Parser output size can be large. Full raw replay JSON, full frame arrays, full ndarray matrices, and full stats timelines should not be committed.
- `ReplayData.frame_data` may contain large arrays for ball frames and every player track.
- Stats confidence is mixed. `external/subtr-actor/docs/stat-confidence.md` marks direct replay stats and simple frame arithmetic as higher confidence, but pressure, positioning, possession, mechanics, whiffs, bumps, and many goal tags are heuristic or experimental.
- Windows/Python/Rust setup risk remains if the Python extension is not already built. Editable install can require maturin, Rust, MSVC build tools, and potentially network access.
- JS/WASM build or npm install was not run. Generated TS files were inspected statically only.
- Generated outputs must not be committed: full parser dumps, matrices, local `.replay` files, `.venv`, Rust `target`, wheels, `.pyd`, `.so`, cache directories, private replay data, credentials, or Ballchasing tokens.
- Open question: how reliable is player/team identity for replays with substitutions, duplicate platform ids, bots, or late player discovery?
- Open question: which subtr-actor output layer should FOFO use first after runtime verification: `get_replay_frames_data`, compact `get_stats_timeline`, or a smaller purpose-built probe summary?

## Next Recommended Action

Create a temporary local probe that imports `subtr_actor` and parses the built-in 2v2 fixture:

`external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay`

Keep the probe temporary and local. Print only:

- import success and exported function names
- top-level keys for `parse_replay`
- top-level keys for `get_replay_meta`
- top-level keys for `get_replay_frames_data`
- team/player counts and player identity samples
- metadata frame count, ball frame count, player track count, and first/last metadata frame
- event counts for touches, goals, demolitions, boost pad events, dodge refreshes, and player stat events
- first small sample of each event type with field names and value types
- ndarray header counts and first few header names

Do not dump full replay JSON, full frame arrays, full stats timelines, or numeric matrices. Use the runtime probe to confirm this source map before FOFO defines any internal data structures.
