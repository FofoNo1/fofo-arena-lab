You are working in the FOFO Arena Lab repository.

Current task:
Review the current state, compare it with the project goal, decide the next logical step, execute only the smallest safe scoped change, run checks, and update project memory docs.

Read and follow:

- README.md
- AGENTS.md
- docs/HANDOFF.md
- docs/NEXT_STEPS.md
- docs/TASK_LOG.md
- relevant docs for the current topic

Project principle:
Understand parser/replay data first.
Build structure second.
Develop analysis third.
Visualize and expand afterwards.

Workflow:

1. Inspect the current repo state.
2. Summarize the current Ist-Stand.
3. Identify the desired Soll-Stand for the current phase.
4. Decide the smallest logical next step.
5. If the step is risky, broad, or architectural, stop and report a plan only.
6. If important questions or unclear decisions come up, stop and ask before continuing.
7. If parsing is required and parser output is malformed or fails, stop immediately:
   - Do not derive structures from incomplete data.
   - Report error compactly (code, file, diagnosis, next check).
   - Do not commit partial dumps or results.
   - Ask user about recovery steps or alternate fixtures.
8. If the step is small and safe, implement it.
9. Run relevant checks.
10. Run whitespace/check validation, especially:
    - git diff --check
    - syntax/compile checks where applicable
11. Do not touch out-of-scope files.
12. Do not modify external/subtr-actor.
13. Do not commit local_data, .replay files, generated dumps, secrets, tokens, or .venv.
14. Update these docs logically if project state changed:

    - docs/HANDOFF.md
    - docs/NEXT_STEPS.md
    - docs/TASK_LOG.md

Important question rule:
If important questions or unclear decisions come up, stop and ask before continuing.

Ask the user before proceeding when:

- the next step would define or change project architecture
- the next step would define FOFO data contracts or stable schemas
- there are multiple reasonable implementation paths
- local/private replay data, API keys, secrets, or user identity mappings could be affected
- a change could touch external/subtr-actor, viewer code, analysis logic, ML logic, or generated data
- the task scope is ambiguous
- the result would create a long-term dependency or convention
- the agent would otherwise need to guess

Do not silently decide important project direction.
Document the question, explain why it matters, and propose 1–3 options if helpful.

Important question rule:
If important questions or unclear decisions come up, stop and ask before continuing.
...

Language rule:
Always respond to the user in German.

This applies even if the prompt or project documents are written in English.

Use English only when:

- writing code identifiers
- writing file names
- writing commit messages if the repository convention uses English
- quoting existing English documentation
- creating English project documentation on purpose

When asking questions, ask them in German.
When reporting results, use German summaries.
Do not silently switch to English just because the prompt was written in English.

At the end, report:

- current state before work
- chosen next step and why
- files changed
- commands/checks run
- whitespace/check results
- docs updated
- risks/open questions
- suggested next action
