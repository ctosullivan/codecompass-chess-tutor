# Project context

This file reflects the *current* state of the project — overwrite the
section below at each stopping point rather than appending to it. History
belongs in git log and `planning/retros/`, not here.

## Current state

Bootstrap (roadmap item 1) and the GPL relicensing/architecture-
simplification phase (roadmap item 1b) are both **done**. 1b's own retro
had flagged a still-pending independent review as a condition of being
done; that review has now actually happened (a fresh, no-prior-involvement
agent, checked against 9 specific criteria) and is recorded in
`planning/retros/0002-gpl-relicensing.md`'s addendum — all 8 substantive
content checks passed; the only real finding was the review-recording gap
itself, which that addendum closes. This — a "done" status change being
recorded in the same commit as the review that justifies it, rather than
trusted to happen in the right order across separate steps — is itself now
logged as a lesson in that retro's "What didn't work" section.

Roadmap item **2A (Python project and chess-state foundation)** has a
detailed plan (`planning/ROADMAP.md`'s "Phase 2A plan" section) and is
about to move into actual implementation. No source code exists in the
repository yet as of this note — this entry will be updated again once
2A's implementation, tests, CodeCompass dogfooding, and its own independent
review land.

**Net effect of the relicensing**: `python-chess` is now a normal runtime
dependency, used directly for board state, legal moves, notation, Syzygy
support, and SVG rendering. The chess-truth/pedagogy epistemic boundary
(`docs/architecture.md` "Chess truth vs. AI explanation") is unchanged —
GPL adoption simplified software boundaries, not the distinction between
mechanically-established facts and AI interpretation.

## Known gaps / rough edges

See `docs/architecture.md`'s "Known gates" section for the full, current
four-way classification (resolved-by-GPL / still relevant / requires future
evidence) — it supersedes any older gate list. Most material right now:

- Lichess's actual `Themes` tag vocabulary hasn't been verified against the
  live dataset yet (`decisions/0009`) — cheap, worth doing early, relevant
  to roadmap item 4, not 2A.
- v1's tactical puzzles still rely on Lichess's own validation pipeline for
  best-move/theme-purity correctness, not this project's own re-derivation
  (`decisions/0011`) — unaffected by Phase 2A.
- Whether/when Stockfish is worth adding remains open and deliberately
  deferred — unaffected by the license change or by Phase 2A.
