# FOFO Normalized Replay V0 Parser Evidence Summary

## Purpose

This document records the minimal parser-visible evidence selected for the next
FOFO Normalized Replay V0 exploration step.

It is not a schema, not a data contract, not a parser adapter, not a resolver,
and not analysis, viewer, or ML logic. It summarizes observed parser evidence
only.

## Source Boundary

This summary follows the Issue #3 source-boundary decision:

- Primary source: `get_replay_frames_data`
- Supporting source: `get_replay_meta`
- Outside this boundary: `parse_replay`, ndarray outputs, stats timelines, JS
  viewer-normalized models, and heuristic analysis/stat outputs

The supporting `get_replay_meta` use here is limited to metadata/team evidence.
It does not make ndarray feature matrices part of the V0 parser source boundary.

## Fixture Set

The initial evidence set is limited to documented public `subtr-actor` ranked
doubles fixtures:

- `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay`
- `external/subtr-actor/assets/post-eac-ranked-doubles-2026-04-28.replay`

These fixtures match FOFO's initial 2v2 focus. Older replay formats, 1v1, 3v3,
private/local replays, and Ballchasing-derived data remain variance evidence or
later scope, not required V0 runtime dependencies.

## Parser-Visible Evidence Summary

| Fixture | Metadata Frames | Ball Frames | Player Tracks | Player Frame Range | Aligned | Team Zero | Team One | get_replay_meta Teams | Boost Pads |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- | ---: |
| `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay` | 9530 | 9530 | 4 | 9530..9530 | True | 2 (Quantavious1234, Jtabor26) | 2 (Darko_oklm, Baptiste2702382) | 2+2 | 34 |
| `external/subtr-actor/assets/post-eac-ranked-doubles-2026-04-28.replay` | 10629 | 10629 | 4 | 10629..10629 | True | 2 (luhbalenci, timehake) | 2 (2Fum2Tastic, Ragnar) | 2+2 | 34 |

| Fixture | Touches | Goals | Demos | Boost Pad Events | Dodge Refreshes | Player Stat Events |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay` | 113 | 5 | 2 | 1581 | 0 | 17 |
| `external/subtr-actor/assets/post-eac-ranked-doubles-2026-04-28.replay` | 137 | 8 | 1 | 1831 | 4 | 28 |

## Null / Optional Observations

| Fixture | touch_events.player | goal_events.player | boost_pad_events.player | boost_pads.pad_id | PlayerFrame.Data.team |
| --- | --- | --- | --- | --- | --- |
| `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay` | null:13, present:100 | null:0, present:5 | null:1266, present:315 | null:0, present:34 | null:37857, present:0 |
| `external/subtr-actor/assets/post-eac-ranked-doubles-2026-04-28.replay` | null:15, present:122 | null:0, present:8 | null:1422, present:409 | null:0, present:34 | null:42401, present:0 |

These are parser-observed nulls. They are not defaults, failures, or inferred
values.

## Variant And Alignment Observations

| Fixture | BallFrame Variants | PlayerFrame Variants |
| --- | --- | --- |
| `external/subtr-actor/assets/recent-ranked-doubles-2026-03-10.replay` | Data:9264, Empty:266 | Data:37857, Empty:263 |
| `external/subtr-actor/assets/post-eac-ranked-doubles-2026-04-28.replay` | Data:10199, Empty:430 | Data:42401, Empty:115 |

For this two-fixture evidence set, metadata frames, ball frames, and player
frame arrays were aligned by count. This remains observed fixture evidence, not
a universal parser guarantee.

The variant labels above are parser-observed labels. They are not translated
into FOFO-owned variant names.

## Explicit Non-Goals

This summary does not create or imply:

- a FOFO schema
- a stable data contract
- a parser adapter
- a resolver API
- inferred player attribution
- analysis logic
- viewer logic
- ML logic
- dependency changes
- replay files or generated dumps
- `local_data` content
- changes under `external/subtr-actor`

## Suggested Next Step

Use this evidence summary, the V0 questions document, and the source-boundary
decision as inputs for a minimal `docs/FOFO_NORMALIZED_REPLAY_V0.md`
documentation proposal.

That proposal should cite parser source areas and preserve raw parser evidence
without introducing schemas, adapters, resolvers, attribution inference,
analysis logic, viewer logic, or ML logic.
