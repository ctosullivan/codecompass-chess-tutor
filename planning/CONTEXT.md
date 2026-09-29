# Project context

This file reflects the *current* state of the project — overwrite the
section below at each stopping point rather than appending to it. History
belongs in git log and `planning/retros/`, not here.

## Current state

Bootstrap phase (roadmap item 1) and the GPL relicensing/architecture-
simplification phase (roadmap item 1b) are both **done**.

Bootstrap delivered: the codecompass-template-adapted process structure;
five research documents under `docs/research/`; the original nine ADRs
(`decisions/0001`–`0009`); `docs/architecture.md`, `README.md`, and an
initial MIT `LICENSE`; an independent review pass that found and fixed six
inconsistencies (`planning/retros/0001-project-bootstrap.md`).

The project owner then explicitly decided the project should be
GPL-3.0-or-later instead of MIT (`planning/prompts/0002-gpl-relicensing-and-simplification.md`).
This phase delivered: `decisions/0010` (the superseding relicensing
decision, reconciling `0002`/`0003`/`0004`/`0007`) and `decisions/0011`
(reassessing tactical-puzzle validation under the simplified dependency
model); a canonical, unmodified GPL-3.0 `LICENSE`; `NOTICE-THIRD-PARTY.md`
for attribution obligations independent of this project's own license;
`docs/architecture.md` and `README.md` reconciled throughout, including a
correction to a hedge-rounding overclaim about board-rendering library
support; `planning/ROADMAP.md` re-planned to reflect reduced infrastructure
work (no bespoke legal-move validator, no rendering isolation boundary)
without broadening the MVP boundary.

**Net effect**: `python-chess` is now a normal runtime dependency, used
directly for board state, legal moves, notation, Syzygy support, and SVG
rendering. The chess-truth/pedagogy epistemic boundary (`docs/architecture.md`
"Chess truth vs. AI explanation") is unchanged — GPL adoption simplified
software boundaries, not the distinction between mechanically-established
facts and AI interpretation.

Next: the implementation phase identified in `planning/ROADMAP.md`'s "Next
implementation phase" section — establish the real Python package with
`python-chess` and the `mcp` SDK as its first dependencies, integrate
`python-chess` as the chess-state representation, build the smallest
concept/state model for the bounded pawn-ending curriculum, and run
CodeCompass against the resulting real project state as this project's
first genuine dogfooding exercise. **Not yet started** — this replanning
task explicitly stopped short of implementing it.

## Known gaps / rough edges

See `docs/architecture.md`'s "Known gates" section for the full, current
four-way classification (resolved-by-GPL / still relevant / requires future
evidence) — it supersedes any older gate list. The gates most material for
the next implementation phase:

- Lichess's actual `Themes` tag vocabulary hasn't been verified against the
  live dataset yet (`decisions/0009`) — cheap, worth doing early.
- v1's tactical puzzles still rely on Lichess's own validation pipeline for
  best-move/theme-purity correctness, not this project's own re-derivation
  — `python-chess` now makes move-legality/state-transition re-derivation
  cheap and could plausibly move into the next phase, but that's an
  opportunity, not a decision made yet (`decisions/0011`).
- Whether/when Stockfish is worth adding remains open and deliberately
  deferred — unaffected by the license change.
