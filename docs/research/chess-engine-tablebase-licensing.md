# Research: chess engine & tablebase licensing (for an MIT-licensed tutor)

Checked 2026-09-30. This feeds the project's licensing decision; it does not
make that decision. Where a source could not be fetched verbatim in this
pass, that is stated explicitly rather than papered over.

## Summary table

| Component | License (verified) | Classification if used | Verified against |
|---|---|---|---|
| `python-chess` (niklasf/python-chess, PyPI: `chess`) | **GPL-3.0-or-later** | Runtime, if imported as a library — see risk below | [LICENSE.txt](https://github.com/niklasf/python-chess/blob/master/LICENSE.txt), [PyPI project page](https://pypi.org/project/chess/) (classifier: `License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)`) |
| Stockfish | **GPL-3.0-or-later** | Optional, external process only (subprocess/UCI) | [Copying.txt](https://raw.githubusercontent.com/official-stockfish/Stockfish/master/Copying.txt) |
| Syzygy tablebase **data** (the `.rtbw`/`.rtbz` files) | No separate copyright claimed by the generator; treated by the chess-programming community as freely redistributable/effectively public-domain-like | External data asset, not code | [Syzygy Bases — Chessprogramming wiki](https://www.chessprogramming.org/Syzygy_Bases); [syzygy1/tb](https://github.com/syzygy1/tb) — **not independently verified against a signed license file in this pass; see gate below** |
| Syzygy **probing code** — `chess.syzygy` module bundled in python-chess | Same GPL-3.0-or-later as the rest of python-chess | Same as python-chess above | Same LICENSE.txt as above (single license for the whole package) |
| Syzygy **probing code** — standalone (e.g. Ronald de Man's original probing code, `syzygy1/tb`, `basil00/Fathom`) | Reported by the community as released for unrestricted use/redistribution (permissive-style) | Optional, isolated C component if ever vendored | [syzygy1/tb](https://github.com/syzygy1/tb), [Fathom](https://github.com/basil00/Fathom) — **exact license text not independently fetched in this pass; see gate below** |
| lichess.org public tablebase API (`https://tablebase.lichess.ovh`) | Not a code-licensing question — it's a hosted service | External service, zero-install dependency | [lila-tablebase](https://github.com/lichess-org/lila-tablebase), [Lichess API docs](https://lichess.org/api) |
| `chess.js` (JS/TS, for comparison — not usable from Python without a bridge) | **MIT** | N/A to a Python stack, cited only to show a permissive analogue exists in another ecosystem | [LICENSE](https://github.com/jhlywa/chess.js/blob/master/LICENSE) |
| Permissive pure-Python chess rules library | **None found** that is mature/adequate for full move generation + PGN/FEN | — | Search performed 2026-09-30; results were dominated by `python-chess` itself and its GPL forks/mirrors |

## 1. `python-chess`: license and the import-vs-subprocess distinction

Confirmed directly from the repository's `LICENSE.txt` (GPLv3 full text) and
the PyPI package metadata: **GPL-3.0-or-later**. This is not ambiguous —
python-chess is unambiguously copyleft, not permissive.

The honest answer on "does importing it as a library make my code GPL": **it
depends on the mechanism, and importing-as-a-library is the case where GPL's
copyleft is most likely to apply, not least likely.**

- If this project's own Python code does `import chess` and calls its
  functions in-process, that is normal library linking. Under the FSF's own
  reading of GPL (and under how the wider ecosystem treats "GPL library
  imported into your code"), a program that statically or dynamically links
  against a GPL library is generally considered a combined work, and the
  combination is expected to be distributed under GPL terms. This is
  different from, and stronger than, the "mere aggregation" case (see §3).
  **I am not asserting this project's whole codebase would legally become
  GPL — that turns on facts (how it's distributed, whether it's ever
  distributed as a combined work at all vs. run as a server nobody
  redistributes) that a lawyer, not this research pass, should confirm** —
  but the risk is real and non-trivial, not a technicality to wave away.
- If instead python-chess (or any GPL component) is only ever invoked as a
  **separate OS process** — e.g. a small isolated GPL-licensed microservice
  or CLI that does move-legality/PGN parsing and talks to the MIT-licensed
  core only via a well-defined IPC boundary (stdin/stdout, a local socket,
  HTTP) — the "mere aggregation" / independent-programs argument is on much
  firmer ground (§3). The cost is architectural: rules-handling has to live
  behind a process boundary, not just a module boundary.

## 2. Permissive Python alternatives for move generation/legality/PGN/FEN

No adequate permissively-licensed pure-Python chess rules engine was found in
this research pass. Search results were dominated by python-chess itself,
its documentation across versions, and direct forks/mirrors that inherit its
GPL license unchanged. This is a **negative result, not proof of absence** —
worth one more targeted search (e.g. PyPI "chess" classifier search filtered
to MIT/BSD/Apache) before treating it as settled, but nothing surfaced here.

Practical implications, in order of architectural cost:

1. **Accept python-chess as GPL, isolate it behind a process boundary.** The
   MIT-licensed core (learner model, pedagogy, MCP surface) talks to a small,
   separately-distributed GPL component that owns board state, legality, and
   PGN/FEN parsing, over a narrow IPC contract. This keeps the project's own
   source MIT while being honest that a GPL component is part of the running
   system for anyone who enables full chess-rules functionality.
2. **Write a minimal in-house legal-move validator scoped to the bounded MVP
   domain** (endgame positions with few pieces, plus tactics puzzles with a
   fixed FEN and a short expected line) rather than a general-purpose engine.
   Full chess move generation (castling, en passant, promotion, check
   detection, threefold repetition, etc.) is a solved but non-trivial amount
   of code; a *narrower* validator for "is this specific king/pawn/rook
   ending move legal and does it match the tablebase-optimal outcome" is
   smaller in scope. This avoids GPL entirely but duplicates real,
   error-prone logic and needs its own correctness testing (ironically,
   against something like python-chess or a tablebase as an oracle during
   *development* — which is fine, dev-only use isn't a distribution
   question).
3. **Use python-chess as a dev-time/offline-only tool** (e.g. to validate a
   generated puzzle corpus before it's baked into a data file), never
   imported by the shipped runtime at all. This is the same isolation idea
   as (1) but even lighter — no runtime process boundary needed because the
   GPL component genuinely never ships.

No option here is free of tradeoffs; this is exactly the kind of choice this
project's `decisions/` should record once made, not something to default
into silently.

## 3. Stockfish: license and the UCI/subprocess boundary

Confirmed from the repository's own `Copying.txt`: **GPL-3.0-or-later**.

Projects commonly integrate Stockfish (and other UCI engines) by launching it
as a **separate OS process** and talking to it over stdin/stdout using the
text-based UCI protocol — this is by far the dominant integration pattern in
the chess-software ecosystem, including in commercial GUIs that are not
themselves GPL.

The FSF's GPL FAQ draws a distinction between:
- **"Mere aggregation"** — two separate programs placed side by side (e.g. on
  the same disk, or communicating as independent processes at arm's length)
  — the GPL on one does not extend to the other, and
- **Combining into one program** — where the FSF's own stated test looks at
  *both* the communication mechanism (in-process function calls / shared
  address space vs. exec/pipes/RPC) *and* the semantics of what's
  exchanged, and treats tight in-process combination as more likely to
  create a combined/derivative work.

I attempted to fetch the FSF's GPL FAQ page directly to quote its exact
current wording and got an HTTP 429 (rate-limited) on this pass — **the
characterization above reflects well-established, widely-cited community
understanding of the FSF's position, not a verbatim quote checked against
the live page in this session.** This is exactly the kind of claim that
should be re-verified against `https://www.gnu.org/licenses/gpl-faq.html`
(the "GPLPipe"/aggregation-related entries) before it's relied on in a real
licensing writeup, and it is **not settled law** — it is the FSF's own
interpretive position, not a court holding, and other lawyers could
reasonably read it differently in an edge case. Flagging this as
interpretation, not fact.

Practical conclusion for this project: invoking a separately-installed
Stockfish binary via subprocess/UCI, where Stockfish is an **optional,
separately-installed, arm's-length process** (not vendored into this
project's own distribution, not statically linked, communicating only over
UCI text), is the standard, low-risk pattern the wider ecosystem relies on.
Treat "optional engine integration" as exactly that boundary if it's ever
built: optional install, separate process, text protocol, never imported.

## 4. Syzygy tablebases: data vs. probing code vs. remote API

Three genuinely different things, easy to conflate:

- **The tablebase data files themselves** (the `.rtbw`/`.rtbz` binary files
  covering up to 7 pieces). Generated by Ronald de Man and collaborators; the
  chess-programming community treats these as freely redistributable, and no
  source found in this pass asserts a restrictive copyright claim over the
  generated data. **This project did not independently locate and read a
  signed license/copyright file dedicated to the data files themselves** —
  the [Chessprogramming wiki's Syzygy Bases page](https://www.chessprogramming.org/Syzygy_Bases)
  and the [syzygy1/tb](https://github.com/syzygy1/tb) repository are the
  sources found, and a direct fetch of `syzygy1/tb`'s `Copyright.txt` 404'd
  in this pass (path may have moved or been renamed). **Gate: re-verify
  directly against the current `syzygy1/tb` repository tree before treating
  "the data is unencumbered" as settled fact**, though it is very unlikely
  to be a real blocker in practice given this is the near-universal community
  understanding.
- **Probing code bundled inside python-chess** (`chess.syzygy`): licensed
  under the same GPL-3.0-or-later as the rest of that package — confirmed,
  same LICENSE.txt as §1.
- **Standalone probing code** (Ronald de Man's original C code, and
  derivatives like [`basil00/Fathom`](https://github.com/basil00/Fathom)):
  community sources describe this as released for unrestricted
  use/redistribution — i.e. permissive in effect. **Not independently
  confirmed against Fathom's own `LICENSE` file in this pass; a follow-up
  fetch of that specific file is a cheap, worthwhile verification step
  before relying on it.**
- **Remote tablebase lookup via lichess's public API**
  (`https://tablebase.lichess.ovh`, documented via the
  [lila-tablebase](https://github.com/lichess-org/lila-tablebase) service and
  [Lichess API docs](https://lichess.org/api)): no authentication required;
  standard Lichess API rate-limiting norms apply (be a good citizen, don't
  hammer it, cache results); the service's own README credits Ronald de Man
  and Bojun Guo for the underlying tables. This is the **lowest-friction MVP
  option** for tablebase lookups — zero install, zero licensing exposure for
  *this* project (it's a network call to someone else's hosted service, not
  a dependency this project redistributes) — at the cost of an external
  runtime dependency and no offline capability. Worth an explicit rate-limit/
  fallback design note if the MVP leans on it for daily puzzle generation at
  any volume.

## 5. Is a full engine even necessary for the endgame-tutor MVP?

For the specific MVP slice under consideration (pawn endings: K+P vs K,
opposition, key squares, pawn races, basic zugzwang) — **no, a full
evaluation engine is not obviously required.** These are exactly the
positions tablebases solve perfectly and cheaply (≤5–6 pieces), so
correctness can be established via:

- a legal-move validator (in-house or isolated GPL component, per §2), plus
- tablebase lookup (remote API per §4, or local Syzygy files later) for
  "what is the actual correct/winning continuation."

This defers "optional engine integration" (Stockfish) to a clearly separate,
later concern — useful for middlegame/tactical-puzzle *generation quality*
(e.g. confirming a candidate tactic isn't secretly refuted or dominated by a
different tactic) rather than for the endgame core at all. That maps cleanly
onto the project's own stated architecture split between mechanical
validation (tablebase/rules/engine) and the AI/pedagogy layer, and keeps the
MVP's dependency surface small.

## Recommendation

Smallest architecture that keeps this project's own code MIT while being
honest about GPL surface area:

1. **Do not import python-chess into the MIT-licensed runtime core.** Either
   (a) keep it as a **dev-time-only** tool (puzzle-corpus validation, testing
   oracle) that never ships as part of the distributed/running product, or
   (b) if in-process legal-move handling is genuinely needed at runtime,
   isolate it behind a **separate process boundary** (its own small
   service/CLI, GPL-licensed, optional to install, invoked over IPC) rather
   than an in-process import — mirroring the Stockfish pattern in (3) below,
   not the "just `import chess`" pattern.
2. **Tablebase lookups: default to the remote lichess tablebase API** for the
   MVP (zero install, no licensing exposure, good enough for the bounded
   K+P-class curriculum), with local Syzygy files as a later, explicitly
   optional, separately-licensed addition if offline/high-volume use ever
   demands it.
3. **Stockfish (or any full engine): optional, separately-installed,
   subprocess/UCI only, never vendored.** Defer entirely until a concrete
   need (tactical-puzzle dominant-tactic rejection, per the bootstrap prompt)
   is reached — don't take the dependency speculatively.
4. **For the MVP's actual legality needs, prefer a small in-house validator
   scoped to the bounded domain** (limited piece count, no need for full
   game-tree features like threefold repetition) over adopting python-chess
   at runtime — smaller GPL exposure, smaller dependency, and the scope is
   genuinely narrow enough that this is plausible rather than naive. This
   should be tested against tablebase output and/or python-chess as a
   dev-time oracle, not shipped without independent verification of its own
   correctness.

This preserves: project's own source MIT-clean; any GPL component (if used
at all) isolated behind a process boundary consistent with how the wider
chess-software ecosystem already treats Stockfish; no speculative engine
dependency; a tablebase story that costs nothing to start.

## Open uncertainty / human decision gate

- **Not legal advice.** Everything above is research, not a legal opinion.
  The "import vs. subprocess" GPL analysis in particular turns on legal
  interpretation (what counts as a "combined work") that a court has not
  settled for this exact scenario — treat §1 and §3 as informed risk
  framing, not a guarantee.
- **FSF GPL FAQ verbatim text not re-fetched** in this pass (HTTP 429) —
  re-verify the exact current wording of the aggregation/pipe-related FAQ
  entries before citing them in anything more formal than internal research.
- **Syzygy data/probing-code license files not independently read**
  (`syzygy1/tb`'s `Copyright.txt` 404'd; Fathom's own `LICENSE` not fetched)
  — high confidence from community consensus, but not a first-party
  verification. Cheap to close: fetch both files directly.
- **Whether a "small in-house legal-move validator" is actually adequate**
  for the full intended scope (including the tactical-puzzle side, which
  likely needs broader move generation than pure pawn endings) is a real
  open question, not resolved here — this recommendation applies most
  cleanly to the endgame-only slice of the MVP, and the tactical-puzzle
  motif work may need a firmer answer on validator scope before this can be
  fully closed out. Recommend a follow-up gate at the point tactical-puzzle
  architecture is designed, not before.
- **No permissive pure-Python chess library was found — but the search was
  not exhaustive** (one focused pass). Worth a second, more targeted look
  (PyPI trove classifier search) before this project commits irreversibly to
  the in-house-validator path in decision §1 above.
