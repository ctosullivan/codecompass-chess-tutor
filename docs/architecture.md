# Architecture

This file describes the project's *current* architecture — a
research-and-decisions foundation, not yet any running code. See
`planning/ROADMAP.md` for what comes next and `decisions/` for the reasoning
behind each choice summarized here.

**Licensing note**: this project is licensed GPL-3.0-or-later
(`decisions/0010`, superseding the bootstrap's original MIT position in
`decisions/0007`). This was a deliberate architectural simplification, not
just a license-file change — `python-chess` is now a normal runtime
dependency rather than something isolated behind adapter/process
boundaries. See "Key dependencies" and "Known gates" below for what changed
and what didn't.

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
solve positions up to 7 pieces exactly — far more than the 3-4 pieces the
bounded pawn-ending curriculum actually needs. Starting here means the tutor can
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
  come only from the chess-validation layer: `python-chess` for board
  state, legal-move generation, and game-state checks; tablebase lookup for
  exact endgame truth; and, later, an optional engine for positions neither
  of those cover (`decisions/0003`, `0010`). This layer never treats an
  LLM's own assertion as ground truth. For the endgame core, facts are
  independently re-derived and tablebase-provable.
  **Move legality and tactical optimality are separate questions, and this
  project is careful not to conflate them** (`decisions/0011`): `python-chess`
  makes independent *move-legality* and *state-transition* re-derivation
  for sourced tactical puzzles cheap and general-purpose (no longer scoped
  to bounded endgames, now that `decisions/0002`'s runtime decision is
  superseded). It does **not** establish that a puzzle's stored solution is
  the *best* available move, or that its apparent theme isn't dominated by
  an unrelated, stronger tactic — that needs engine or tablebase
  *evaluation*, which remains deferred (`decisions/0003`). **For v1's
  sourced tactical puzzles, this project's own independent best-move/
  theme-purity re-derivation does not yet exist**; v1 relies on, and
  honestly records provenance as, Lichess's own external generator/
  human-review pipeline for that part. Building this project's own
  engine-backed re-derivation pass is explicit follow-up work, not yet done
  (`decisions/0006`, `0011`).
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
        ├── visualisation / board rendering   (decisions/0004, 0010)
        │
        └── chess validation layer
                 ├── python-chess: board state,
                 │   legal moves, notation      (decisions/0010)
                 ├── tablebase                   (decisions/0003)
                 └── engine, deferred/optional   (decisions/0003)
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

The chess-validation layer (`python-chess`, tablebase lookup, deferred
engine — `decisions/0003`, `0010`) and the rendering layer (`decisions/0004`,
`0010`) each still sit behind their own module boundary — but, since
`decisions/0010` relicensed this project GPL-3.0-or-later, that boundary is
no longer a *licensing* isolation requirement. It's kept because it's good
architecture on its own merits: the domain/rendering layers depend on a
specific chess library and a specific rendering primitive, and keeping that
dependency behind a defined interface (rather than scattering direct
`python-chess` imports through the whole codebase) keeps those choices
swappable and the codebase legible, the same reason any well-factored
project isolates a specific third-party library behind an interface. No
GPL-type-leakage concern drives this anymore — `python-chess` types may
appear directly wherever the domain/rendering code actually needs them.

## Visual pedagogy: view specification vs. rendering

Board rendering is treated as part of the pedagogy, not presentation detail.
Research surveyed a range of board-rendering libraries and artwork sources
and found that **none of the surveyed candidates** support rendering a
bounded sub-region of the board (a 3×3/4×4 cutaway, a pawn-race lane, a
promotion zone) — see `docs/research/board-rendering-options.md` for the
full list. This is a bounded search result, not proof that no such tool
exists anywhere; it is, however, sufficient evidence that this project
should plan to build that layer itself rather than expect to find it
off-the-shelf. This project therefore separates *what to show* from *how to
draw it*:

```
position / board state
        ↓
Pedagogical View Specification
    ├── full board / cutaway bounds
    ├── orientation
    ├── highlighted squares
    ├── arrows / trajectories
    ├── annotations
    └── comparison state
        ↓
project-owned pedagogical composition   (crop, highlight, arrows, comparisons)
        ↓
python-chess / chess.svg primitive       (decisions/0004, 0010 — ordinary
        ↓                                 dependency, no isolation needed)
SVG artifact
        ↓
Obsidian / MCP consumer
```

The project-owned composition layer answers *what should the learner see?*;
`chess.svg` (now a normal base primitive, not something requiring an
isolation boundary — `decisions/0010`) answers only *how are squares and
pieces drawn?*. A view specification is plain data (which squares are in
view, what's highlighted, what arrows exist, whether this is a before/after
pair) — never logic embedded inside rendering code. The choice of crop is itself a
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
| `python-chess` | Board state, legal move generation, game-state checks, SAN/UCI notation, Syzygy support, `chess.svg` rendering — **normal runtime dependency** | GPL-3.0-or-later (same as this project) | Direct dependency, no isolation needed; kept behind a module boundary for ordinary separation-of-concerns reasons, not licensing | `0010` |
| lichess tablebase API (`tablebase.lichess.ovh`) | Endgame correctness lookup | Hosted service, not a licensed dependency | Network call; MVP default for operational-simplicity reasons | `0003`, `0010` |
| Stockfish | Deferred, optional future engine use | GPL-3.0-or-later | Subprocess/UCI only, if ever added — now for process-isolation reasons, not licensing | `0003`, `0010` |
| `chess.svg` (part of `python-chess`) | Full-board SVG rendering primitive | GPL-3.0-or-later | Normal dependency, used directly by the project-owned composition layer | `0004`, `0010` |
| cburnett piece artwork | Piece glyphs | BSD-3-clause (option exercised from a multi-license offer) | Attribution notice required (`NOTICE-THIRD-PARTY.md`), independent of this project's own license | `0004`, `0010` |
| SQLite | Concept graph + learner-evidence store | Public domain | Direct runtime dependency, no isolation needed | `0005`, `0008` |
| Lichess CC0 puzzle/game/eval exports | Tactical puzzle sourcing, plus strong-player game positions (Elite Database, 2300+ rated — not classical "master game" corpora) | CC0 1.0 | Data, not code; no isolation needed | `0006` |
| CodeCompass (`codecompass-context`) | Development-time context tool only | GPL-3.0-or-later (same as this project) | Never imported by runtime code — see below | `CLAUDE.md` §8 |

