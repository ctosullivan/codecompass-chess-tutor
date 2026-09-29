# Architecture

This file describes the project's *current* architecture as of the bootstrap
phase — a research-and-decisions foundation, not yet any running code. See
`planning/ROADMAP.md` for what comes next and `decisions/` for the reasoning
behind each choice summarized here.

## What this project is

CodeCompass Chess Tutor is an experimental AI-assisted chess-learning
system. Its first milestone is deliberately narrow: an **endgame tutor**
covering a bounded pawn-endings curriculum, plus a **daily thematic tactical
puzzle** capability, exposed as an MCP tool/server so a learner's AI
assistant can use it directly, and designed to work alongside — never
lock into — a learner's Obsidian vault. It treats chess learning as
several interacting concerns (board state, chess concepts, a learner model,
a pedagogical model, evidence/provenance) rather than as a single
engine-evaluation problem, but starts with the smallest representation of
those concerns that can actually hold together — see `decisions/0008`.

It is explicitly *not*, at this stage, a general chess coach, a full
opening/middlegame trainer, or a broad concept-graph platform. See
`planning/ROADMAP.md` for the themes deferred past this MVP.

## Why an endgame tutor, and why daily tactics too

Bounded pawn endings (K+P vs K, opposition, key squares, pawn races, king
activity, zugzwang, basic passed-pawn concepts — `decisions/0009`) are the
one area where this project's chosen correctness mechanism — tablebase
lookup — is both perfect and cheap (`decisions/0003`): Syzygy tablebases
solve positions up to 5–6 pieces exactly. Starting here means the tutor can
make an unusually strong claim for an AI-assisted learning tool: every
"this move is correct" statement in the endgame core is mechanically
provable, not merely engine-plausible.

Daily thematic tactical puzzles are a required MVP capability, not a
bolt-on, because they exist specifically to test whether tactical training
can reuse the *same* conceptual/learner/evidence architecture as the
endgame core (`decisions/0006`, `decisions/0008`) rather than becoming a
disconnected generic puzzle feed. If a fork puzzle and a king-and-pawn
lesson can share one concept model, one learner-evidence store, and one
provenance mechanism, that's real evidence the architecture is doing its
job; if they can't, that's worth learning now, at bootstrap scale, rather
than after both are built out separately.

## Chess truth vs. AI explanation

A hard line runs through this project, referenced throughout `decisions/`:

- **Mechanically established facts** — is a move legal, is a position won/
  drawn/lost per tablebase, does a claimed tactical solution actually hold —
  come only from the chess-validation layer (a bounded in-house legal-move
  validator, tablebase lookup, and, later, an isolated optional engine —
  `decisions/0002`, `0003`). This layer never trusts an LLM's or a dataset's
  claim without mechanical re-derivation (`decisions/0006`).
- **Explanation, teaching, and interaction** are the AI assistant's job,
  operating through MCP on top of facts the validation layer has already
  established. An LLM-generated explanation of *why* a position is winning
  is pedagogically valuable but is never allowed to silently become the
  *source* of whether it's actually winning.
- **Provenance is tracked, not assumed**: a concept claim, worked example, or
  puzzle carries a record of where it came from (a book, a tablebase, an
  engine, a master game, a generated example, or an LLM's own interpretation
  — `decisions/0008`), so a reader can always tell objective chess truth
  apart from source claims, tutor interpretation, and learner understanding.

```
LLM / AI assistant
        │
        │ MCP  (decisions/0001)
        ▼
Chess Tutor
        │
        ├── learner/pedagogical model      ─┐
        ├── concepts/evidence               │  one lightweight concept
        ├── endgame lesson/exercise         │  graph + evidence store,
        │   selection                       │  SQLite (decisions/0005, 0008)
        ├── daily thematic tactical puzzles ─┘
        ├── visualisation / board rendering   (decisions/0004)
        │
        └── chess validation layer
                 ├── legal chess state        (decisions/0002)
                 ├── tablebase                (decisions/0003)
                 └── engine, deferred/optional (decisions/0003)
```

## Layered boundaries

Two separate layering diagrams from the bootstrap prompt hold in this
architecture, kept deliberately distinct so interfaces and renderers can be
swapped later without touching the domain core:

