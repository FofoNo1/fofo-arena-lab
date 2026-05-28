# FOFO Arena Lab

**Replay Intelligence by Kapautz**

FOFO Arena Lab is a project for context-aware Rocket League replay analysis.

The goal is to read `.replay` files, inspect the contained game data, structure that data in a useful way, and generate an understandable analysis of the match.

The core of the project is not the raw output of statistics. The core is the evaluation of gameplay situations in context.

Many existing analysis tools evaluate individual values in isolation, such as speed, boost usage, positioning, or ball touches. FOFO Arena Lab should instead investigate why a player acted a certain way in a specific situation and whether that decision was useful, risky, poor, necessary, or even especially strong under the given circumstances.

An action should not be judged in isolation. It should always be evaluated in relation to the current game situation:

- What was happening with the ball?
- Where were the teammates?
- Where were the opponents?
- How much pressure existed?
- How much boost was available?
- Which options were realistically available?
- What was the scoreline?
- What consequence did the decision have?

The project starts with a focus on 2v2 replays, but it should be built in a way that allows future 3v3 analysis.

Another important part of the project is that it should not only highlight mistakes or weaknesses. FOFO Arena Lab should also detect and show positive decisions, so the analysis does not only criticize, but also explains which plays, decisions, and habits should be kept.

## Basic Workflow

```txt
.replay file
→ parse replay
→ understand available data
→ derive a stable internal data structure
→ detect gameplay situations
→ evaluate context
→ output analysis
```

The project should evolve step by step. Data structures, classes, types, and analysis modules should only be defined after real replay data has been parsed and inspected.

## Guiding Principle

```txt
Understand the data first.
Build structure second.
Develop analysis third.
Visualize and expand afterwards.
```

Long-term, FOFO Arena Lab should become a tool that extracts real gameplay insight from replay data: not only what happened, but why it mattered.

## Current Scope

This project is in an early exploration and foundation phase.

The first milestones are not about building a perfect analysis engine immediately. The first milestones are about understanding the parser output, documenting the available data, and building a clean foundation that can later support context-aware analysis, viewer integration, coaching feedback, and possibly machine-learning experiments.