## On this project's relationship to CodeCompass

CodeCompass is a **development tool**, not part of this project's product
architecture. Developers may install and run `codecompass-context` and use
`vendor.toml` to track dependency/first-party-source context during
development; CodeCompass-generated artifacts (`context-graph.db`,
`vendor/<name>/` digests, generated skills) are reproducible outputs, never
committed (see `.gitignore`). **Production/runtime code must never import or
depend on CodeCompass**, and anyone must be able to clone, install, test,
and run this project's own tutor without CodeCompass installed at all. This
boundary was never a licensing question, even during the project's earlier
MIT phase — CodeCompass and this project now happen to share the same
license (both GPL-3.0-or-later, `decisions/0010`) — it is a *deployability*
boundary: no one should need to install a development-context tool to run
the finished tutor, regardless of what license either carries.

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

See `decisions/` for the full, append-only record. `0001` (language/MCP
SDK), `0002` (chess-rules validation boundary — **superseded by `0010`**),
`0003` (tablebase/engine strategy — **narrowed by `0010`**), `0004` (board
rendering — **narrowed by `0010`**), `0005` (Obsidian integration), `0006`
(tactical puzzle sourcing/validation), `0007` (project license —
**superseded by `0010`**), `0008` (concept model representation), `0009`
(MVP curriculum boundary), `0010` (GPL relicensing and dependency
simplification), `0011` (tactical-puzzle validation reassessed under GPL).
A decision marked superseded/narrowed keeps its original body unedited, as
history — the superseding decision's own reasoning is what's currently in
effect; see `decisions/0010`'s reconciliation table for exactly what
changed in each case.

## Known gates

The bootstrap phase produced a number of open gates, several of which
existed only because of the original MIT licensing goal. Following
`decisions/0010`'s relicensing, each is reclassified below rather than
carried forward unexamined — obsolete gates are retired here (their history
stays visible in git and in the superseded ADRs), not kept indefinitely as
clutter.

**Resolved/superseded by the GPL relicensing (`decisions/0010`)** — no
longer open questions:

- Whether in-process `python-chess` import threatens the project's
  preferred license — moot; the project's own license is now GPL.
- Whether `chess.svg` needs a licensing-motivated isolation boundary — no;
  see "Layered boundaries" above.
- Whether a custom legal-move validator is necessary to preserve MIT — no;
  `decisions/0002`'s runtime decision is superseded, `python-chess` is used
  directly.
- The FSF GPL FAQ's exact wording on library-linking and program-output
  licensing (previously unverified, rate-limited during bootstrap
  research) — no longer load-bearing for this project's own licensing
  position, since there is no longer an MIT claim depending on that
  interpretation. (It could still matter if this project ever needed to
  reason about *other* projects' GPL obligations, but not its own.)
- Whether an adapter-module boundary was *sufficient* isolation for an MIT
  claim (`0004`'s own flagged gate) — moot for the same reason.

**Still relevant** — unaffected by the license change, still open:

- Lichess's actual `Themes` tag vocabulary was not fetched/verified against
  the live dataset in research — only the column's existence was confirmed.
  Confirming real tag spellings against a downloaded copy is a cheap first
  step of roadmap item 4 (`decisions/0009`).
- **v1 does not yet independently re-derive sourced tactical puzzles' best-
  move/theme-purity correctness** — `python-chess` now makes move-legality
  and state-transition re-derivation cheap (`decisions/0011`), but best-move
  and theme-purity verification still need engine/tablebase analysis this
  project has not built. v1 continues to rely on Lichess's own generator/
  human-review pipeline for that part (`decisions/0006`, `0011`).
- The exact tactical-puzzle "dominant unrelated tactic" rejection check has
  no off-the-shelf precedent and is original design work for a later phase.
- Whether/when Stockfish is worth adding is still an open, deliberately
  deferred question — unaffected by licensing (`decisions/0003`, `0011`).
- True concurrent-write safety between this project's vault writes and a
  live Obsidian instance has not been empirically validated.
- Whether cropping should be automatic (inferred from the concept being
  taught) or explicit in lesson metadata, or both — a design question for
  roadmap item 6.

**Requires future evidence** — narrower verification tasks, not expected to
change any current decision but not yet independently confirmed:

- Syzygy tablebase data/probing-code licenses were not independently
  confirmed against a signed license file — relevant only if/when local
  tablebases are added, and lower-stakes now that GPL is available as a
  fallback if the probing-code license turns out to be GPL rather than
  permissive (unlike under the MIT goal, where this mattered more).
