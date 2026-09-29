# Retro: Phase 2A — Python project and chess-state foundation

## Where things stood before this

The GPL relicensing phase was done and its review gap closed
(`planning/retros/0002-gpl-relicensing.md`). No source code existed yet —
everything so far was research, decisions, and planning documents.

## Goal

Establish the first real executable project state with the minimum
infrastructure necessary for later domain work: package structure, pinned
dependencies (`python-chess`, `mcp`), `python-chess` adopted directly as
the chess-state primitive, and tests proving FEN loading, legal-move
handling, applying moves/state transitions, and SAN/UCI round-tripping —
nothing more. Also: run CodeCompass against the resulting real manifest as
this project's first genuine dogfooding exercise.

## What happened

Delivered exactly the scoped slice: `pyproject.toml`, `src/chess_tutor/`
(a two-file package — `__init__.py` and `chess_state.py`), and 23 tests in
`tests/test_chess_state.py`, all passing. `python-chess` is used directly
as a normal runtime dependency (per `decisions/0010`), wrapped behind one
small module for ordinary separation-of-concerns reasons, not licensing
isolation. CodeCompass was actually run against the real manifest — twice,
because the first attempt (using a pre-existing global binary rather than
installing into this project's own `.venv`) crashed with an opaque
`PackageNotFoundError`, which turned out to be a self-inflicted deviation
from the template's own documented workflow, not a tool defect. The second
attempt worked cleanly: auto-discovery populated `vendor.toml`, and
`sync --budget 0` generated real per-vendor digests while safely refusing
to spend anything on AI enrichment.

An independent review (fresh agent, no prior involvement) then re-ran the
test suite itself rather than trusting the commit message, independently
re-verified every "verified empirically" chess-fact claim in the tests
against python-chess directly, checked `chess_state.py` for correctness
bugs, checked for scope creep, checked the GPL license headers against the
FSF's own recommended boilerplate, and independently reproduced both
CodeCompass dogfooding findings. It found nothing to fix — the only gap
was procedural (this retro, and the `CONTEXT.md`/`ROADMAP.md` updates it
required, hadn't been written yet at the moment the review ran).

This matches the goal fully, with no scope drift in either direction (no
early expansion into concept modeling or tablebase work; nothing skipped
from the stated scope either).

## What worked

- **Verifying every chess fact empirically before writing it into a test,
  rather than trusting memory or "well-known" chess trivia.** The fool's
  mate FEN, the stalemate FEN, and the check-not-mate FEN were all run
  through python-chess directly first. The independent reviewer then
  re-ran all three itself and confirmed each — this is the same practice
  `planning/retros/0002-gpl-relicensing.md` already flagged as worth
  repeating (fetch/verify the real thing, don't trust an intermediate
  summary or memory), and it held up under a second, independent check
  this time.
- **Catching the wrong-environment CodeCompass crash and fixing it by
  reading the template's own documented workflow again**, rather than
  concluding the tool was broken. The failure mode (opaque
  `PackageNotFoundError` instead of a clear "wrong environment" message)
  is now on record in `planning/knowledge/0002` so it's recognized faster
  next time, by this project or elsewhere.
- **A real, not-manufactured CodeCompass finding** (`query symbol` missing
  method-level symbols) came out of actually needing an answer while
  writing code, not from probing the tool for a test-worthy result to
  report either way. The independent reviewer confirmed this by
  reproducing it exactly, including the specific line number.

## What didn't work

- The roadmap/context status updates for a finished phase were written
  *after* independent review pointed out they were still stale, rather
  than as part of the same batch of work that finished the phase's actual
  code. This is a close cousin of the exact lesson `planning/retros/0002`
  already recorded (a status change and the review that justifies it need
  to land together) — the review this time caught it before anything was
  falsely marked "done" on the roadmap, but the pattern of "finish the
  code, then remember the docs" is worth tightening further: update
  `CONTEXT.md`'s "next" framing to already describe the review-in-progress
  state before launching a review agent, not just before/after.

## Anything worth remembering

Already captured: `planning/knowledge/0002` (CodeCompass environment
mismatch, `--budget 0` safety, usage-detection accuracy) and
`planning/context-gaps/0001` (method-level symbol lookup gap). The
"finish docs in the same step as the code, not after review flags it"
observation above is close enough to `0002`'s existing "what didn't work"
note that it doesn't need its own new knowledge entry yet — worth watching
for a third occurrence before promoting to a `CLAUDE.md` rule.

## What's next

Roadmap item 2B: the endgame concept/state model. Per
`planning/prompts/0003-close-review-gate-and-begin-implementation.md` and
`planning/ROADMAP.md`, this gets its own detailed plan when it's actually
started (not drafted speculatively here) — a deliberately small slice
(opposition, key squares, K+P vs K) with the smallest SQLite schema
justified by real domain queries, kept separate from Phase 3's tablebase
integration. Not started by this task, by design — the directing prompt
explicitly asked for a stop-and-report before Phase 2B begins.
