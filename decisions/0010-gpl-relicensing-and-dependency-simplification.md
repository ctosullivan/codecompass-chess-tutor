# 0010. Relicense GPL-3.0-or-later; adopt python-chess as a normal runtime dependency

## Status

Accepted (2026-09-30). Supersedes `decisions/0007` in full. Supersedes
`decisions/0002`'s runtime decision. Narrows `decisions/0004`'s isolation
reasoning while leaving its pedagogical-layer decision intact. Narrows
`decisions/0003`'s licensing-motivated sub-choices while leaving its
operational strategy intact. See "Reconciliation" below for exactly which
parts of each. Directed by
`planning/prompts/0002-gpl-relicensing-and-simplification.md`.

## Context

The bootstrap (`planning/prompts/0001-project-bootstrap.md`) treated MIT as
the preferred license conditional on dependency research, and
`decisions/0001`–`0009` built real architecture to make that conditional
license achievable: a bespoke in-house legal-move validator to avoid
importing GPL-licensed `python-chess` at runtime (`0002`), a rendering-
adapter boundary to isolate GPL-licensed `chess.svg` (`0004`), and a
preference for standalone Syzygy probing code over python-chess's own
bundled `chess.syzygy` module specifically to avoid GPL exposure in a local-
tablebase path (`0003`).

**The project owner has now explicitly decided the project should be
licensed GPL-3.0-or-later instead of MIT**, because the available chess
ecosystem dependencies (chiefly `python-chess`) make GPL a better fit for
this project, and avoiding them would introduce unnecessary custom
infrastructure — specifically, the bespoke legal-move validator that
`decisions/0002` committed to building, and the isolation boundaries that
`decisions/0002` and `0004` built around `python-chess` and `chess.svg`.
This is a deliberate architectural simplification, not merely a change to
the `LICENSE` file's text.

