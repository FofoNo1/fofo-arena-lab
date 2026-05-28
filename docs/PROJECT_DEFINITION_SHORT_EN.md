# FOFO Arena Lab — Short Project Definition

**Replay Intelligence by Kapautz**

FOFO Arena Lab is a Rocket League replay analysis project.

## Goal

`.replay` in → context-aware analysis out.

The project should not only evaluate isolated statistics. Instead, it should understand gameplay situations as a whole.

## Important Principle

Do not invent fixed classes, modules, or data contracts before real parser output has been inspected.

## Working Approach

1. Parse a replay.
2. Inspect the raw output.
3. Document the available fields and structures.
4. Derive a useful internal data model from the actual data.
5. Only then plan analysis, viewer, and coaching modules.

## Initial Focus

The first focus is 2v2 replay analysis.

Long-term, the project should be expandable to 3v3 analysis.

## Analysis Principle

An action is not automatically good or bad.

It has to be evaluated in context:

- ball state
- players
- opponents
- boost
- pressure
- scoreline
- available options
- consequences of the decision

FOFO Arena Lab should also identify positive aspects of gameplay, not only mistakes.
