# FOFO Normalized Replay V0 Questions

## Purpose

This document collects unresolved modeling questions that should be answered
before FOFO Arena Lab drafts a first **Normalized Replay V0**.

It is intentionally **not** a schema, not a data contract, not an adapter plan,
not a resolver design, and not analysis/viewer/ML logic.

The questions below are derived from the current parser-output exploration
state. They should help FOFO decide what must be clarified next without
prematurely inventing project-owned structures.

## Evidence Base

Current evidence comes from the existing parser exploration documents:

- `README.md` and `AGENTS.md` establish that FOFO must derive structures from
  real parser output, not from assumptions.
- `docs/HANDOFF.md` and `docs/NEXT_STEPS.md` identify the current project phase
  and explicitly recommend this questions-only document as the next step.
- `docs/TASK_LOG.md` records the parser-output variance work completed so far.
- `docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md` confirms the built-in 2v2 fixture can
  be parsed and summarizes first observed counts.
- `docs/SUBTR_ACTOR_OUTPUT_FIELD_REFERENCE.md` documents observed field shapes
  and parser-visible structures from the first probe.
- `docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md` maps likely parser source structures
  to runtime output areas and lists fields that still need runtime verification.
- `docs/SUBTR_ACTOR_FIXTURE_VARIANCE_REPORT.md` compares variance across
  built-in fixtures, including frame alignment, optional/null fields, event
  stream variance, and frame variant shapes.

The evidence is useful, but it is still bounded. Observed facts are not yet
universal parser guarantees.

## 1. Replay / Match Metadata

### Open questions

- Which replay-level metadata is essential for V0: parser version, replay format
  version, map, playlist, date, duration, team size, scoreline, or only fields
  proven stable in `get_replay_frames_data` and `get_replay_meta`?
- Should V0 distinguish between raw replay header metadata and derived match
  metadata?
- How should V0 represent metadata that is present in one parser output path but
  absent or differently shaped in another?
- Should V0 include parser provenance such as `subtr-actor` version and output
  function name so later changes can be audited?

### Why it matters

FOFO needs enough metadata to understand match context and replay provenance,
but over-selecting fields too early would create a data contract before the
parser output is fully understood.

### Evidence

- The first probe found that `get_replay_meta` exposes `column_headers` and
  `replay_meta`, while `get_replay_frames_data` exposes structured frame and
  event data.
- The variance report found stable top-level key sets for `parse_replay`,
  `get_replay_frames_data`, `frame_data`, and first observed metadata frame
  keys across inspected fixtures.
- The field reference warns that observed counts and samples are fixture facts,
  not universal guarantees.

### Possible decision options

- Start V0 metadata with only fields observed as stable across the variance pass.
- Include a separate provenance/debug section for parser/source information.
- Keep raw header fields out of V0 until header prop serialization is verified
  across more replay types.

### Do not decide yet

Do not define final V0 metadata field names, required fields, or a stable replay
metadata object yet.

## 2. Team Identity

### Open questions

- Which source should be the primary team identity anchor: `meta.team_zero` /
  `meta.team_one`, `PlayerFrame.Data.is_team_0`, event-level team fields, or a
  reconciliation of all available signals?
- How should FOFO handle `PlayerFrame.Data.team` being null while `is_team_0` is
  present?
- Should V0 preserve parser-side `team_zero` / `team_one` naming, or should it
  use a FOFO-neutral concept such as side/team slot later?
- How should V0 represent team identity in replays where player track count does
  not match visible team metadata counts?
- Should team names, colors, or club metadata be V0 concerns, or later viewer
  concerns?

### Why it matters

Context-aware analysis depends on separating teammate and opponent positions.
Incorrect team identity would invalidate pressure, option, rotation, and
consequence interpretation.

### Evidence

- Current handoff evidence says `meta.team_zero` and `meta.team_one` are
  important player/team identity anchors.
- The handoff and task log both note that `PlayerFrame.Data.team` is unreliable
  or null in tested modern replays, while `PlayerFrame.Data.is_team_0` is more
  useful for frame-level team-side information.
- The next-steps document calls out team identity reconciliation between meta
  teams, player track ids, frame `is_team_0`, and event team fields.
- The variance report warns not to assume player track count equals team size.

### Possible decision options

- Treat `meta.team_zero` / `meta.team_one` as the initial roster anchor and use
  frame/event fields as validation signals.
