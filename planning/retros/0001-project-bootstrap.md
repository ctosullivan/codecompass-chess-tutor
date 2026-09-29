# Retro: project bootstrap

## Where things stood before this

Nothing existed. The repository was blank; this was the first work on the
project, directed by the prompt preserved verbatim at
`planning/prompts/0001-project-bootstrap.md`.

## Goal

Bootstrap the project's process and produce an evidence-backed initial
architecture and roadmap — without implementing the tutor itself, and
without assuming answers to licensing/architecture questions that needed
real research first.

## What happened

Delivered, in full: the codecompass-template-adapted process structure
(`CLAUDE.md`, `decisions/`, `planning/{ROADMAP,CONTEXT,retros,knowledge,
context-gaps,prompts}/`, `vendor.toml`, `.gitignore`); five research
documents (`docs/research/`) covering chess-engine/tablebase licensing, MCP
SDK/protocol and language choice, board-rendering options, Obsidian
integration and learner storage, and tactical-puzzle/dataset licensing;
nine architecture decision records (`decisions/0001`–`0009`) covering
language/SDK choice, the chess-rules validation boundary, tablebase/engine
strategy, board rendering, Obsidian integration, puzzle sourcing, the
concept-model representation, the MVP curriculum boundary, and the project
license; a synthesized `docs/architecture.md`; `README.md`; and `LICENSE`
(MIT). An independent review pass (a fresh agent with no stake in the
material) checked all of it against the bootstrap prompt's own 18-question
"definition of success" list and found six real inconsistencies, all fixed
in a follow-up commit before this retro was written.

This matches the goal as scoped: no tutor code was written, and every
non-obvious tradeoff (licensing above all) rests on cited primary-source
research rather than assumption, with genuinely unresolved items carried
forward explicitly as decision-gate notes rather than quietly resolved by
omission.

## What worked

- **Parallel research forks for independent, non-overlapping questions**
  (chess-engine/tablebase, MCP/language, board-rendering, Obsidian/storage,
  puzzle datasets) let five real research passes happen concurrently
  without polluting the orchestrator's own context with search noise, and
  each came back with a genuinely useful, appropriately-hedged evidence
  document rather than a confident-sounding but unverified one.
- **Treating "not independently verified" as a first-class, explicitly
  labeled outcome** (rather than silently dropping the hedge in the
  synthesizing docs) mostly worked — the independent review found the
  GPL-FAQ and Syzygy-license hedges were carried through consistently
  everywhere they appeared. The two places it wasn't carried through
  cleanly (Lichess theme-tag spellings, the "master-game" label) were both
  narrower, more easily-missed claims than the headline licensing ones —
  worth remembering as the specific failure mode to watch for next time
  (see `planning/knowledge/` entry).
- **An actually-independent review agent, with no stake in having written
  the material, reading everything fully rather than skimming.** It caught
  a real, load-bearing logical gap (decision 0006 claiming a validation
  capability that decisions 0002/0003 explicitly don't build yet) that
  would have been easy to miss reviewing one's own writing — the two ADRs
  were each individually well-hedged about their own scope, but the
  contradiction only became visible reading all three side by side.

## What didn't work

- A confident-sounding synthesis (`docs/architecture.md`, and the summary
  bullets in `decisions/0006`/`0009`) drifted slightly past what the
  underlying evidence actually supported in a few places, even while the
  research documents themselves stayed carefully hedged. The failure mode
  wasn't inventing evidence — it was *rounding off* an already-correct
  hedge ("the column exists and is populated" became "the taxonomy covers
  these named motifs," which reads as more specific/verified than the
  source). Worth treating "does my summary claim more precision than the
  document I'm citing actually gives?" as an explicit check when writing
  any ADR or architecture-doc paragraph that cites research, not just when
  first writing the research itself.
- One research fork (`docs/research/tactical-puzzle-datasets.md`'s author)
  attempted to spawn its own sub-forks for the other four research topics,
  which silently failed (forking isn't available from inside a fork) — no
  harm done since those four topics were already independently launched by
  the orchestrator in the same batch, but it's a coordination assumption
  (that a forked agent might try to delegate further) worth knowing about
  before relying on a fork to fan out further work itself.

## Anything worth remembering

Added to `planning/knowledge/`: the "rounding off a hedge" failure pattern
above, and the "sub-forks can't spawn from inside a fork" tooling
constraint.

## What's next

Roadmap item 2: the endgame-domain model. Concretely, per
`decisions/0008`/`0009`: design the SQLite concept-graph schema (concepts +
typed relations, shared by motifs and principles), and build out the
bounded pawn-ending curriculum (K+P vs K, opposition, key squares, pawn
races, king activity, zugzwang, passed pawns) against it — the first phase
that produces real code.
