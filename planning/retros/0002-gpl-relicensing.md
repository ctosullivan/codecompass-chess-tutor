# Retro: GPL relicensing and architecture simplification

## Where things stood before this

The bootstrap (`planning/retros/0001-project-bootstrap.md`) had concluded
MIT, on the strength of isolating every GPL dependency the project touched
behind adapter or process boundaries. No code existed yet.

## Goal

Record the project owner's explicit decision to relicense
GPL-3.0-or-later instead, treat it as a real architecture simplification
rather than a license-file swap, and reconcile every piece of prior
documentation/decisions that depended on the old MIT goal — without
broadening the MVP or silently rewriting history.

## What happened

Delivered, in full: `planning/prompts/0002` (verbatim); `decisions/0010`
(the superseding relicensing decision, with an explicit reconciliation
table against `0001`–`0009`) and `decisions/0011` (reassessing
tactical-puzzle validation under the new dependency model); status notes
appended to `0002`, `0003`, `0004`, `0007` (superseded/narrowed, bodies
left untouched) and a non-superseding cross-reference note on `0006`; a
canonical, unmodified GPL-3.0 `LICENSE` fetched directly from
`gnu.org/licenses/gpl-3.0.txt` (not reproduced from memory, to guarantee
verbatim accuracy); `NOTICE-THIRD-PARTY.md` for attribution obligations
independent of the project's own license; `docs/architecture.md` and
`README.md` reconciled throughout, including correcting a further instance
of the "hedge-rounding" pattern already logged in
`planning/knowledge/0001` (the "no library anywhere" overclaim about
board-rendering cropping support, corrected to "none of the surveyed
candidates"); `planning/ROADMAP.md` re-planned with reduced infrastructure
scope in items 2/3/6 and an explicit "next implementation phase" section
identified but not started.

This matches the goal as scoped. The MVP boundary from `decisions/0009` was
deliberately left untouched — GPL made some infrastructure easier, and the
temptation to use that slack to expand scope was explicitly named and
avoided, per the directing prompt's own instruction.

## What worked

- **Fetching the actual GPL-3.0 text via `curl` from gnu.org rather than
  reproducing it from memory.** A license file is exactly the kind of
  document where "close enough" isn't good enough — verifying byte-for-byte
  fidelity against the authoritative source cost almost nothing and removed
  a real risk.
- **Treating "superseded" and "narrowed" as genuinely different outcomes**
  rather than defaulting every affected ADR to "superseded." `0003`'s core
  strategy (tablebase-preferred, engine-deferred) survived essentially
  intact because its reasoning was operational, not licensing-driven —
  collapsing it into "superseded by 0010" would have overstated how much
  actually changed.
- **The append-only convention held up well under real pressure to
  "clean up" old decisions.** Every correction to `0002`/`0003`/`0004`/`0007`
  landed as an added `Status:` note, never a body edit — the historical
  record stays legible as "what was believed true at the time," exactly as
  `decisions/README.md` intends.

## What didn't work

- Nothing significant surfaced during this phase itself; the independent
  review that follows this retro is the actual test of whether the
  reconciliation held together across all the touched documents
  simultaneously (a single self-review, however careful, is a weaker check
  than a fresh reader with no stake in the material — see the bootstrap's
  own retro for why).

## Anything worth remembering

The GPL-text-fetched-verbatim practice (fetch canonical legal/reference
text directly rather than reproduce from memory, even when confident) is
general enough to be worth a `planning/knowledge/` entry if it recurs on a
future document with similar stakes — not promoted yet, one instance.

## What's next

The implementation phase identified in `planning/ROADMAP.md`'s "Next
implementation phase" section: establish the real Python package with
`python-chess` and the `mcp` SDK, integrate `python-chess` as the
chess-state representation, build the smallest concept/state model for the
bounded pawn-ending curriculum, and run CodeCompass against the resulting
real project state as this project's first genuine dogfooding exercise.
Not started by this task, by design.