- Treat frame-level `is_team_0` as authoritative for per-frame state but keep
  metadata rosters for identity display.
- Create a future reconciliation note before defining V0, but do not implement a
  resolver yet.

### Do not decide yet

Do not invent a FOFO team resolver, stable team id format, color convention, or
viewer-facing team model yet.

## 3. Player Identity And Active Player Selection

### Open questions

- How should FOFO distinguish parser player tracks from active match players?
- When player track count exceeds visible team metadata counts, which tracks are
  active, inactive, spectator-like, bot-like, substitute-like, or parser
  artifacts?
- Which player identity fields are reliable enough for V0: display name,
  `remote_id`, header `OnlineID`, `PlayerID`, track id, or per-frame
  `player_name`?
- How should duplicate names, duplicate platform ids, bots, platform-specific
  ids, missing ids, and late player discovery be represented?
- Should V0 include identity aliases or only preserve parser-observed identity
  fields for later resolution?

### Why it matters

Player identity connects frames, events, score stats, and future coaching output.
A V0 model that assumes clean one-to-one player identity could break on real
replays and could misattribute touches, goals, demos, or boost usage.

### Evidence

- The first 2v2 probe observed four player tracks and two players per metadata
  team.
- The variance report observed fixture-dependent player track counts and warns
  not to assume player track count equals team size or that all tracks are
  active players.
- The schema map lists reliability questions around substitutions, duplicate
  platform ids, bots, and late player discovery.
- The field reference lists player identity sources such as `PlayerInfo.name`,
  `remote_id`, `stats`, player track ids, and `PlayerFrame.Data.player_name`.

### Possible decision options

- Keep parser player tracks and match roster candidates separate in V0.
- Require a documented active-player selection rule before V0 is drafted.
- Defer identity normalization and preserve parser-observed identity evidence
  only.

### Do not decide yet

Do not define player id semantics, identity merge rules, or an active roster
resolver yet.

## 4. Frame Alignment And Timebase

### Open questions

- Can V0 assume `metadata_frames`, `ball_data.frames`, and every player frame
  array are aligned by index, or should this remain a validation result attached
  to each replay?
- Should events reference both `frame` and `time`, or should one be canonical?
- How should V0 handle parser outputs that use different sampling controls such
  as frame arrays, ndarray FPS, or `frame_step_seconds`?
- What should happen if a future replay has mismatched metadata, ball, or player
  frame lengths?
- Should kickoff countdown, replicated game state, and seconds remaining be
  considered part of frame alignment or match-phase metadata?

### Why it matters

Frame alignment is the backbone for context-aware analysis. Ball, player, and
score context must refer to the same moment before any later decision review can
be trusted.

### Evidence

- Handoff evidence says metadata frames, ball frames, and player frame arrays
  aligned in tested samples.
- The first probe observed 9530 metadata frames and four player tracks for the
  built-in 2v2 fixture.
- The variance report observed ball/player frame lists aligned with metadata
  frame count in the inspected fixture set, but still frames this as observed
  fixture evidence.
- The schema map says frame counts and sampling differences between output
  functions still need runtime verification.

### Possible decision options

- Treat alignment as a per-replay validation result rather than a universal
  assumption.
- Store both event `time` and event `frame` as parser-observed anchors once V0 is
  drafted.
- Defer ndarray/timebase alignment until FOFO actually needs ML or feature
  matrix inputs.

### Do not decide yet

Do not define a canonical FOFO frame index, interpolation policy, or resampling
contract yet.

## 5. Ball Frames And Rigid Body State

### Open questions

- How should V0 represent ball frames when the parser returns `Data` versus a
  scalar/string variant such as a likely `Empty` value?
- Which rigid-body subfields are essential for V0: location, rotation, linear
  velocity, angular velocity, or only the fields observed present per frame?
- How should nullable ball velocity fields be represented without implying zero
  velocity?
- Should ball-frame absence be represented as missing state, unknown state,
  parser empty variant, or replay phase state?
- Should coordinate orientation and replay-version differences be investigated
  before V0 names coordinate fields?

### Why it matters

Ball state is central to context. Missing or nullable velocity must not be
silently interpreted as no motion, and variant handling affects every later
spatial or pressure calculation.

### Evidence

- The variance report observed both `Data` and scalar string variants in ball
  frames across fixtures.
- Deeper sampled `BallFrame.Data` contained `rigid_body` only.
- Rigid-body keys included `sleeping`, `location`, `rotation`,
  `linear_velocity`, and `angular_velocity`.