```
core chess-learning domain
        ↑
application/service layer
        ↑
MCP adapter                    (decisions/0001)
        ↑
learner's AI + Obsidian environment

visual teaching specification
        ↓
renderer adapter                (decisions/0004)
        ↓
SVG / image artifact
```

The chess-validation layer (`decisions/0002`, `0003`) and the rendering
layer (`decisions/0004`) are each isolated behind their own adapter boundary
for the same underlying reason: both are the places a GPL-licensed
dependency (python-chess, Stockfish, `chess.svg`) may sit, and isolating
them keeps that boundary legible and keeps this project's own MIT-licensed
core free of GPL types leaking into its public domain model or MCP surface
(`decisions/0007`).

## Visual pedagogy: view specification vs. rendering

Board rendering is treated as part of the pedagogy, not presentation detail.
Research found no board-rendering library, in any license, that supports
rendering a bounded sub-region of the board (a 3×3/4×4 cutaway, a pawn-race
lane, a promotion zone) — that capability doesn't exist off the shelf
anywhere (`docs/research/board-rendering-options.md`). This project
therefore separates *what to show* from *how to draw it*:

```
Position
    ↓
Pedagogical View Specification
    ├── full board / cutaway bounds
    ├── orientation
    ├── highlighted squares
    ├── arrows / trajectories
    ├── annotations
    └── comparison state
    ↓
Renderer                          (decisions/0004)
    ↓
SVG / image / notebook artifact
```

A view specification is plain data (which squares are in view, what's
highlighted, what arrows exist, whether this is a before/after pair) — never
logic embedded inside rendering code. The choice of crop is itself a
pedagogical decision: a full board matters when broader positional context
is the point (e.g. king activity across the whole board); a narrow cutaway
matters when the learner needs to perceive one specific relationship (e.g.
opposition on a 3×3 patch, a pawn-race lane's key squares) without visual
noise from irrelevant material elsewhere on the board. Whether cropping
should be automatic (inferred from the concept being taught) or explicit in
lesson metadata, or both, is not resolved by this bootstrap — it's a design
question for roadmap item 6, informed by this separation but not answered by
it.

## Obsidian and MCP: how the learner participates

The tutor is not an Obsidian plugin. It reads and writes a learner's vault
directly as a folder on disk, via a single configured vault-root path and a
path-resolution boundary that refuses to leave that root
(`decisions/0001`), writing its own generated artifacts only to a dedicated
subfolder and never touching `.obsidian/` or rewriting the learner's own
notes wholesale (`decisions/0005`). The learner's qualitative notes stay
ordinary portable Markdown — the tutor's own structured evidence/learner-
model state lives in a small, regenerable, project-owned SQLite file, never
the learner's only copy of anything meaningful (`decisions/0005`, `0008`).

The MCP surface (`decisions/0001`) is the only way an AI assistant reaches
any of this — the core chess-learning domain has no direct dependency on
MCP, Obsidian, or any specific renderer (see the layering diagram above),
so another interface could be added later without a domain rewrite. The
bootstrap prompt's candidate MCP capabilities (analyse/register a position,
explain a concept, prepare a daily puzzle set, validate an answer, render a
view, compare positions, read/update learner progress, work with vault
notes) are candidates for the MCP interface design phase (roadmap item 7),
not a fixed API decided here.

## Key dependencies

Once real dependencies exist, `codecompass query vendors` (via `vendor.toml`)
gives a mechanical listing; this section is for the *reasoning* that gives,
summarized from `decisions/`:

