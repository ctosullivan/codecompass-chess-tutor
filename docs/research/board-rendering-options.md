# Research: chess-board/diagram rendering options

Checked 2026-09-30. Focused on: can we get arbitrary board cutaways/crops,
square highlighting, arrows, and minimal-pair "before → after" comparisons,
embeddable in Markdown/Obsidian and MCP responses, while keeping the project
MIT-licensable?

## Summary table

| Component | License (verified) | Verdict for an MIT project |
|---|---|---|
| `python-chess` library (incl. `chess.svg` module) | GPL-3.0-or-later ([LICENSE.txt](https://github.com/niklasf/python-chess/blob/master/LICENSE.txt), confirmed in [README](https://github.com/niklasf/python-chess)) | Usable as an isolated GPL *dependency* behind a clean process/API boundary; do not statically link/vendor its code into an MIT-licensed distribution. Its **generated SVG output is not itself GPL** (see below) — the license risk is about depending on the library, not about the pictures it produces. |
| `chess.svg` piece artwork (the bundled default piece images, "cburnett") | **Triple-licensed**: GFDL v1.2+, CC BY-SA 3.0, and **BSD 3-clause** — confirmed on the piece's [Wikimedia Commons file page](https://commons.wikimedia.org/wiki/File:Chess_kdt45.svg) and referenced in the [chess.svg docs](https://python-chess.readthedocs.io/en/latest/svg.html) ("triple licensed under the GFDL, BSD and GPL by Colin M.L. Burnett") | **Good news, not a blocker**: because BSD-3-clause is one of the three licenses offered, an MIT project can choose to use/redistribute this artwork *under the BSD option* and avoid GFDL/CC-BY-SA's share-alike and invariant-section machinery entirely. Still requires a copyright/attribution notice per BSD-3-clause terms. |
| Lichess `chessground` (interactive web board) | GPL-3.0 ([LICENSE](https://github.com/lichess-org/chessground/blob/master/LICENSE)) | JS/browser widget, not a server-side SVG generator — not directly relevant to MCP/Markdown output. Same "isolated dependency, don't vendor" logic would apply if ever used for a web view. |
| `chess-viewer-utils` (npm, "dependency-free... render SVG diagrams") | **Marketed as MIT in its README/description, but its actual `LICENSE` file is AGPL-3.0** ([LICENSE](https://github.com/chessviewer-org/chess-viewer-utils/blob/main/LICENSE), copyright Free Software Foundation) | **Reject / do not trust the description.** This is exactly the kind of discrepancy that has to be checked against the actual `LICENSE` file, not marketing copy — AGPL-3.0 is materially more restrictive than GPL for anything reachable over a network (MCP server counts). |
| `fenwoody`, `FEN2SVG`, and similar small hobby FEN→SVG tools found via search | No verified license file checked (small/personal repos, license not confirmed) | Unverified — do not adopt without checking an actual `LICENSE` file; treat as unresearched, not as "probably fine." |
| Board-cropping/partial-region rendering, in any library surveyed | Not found anywhere | **No library surveyed — GPL, BSD/MIT, or unverified — has built-in support for rendering a bounded sub-region of the board** (e.g. a 3×3 or 4×4 crop). This capability appears to not exist as an off-the-shelf feature anywhere. |

## 1. `python-chess` / `chess.svg`

- License: GPL-3.0-or-later, confirmed directly from the repo's `LICENSE.txt` and restated in the README ("python-chess is licensed under the GPL 3 (or any later version at your option)").
- `chess.svg.board()` supports: `orientation`, `lastmove`, `check`, `arrows` (an `Arrow` class with `tail`/`head`/`color`, including PGN `%csl`/`%cal` annotation round-tripping), `fill` (square → color highlighting), `squares` (mark a `SquareSet` with an X), `size`, `coordinates`, `colors` override, `borders`, and a custom `style` stylesheet. This is a genuinely capable full-board primitive.
- **No built-in cropping/viewport feature.** The documentation has no parameter for rendering only part of the board. Because the output is plain SVG, a `viewBox`/coordinate-math post-process to crop to an arbitrary square region is straightforward to build as project-owned code sitting on top of the library's output — but it does not come for free.
- **Output-licensing question — resolved, not just "likely fine":** the FSF's own GPL FAQ directly addresses this ("Does the GPL have special requirements for uses in cloud computing environments?" is a different entry — the relevant one is on GPL-covered programs and their output): *"In general this is legally impossible; copyright law does not give you any say in the use of the output people make from their data using your program... The only way you have a say in the use of the output is if substantial parts of the output are copied (more or less) from text in your program."* (gnu.org GPL FAQ, "GPLOutput" entry, via web search snippet 2026-09-30 — the canonical page `gnu.org/licenses/gpl-faq.html` returned HTTP 429 on direct fetch at research time; the quoted text is from a search-engine-cached excerpt of that exact page and should be re-verified against the live page before this is relied on in a legal sense). A generated board SVG (paths/coordinates for squares, plus the separately-and-permissively-licensed piece artwork) is not "text copied from the program" — it's data, generated the way a PDF from a GPL'd typesetting program isn't itself GPL. This is a reasonable, sourced position, not a certainty; see the decision gate below.

## 2. The bundled piece set ("cburnett")

Verified directly on Wikimedia Commons ([File:Chess_kdt45.svg](https://commons.wikimedia.org/wiki/File:Chess_kdt45.svg), one of the standard piece files in the set): the artist (User:Cburnett) released the set under **all of**:

1. GFDL v1.2+ ("Permission is granted to copy, distribute and/or modify this document under the terms of the GNU Free Documentation License")
2. CC BY-SA 3.0 Unported
3. **BSD (3-clause)** — "Redistribution permitted with conditions including retaining copyright notice and disclaimer"
4. GPL v2+

A user/redistributor picks **whichever one license** suits them — it is not a "must satisfy all four simultaneously" situation. For an MIT project, **option 3 (BSD-3-clause) is the one to use**: it requires retaining the copyright notice and disclaimer (attribution to Cburnett, dated 2006) but carries no share-alike/copyleft obligation on either the artwork or anything else. This removes what looked like the biggest asset-licensing risk in this whole area, *if* the project deliberately documents that it's exercising the BSD option and keeps the required notice next to the artwork.

## 3. Lichess `chessground`

Confirmed GPL-3.0 via the repo's own `LICENSE` file. It's a client-side interactive board widget (drag/drop, animation), not a server-side diagram generator, so it isn't a real candidate for MCP/Markdown SVG generation regardless of license. Noted here only because the prompt asked about it; not pursued further.

## 4. Permissively-licensed alternatives

Search turned up no library, in any language, that is (a) clearly MIT/BSD/permissively licensed *by its actual LICENSE file* (not just a README claim) **and** (b) supports FEN→SVG board rendering with any built-in cropping. The one candidate that looked promising by description (`chess-viewer-utils`, advertised as dependency-free with an MIT-sounding pitch) turned out to ship an **AGPL-3.0** `LICENSE` file when checked directly — a real trap, and the exact reason to check the actual license file rather than a repo's marketing description. `fenwoody` and `FEN2SVG` are small enough (single-purpose, low-visibility) that no license could be confirmed at all in this pass; treat as unresearched rather than assuming permissive-by-default.

**No cropping support exists anywhere surveyed.** Whichever underlying board-drawing primitive is chosen, the pedagogical viewport/crop/arrow/annotation layer described in the bootstrap prompt will be project-owned code regardless of vendor choice.

## Recommendation

**Option (a) — take `python-chess`'s `chess.svg.board()` purely as a full-board SVG primitive, isolated behind a project-owned rendering-adapter module, and build the pedagogical viewport/cropping/comparison layer entirely as project code on top of its raw SVG output.**

Reasoning:

- `python-chess` is very likely already the right dependency for legal-move validation and FEN/PGN handling elsewhere in the architecture (see the chess-engine/tablebase research thread) — using its SVG module too avoids adding a second, less-proven rendering dependency on top.
- The GPL exposure is real but manageable and already well-precedented: isolate `python-chess` behind a single adapter boundary (a "chess validation/rendering" module), never let its types leak into the MIT-licensed public API/domain model, and the project's own code remains cleanly MIT. This mirrors the CodeCompass-as-dev-tool boundary already established elsewhere in this bootstrap — "depend on a GPL tool without becoming GPL" is the same shape of problem.
- The piece-artwork licensing risk, which looked like it might force a "draw our own pieces" fallback, is resolved by deliberately exercising the BSD option on the cburnett set (with attribution) rather than the GFDL/CC-BY-SA options.
- Writing project-owned code for: SVG `viewBox` cropping to an arbitrary rank/file window, key-square highlighting beyond what `fill`/`squares` already give, arrow paths between arbitrary points (not just squares) for pawn-race lanes, and side-by-side before/after composition — is a bounded, well-testable amount of work (pure SVG/XML string or DOM manipulation, deterministic, easy to snapshot-test), much smaller than writing a full board-and-piece renderer from scratch.
- Option (b), a from-scratch renderer with self-drawn/geometric pieces, avoids the GPL dependency question entirely but means owning piece-shape drawing (a real design/maintenance cost, and arguably a worse learner experience than recognizable standard piece glyphs) for a licensing benefit that option (a) already captures via the BSD option.

This recommendation should be captured as an ADR before the rendering implementation phase begins — it's exactly the kind of non-obvious tradeoff `decisions/` exists for.

## Open uncertainty / human decision gate

1. **GPL-FAQ citation reliability**: the "GPL-covered program's output is not itself GPL, unless substantial program text is copied into it" position is well-established FSF guidance, but this research pass could only retrieve it via a search-engine cache excerpt (`gnu.org/licenses/gpl-faq.html` returned HTTP 429 directly, twice, at research time). **Before finalizing the rendering-adapter ADR, re-fetch the live FAQ page and quote the exact "GPLOutput" entry directly**, rather than relying on the cached excerpt in this document.
2. **Whether "isolated GPL dependency behind an adapter boundary" is sufficient for the project's actual MIT claim**, versus needing a stronger structural separation (e.g. an optional-install rendering plugin, invoked as a subprocess rather than an in-process import) — this is a licensing-risk-tolerance question, not a pure research question, and belongs with whoever is making the final MIT-license call for the whole project.
3. **The BSD-option choice for cburnett artwork must be documented in-repo** (e.g. a `NOTICE`/`THIRD_PARTY_LICENSES` file naming Cburnett and the BSD-3-clause terms exercised) once artwork is actually vendored — not yet done, since no rendering code exists yet.