- Ball rigid-body velocity fields were sampled as null in early portions of all
  deeper fixtures.
- The schema map flags coordinate normalization and orientation for old replay
  versions as needing runtime verification.

### Possible decision options

- Keep explicit parser variant state in V0 rather than flattening every ball
  frame into required numeric fields.
- Treat null velocity as unknown/unavailable, not zero.
- Defer coordinate normalization decisions until older replay behavior is
  inspected further.

### Do not decide yet

Do not define final ball-frame field names, coordinate transforms, or velocity
fallback behavior yet.

## 6. Player Frames And Car State

### Open questions

- How should V0 represent player frames when the parser returns `Data` versus
  scalar/string variants?
- Which player-frame fields are essential for V0: rigid body, boost amount,
  boost active, jump/dodge flags, powerslide, player name, team fields, or a
  smaller observed subset?
- How should nullable player rigid-body velocity fields be represented?
- Should `PlayerFrame.Data.player_name` be treated as identity evidence, display
  metadata, or frame-local parser detail?
- Should action flags be considered raw parser state only, or should they later
  be converted into gameplay concepts such as recovery, challenge readiness, or
  mechanics?

### Why it matters

Player state defines available options, boost economy, recovery, pressure, and
teammate/opponent context. Flattening parser variants too early could hide
missing frames or replay-version differences.

### Evidence

- The variance report observed both `Data` and scalar string variants in player
  frames, with older fixtures having many string-variant frames.
- Deeper sampled `PlayerFrame.Data` keys included `rigid_body`, `boost_amount`,
  `boost_active`, `powerslide_active`, `jump_active`, `double_jump_active`,
  `dodge_active`, `player_name`, `team`, and `is_team_0`.
- Player rigid-body velocity fields were usually present in deeper modern
  samples, but sampled nulls occurred in the 2017 fixture.
- Current evidence says `PlayerFrame.Data.team` is null/unreliable in tested
  modern replays.

### Possible decision options

- Preserve frame variants explicitly and require consumers to handle non-`Data`
  frames.
- Include raw car-state fields only after confirming their presence and null
  behavior across the intended V0 replay set.
- Defer gameplay interpretations of flags to later analysis modules.

### Do not decide yet

Do not define player-frame contracts, recovery/challenge states, or action
interpretation logic yet.

## 7. Events And Timeline Semantics

### Open questions

- Which parser event streams belong in V0: touches, goals, demos, boost pad
  events, dodge refreshes, player stat events, or only streams needed to anchor
  context?
- Should empty event streams be represented as valid empty lists, omitted fields,
  or warnings?
- How should V0 order events that share the same frame or time?
- Should `player_stat_events` be treated as raw replay events, derived stats
  events, or later supporting evidence only?
- Which stats/timeline outputs are reliable enough to use as V0 evidence, given
  that some stats are heuristic or experimental?

### Why it matters

Events are likely anchors for later review, but treating heuristic or empty
streams incorrectly could create false analysis signals.

### Evidence

- The first probe observed top-level event streams for boost pad events,
  demolitions, dodge refreshes, goal events, player stat events, and touch
  events.
- The variance report found core event streams were always present as lists,
  even when empty, and event counts varied heavily by fixture type, playlist,
  replay age, and mechanic focus.
- The field reference says stats/timeline outputs may be useful as supporting
  signals, but heuristic stats should not be treated as ground truth.
- The schema map warns that stats confidence is mixed and pressure, possession,
  mechanics, whiffs, bumps, and many goal tags are heuristic or experimental.

### Possible decision options

- Include only raw parser event streams in V0 questions for now and defer
  heuristic stats/timeline signals.
- Treat empty streams as valid observed parser output, not parser failure.
- Require each V0 event type to carry parser-source notes once a schema is later
  drafted.

### Do not decide yet

Do not define event classes, event taxonomy, event ordering guarantees, or
analysis-level event meaning yet.

## 8. Touch / Goal / Demo / Boost Attribution

### Open questions

- How should V0 represent event attribution when `player` is null?
- Should team attribution be preserved independently from player attribution
  when event-level team fields exist?
- How should FOFO distinguish direct parser attribution from later inferred or
  resolved attribution?
- Should touch attribution use `player`, `team_is_team_0`,
  `closest_approach_distance`, frame-local nearest-player context, or no
  inference in V0?
