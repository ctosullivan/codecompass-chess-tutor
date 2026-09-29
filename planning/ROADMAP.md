# Roadmap

An at-a-glance view of what's done, in progress, or planned. Not a detailed
spec for each item — that belongs in the item's own plan (if it had one) or
in `decisions/` for any real tradeoff it involved.

Update this file whenever something starts, finishes, or its scope changes
materially — in the same change that does the starting/finishing/re-scoping,
not as a separate housekeeping pass later.

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap: process, evidence-gathering, initial architecture | done | Research, decisions 0001-0009, architecture/README/LICENSE, independent review, fixes, and retro all complete. See `planning/prompts/0001-project-bootstrap.md`, `docs/research/`, `decisions/`, `planning/retros/0001-project-bootstrap.md`. |
| 1b | GPL relicensing and architecture simplification | done | Decision content (`decisions/0010`, `0011`), reconciliation, and — per `CLAUDE.md` §7 — a fresh independent review are all complete and recorded; see the addendum in `planning/retros/0002-gpl-relicensing.md` for the review's outcome (all 8 substantive checks passed; the only real finding was the review-recording gap itself, closed by that addendum). See `planning/prompts/0002-gpl-relicensing-and-simplification.md`, `decisions/0010`, `0011`. |
| 2A | Python project and chess-state foundation | done | `pyproject.toml`, `src/chess_tutor/chess_state.py` (python-chess wrapped behind one module boundary), 23 passing tests, first real CodeCompass dogfooding run. Independent review re-ran the tests itself, re-verified every empirical chess-fact claim, and found no correctness bugs or scope creep — see `planning/retros/0003-phase-2a.md`. |
| 2B | Endgame concept/state model | planned | Deliberately small slice (opposition, key squares, K+P vs K) on top of 2A's `python-chess` foundation. Smallest SQLite schema justified by real queries (what concepts apply to this position? what are its prerequisites? what illustrates/counters it?) — not a general graph platform. Concept-graph shape in `decisions/0008`; curriculum bound in `decisions/0009`. Kept separate from Phase 3 (tablebase truth) per the directing prompt. |
| 3 | Tablebase-backed endgame truth | planned | Separate from 2B by design: tablebase abstraction/integration (remote lichess API per `decisions/0003`/`0010`), W/D/L lookup, successor-state verification, tests showing 2B's examples agree with tablebase truth, explicit handling of network/unavailability failure. Explanation prose never substitutes for this verification. |
| 4 | Tactical motif / daily-puzzle model | planned | See `docs/research/tactical-puzzle-datasets.md` for sourcing; `decisions/0011` for what's newly cheap (move-legality/state-transition re-derivation, via `python-chess`) versus still deferred (best-move/theme-purity verification). Verify the real Lichess `Themes` vocabulary against actual dataset data before hard-coding any mapping. |
| 5 | Learner / pedagogical model | planned | Concepts encountered, recurring errors, recognition/candidate-generation/calculation failure distinctions, prerequisites, review history, transfer evidence. Map → Explore → Commit → Practice → Feedback → Revise. No arbitrary gamification/scoring unless justified. |
| 6 | Visual pedagogy and rendering | planned | Build the `PedagogicalViewSpec` → project-owned composition → `chess.svg` primitive pipeline (`decisions/0004`, `0010`). Full board and bounded cutaways (3×3/4×4/5×5), orientation, highlights, arrows, minimal-pair/now-then comparisons. Crop size/content is teaching intent, not rendering config. No surveyed library provides this (`docs/research/board-rendering-options.md`) — original work regardless of licensing. |
| 7 | MCP interface | planned | A deliberately small surface of coarse learner-facing capabilities (inspect/explain a position, practise a concept, prepare daily puzzles, submit an answer, render a view, read/update progress, work with vault notes) — not dozens of low-level tools. Designed only once the underlying domain operations it exposes actually exist. See `docs/research/mcp-protocol-and-language-choice.md`. |
| 8 | Obsidian / vault integration | planned | Vault as ordinary files, strict path-root safety, dedicated tutor subfolder, Markdown + simple frontmatter + relative links to generated artifacts. SQLite only for regenerable system state, never the learner's only copy of anything. No hard runtime dependency on Obsidian or an Obsidian plugin. See `docs/research/obsidian-integration-and-learner-storage.md`. |
| 9 | First integrated endgame-learning + daily-tactics loop | planned | The first end-to-end MVP slice — the two loops sketched in `planning/prompts/0003-close-review-gate-and-begin-implementation.md` §5 (concept-study loop; daily-tactics loop), sharing one learner/concept/evidence architecture. Depends on 2A–8. |
| 10 | Evaluation with real learning scenarios | planned | Depends on 9 existing and being used. |

