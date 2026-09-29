# 0006. Source daily tactical puzzles from Lichess's CC0 exports for v1; defer generation

## Status

Accepted (2026-09-30). Not superseded. **See also `decisions/0011`**
(2026-09-30), which reassesses this record's independent-re-derivation gate
under the GPL relicensing in `decisions/0010` — `python-chess` now makes
move-legality/state-transition re-derivation cheap, but this record's
underlying conclusions (Lichess CC0 sourcing, deferred generation,
reliance on Lichess's pipeline for best-move/theme-purity correctness)
stand unchanged.

## Context

The MVP requires a daily thematic tactical-puzzle capability that must not
become a disconnected generic puzzle feed, and puzzle solutions must be
mechanically validated — the project must not trust an LLM's (or, by
extension, a bare engine claim's) assertion that a tactical solution is
correct or that its stated theme is the actual dominant tactic. See
`docs/research/tactical-puzzle-datasets.md`.

Several candidate sources and approaches were researched: Lichess's own open
exports, ChessBase's commercial database, chess.com's API/ToS, Lichess's own
(AGPL) puzzle generator as a methodology reference, and two MIT-licensed
smaller puzzle-generation tools as further methodology references.

## Decision

- **v1 sources tactical puzzles entirely from Lichess's CC0-licensed exports**
  (`lichess_db_puzzle.csv.zst` for pre-vetted puzzles with `FEN, Moves,
  Rating, Themes` already assigned; the Elite Database / standard game
  exports, also CC0, as a further source of strong-player positions if
  needed; the eval export as an optional precomputed-analysis hint). No
  attribution is legally required under CC0, but Lichess is credited in
  project documentation regardless, per this project's own evidence/
  provenance principle.
- **Do not use chess.com data or the ChessBase Mega Database** for puzzle
  sourcing. chess.com's User Agreement's commercial/redistribution
  restrictions are a poor fit for a redistributable open tool without
  explicit written permission (not sought in this bootstrap); ChessBase is a
  paid, activation-locked commercial product with no redistribution license.
- **Position/solution generation (constructing or modifying positions rather
  than selecting pre-existing ones) is explicitly deferred past v1.**
  Selecting from Lichess's already-large, pre-tagged corpus (6.1M+ puzzles)
  is sufficient to support a daily thematic set without needing generation
  on day one.
- **For v1, a sourced puzzle's solution provenance is "validated by Lichess's
  own generator/human-review pipeline," recorded as such — not
  "independently re-derived by this project."** This is a narrower claim
  than this record originally made, and the narrowing matters: `0002`'s own
  in-house legal-move validator is explicitly scoped to bounded endgame
  positions (few pieces), and `0003` defers full engine integration entirely
  for the MVP. Neither currently covers the arbitrary-middlegame legality
  and best-move confirmation that independently re-deriving a general
  tactical puzzle's solution would require. Claiming this project
  mechanically re-derives every sourced solution itself would overstate what
  `0002`/`0003` actually build for v1 — exactly the kind of unearned
  confidence `CLAUDE.md` §2 and `decisions/0007` warn against.
  **Independent mechanical re-derivation of sourced puzzles (via a dev-time
  `python-chess` + engine oracle pass over the corpus, per `0002`'s
  dev-time-only carve-out) is deferred to the tactical-puzzle-model phase
  (roadmap item 4)**, tracked as a follow-up gate, not built in this
  bootstrap. Until then, v1 relies on — and explicitly records provenance
  as — Lichess's own pipeline (engine analysis plus a human-review step,
  per `docs/research/tactical-puzzle-datasets.md` §2), which is itself a
  real, if external, mechanical-plus-human validation, not a bare unvetted
  claim. This is consistent with `ChessPuzzleForge`'s re-proving precedent
  as a *design target* for the deferred phase, not as something this
  bootstrap builds now.
- **When generation/modification of positions is eventually built** (a later
  phase, not v1), the pipeline must follow this shape, informed by the
  precedents in the research document but designed by this project (no
  off-the-shelf algorithm exists for the last two steps):
  `theme → candidate position → legality check → engine/tablebase analysis of
  best move + best alternative → reject if the score gap is below a
  strictness threshold (this project's own parameter, precedented as a
  pattern by pgn-tactics-generator's --strict flag, not copied as a value) →
  reject if the winning line is dominated by a stronger tactic unrelated to
  the intended theme (no existing precedent — original design work) →
  mechanically re-derive/re-check the full solution before it is ever
  learner-facing → tag with source + validation method for provenance.`
- **`ornicar/lichess-puzzler` (AGPL-3.0) is a methodology reference only,
  never a code dependency** — its generator→engine→human-review shape (engine
  analysis is necessary but Lichess does not skip human review even with
  engine backing) informs this project's own design; its AGPL license rules
  it out as a dependency of an MIT project.

## Alternatives considered

- **Build a generation pipeline for v1 instead of/alongside selection.**
  Rejected for v1: selection-only from a large, already-curated, freely
  licensed corpus is sufficient to prove out the daily-thematic-set feature
  and the shared conceptual/learner/evidence architecture (per the bootstrap
  prompt's own framing — testing whether tactics training can share that
  architecture with the endgame tutor doesn't require generation to work
  first). Generation adds real, currently-undesigned validation complexity
  (the "dominant unrelated tactic" check has no precedent) that would slow
  down reaching a working MVP loop for no immediate necessity.
- **Adopt `ornicar/lichess-puzzler` or another AGPL/GPL tool as a dependency.**
  Rejected: AGPL is materially incompatible with the MIT goal, especially for
  a network-reachable MCP server (AGPL's network-use trigger is stronger than
  plain GPL's).
- **Seek chess.com data via explicit permission.** Not pursued in this
  bootstrap — left as a possible future gate if Lichess's corpus proves
  insufficient for some specific need Lichess doesn't cover; not needed for
  v1.

## Consequences

- v1's puzzle corpus is bounded by whatever themes/positions Lichess's own
  tagging already covers — the bootstrap prompt's motif list (forks, pins,
  skewers, discovered attacks, etc.) is expected to map onto Lichess's
  `Themes` column, but the exact tag vocabulary was not independently
  fetched/verified against the live dataset in research (only the column's
  existence was confirmed) — **verifying the actual tag names is a concrete,
  cheap first step of roadmap item 4, not yet done.** This project inherits
  Lichess's own tagging quality/limitations rather than defining its own
  from scratch for v1.
- **v1 does not yet independently re-derive sourced puzzle solutions** — see
  the narrowed Decision above. It relies on Lichess's own pipeline
  validation plus honest provenance tagging. Building this project's own
  independent re-derivation pass is real future work (roadmap item 4), not
  something to silently treat as already covered by `0002`/`0003`.
- The harder, currently-undesigned validation problem (rejecting a
  theme-mismatched dominant tactic) is deliberately deferred, not solved —
  tracked as unfinished design work for the generation phase (roadmap item
  4), not something to quietly skip when that phase arrives.
- `docs/research/tactical-puzzle-datasets.md` flags the exact score-gap
  threshold and the dominant-tactic check as this project's own design work
  with no authoritative off-the-shelf answer — carried forward here as an
  explicit open item, not resolved by this decision.
