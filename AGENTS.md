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

- ball state
- teammate positions
- opponent positions
- pressure
- boost
- scoreline
- available options
- consequences

Positive gameplay decisions are as important as mistakes.

## Initial Focus

Start with 2v2 replay analysis.

The project should remain expandable toward 3v3 later.

## Decision Priority

When constraints conflict, prioritize in this order:

1. **User instruction in current task** – explicit direction takes precedence
2. **Safety rules** – no secrets, no replays, no `local_data/`, no external modifications
3. **Project principle** – understand parser data first, then structure, then analysis
4. **Workflow rules** – ask before architecture/contract decisions; prefer data-driven design
5. **Style/language rules** – German for communication, English for code identifiers and commits

Example: If a user asks to inspect parser output, and that requires skipping a safety checklist, you still follow rule 2 (safety) before proceeding.

## Parser Error Handling

If replay parsing fails or parser output is malformed:

1. Stop processing immediately.
2. Do not derive data structures from incomplete output.
3. Do not generate analysis or normalized models.
4. Report the error compactly:
   - Error code or parser function name
   - Affected file or input path
   - Brief diagnosis (e.g., "frame count mismatch", "null key in expected dict")
   - Suggested next check (e.g., "verify fixture file integrity", "confirm parser version")
5. Do not commit dumps or partial results.

## Agent Rules

- Do not overdesign upfront.
- Do not create large architecture documents unless explicitly asked.
- Do not add dependencies without explaining why.
- Do not commit private replay files, secrets, tokens, company data, or personal data.
- **Keep changes small and reviewable** (guidelines, not hard limits):
  - One logical change per commit (non-negotiable).
  - Scope guidance: preferably under 5 files; preferably under ~300–500 relevant changed lines.
  - Documentation updates (HANDOFF.md, NEXT_STEPS.md, TASK_LOG.md) are expected companions and do not count toward file limits.
  - Larger, logically cohesive changes are acceptable if justified in the commit message or PR description.
  - If scope grows ambiguous or substantially larger than guidelines, ask the user first.
  - No hard limits that block sensible work blocks; use judgment and explain scope when exceeding guidelines.
- If parser data is unknown, inspect and document before implementing abstractions.
- Prefer documenting assumptions over guessing.

## Workflow

For detailed step planning, project-memory updates, German user communication, and question handling, follow:

- [docs/AGENT_WORKFLOW.md](docs/AGENT_WORKFLOW.md)

Agents should treat this file as the short project guidance and `docs/AGENT_WORKFLOW.md` as the detailed working procedure.

## Flexibility

These instructions are project guardrails, not a rigid task list.

Agents may suggest better next steps when the repository state, evidence, or user goal indicates a more logical path.

However, agents must not silently decide important project direction.

Ask the user before proceeding when:

- the next step would define or change project architecture
- the next step would define FOFO-owned data contracts or stable schemas
- there are multiple reasonable implementation paths
- local/private replay data, API keys, secrets, or user identity mappings could be affected
- a change could touch `external/subtr-actor`, viewer code, analysis logic, ML logic, or generated data
- the task scope is ambiguous
- the result would create a long-term dependency or convention
- the agent would otherwise need to guess

When asking, explain why the question matters and propose 1-3 practical options if useful.

## Language

Respond to the user in German.

This applies even if prompts, code comments, or project documents are written in English.

Use English only when it is useful for:

- code identifiers
- file names
- commit messages
- existing English documentation
- deliberately English project documentation

Questions, summaries, risk reports, and final task reports to the user should be in German.

## Safety

Keep Ballchasing, local replay files, and local generated summaries as optional local research sources.

Do not make Ballchasing a required runtime dependency.

Do not commit:

- API keys
- `.env`
- `.venv/`
- `local_data/`
- `.replay` files
- generated full parser dumps
- private player/replay data
- build artifacts or caches

Treat `external/subtr-actor` as read-only unless the user explicitly requests otherwise.
