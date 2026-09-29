# Roadmap

An at-a-glance view of what's done, in progress, or planned. Not a detailed
spec for each item — that belongs in the item's own plan (if it had one) or
in `decisions/` for any real tradeoff it involved.

Update this file whenever something starts, finishes, or its scope changes
materially — in the same change that does the starting/finishing/re-scoping,
not as a separate housekeeping pass later.

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | Bootstrap: process, evidence-gathering, initial architecture | in progress | This phase. See `planning/prompts/0001-project-bootstrap.md` and `docs/research/`. |
| 2 | Endgame-domain model (state, concepts, principles) | planned | Scope depends on the bounded starting curriculum chosen in `docs/architecture.md` / the relevant ADR. |
| 3 | Mechanically validated endgame core (legal-move validation, tablebase-backed correctness) | planned | See `docs/research/chess-engine-tablebase-licensing.md` for the licensing boundary this depends on. |
| 4 | Tactical motif / daily-puzzle model | planned | See `docs/research/tactical-puzzle-datasets.md` for sourcing/validation approach. |
| 5 | Learner / pedagogical model | planned | Concepts encountered, recurring errors, prerequisites, transfer evidence. |
| 6 | Visual pedagogy and rendering | planned | See `docs/research/board-rendering-options.md` for the build-vs-dependency call. |
| 7 | MCP interface | planned | See `docs/research/mcp-protocol-and-language-choice.md`. |
| 8 | Obsidian / vault integration | planned | See `docs/research/obsidian-integration-and-learner-storage.md`. |
| 9 | First integrated endgame-learning + daily-tactics loop | planned | The first end-to-end MVP slice; depends on 2–8. |
| 10 | Evaluation with real learning scenarios | planned | Depends on 9 existing and being used. |

Status values: `planned` / `in progress` / `done` / `deferred` (on the list,
not scheduled — say why) / `dropped` (say why, briefly, so it isn't silently
reconsidered later without that context).

These ten items are roadmap themes from the bootstrap prompt, not mandated
phase boundaries — see `planning/prompts/0001-project-bootstrap.md`. They may
be combined or split as evidence supports doing so; keep early phases small.