Status values: `planned` / `in progress` / `done` / `deferred` (on the list,
not scheduled — say why) / `dropped` (say why, briefly, so it isn't silently
reconsidered later without that context).

These items are roadmap themes from the bootstrap prompt, not mandated phase
boundaries — see `planning/prompts/0001-project-bootstrap.md`. They may be
combined or split as evidence supports doing so; keep early phases small.
GPL relicensing (`1b`) reduces the *infrastructure* cost of items 2A, 3, and
6 (no bespoke validator, no rendering isolation boundary to build) — it does
not remove or merge them, and it does not broaden the MVP boundary set in
`decisions/0009` (see `decisions/0010`'s own Consequences section). Item 2
from the prior version of this roadmap is split into 2A (chess-state
foundation) and 2B (concept/state model) because they are genuinely
different-sized, independently reviewable pieces of work — establishing
`python-chess` as a dependency is not the same task as designing a concept
schema on top of it, and collapsing them risked exactly the "one large
implementation phase" this project's own process rules warn against.

The MVP is explicitly bounded (see
`planning/prompts/0003-close-review-gate-and-begin-implementation.md` §7):
no opening training, general middlegame strategy, broad master-game mining,
generated synthetic puzzles, cloud services, web/mobile UI, a dedicated
graph database, a large permanent multi-agent system, broad Stockfish
integration, or general-purpose engine functionality — unless real evidence
gathered while building items 2A–10 shows one is actually required to
complete the MVP as defined. An attractive capability that shows up along
the way is recorded as a later candidate here, not built silently.

## Phase 2A plan: Python project and chess-state foundation

**Goal**: establish the first real executable project state with the
minimum infrastructure necessary for later domain work — nothing more.

**In scope**:

- Python project/package structure (`pyproject.toml`, a `src/` layout,
  minimal packaging metadata consistent with GPL-3.0-or-later).
- Pinned dependencies: `python-chess` (the chess-state primitive,
  `decisions/0010`) and the official `mcp` Python SDK (`decisions/0001`) —
  added now to establish the real manifest, **not** to build the MCP
  surface yet (that's roadmap item 7).
- A first-party source tree with a small `chess_tutor` (or equivalent)
  package, wrapping `python-chess` usage behind a thin, testable module
  boundary — kept for ordinary separation-of-concerns reasons per
  `decisions/0010`, not licensing.
- Tests proving: FEN loading; legal-move enumeration/handling; applying a
  move and observing the resulting state transition; SAN/UCI
  round-tripping where relevant.
- Minimum justified test/tooling configuration (a test runner, nothing
  speculative).
- CodeCompass dogfooding once the manifest and source tree are real: run
  the current supported discovery/sync workflow, let it populate
  `vendor.toml` if it does so, and honestly record whether it helped —
  see "CodeCompass dogfooding" below.

**Explicitly out of scope for 2A**: the concept graph (2B), tablebase
integration (3), pedagogy, the daily-puzzle workflow, visual/cutaway
rendering, the MCP tool surface itself, and Obsidian integration. None of
these are touched in this phase.

**Done when**: the package installs and imports cleanly; the test suite
above passes; `vendor.toml` reflects reality (populated or deliberately
left as-is, either way for a recorded reason); an independent review of
this phase has actually happened and passed (or its fixes have landed);
`planning/ROADMAP.md`/`CONTEXT.md` are updated to reflect it; a retro and
any knowledge/context-gap entries are recorded.

### CodeCompass dogfooding (Phase 2A)

This is this project's first genuine clean-slate test of the CodeCompass
template workflow it was bootstrapped from — `vendor.toml` has stayed
empty until now because there was nothing real to track. Once Phase 2A's
manifest and source tree exist: run CodeCompass's current discovery/sync
workflow; use it as a development aid only, never a runtime requirement
(`CLAUDE.md` §8); record honestly in `planning/knowledge/` and
`planning/context-gaps/` whether its dependency/source context was
actually useful, or actually missing/misleading — not manufactured usage
to generate a positive result either way.

## Later implementation phases (not detailed yet)

Phases 2B, 3, and beyond (roadmap items 4–10 above) get their own detailed
plan, in this same lightweight format, when each is actually started — not
speculatively drafted now. Drafting a phase's detailed plan before the
phase before it is done and reviewed risks exactly the kind of large,
unreviewed, all-at-once planning this project's process is meant to avoid.
