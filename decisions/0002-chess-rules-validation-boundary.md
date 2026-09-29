# 0002. Bounded in-house legal-move validator at runtime; python-chess as a dev-time oracle only

## Status

Accepted (2026-09-30). **Superseded by `decisions/0010` (2026-09-30)**: the
runtime decision below (build a bespoke in-house legal-move validator to
avoid importing GPL-licensed `python-chess`) no longer applies now that the
project is GPL-3.0-or-later licensed. `python-chess` is adopted directly as
a normal runtime dependency instead. This note is added per this file's own
append-only rule; the rest of this record is left exactly as originally
written, as history.

## Context

The project needs mechanically validated chess state and legal-move handling
for the endgame core, and wants to remain MIT-licensed. `python-chess`, the
de facto standard Python chess library (board representation, legality,
PGN/FEN, SAN, Syzygy probing), is **GPL-3.0-or-later** — confirmed directly
against its `LICENSE.txt` (see
`docs/research/chess-engine-tablebase-licensing.md`). No adequately mature,
permissively-licensed pure-Python alternative for full move generation was
found in that research pass (a negative result from one focused search, not
proof of absence).

Importing a GPL library in-process and shipping the combination is the case
where GPL copyleft is most likely to apply — materially different, and
weaker ground for staying non-GPL, than invoking a separate GPL process
arm's-length (the pattern already accepted for Stockfish, see `0003`). This
is legal interpretation, not settled law; treated here as a real risk to
design around, not a technicality.

The MVP's actual rules-handling scope is narrow: bounded pawn-ending
positions (few pieces) for the endgame core, and fixed-FEN tactical puzzles
with a short expected line. Full game-tree features (threefold repetition,
50-move rule, full castling/en-passant edge cases across an open-ended
middlegame) are not required for that bounded scope.

## Decision

- **Runtime**: this project writes its own small, in-house legal-move
  validator scoped to the bounded MVP domain (limited piece count endgame
  positions; puzzle positions with a fixed FEN and short expected line),
  rather than importing python-chess into the shipped, running tutor.
- **Development-time**: python-chess (and its GPL license) may be used as a
  dev-time-only tool — e.g. an oracle to test the in-house validator against,
  or to pre-validate a generated puzzle/lesson corpus offline before it's
  baked into a data file the runtime reads. This never ships as part of the
  distributed/running product, so it is not a distribution question at all.
- The in-house validator must itself be tested against python-chess and/or
  tablebase output as a dev-time correctness oracle before being trusted —
  writing a narrower validator does not exempt it from correctness
  verification, it only shrinks the amount of logic that needs verifying.

## Alternatives considered

- **Import python-chess into the runtime, isolated behind an in-process
  adapter module only.** Rejected as the default: an in-process import is
  exactly the linking pattern most likely to make the combined work GPL;
  an internal module boundary doesn't change that, only a process boundary
  would (see `0003`'s subprocess pattern). Left open as a fallback if the
  in-house validator later proves inadequate for real puzzle-generation
  needs (see Consequences).
- **Import python-chess into the runtime, isolated behind a separate OS
  process (its own small GPL-licensed service/CLI, optional install, IPC
  boundary).** Not rejected outright — this is the credible fallback if
  scope grows — but not chosen as the default because it adds real
  architectural cost (a second process, an IPC contract) that the currently
  bounded MVP scope doesn't yet justify.
- **Do nothing special; accept python-chess as a normal dependency and
  reconsider the MIT goal.** Rejected — the bootstrap prompt's licensing
  goal is explicit, and the isolation options above make it achievable
  without abandoning MIT.

## Consequences

- The project now owns a real, non-trivial piece of domain logic (legal-move
  validation) rather than getting it for free, and must maintain and test it
  itself. This is accepted as a deliberate, bounded scope tradeoff, not an
  oversight.
- **This decision is explicitly scoped to the endgame core.** The
  tactical-puzzle/daily-motif work (roadmap item 4) likely needs broader move
  generation than pure pawn endings (arbitrary middlegame positions sourced
  from datasets or master games). Whether the same in-house validator can
  cover that scope, or whether tactical-puzzle *sourcing/validation* should
  instead lean on a dev-time-only python-chess pass over externally-sourced
  positions (never touching the shipped runtime, per the dev-time carve-out
  above) is an **open follow-up gate**, to be resolved when tactical-puzzle
  architecture is designed (see `docs/research/chess-engine-tablebase-licensing.md`,
  §"Open uncertainty," and the pending `decisions/0006-tactical-puzzle-sourcing.md`).
- If the in-house validator ever proves inadequate at runtime, the fallback
  is the process-isolated python-chess option above — not a silent in-process
  import — and that reversal should get its own superseding decision record.
- The FSF's own position on GPL-library-linking was not re-verified verbatim
  against the live GPL FAQ page in the underlying research (rate-limited at
  research time). This decision's risk framing should be revisited if that
  verification, once done, changes the picture materially.
