# 0011. GPL adoption lowers the cost of move-legality re-derivation, not tactical-optimality re-derivation

## Status

Accepted (2026-09-30). Reassesses (does not supersede) `decisions/0006`'s
open gate on independent puzzle-solution re-derivation, in light of
`decisions/0010`.

## Context

`decisions/0006` narrowed an earlier overclaim: v1 does not independently
re-derive every Lichess-sourced tactical puzzle's solution; it relies on
Lichess's own generator/human-review pipeline plus honest provenance
tagging, because `0002`'s in-house validator was endgame-scoped and `0003`
deferred engine integration. `decisions/0010` has now superseded `0002`'s
runtime decision — `python-chess` is a normal runtime/development
dependency, with full move generation (not scoped to bounded endgames).
`planning/prompts/0002-gpl-relicensing-and-simplification.md` asks whether
this materially lowers the cost of independent tactical-puzzle
verification, and is explicit that it must not be read as establishing
more than it actually does: **move legality and best-move/tactical-
optimality correctness are separate questions**, and adopting a legal-move
library answers only the first.

## Decision

**GPL adoption and `python-chess`'s new runtime role materially lower the
cost of three of the four things `0006`'s deferred pipeline needed, but not
the fourth:**

- **Replaying a Lichess puzzle's stored solution line, move by move,
  through a legal-move engine to confirm every move in `Moves` is actually
  legal from the position it's played in** — now cheap and general-purpose
  (not endgame-scoped), using `python-chess` directly. This was previously
  blocked by `0002`'s validator being scoped to bounded endgame positions
  only.
- **Independently verifying move legality** at any point in a puzzle's
  line, including intermediate positions — same as above, now general
  rather than endgame-scoped.
- **Checking puzzle state transitions** (that applying `Moves` to the
  stored `FEN` produces a self-consistent sequence of positions, correct
  side-to-move alternation, etc.) — mechanical, cheap, and now
  straightforward with `python-chess`'s board/move-application API.
- **Best-move / tactical-optimality verification — NOT resolved by this
  decision.** Confirming that a puzzle's stored solution is actually the
  *best* available move (not merely *a legal* move), and confirming a
  candidate puzzle's theme isn't dominated by a stronger, unrelated tactic,
  both require engine (or, for sufficiently reduced positions, tablebase)
  *evaluation*, not just legal-move generation. `decisions/0003` (as
  narrowed by `0010`) still defers engine integration until a concrete need
  justifies it, and `python-chess` itself performs no position evaluation
  — it is a rules/notation library, not an engine. **This project does
  not claim, and must not claim, that adopting `python-chess` establishes
  tactical optimality.** If/when engine-backed best-move verification is
  built, it remains subject to `0003`'s subprocess/UCI boundary (now
  justified by process isolation, not licensing) and to the "don't add
  Stockfish speculatively" scope discipline `0003` already established.

**Practical effect on `decisions/0006`'s deferred work**: the
"legality check" and "state transition" steps of `0006`'s generation
pipeline sketch (`theme → candidate position → legality check →
engine/tablebase analysis... → mechanically re-derive/re-check the full
solution`) can now be built cheaply and early — potentially as part of the
*next* implementation phase's CodeCompass dogfooding work, rather than
waiting for the full tactical-puzzle-model phase (roadmap item 4) — since
they need nothing but `python-chess`, which the domain layer will already
depend on. The "engine/tablebase analysis of best move + best alternative"
and "reject if dominated by an unrelated stronger tactic" steps remain
exactly as open as `0006` and `0003` left them: **genuinely deferred, not
newly unblocked.**

**The following open gates from `0006`/`0009` are unaffected by this
decision and remain open**, tracked in `docs/architecture.md`'s open-gates
section:

- Lichess's actual `Themes` tag vocabulary has still not been fetched/
  verified against the live dataset (`0009`) — a data-verification task,
  unrelated to licensing or to `python-chess`'s capabilities.
- The "dominant unrelated tactic" rejection check still has no off-the-
  shelf precedent and is still original design work requiring engine
  analysis this project has not built.
- Whether/when Stockfish is worth adding is still an open, deliberately
  deferred question — `python-chess` being a normal dependency now does not
  change the cost-benefit of adding an engine, since `python-chess` doesn't
  substitute for one.

## Alternatives considered

- **Claim that `python-chess` adoption resolves `0006`'s re-derivation gate
  outright.** Rejected: this would repeat exactly the kind of overclaim
  `planning/knowledge/0001-hedge-rounding-and-fork-limits.md` already
  flagged as this project's own recurring failure mode — conflating "move
  legality is now cheap to check" with "tactical correctness is now
  established." The two are different claims with different evidence
  requirements.
- **Treat this as fully unaffected by `decisions/0010` and leave `0006`'s
  gate exactly as worded.** Rejected: `0006`'s gate was worded in terms of
  what `0002` could support ("the in-house validator is endgame-scoped"),
  and that premise has changed. Leaving the gate's wording unchanged would
  make it read as more pessimistic than the current architecture actually
  is about the legality/state-transition sub-problem, which is now solved
  by adopting a normal dependency.

## Consequences

- The tactical-puzzle-model phase (roadmap item 4) inherits a smaller
  remaining scope than the bootstrap left it: legality/state-transition
  re-derivation can plausibly move earlier (even into the next
  implementation phase, as a natural extension of adopting `python-chess`
  for the endgame core), while best-move/theme-purity verification remains
  full future scope, unchanged in difficulty.
- `docs/architecture.md`'s "Chess truth vs. AI explanation" section and
  open-gates list are updated to reflect this narrower, more precise
  picture rather than the pre-`0010` framing that treated both legality
  and optimality re-derivation as equally blocked by `0002`'s scope.
- If engine-backed best-move verification is ever built, it should get its
  own decision record when designed (per `0003`'s own instruction that
  engine integration is deferred, not designed) — this record does not
  pre-design it, only clarifies what `python-chess` alone does and doesn't
  contribute toward it.