This decision does not reopen or relitigate the bootstrap's other
conclusions (MVP scope, curriculum boundary, concept-model shape, MCP/
Obsidian architecture, CodeCompass's dev-tool-only role) — those stand as
recorded in `decisions/0001`, `0005`, `0006`, `0008`, `0009`, and are not
touched here.

## Decision

**This project is relicensed GPL-3.0-or-later.** The `LICENSE` file now
contains the FSF's own canonical GPL-3.0 license text, unmodified, with no
project-specific commentary appended to it — that commentary moves to
`README.md`, `docs/architecture.md`, this record, and
`NOTICE-THIRD-PARTY.md` (added in this same change) — see "Consequences."

As a direct result, three prior architecture choices are superseded or
narrowed:

### `python-chess` becomes a normal runtime dependency (supersedes `decisions/0002`'s runtime decision)

The bespoke in-house legal-move validator that `0002` committed to building
existed **only** to avoid importing a GPL-licensed library into an
MIT-licensed runtime. With GPL now the project's own license, that reason is
gone, and no independent product reason to hand-roll chess move generation
has been identified — `python-chess` is a mature, widely-used,
perft-verified implementation, and building a narrower equivalent would be
pure duplicated effort with no offsetting benefit now that the licensing
constraint that justified it no longer applies.

**`python-chess` is adopted directly as a normal runtime dependency**, used
for:

- FEN/board representation and applying state transitions;
- legal move generation;
- check/checkmate/stalemate and other game-state checks;
- SAN/UCI notation;
- Syzygy tablebase probing support, if/when local tablebases are used (see
  `decisions/0003`'s continuing operational strategy below);
- SVG board rendering (`chess.svg`, see the rendering reconciliation below).

No adapter boundary, process boundary, or "dev-time-only" restriction is
required for licensing purposes. `python-chess` types may appear directly in
the chess-state/domain layer's own code.

This project explicitly **does not** spend effort evaluating or adopting
permissively-licensed alternatives (e.g. `ChessMG` or other perft-verified
move generators, noted as existing during the bootstrap's research) purely
to avoid `python-chess` — that would be solving a licensing problem that no
longer exists at the cost of real engineering time. An alternative would
only be worth revisiting for a concrete, independently-justified product
reason (materially better portability, performance, maintenance, or
capability) — not found or sought in this decision.

**This does not remove the need for independent correctness testing of this
project's own domain logic.** Adopting `python-chess` removes the need to
recreate generic chess rules; it does not remove the need to test how this
project's own endgame-curriculum and tactical-puzzle code *uses* those
rules (e.g. that a lesson's stated "key square" claim is actually correct
for the position it's attached to, or that a puzzle's stored FEN and side-
to-move are internally consistent) — that testing responsibility is
unchanged by this decision.

### Board rendering: `chess.svg` becomes a normal base primitive (narrows `decisions/0004`)

`0004`'s **isolation-boundary reasoning** — "nothing outside the rendering-
adapter module may import `python-chess`/`chess.svg` directly," and the
careful GPL-output-vs-GPL-code argument for why a generated SVG isn't
itself GPL — existed only to protect an MIT claim. That reasoning is now
moot: the project's own code can be GPL-licensed and combined with
`chess.svg` freely, so there is no licensing reason to keep `python-chess`'s
types out of the rendering layer or anywhere else.

**`0004`'s pedagogical decision is not superseded and remains fully
valid**: the separation of *what to show* (a `PedagogicalViewSpec` — bounds,
orientation, highlighted squares, arrows/trajectories, annotations,
comparison state) from *how to draw it* (a renderer) is good architecture on
its own technical merits — it keeps teaching intent legible as data and
keeps the renderer swappable — independent of licensing. What changes is
*why* the boundary between "project-owned composition" and "underlying
board-drawing primitive" exists: not to keep a GPL dependency's types from
leaking into an MIT core, but because *what the learner should see* and
*how squares/pieces are drawn* are genuinely different concerns that
change for different reasons and at different rates. The revised shape:

```
position / board state
        ↓
PedagogicalViewSpec
        ↓
project-owned pedagogical composition   (crop, highlight, arrows, comparisons)
        ↓
python-chess / chess.svg primitive       (ordinary dependency, no isolation)
        ↓
SVG artifact
        ↓
Obsidian / MCP consumer
```

The cburnett piece-artwork attribution decision in `0004` (exercising the
BSD-3-clause option, retaining a copyright notice) is **also not
superseded** — see "Third-party attribution is independent of this
project's own license" below.

### Tablebase and engine strategy: operational strategy retained, licensing-motivated sub-choices narrowed (`decisions/0003`)

`0003`'s core strategy — **tablebases as the preferred exact oracle for
bounded endgames; a full evaluation engine deferred until a concrete need
justifies it** — rests on operational and scope reasoning (tablebases are
perfect and cheap for the bounded curriculum; an engine adds a real
dependency for a need not yet reached) that has nothing to do with
licensing. **That strategy is retained in full.**

Two of `0003`'s sub-choices *were* licensing-motivated and are narrowed:

- `0003` preferred **standalone Syzygy probing code over python-chess's own
  bundled `chess.syzygy` module**, specifically to keep a local-tablebase
  path out of GPL. With GPL now the project's own license, this reason is
  gone: **if/when local Syzygy tablebases are added, python-chess's own
  `chess.syzygy` module is the simpler, better-integrated choice**, and
  there is no longer a reason to prefer sourcing separate standalone probing
  code instead. The remote lichess tablebase API remains the default for
  the MVP regardless — that choice was about zero-install operational
  simplicity, not licensing, and is unaffected.
- `0003` required Stockfish, if ever introduced, to be "optional,
  separately-installed, subprocess/UCI-only... never vendored, never
  imported in-process," reasoning explicitly grounded in keeping a GPL
  engine from making the *project* GPL. **The subprocess/UCI pattern is
  retained**, but for a different, still-valid reason: process isolation
  from an external engine binary is good architecture regardless of license
  (stability — an engine crash doesn't take down the tutor process;
  optionality — Stockfish stays a separately-installed, not-required
  dependency; resource control — engine analysis can be time/depth-bounded
  and run out-of-process). **This project does not introduce Stockfish now
  merely because GPL permits an in-process import** — the "deferred until a
  concrete tactical-analysis or validation need justifies it" scope
  decision in `0003` is unchanged and still applies.

## Reconciliation of `decisions/0001`–`0009`

| ADR | Disposition | What changes | What doesn't |
|---|---|---|---|
| `0001` (Python + MCP SDK) | Unaffected | — | Language, SDK, transport, vault path-resolution boundary all stand; none of that reasoning was licensing-motivated. |
| `0002` (bespoke validator) | **Superseded** (runtime decision) | The in-house legal-move validator is not built; `python-chess` is the runtime chess-state representation. | The dev-time correctness-testing principle survives in different form: this project's *own* domain-logic tests (see above) still matter. |
| `0003` (tablebase/engine strategy) | **Narrowed** | Standalone-Syzygy-probing-code-over-python-chess preference is superseded (use python-chess's `chess.syzygy` if/when local tablebases are added); Stockfish's "never in-process" *licensing* rationale is superseded. | Tablebase-preferred/engine-deferred strategy stands; remote-API-default-for-MVP stands; subprocess/UCI-for-Stockfish stands, now for process-isolation reasons instead of licensing reasons; "don't add Stockfish speculatively" stands. |
| `0004` (board rendering) | **Narrowed** (isolation reasoning superseded; pedagogical decision retained) | The rendering-adapter module is no longer a licensing-required boundary; `chess.svg`/`python-chess` types may be used directly in rendering code. | `PedagogicalViewSpec` → composition → primitive → SVG separation stands, now justified purely by separation-of-concerns; the BSD-option cburnett attribution decision stands. |
| `0005` (Obsidian integration) | Unaffected | — | Nothing in `0005` was licensing-motivated. |
| `0006` (puzzle sourcing/validation) | Unaffected in its licensing conclusions; reassessed for feasibility in `decisions/0011` | — | Lichess CC0 sourcing, chess.com/ChessBase exclusion, and AGPL-`lichess-puzzler`-as-reference-only all stand (none were about *this* project's own license). See `decisions/0011` for whether GPL adoption changes what's newly *feasible* for re-derivation. |
| `0007` (MIT license) | **Superseded in full** | Project license is now GPL-3.0-or-later. | — |
| `0008` (concept model) | Unaffected | — | Nothing in `0008` was licensing-motivated. |
| `0009` (MVP curriculum) | Unaffected | — | Nothing in `0009` was licensing-motivated; the MVP boundary is explicitly *not* being broadened by this decision (see Consequences). |

Per `decisions/README.md` and `CLAUDE.md` §4, none of `0002`–`0004`'s or
`0007`'s own historical bodies are edited. Each gets only a short
`Status:` line appended, in the format their own `TEMPLATE.md` anticipates
("superseded by `decisions/NNNN`, once that record exists — added as a note
here, the rest of this file's content left untouched"), pointing to this
record.

## Third-party attribution is independent of this project's own license

**Relicensing to GPL does not remove any attribution obligation this
project already owed.** The cburnett chess-piece artwork (used via
`chess.svg`'s default piece set) is licensed by its author under a choice
of GFDL, CC-BY-SA 3.0, BSD-3-clause, or GPL v2+ — `decisions/0004`'s choice
to exercise the **BSD-3-clause option** (requiring only a retained
copyright/attribution notice, no share-alike) remains the right choice: it
is simple, well-understood, and — notably — this project's own license
choice does not change which option is *simplest*, since BSD's obligation
(attribution) is a strict subset of what any of the other three options
would also require. A `NOTICE-THIRD-PARTY.md` file recording this
attribution is added in this same change (see Consequences) — this was
already flagged as outstanding follow-up work in `0004`'s own Consequences
section (no rendering code existed at bootstrap time to attach it to; none
exists now either, but the file is added proactively alongside this
licensing change so it isn't lost when rendering code does land).

## Correcting a hedge-rounding overclaim (bootstrap review follow-up)

While reconciling `docs/architecture.md` for this decision, a further
instance of the "hedge-rounding" failure pattern already logged in
`planning/knowledge/0001-hedge-rounding-and-fork-limits.md` was found and
fixed: `docs/architecture.md`'s "Visual pedagogy" section stated, as a flat
claim, that "no board-rendering library, in any license, that supports
rendering a bounded sub-region of the board... that capability doesn't
exist off the shelf anywhere." The underlying research
(`docs/research/board-rendering-options.md`) only established that **none
of the specific candidates surveyed** in that research pass supported it —
a bounded search result, not proof that no such tool exists anywhere. This
is corrected directly in `docs/architecture.md` (not in the research
document itself, which is a dated evidence snapshot, or in `decisions/0004`,
which is not edited per the append-only rule). See that document's own
revised wording.

## Alternatives considered

- **Keep MIT and the isolation architecture, do nothing.** Rejected: this
  is the project owner's explicit decision, made on its own terms (the
  chess ecosystem fits GPL better; the isolation architecture is
  unnecessary custom infrastructure) — not something this record is
  evaluating from scratch. The evidence in `docs/research/` already showed
  the isolation approach was *achievable*, not that it was the *only*
  reasonable choice; GPL was flagged as a live alternative in `0007`'s own
  "Alternatives considered" section at the time.
- **Relicense to GPL but keep the bespoke validator/rendering-adapter
  architecture anyway** (treat the isolation boundaries as good engineering
  independent of licensing). Rejected for the *validator*: no independent
  product reason for owning generic chess-rules logic was identified, and
  the prompt directing this decision is explicit that one should exist
  before keeping it. Rejected differently for *rendering*: here the
  boundary genuinely does have independent technical value (separation of
  teaching intent from drawing mechanics), so it's retained — but its
  *isolation* aspect (keeping `python-chess` types out) is dropped since
  that specific aspect had no independent justification.
- **Use python-chess's `chess.syzygy` and drop the remote lichess API
  default too, now that local tablebases are "free" licensing-wise.**
  Rejected: the remote API's appeal was operational (zero install, zero
  storage, adequate for the bounded MVP curriculum), not licensing — that
  reasoning is untouched by this decision, so the remote API remains the
  MVP default per `0003`.

## Consequences

- **What this deletes/avoids building**: the bespoke in-house legal-move
  validator (never built — no code existed at bootstrap time — so nothing
  is deleted from a codebase, but it is removed from the plan/roadmap
  before any effort was spent on it); the rendering-adapter's *isolation*
  requirement (the compositional structure itself is kept, per above); the
  requirement to source standalone Syzygy probing code instead of using
  python-chess's bundled module, if/when local tablebases are added.
- **What this adds**: `python-chess` as a normal, direct runtime dependency
  (with all the maintenance-by-upstream benefit that implies, and the
  corresponding loss of full control over that piece of logic — accepted
  as the right tradeoff now that no licensing reason favors owning it);
  `NOTICE-THIRD-PARTY.md`, recording the cburnett BSD-option attribution;
  a canonical, unmodified GPL-3.0 `LICENSE` file, with the explanatory
  material it previously carried moved to `README.md` and
  `docs/architecture.md`.
- **The MVP boundary is explicitly not broadened by this decision.** GPL
  adoption makes some infrastructure easier to build, but the bounded
  pawn-ending curriculum (`0009`), the daily-thematic-tactics requirement,
  the MCP/Obsidian architecture (`0001`, `0005`), and the concept-model
  shape (`0008`) are all unchanged. Easier infrastructure is not itself a
  reason to do more.
- **The chess-truth/pedagogy epistemic boundary is unchanged and is a
  software-boundary question, not a licensing one** — see the reconciled
  `docs/architecture.md` "Chess truth vs. AI explanation" section. Legal
  chess state and move mechanics (now `python-chess`), exact tablebase
  truth, optional engine analysis, sourced tactical-puzzle claims, tutor
  interpretation, and learner understanding remain six distinct things;
  making the underlying library easier to use does not make an LLM's own
  assertion a valid substitute for any of them.
- **Tactical-puzzle validation claims are reassessed, not automatically
  strengthened, by this decision** — see `decisions/0011` for what GPL
  adoption does and doesn't change about the cost of independently
  re-deriving sourced puzzle solutions. `python-chess` lowers the cost of
  *move-legality* verification; it says nothing about *best-move*/
  *tactical-optimality* verification, which still requires engine or
  tablebase analysis this project has not built.
- **CodeCompass's role is unaffected.** `vendor.toml` remains empty until
  real source/dependencies exist (the next implementation phase); when it
  does, `python-chess` and the MCP SDK become its first real tracked
  entries, and running CodeCompass against that real manifest becomes this
  project's first genuine dogfooding exercise of the template's own
  workflow — see `planning/ROADMAP.md` and `planning/CONTEXT.md`.
- **Future reversal.** If this project ever needed to become permissively
  licensed again (e.g. an embedding use case that GPL's copyleft would
  block), that would need its own superseding decision record and would
  need to re-examine whether `python-chess`'s now-direct integration into
  the domain/rendering layers could be un-wound — this decision does not
  attempt to keep that door open architecturally, since the owner's
  decision is to stop paying that cost.