- How should boost pad pickups be represented when many `boost_pad_events` have
  null `player` fields?
- Should goal attribution allow null scorer while still preserving score changes
  and goal frame/time?
- For demos, which ids or fields identify attacker and victim reliably across
  replay variants?

### Why it matters

Attribution errors are especially damaging: they would assign decisions,
outcomes, or resources to the wrong player. V0 should separate parser-observed
attribution from future inferred attribution.

### Evidence

- Handoff evidence says `touch_events.player` and `boost_pad_events.player` can
  be null, and `goal_events.player` can be null in fixture variance.
- The variance report observed nullable touch player fields, nullable
  `closest_approach_distance`, often-null boost pad event player fields, and one
  fixture with a null goal player.
- In the built-in 2v2 fixture, boost pad events were numerous, but the variance
  report notes many null player fields for boost pad events.
- The field reference identifies touch, goal, demo, and boost fields as
  context-relevant but does not make them FOFO contracts.

### Possible decision options

- Preserve parser attribution as nullable and add no inference in V0.
- Later introduce a separate resolved-attribution layer, clearly marked as
  derived and lower confidence.
- Require V0 to distinguish event team side from event player id where both are
  available.

### Do not decide yet

Do not implement attribution resolvers or infer missing player attribution yet.

## 9. Boost Amounts, Boost Pads, And Resource Context

### Open questions

- Are boost amounts consistently raw replay units (`0..255`) in all selected
  parser paths, or can some paths expose normalized values?
- Should V0 preserve raw boost amount only, normalized percentage only, or both
  after unit behavior is verified?
- How should V0 represent `boost_active` versus boost amount?
- How should boost pad identity be represented when `boost_pads[].pad_id` can be
  null?
- Should boost pad availability/pickup events be considered V0 raw state, or
  deferred until attribution and pad id variance are better understood?

### Why it matters

Boost availability is core to evaluating realistic options. Unit confusion or
incorrect pad attribution would distort challenge, rotation, and recovery
context.

### Evidence

- The schema map says `PlayerBoost` and `PlayerFrame.boost_amount` are raw
  replay units, while the JS viewer derives `boostFraction = boost_amount / 255`,
  but it still flags boost units across exposed paths as needing runtime
  verification.
- The field reference lists boost amount, boost active, boost pad events,
  resolved boost pads, and ndarray `PlayerBoost` as context-relevant fields.
- The variance report observed `boost_pads` present with 34 items in every
  fixture, but boost pad events could be zero in older replay output.
- The variance report also observed nullable `boost_pads[].pad_id` in some
  fixtures and often-null `boost_pad_events[].player`.

### Possible decision options

- Preserve raw parser boost units in V0 and document units explicitly later.
- Defer normalized boost percentages to viewer or analysis layers.
- Treat boost pad id and pickup player as nullable parser fields until more
  evidence exists.

### Do not decide yet

Do not define boost-unit conversion rules, pad-id resolver behavior, or boost
resource metrics yet.

## 10. Optional / Null Fields And Missing Data Policy

### Open questions

- Should V0 require every nullable parser field to remain nullable, or should
  V0 omit unavailable fields?
- How should FOFO distinguish null, omitted, empty list, parser empty variant,
  and validation failure?
- Which null fields should produce warnings, and which are normal replay/parser
  behavior?
- Should V0 carry per-replay data-quality notes for null counts and missing
  structures?

### Why it matters

Null handling determines whether FOFO can safely process old, focused, private,
Ballchasing, and modern ranked replays without inventing false data.

### Evidence

- The variance report says optional fields should be treated as genuinely
  optional until more replay types are inspected.
- Observed nulls include touch player, touch closest approach distance, boost pad
  event player, boost pad id, goal player, player frame team, and rigid-body
  velocities.
- The schema map asks whether optional fields are present, omitted, or present as
  `None`/`null` in Python and JS for each fixture.
- Handoff evidence says event streams can be empty and should not be treated as
  missing parser output.

### Possible decision options

- Keep parser nulls explicit and add data-quality summaries later.
- Treat empty event streams as valid, but mismatched frame lengths or malformed
  variants as validation warnings/errors.
- Defer any fill/default policy until V0 schema drafting.

### Do not decide yet

Do not choose default values for null numeric fields, missing player ids, or
missing event attribution yet.

## 11. Variant Handling And Parser Serialization Shapes

### Open questions

