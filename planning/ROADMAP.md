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
| 1b | GPL relicensing and architecture simplification | done | Project owner decided GPL-3.0-or-later over MIT (`decisions/0010`); `python-chess` adopted as a normal runtime dependency, dropping the bespoke legal-move validator before it was built. See `planning/prompts/0002-gpl-relicensing-and-simplification.md`, `decisions/0010`, `0011`. |
| 2 | Endgame-domain model (state, concepts, principles) | planned | Scope is the bounded pawn-ending curriculum in `decisions/0009`; concept-graph shape in `decisions/0008`. `python-chess` (`decisions/0010`) now supplies the chess-state primitive directly — this phase is about the concept/curriculum layer built on top of it, not about chess-state representation itself, which is no longer this project's own code to write. |
| 3 | Tablebase-backed correctness: integration and verification | planned | Reduced in scope from the bootstrap's original framing: with `python-chess` adopted directly (`decisions/0010`), this phase is integration and testing — does the curriculum's use of `python-chess` + tablebase lookup actually produce correct, mechanically-provable lesson content — not implementation of generic chess rules, which this project no longer builds. |
| 4 | Tactical motif / daily-puzzle model | planned | See `docs/research/tactical-puzzle-datasets.md` for sourcing; `decisions/0011` for what's newly cheap (move-legality/state-transition re-derivation, now plausible early via `python-chess`) versus still deferred (best-move/theme-purity verification, needs engine/tablebase analysis not yet built). |
| 5 | Learner / pedagogical model | planned | Concepts encountered, recurring errors, prerequisites, transfer evidence. |
| 6 | Visual pedagogy and rendering | planned | Build the `PedagogicalViewSpec` → project-owned composition → `chess.svg` primitive pipeline (`decisions/0004`, `0010`); no licensing-motivated isolation boundary needed, but the pedagogical composition layer (cropping, arrows, comparisons) is still original work — no surveyed library provides it (`docs/research/board-rendering-options.md`). |
| 7 | MCP interface | planned | See `docs/research/mcp-protocol-and-language-choice.md`. |
| 8 | Obsidian / vault integration | planned | See `docs/research/obsidian-integration-and-learner-storage.md`. |
| 9 | First integrated endgame-learning + daily-tactics loop | planned | The first end-to-end MVP slice; depends on 2–8. |
| 10 | Evaluation with real learning scenarios | planned | Depends on 9 existing and being used. |

Status values: `planned` / `in progress` / `done` / `deferred` (on the list,
not scheduled — say why) / `dropped` (say why, briefly, so it isn't silently
reconsidered later without that context).

These items are roadmap themes from the bootstrap prompt, not mandated phase
boundaries — see `planning/prompts/0001-project-bootstrap.md`. They may be
combined or split as evidence supports doing so; keep early phases small.
GPL relicensing (`1b`) reduces the *infrastructure* cost of items 2, 3, and
6 (no bespoke validator, no rendering isolation boundary to build) — it does
not remove or merge them, and it does not broaden the MVP boundary set in
`decisions/0009` (see `decisions/0010`'s own Consequences section).

## Next implementation phase (identified, not started)

The smallest sensible next phase, reassessed against the simplified
architecture in `decisions/0010` rather than assumed unchanged from the
bootstrap's original item-2-first framing:

1. Establish the Python project/package and pinned dependencies
   (`pyproject.toml` or equivalent), including `python-chess` and the `mcp`
   SDK as the first two real entries.
2. Integrate `python-chess` as the chess-state representation (board, legal
   moves, FEN/SAN) — this is now adopting a dependency, not implementing
   rules.
3. Define the smallest concept/state model needed for the bounded
   pawn-ending curriculum (`decisions/0008`, `0009`) — the first few
   concepts (opposition, key squares) and their relationships.
4. Introduce the initial SQLite schema only to the extent required by real
   domain queries arising from step 3 — not speculatively.
5. Establish the first few mechanically grounded endgame concepts/examples,
   verified against tablebase lookup (`decisions/0003`).
6. **Run CodeCompass against the resulting real project state** once a real
   dependency manifest and first-party source exist — this project's first
   genuine dogfooding of the template/CodeCompass workflow it was
   bootstrapped from (`vendor.toml` has stayed empty until now because
   there was nothing real to track). Use it as a development aid only,
   never a runtime requirement (`CLAUDE.md` §8); record in
   `planning/knowledge/` and `planning/context-gaps/` whether its
   source/dependency context was actually useful, and file any real
   missing/misleading context found — not manufactured usage to generate
   positive evidence.

This phase is **identified here, not implemented** — see
`planning/CONTEXT.md` for current status.
