# Handoff

This file is the compact handoff for continuing FOFO Arena Lab in a new chat or with another agent.

## Project identity

Project name: FOFO Arena Lab

Claim: Replay Intelligence by Kapautz

Repository: FofoNo1/fofo-arena-lab

## Core goal

.replay in -> context-aware Rocket League analysis out

The project should not judge isolated statistics. It should evaluate gameplay decisions in the context of the full game situation.

## Current project phase

Early foundation and setup phase.

The repository contains the initial README and German/English project definition documents. The project intentionally avoids fixed data structures, classes, or modules until real parser output has been inspected.

## Current guiding principle

Understand the data first.  
Build structure second.  
Develop analysis third.  
Visualize and expand afterwards.

## Initial focus

- First visible analysis focus: 2v2 replay analysis
- Long-term direction: expandable context-aware analysis for 2v2 and 3v3
- Positive gameplay decisions should be identified alongside mistakes

## Important constraints

- Do not overdesign upfront.
- Do not invent fixed data models before parser output is known.
- Do not commit private replay files or heavy generated parser outputs.
- Do not commit secrets, tokens, company data, or personal data.
- Keep changes small and reviewable.

## Current setup files

- README.md
- AGENTS.md
- docs/PROJECT_DEFINITION_EN.md
- docs/PROJECT_DEFINITION_SHORT_EN.md
- docs/TASK_LOG.md
- docs/NEXT_STEPS.md
- docs/HANDOFF.md

## Next recommended step

Prepare a minimal parser-output exploration workflow.

The next work should focus on parsing one replay locally, inspecting the raw output, and documenting the available fields and structures before planning internal data models or analysis modules.

Suggested next branch:

codex/parser-output-exploration

## How to continue in a new chat

Tell the assistant:

We are working on FOFO Arena Lab. Please use the GitHub repository FofoNo1/fofo-arena-lab and follow README.md, AGENTS.md, docs/HANDOFF.md, and docs/NEXT_STEPS.md. Continue from the current foundation/setup phase and do not overdesign before parser output has been inspected.