- How exactly should FOFO identify enum/variant shapes emitted through Python
  conversion and JSON serialization?
- Are scalar string variants always unit variants such as `Empty`, or are there
  other scalar representations?
- Should V0 preserve parser variant names directly or translate them into a
  FOFO-owned vocabulary later?
- How should variant-shaped event fields such as `BoostPadEvent.kind` be
  represented without hard-coding unverified forms?

### Why it matters

Variant handling affects ball frames, player frames, boost events, remote ids,
header props, and event metadata. Hard-coding shapes too early could make V0
fragile across parser versions.

### Evidence

- The schema map flags exact Python dict keys after `convert_to_py` and enum
  variant serialization from `serde_json` as needing runtime verification.
- It also flags JSON serialization shape for `RemoteId`, `HeaderProp`,
  `BallFrame`, `PlayerFrame`, and event enum variants.
- The variance report observed frame `Data` variants and scalar string variants,
  and notes that string variants likely represent unit variants but should not be
  hard-coded yet.
- `BoostPadEvent.kind` was observed as variant-shaped.

### Possible decision options

- Preserve observed parser variants verbatim in a future raw/intermediate layer.
- Create a minimal variant-normalization table only after more samples are
  inspected.
- Avoid translating variants in V0 unless the parser shape is verified.

### Do not decide yet

Do not define FOFO-owned variant names or variant decoding rules yet.

## 12. Data Quality, Validation, And Warnings

### Open questions

- Which conditions should be considered parser failure, V0 validation failure,
  warning, or normal variance?
- Should V0 include explicit quality indicators such as frame alignment status,
  null attribution counts, variant counts, and event stream counts?
- How should FOFO report malformed parser output without deriving structures from
  incomplete data?
- Should data-quality checks be generated by temporary probes first, or designed
  as part of V0 later?

### Why it matters

FOFO's later analysis must know when input context is trustworthy. Data quality
also protects against silently interpreting incomplete parser output as real
match state.

### Evidence

- `AGENTS.md` says parsing failures or malformed parser output must stop
  processing immediately and must not produce normalized models from incomplete
  output.
- Handoff evidence and the variance report distinguish normal empty event
  streams from missing parser output.
- The variance report lists multiple areas needing verification and warns that
  observed counts are not universal guarantees.
- The field reference warns not to commit full dumps or generated parser output.

### Possible decision options

- Draft V0 later with a small validation/quality section before analysis logic
  exists.
- Keep validation outputs separate from normalized match state to avoid making
  warnings part of core gameplay data prematurely.
- Start with documented probe checks before implementing reusable validation
  code.

### Do not decide yet

Do not implement validation classes, warning enums, or parser error taxonomies
beyond the existing project rule yet.

## 13. Ballchasing Replays Versus Local User Replays

### Open questions

- Should V0 be tested against built-in fixtures first, local user replays first,
  Ballchasing-derived fixtures first, or a clearly separated mix?
- How should FOFO document evidence from ignored `local_data/` summaries without
  making private replays or generated reports part of the repository?
- Should Ballchasing identifiers, URLs, or metadata ever enter V0, or remain
  optional local research metadata?
- How should FOFO prevent public fixture evidence and private replay evidence
  from being mixed in a way that creates privacy or reproducibility issues?

### Why it matters

FOFO needs real replay variance, but local replay data and Ballchasing data have
privacy, reproducibility, and dependency implications.

### Evidence

- Project safety rules say not to commit local replay files, `local_data/`, full
  parser dumps, secrets, tokens, or private replay data.
- Handoff says `local_data/` is ignored and contains local replay inputs and
  generated local summaries only.
- Handoff also notes modern/local 2v2 variance was explored through ignored
  local data inputs, while built-in fixtures remain documented evidence.
- Project safety rules say Ballchasing should remain optional local research and
  must not become a required runtime dependency.

### Possible decision options

- Base initial public V0 discussion on committed fixture documentation only.
- Use local/private replay findings only as summarized non-identifying evidence.
- Keep Ballchasing metadata outside V0 unless a later explicit import workflow is
  designed.

### Do not decide yet

Do not make Ballchasing, local replay paths, replay ids, or private summaries
part of V0.

## 14. Replay Version, Playlist, And Mode Variance

### Open questions

- Which replay categories must V0 support initially: only modern ranked 2v2,
  all 2v2 fixtures, old replay versions, 1v1/3v3 fixtures for negative tests, or
  private/Ballchasing examples?
