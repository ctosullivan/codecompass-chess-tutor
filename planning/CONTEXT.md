# Project context

This file reflects the *current* state of the project — overwrite the
section below at each stopping point rather than appending to it. History
belongs in git log and `planning/retros/`, not here.

## Current state

Bootstrap (roadmap item 1) is **done**.

The GPL relicensing/architecture-simplification phase (roadmap item 1b) is
**in progress, not done**: its decision content is complete
(`decisions/0010`, `0011`, reconciled `docs/architecture.md`/`README.md`,
canonical `LICENSE`, `NOTICE-THIRD-PARTY.md`), but that phase's own retro
(`planning/retros/0002-gpl-relicensing.md`) explicitly flagged that an
independent review still needed to happen before the phase could be
considered done, per `CLAUDE.md` §7 — and no prior commit in this
repository ever recorded that review's outcome. A fresh independent review
is being run now, specifically against this phase, to close that gap
honestly rather than leave it as unrecorded "done." See that retro's own
addendum (once added) for the result.

In parallel, roadmap item **2A (Python project and chess-state
foundation)** is **in progress**: a detailed plan now exists in
`planning/ROADMAP.md`'s "Phase 2A plan" section. No source code exists in
the repository yet — this context entry will be updated again once 2A's
implementation, tests, CodeCompass dogfooding, and its own independent
review actually land.

**Net effect of the relicensing (pending its own review closeout)**:
`python-chess` is now a normal runtime dependency, used directly for board
state, legal moves, notation, Syzygy support, and SVG rendering. The
chess-truth/pedagogy epistemic boundary (`docs/architecture.md` "Chess
truth vs. AI explanation") is unchanged — GPL adoption simplified software
boundaries, not the distinction between mechanically-established facts and
AI interpretation.

## Known gaps / rough edges

See `docs/architecture.md`'s "Known gates" section for the full, current
four-way classification (resolved-by-GPL / still relevant / requires future
evidence) — it supersedes any older gate list. Most material right now:

- **The 1b independent-review gap itself** (above) — being closed in this
  same phase of work, not carried forward silently.
- Lichess's actual `Themes` tag vocabulary hasn't been verified against the
  live dataset yet (`decisions/0009`) — cheap, worth doing early, relevant
  to roadmap item 4, not 2A.
- v1's tactical puzzles still rely on Lichess's own validation pipeline for
  best-move/theme-purity correctness, not this project's own re-derivation
  (`decisions/0011`) — unaffected by Phase 2A.
- Whether/when Stockfish is worth adding remains open and deliberately
  deferred — unaffected by the license change or by Phase 2A.
