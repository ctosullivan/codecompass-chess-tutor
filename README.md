# codecompass-chess-tutor

An experimental AI-assisted chess-learning system. This repository is
currently a **research-and-architecture bootstrap** — there is no running
tutor yet. See `planning/CONTEXT.md` for exactly where things stand.

**Licensing note**: this project is licensed **GPL-3.0-or-later**. It began
as an MIT-conditional bootstrap; the project owner subsequently decided GPL
is the better fit, since the available chess ecosystem (chiefly
`python-chess`) fits GPL naturally and avoiding it would have meant building
unnecessary custom infrastructure. See `decisions/0010` and the License
section below.

## What this is trying to be

CodeCompass Chess Tutor treats chess learning as several interacting
concerns — chess state, chess concepts and principles, a learner model, a
pedagogical model, and evidence/provenance — rather than as a single
engine-evaluation problem. The first milestone is deliberately narrow: an
**endgame tutor** for a bounded pawn-endings curriculum, plus a **daily
thematic tactical puzzle** capability, exposed as an MCP tool/server so a
learner's AI assistant can call it directly, designed to live alongside a
learner's Obsidian vault without locking their notes into a proprietary
format.

See `docs/architecture.md` for the full picture, and
`planning/prompts/0001-project-bootstrap.md` for the original brief this
project was bootstrapped from, preserved verbatim.

## What's explicitly in the first MVP

- An endgame core covering king-and-pawn-vs-king, opposition, key squares,
  pawn races, king activity, zugzwang, and basic passed-pawn concepts —
  chosen because it's exactly the scope where tablebase lookup makes every
  "this move is correct" claim mechanically provable, not just
  engine-plausible (`decisions/0003`, `decisions/0009`).
- A daily thematic tactical-puzzle session, sourced from Lichess's
  CC0-licensed puzzle export, covering forks, pins, skewers, discovered
  attacks, removal of defender, deflection, decoys, clearance, interference,
  overloaded pieces, back-rank motifs, forcing-move recognition, and
  loose/undefended pieces (`decisions/0006`,
  `0009`).
- Both features sharing one lightweight concept model and one learner-
  evidence store, to test whether tactics and endgame training can
  genuinely share an architecture rather than becoming disconnected
  features (`decisions/0008`).
- An MCP server surface, and direct (non-plugin) read/write access to a
  learner's Obsidian vault as an ordinary folder of Markdown files
  (`decisions/0001`, `0005`).
- Pedagogical board rendering — including cropped/cutaway views, not just
  full 8×8 boards — as a first-class part of the teaching model, built as
  project-owned composition logic on top of `python-chess`'s `chess.svg` as
  an ordinary rendering primitive (`decisions/0004`, `0010`,
  `docs/architecture.md`).

## What's explicitly out of the first MVP

- A general chess coach, opening/middlegame training, or broad
  concept-graph platform beyond the bounded slice above.
- Position/puzzle *generation* (constructing or modifying positions) —
  v1 selects from Lichess's existing corpus; generation is a later,
  explicitly deferred phase (`decisions/0006`).
- A full evaluation engine (e.g. Stockfish) — not needed for tablebase-scope
  endgames; deferred until a concrete need (puzzle-quality validation)
  justifies it, and then only as an optional, subprocess-isolated component
  (`decisions/0003`, `0010` — the subprocess pattern is kept for process-
  isolation reasons, not licensing; GPL permitting an in-process engine is
  not itself a reason to add one).
- Any dependency on Obsidian actually running, or on Obsidian plugins — the
  tutor works with a vault as a plain folder on disk (`decisions/0005`).
- CodeCompass as anything other than a development-time tool — it is never
  a runtime dependency of the tutor itself (see below).

## Development process

This project follows the lightweight workflow from
[`codecompass-template`](https://github.com/ctosullivan/codecompass-template):
understand → research/evidence → plan → design → implement → verify → retro
→ update knowledge — adapted rather than inheriting CodeCompass's own larger
accumulated governance. See `CLAUDE.md` for the working rules, and:

- `docs/architecture.md` — current system architecture.
- `decisions/` — append-only architecture decision records.
- `docs/research/` — evidence documents behind the decisions above.
- `planning/ROADMAP.md` / `planning/CONTEXT.md` — what's done, in progress,
  or planned, and where things stand right now.
- `planning/prompts/` — the substantial prompts that directed this
  project's work, preserved verbatim.
- `planning/retros/`, `planning/knowledge/`, `planning/context-gaps/` — a
  closing-the-loop log, a durable-learnings log, and a missing-context log.

## CodeCompass's role

[CodeCompass](https://github.com/ctosullivan/codecompass) is used as a
**development-time context tool** for this project — dependency and
first-party-source indexing during development — and is **not** part of the
chess tutor's own product architecture. Production/runtime code never
imports or depends on CodeCompass; anyone can clone, install, test, and run
this project without it installed. See `docs/architecture.md`'s "On this
project's relationship to CodeCompass" section and `CLAUDE.md` §8.

## License

**GPL-3.0-or-later** — see `LICENSE`, which contains the FSF's own
canonical GPLv3 license text, unmodified (per the FSF's own guidance that
copies of the license itself must stay verbatim).

This project began its bootstrap with MIT as the preferred, conditional
license (`decisions/0007`), supported at the time by an architecture that
deliberately isolated every GPL-licensed dependency it touched (a bespoke
in-house legal-move validator instead of importing `python-chess`; an
isolation boundary around `chess.svg`). **The project owner subsequently
decided GPL-3.0-or-later is the better fit**: the chess ecosystem this
project depends on (`python-chess` chief among it) is itself GPL-licensed,
and the isolation architecture built to avoid it was unnecessary custom
infrastructure once GPL was an acceptable license for the project itself.
See `decisions/0010-gpl-relicensing-and-dependency-simplification.md` for
the full reasoning, and `decisions/0007` (marked superseded, left otherwise
unedited as history) for why MIT was the original conclusion.

Some components this project depends on or interoperates with carry their
own separate licenses and attribution terms, independent of this project's
own license choice — see `NOTICE-THIRD-PARTY.md` (notably: the cburnett
chess-piece artwork's BSD-3-clause attribution requirement, which GPL
adoption does not remove) and `docs/architecture.md`'s "Key dependencies"
table.

## Status

Bootstrap phase. No code exists yet — see `planning/CONTEXT.md` for current
state and `planning/ROADMAP.md` for what's next.