- Should V0 explicitly scope itself to 2v2 while preserving enough information
  to avoid blocking later 3v3 support?
- How should V0 represent old replay formats with different boost pad event
  availability, null pad ids, nullable velocities, and many string-variant
  player frames?
- Should playlist/mode detection be required before active-player selection?

### Why it matters

The project starts with 2v2 but should remain expandable toward 3v3. V0 should
not silently assume one playlist or replay era when parser evidence already
shows broader variance.

### Evidence

- README and AGENTS define initial focus as 2v2 with later 3v3 expandability.
- The first probe used a built-in ranked doubles fixture.
- The variance report compared duel, doubles, standard, old replay formats,
  mechanic-focused fixtures, private fixtures, and Ballchasing fixtures.
- The variance report found event counts vary heavily by fixture type, playlist,
  replay age, and mechanic focus.

### Possible decision options

- Scope V0 to modern 2v2 replay normalization questions first, with explicit
  non-goals for older formats and 3v3.
- Include old/3v3 fixtures as variance tests but not as V0 completeness targets.
- Require V0 to record observed team/player counts without assuming exactly 2v2
  in every parser output.

### Do not decide yet

Do not commit to full old-format, 1v1, or 3v3 normalization support in V0 unless
explicitly requested later.

## 15. Later Resolver Questions

### Open questions

- Which future resolver layers may be needed: team reconciliation, active-player
  selection, player identity merge, event attribution, boost pad identity,
  frame/time alignment, or replay-version normalization?
- Which resolver questions must be answered before V0, and which can wait until
  after a raw normalized replay shape exists?
- How should FOFO mark a field as parser-observed versus derived by a future
  resolver?
- Should future resolver confidence be represented, or is that an analysis-layer
  concern?

### Why it matters

Several open issues clearly point toward resolvers, but building resolver classes
now would violate the project principle. The useful next step is to name the
questions without designing the machinery.

### Evidence

- Handoff and next steps identify active-player selection, team identity
  reconciliation, optional attribution, frame variants, frame/event alignment,
  nullable velocity/boost/event fields, and playlist variance as unresolved.
- The schema map explicitly asks which subtr-actor output layer FOFO should use
  first after runtime verification.
- The variance report says V0 should be informed by parser/player track
  distinctions, optional/null handling, enum/variant shapes, event streams,
  boost variance, and team identity from more than one source.

### Possible decision options

- Keep V0 limited to parser-observed data plus validation notes, and defer
  derived resolver outputs.
- Draft resolver requirements as a later document after V0 questions are
  answered.
- Require every future derived field to cite its parser source and confidence.

### Do not decide yet

Do not create resolver classes, resolver APIs, derived identity fields, or
confidence schemas yet.

## Cross-Cutting Questions To Answer Before Drafting V0

- What is the minimal replay set that V0 must be checked against before it is
  credible: one built-in 2v2 fixture, both built-in ranked doubles fixtures,
  selected old-format fixtures, and/or non-identifying local summaries?
- Which parser output function is the first V0 source of truth:
  `get_replay_frames_data`, `get_replay_meta`, a combination of both, or a
  smaller purpose-built probe summary?
- Which observations are stable enough to become V0 requirements, and which must
  remain optional evidence fields?
- How will V0 separate raw parser evidence, validation/quality notes, and later
  derived/resolved concepts?
- How will FOFO avoid making analysis judgments while defining a replay data
  foundation?

## Explicit Non-Decisions

Before a first V0 draft, FOFO should **not** decide or implement:

- FOFO-owned schemas, classes, data contracts, adapters, or resolver APIs.
- Analysis, coach, viewer, ML, pressure, rotation, possession, or decision logic.
- Inferred player attribution for null event `player` fields.
- Final player/team identity semantics.
- Canonical coordinate transforms or resampling/interpolation rules.
- Ballchasing or private local replay data as required runtime dependencies.
- Any change under `external/subtr-actor`.

## Suggested Immediate Follow-Up

Before drafting Normalized Replay V0, choose the smallest evidence set and source
boundary for V0. A practical next step would be a short decision note that answers
only:

1. Which parser output path is the initial V0 source boundary?
2. Which replay fixtures must V0 account for initially?
3. Which fields remain raw parser evidence versus later resolved/derived data?

If these cannot be answered from committed evidence, ask the user before making
project-direction decisions.
