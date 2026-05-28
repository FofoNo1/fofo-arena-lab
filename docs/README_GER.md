# FOFO Arena Lab

**Replay Intelligence by Kapautz**

FOFO Arena Lab is a Rocket League replay analysis project focused on context-aware gameplay evaluation.

The goal is:

`.replay` in → context-aware analysis out.

Instead of judging isolated statistics, the project aims to understand gameplay decisions within the full match context: ball state, teammates, opponents, pressure, boost, scoreline, available options and consequences.

The project starts by parsing real replay data first. Data structures, modules and analysis layers will be derived from the actual parser output instead of being overdesigned upfront.

Initial focus: 2v2 replay analysis.  
Long-term goal: expandable context-aware analysis for 2v2 and 3v3.

FOFO Arena Lab should highlight both weaknesses and positive gameplay decisions.