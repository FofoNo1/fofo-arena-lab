# FOFO Normalized Replay V0 Source Boundary

## Purpose

This document records the Issue #3 decision for the initial **Normalized Replay
V0** source boundary.

It is a short decision note only. It is not a schema, not a data contract, not a
parser adapter plan, not a resolver design, and not analysis, viewer, or ML
logic.

## Decision Summary

- Use `get_replay_frames_data` as the initial primary V0 parser source boundary.
- Use `get_replay_meta` as a supporting source for metadata, headers,
  team/player identity evidence, and column-header awareness.
- Treat `parse_replay` as raw audit, provenance, and debug evidence only, not as
  the normal V0 source boundary.
- Keep ndarray outputs, stats timelines, JS viewer-normalized models, and
  analysis/stat heuristic outputs outside the initial V0 source boundary.
- Base initial public V0 scope on documented public `subtr-actor` fixture
  evidence.
- Focus initial V0 thinking on modern 2v2/doubles evidence.
- Treat older replay formats, 1v1, 3v3, private/local replays, and
  Ballchasing-derived data as variance evidence or later scope, not required V0
  runtime dependencies.
- Keep raw parser evidence separate from later resolved or derived concepts.

## Initial Parser Source Boundary

The initial V0 source boundary starts with parser-visible structured output from
`get_replay_frames_data`.

This includes the currently documented structured replay areas such as frame
data, replay metadata embedded in the frames output, ball/player frame arrays,
boost pads, and core event streams. These remain parser-observed inputs, not
FOFO-owned contracts.

`get_replay_meta` may support V0 decisions where metadata, header props,
team/player identity evidence, or feature column awareness matter. It should not
replace `get_replay_frames_data` as the initial structured replay boundary.

`parse_replay` remains useful for raw parser audit, replay provenance, and debug
checks. It is too low-level and broad to be the normal V0 boundary.

The initial boundary excludes:

- ndarray feature matrices and sampled numeric feature outputs
- stats snapshot and stats timeline outputs
- JS viewer-normalized playback models
- heuristic analysis/stat outputs
- Ballchasing API data as a runtime dependency

## Initial Fixture/Evidence Scope

Initial public V0 decisions should be based on committed documentation from
public `subtr-actor` fixture exploration:

- `docs/SUBTR_ACTOR_FIRST_PROBE_RESULT.md`
- `docs/SUBTR_ACTOR_OUTPUT_FIELD_REFERENCE.md`
- `docs/SUBTR_ACTOR_OUTPUT_SCHEMA_MAP.md`
- `docs/SUBTR_ACTOR_FIXTURE_VARIANCE_REPORT.md`
- `docs/FOFO_NORMALIZED_REPLAY_V0_QUESTIONS.md`

The first V0 thinking should focus on modern ranked doubles / 2v2 evidence,
especially the documented built-in ranked-doubles fixtures.

Older replay formats, 1v1, 3v3, mechanic-focused fixtures, private/local replay
summaries, and Ballchasing-derived data remain useful variance evidence. They do
not become required V0 runtime dependencies or completeness targets in the
initial V0 boundary.

## Raw Parser Evidence Vs Later Resolved/Derived Data

V0 should preserve parser-observed evidence without silently resolving it into
stronger claims.

For the initial boundary:

- Do not infer missing player attribution.
- Do not normalize `null` values into default values.
- Do not translate parser variants into FOFO-owned variants yet.
- Do not assume all player tracks are active match players.
- Do not assume player track count equals visible team size.
- Do not treat empty event streams as parser failure.
- Do not treat heuristic stats as analysis truth.

Later resolved or derived concepts may include active-player selection, team
identity reconciliation, player identity merging, event attribution, boost pad
identity resolution, data-quality summaries, and frame/time validation. Those
concepts must remain outside this source-boundary decision and should be
introduced only after their parser evidence and confidence are documented.

## Explicit Non-Goals

This decision does not create:

- a FOFO schema
- a data contract
- a parser adapter
- a resolver API
- parser code
- viewer logic
- ML logic
- analysis logic
- dependency changes
- replay files
- generated dumps
- `local_data` content
- secrets, tokens, private data, or company data
- changes under `external/subtr-actor`

## Open Follow-Up Questions

- Which minimal fields can a first V0 draft describe without turning them into
  stable required fields?
- Which data-quality notes should be present before any later analysis consumes
  V0 output?
- Which modern 2v2 fixture category should be the first acceptance reference for
  a V0 documentation draft?
- Which parser-observed fields must be marked explicitly as nullable,
  variant-shaped, or optional-empty?
- Which derived concepts must remain named only as future resolver questions?

## Suggested Next Step

Draft a minimal Normalized Replay V0 documentation proposal from this source
boundary and the existing questions document.

That draft should cite parser source areas, preserve raw/nullable/variant
evidence, and avoid schemas, adapters, resolvers, attribution inference,
analysis logic, viewer logic, and ML logic.
