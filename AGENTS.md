# FOFO Arena Lab - Agent Instructions

FOFO Arena Lab is a Rocket League replay analysis project.

Claim: Replay Intelligence by Kapautz

Goal:

.replay in -> context-aware analysis out.

## Core Principle

Do not invent fixed classes, modules, data contracts, or architecture before real parser output has been inspected.

Work sequence:

1. Parse replay data.
2. Inspect raw parser output.
3. Document available fields and structures.
4. Derive project-owned data structures from real data.
5. Only then plan analysis, viewer, and coaching modules.

## Analysis Principle

Do not judge isolated statistics.

A gameplay action must be evaluated in context:

* ball state
* teammate positions
* opponent positions
* pressure
* boost
* scoreline
* available options
* consequences

Positive gameplay decisions are as important as mistakes.

## Initial Focus

Start with 2v2 replay analysis.

The project should remain expandable toward 3v3 later.

## Agent Rules

* Do not overdesign upfront.
* Do not create large architecture documents unless explicitly asked.
* Do not add dependencies without explaining why.
* Do not commit private replay files, secrets, tokens, company data, or personal data.
* Keep changes small and reviewable.
* If parser data is unknown, inspect and document before implementing abstractions.
* Prefer documenting assumptions over guessing.