| Dependency | Role | License | Isolation | Decision |
|---|---|---|---|---|
| Python | Implementation language | PSF | — | `0001` |
| `mcp` (official Python MCP SDK) | MCP server binding | MIT (medium-high confidence) | Direct runtime dependency, no isolation needed | `0001` |
| In-house legal-move validator | Runtime chess-rules boundary for the bounded MVP domain | This project's own (MIT) | N/A — it's the isolation | `0002` |
| `python-chess` | Dev-time oracle/validation tool; possible future process-isolated runtime component | GPL-3.0-or-later | Dev-time only by default; process boundary if ever runtime | `0002` |
| lichess tablebase API (`tablebase.lichess.ovh`) | Endgame correctness lookup | Hosted service, not a licensed dependency | Network call, no local licensing exposure | `0003` |
| Stockfish | Deferred, optional future engine use | GPL-3.0-or-later | Subprocess/UCI only, never vendored | `0003` |
| `chess.svg` (part of `python-chess`) | Full-board SVG rendering primitive | GPL-3.0-or-later | Isolated behind a rendering-adapter module | `0004` |
| cburnett piece artwork | Piece glyphs | BSD-3-clause (option exercised from a multi-license offer) | Attribution notice required, no share-alike | `0004` |
| SQLite | Concept graph + learner-evidence store | Public domain | Direct runtime dependency, no isolation needed | `0005`, `0008` |
| Lichess CC0 puzzle/game/eval exports | Tactical puzzle and master-game sourcing | CC0 1.0 | Data, not code; no isolation needed | `0006` |
| CodeCompass (`codecompass-context`) | Development-time context tool only | GPL-3.0-or-later | Never imported by runtime code — see below | `CLAUDE.md` §8 |

## On this project's relationship to CodeCompass

CodeCompass is a **development tool**, not part of this project's product
architecture. Developers may install and run `codecompass-context` and use
`vendor.toml` to track dependency/first-party-source context during
development; CodeCompass-generated artifacts (`context-graph.db`,
`vendor/<name>/` digests, generated skills) are reproducible outputs, never
committed (see `.gitignore`). **Production/runtime code must never import or
depend on CodeCompass**, and anyone must be able to clone, install, test,
and run this project's own tutor without CodeCompass installed at all. This
boundary is the same shape as the GPL-isolation boundaries in `decisions/`
0002–0004 — a useful GPL-licensed tool, kept out of the distributed
product — and CodeCompass's own GPL-3.0-or-later license has no bearing on
this project's MIT license as a result (`decisions/0007`).

This project is bootstrapped from
[`codecompass-template`](https://github.com/ctosullivan/codecompass-template)
(itself MIT-licensed, independently authored, and not a redistribution of
CodeCompass's own GPL-licensed source or documentation), adapted rather than
adopting CodeCompass's own much larger accumulated governance and
specialist-agent roster — see `CLAUDE.md` §9 and
`planning/prompts/0001-project-bootstrap.md`.

## Concept model and process

- **One lightweight concept graph, in SQLite**, not five separate models or
  a dedicated graph database — see `decisions/0008` for why tactical motifs
  and endgame principles share one model, and why plain relational tables
  with typed edges are believed adequate at this project's scale.
- **Process**: understand → research/evidence → plan → design → implement →
  verify → retro → update knowledge (from `codecompass-template`, adapted in
  `CLAUDE.md`). Substantial prompts that direct or redirect a phase of work
  are preserved verbatim in `planning/prompts/`. Consequential architecture
  decisions get an independent review pass (`CLAUDE.md` §7) rather than
  being accepted on the original author's say-so alone.

## Decisions

See `decisions/` for the full, append-only record. As of this bootstrap:
`0001` (language/MCP SDK), `0002` (chess-rules validation boundary), `0003`
(tablebase/engine strategy), `0004` (board rendering), `0005` (Obsidian
integration), `0006` (tactical puzzle sourcing/validation), `0007` (project
license), `0008` (concept model representation), `0009` (MVP curriculum
boundary).

## Known open gates

Carried forward explicitly from `decisions/` rather than treated as settled
— see each decision's own "Consequences"/gate section for full detail:

- The FSF GPL FAQ's exact current wording (library-linking and
  program-output licensing) was not re-fetched verbatim during research
  (rate-limited both times) — re-verify before relying on this project's
  GPL-isolation reasoning in anything more formal than internal docs.
- Syzygy tablebase data/probing-code licenses were not independently
  confirmed against a signed license file — relevant only if/when local
  tablebases are added.
- Whether an adapter-module boundary (rendering) is sufficient isolation
  versus a stronger subprocess boundary is a risk-tolerance call, not fully
  closed by research alone.
- The exact tactical-puzzle "dominant unrelated tactic" rejection check has
  no off-the-shelf precedent and is original design work for a later phase.
- True concurrent-write safety between this project's vault writes and a
  live Obsidian instance has not been empirically validated.
- Whether the bounded in-house validator's scope is adequate once
  tactical-puzzle move-generation needs are designed (likely broader than
  pure pawn endings) is an explicit follow-up gate, not resolved here.
