# FOFO Arena Lab

**Replay Intelligence by Kapautz**

FOFO Arena Lab is a Rocket League replay analysis project focused on context-aware gameplay evaluation.

The goal is simple:

```txt
.replay in → context-aware analysis out
```

Instead of judging isolated statistics, FOFO Arena Lab aims to understand gameplay decisions within the full match context: ball state, teammates, opponents, pressure, boost, scoreline, available options, and the consequences of each decision.

## Why this project exists

Many replay analysis tools are good at measuring individual stats. They can tell you that you were slow, low on boost, too far back, or too passive.

FOFO Arena Lab aims to go one step deeper:

```txt
Was the action actually bad in that specific situation?
Or was it the right decision because of the context?
```

For example, being slow is not always bad. Sometimes delaying the play is the correct decision because a teammate is recovering, the opponent has no immediate shot threat, or challenging would create an unnecessary overcommit.

The project should also highlight positive gameplay decisions, not only mistakes. A useful analysis tool should show what to improve, but also what to keep.

## Current development principle

This project starts from real replay data.

Data structures, modules, and analysis layers should be derived from actual parser output instead of being overdesigned upfront.

The intended workflow is:

```txt
1. Parse real replay data
2. Inspect the raw output
3. Document available fields and structures
4. Derive an internal data model
5. Build analysis modules on top of that foundation
6. Add viewer, timeline, and coaching features step by step
```

## Initial focus

- First focus: 2v2 replay analysis
- Long-term goal: expandable context-aware analysis for 2v2 and 3v3
- Main idea: evaluate decisions in context, not just isolated numbers

## Project status

Early foundation phase.

The first goal is to understand parser output and build a clean, flexible project structure.

## Contributions

Ideas, feedback, experiments, and technical suggestions are welcome.

This project is still young, so the most useful contributions right now are:

- parser-output exploration
- replay-data documentation
- architecture feedback
- ideas for context-aware analysis
- Rocket League tactical knowledge
- viewer and visualization ideas

## Note

FOFO Arena Lab is an unofficial fan-made project and is not affiliated with Rocket League, Psyonix, or Epic Games.
