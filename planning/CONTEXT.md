# Project context

This file reflects the *current* state of the project — overwrite the
section below at each stopping point rather than appending to it. History
belongs in git log and `planning/retros/`, not here.

## Current state

Bootstrap phase (roadmap item 1) is **done**. Delivered and committed: the
codecompass-template-adapted process structure; five research documents
under `docs/research/` (chess engine/tablebase licensing, tactical puzzle
dataset licensing and validation, MCP SDK/protocol and language choice,
board rendering options, Obsidian integration/learner storage); nine ADRs
(`decisions/0001`–`0009`) covering language/SDK choice, the chess-rules
validation boundary, tablebase/engine strategy, board rendering, Obsidian
vault integration, tactical-puzzle sourcing/validation, the concept-model
representation, the MVP curriculum boundary, and the project license;
`docs/architecture.md` synthesizing all of it; `README.md`; `LICENSE` (MIT);
an independent review pass against the bootstrap prompt's own 18-question
"definition of success" list, which found and led to fixing six real
inconsistencies (see `planning/retros/0001-project-bootstrap.md` and the
commit that followed it); and this retro plus a
`planning/knowledge/` entry capturing the two generalizable patterns that
review surfaced.

Next: roadmap item 2, the endgame-domain model — design the SQLite
concept-graph schema (`decisions/0008`) and build the bounded pawn-ending
curriculum (`decisions/0009`) against it. This is the first phase that
produces real code.

## Known gaps / rough edges

- No code exists yet — this was intentionally a research-and-architecture-only
  bootstrap, per `planning/prompts/0001-project-bootstrap.md`.
- Several research documents and ADRs carry explicit, unresolved human
  decision gates rather than settled facts — see each document's own "Open
  uncertainty" section and `docs/architecture.md`'s "Known open gates" for
  the full list. The most material for near-term work: (a) v1's tactical
  puzzles rely on Lichess's own validation pipeline, not this project's own
  independent re-derivation, which is deferred to roadmap item 4
  (`decisions/0006`); (b) Lichess's actual `Themes` tag vocabulary hasn't
  been verified against the live dataset yet (`decisions/0009`) — a cheap
  first step of that same phase; (c) whether the bounded in-house validator
  (`decisions/0002`) is adequate once tactical-puzzle move-generation needs
  are designed is an open follow-up gate.
