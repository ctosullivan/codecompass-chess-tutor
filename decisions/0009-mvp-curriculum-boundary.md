# 0009. MVP endgame curriculum: bounded pawn endings; tactical motifs from Lichess's existing taxonomy

## Status

Accepted (2026-09-30).

## Context

The bootstrap prompt asks for the smallest useful initial endgame
curriculum, suggesting pawn endings (K+P vs K, opposition, key squares, pawn
races, king activity, zugzwang, basic passed-pawn concepts) as a likely but
not mandated starting slice, and for an MVP daily-tactics theme set drawn
from a list of named motifs (forks, pins, skewers, discovered attacks,
removal of defender, deflection, decoys, clearance, interference, overloaded
pieces, back-rank motifs, forcing-move recognition, loose/undefended
pieces).

`decisions/0003-tablebase-and-engine-strategy.md` establishes that Syzygy
tablebases solve positions with up to 5–6 pieces perfectly and cheaply —
which is exactly the piece-count range of K+P vs K and related basic pawn
endings. `decisions/0006-tactical-puzzle-sourcing-and-validation.md`
establishes that Lichess's puzzle export already carries a `Themes` tagging
taxonomy covering essentially all of the named motifs above.

## Decision

- **The endgame core's MVP curriculum is the bounded pawn-ending slice named
  in the bootstrap prompt**: king and pawn vs. king, opposition, key
  squares, pawn races, king activity, zugzwang, and basic passed-pawn
  concepts. This is accepted as proposed rather than revised, because the
  tablebase-scope finding in `0003` directly confirms it is exactly the
  scope where this project's chosen correctness mechanism (tablebase lookup)
  is perfect and cheap — the curriculum boundary and the mechanical-
  validation boundary line up, which is the strongest evidence available
  for "this is a well-bounded starting slice" rather than an arbitrary one.
- **The MVP's tactical-puzzle theme set is drawn directly from Lichess's
  existing puzzle `Themes` taxonomy**, restricted to the motifs named in the
  bootstrap prompt (fork, pin, skewer, discoveredAttack, removeDefender,
  deflection, decoy, clearance, interference, overloading, back-rank motifs,
  hangingPiece/loose-piece patterns, and forcing-move-recognition-style
  themes such as forced mate sequences) rather than inventing a new
  taxonomy. This keeps the tactical-puzzle model's theme vocabulary directly
  queryable against the sourced dataset (`0006`) with no translation layer
  needed at MVP.
- **Daily set size and difficulty progression are deferred to the
  learner/pedagogical-model design phase (roadmap item 5)**, not fixed here
  — the bootstrap prompt explicitly asks for an appropriate size to be
  determined rather than assumed, and doing so meaningfully requires the
  learner-model work this bootstrap does not implement.

## Alternatives considered

- **A broader initial endgame scope** (e.g. including basic rook endings or
  minor-piece endings). Rejected for MVP: broader scope means more pieces,
  which moves outside tablebases' cheapest/most-certain range and reduces
  the alignment between curriculum scope and validation-mechanism scope that
  makes the bounded slice defensible. Revisit once the bounded slice is
  actually working end-to-end (roadmap item 9).
- **A curriculum-first, dataset-second approach to tactical themes** (design
  an ideal motif taxonomy, then map it onto Lichess's tags). Rejected for
  MVP: the bootstrap prompt's own motif list already maps cleanly onto
  Lichess's existing `Themes` values, so designing a separate taxonomy first
  would be speculative work with no identified gap it closes.

## Consequences

- The endgame core's scope is now concrete enough to design a schema and
  lesson set against (roadmap item 2) — a real deliverable of this
  bootstrap, not left as an open question.
- If real learner use later shows this slice is too narrow or the wrong
  starting point, that's a roadmap re-scoping (`planning/ROADMAP.md`) and
  potentially a superseding decision record — not something this record
  tries to anticipate speculatively.
- Daily-set size/progression remains a genuinely open design question,
  carried forward to roadmap item 5, not silently defaulted to an arbitrary
  number here.
