# 0004. python-chess's SVG renderer as an isolated primitive; pedagogical cropping/annotation layer is project-owned

## Status

Accepted (2026-09-30). **Narrowed by `decisions/0010` (2026-09-30)**: the
isolation-boundary reasoning below (keeping `python-chess`/`chess.svg`
types out of the rest of the codebase specifically to protect an MIT
claim) no longer applies now that the project is GPL-3.0-or-later licensed
— `chess.svg` is now a normal base rendering primitive, usable directly.
The pedagogical decision itself — separating a `PedagogicalViewSpec` from
the underlying rendering primitive, and building the cropping/annotation
layer as project-owned code — remains fully valid, now justified purely by
separation of concerns rather than by licensing. The cburnett BSD-option
attribution decision below also remains valid and unaffected. This note is
added per this file's own append-only rule; the rest of this record is left
exactly as originally written, as history.

## Context

The tutor treats board rendering as part of the pedagogy, not UI polish: it
needs arbitrary board cutaways/crops (e.g. 3×3/4×4 regions), key-square
highlighting, arrows/trajectories, and minimal-pair before/after comparisons,
embeddable cleanly in Markdown/Obsidian and MCP responses. See
`docs/research/board-rendering-options.md`.

No library surveyed, in any license, has built-in support for rendering a
bounded sub-region of the board — that layer is project-owned regardless of
which underlying board-drawing primitive is chosen. The choice is therefore
about the full-board primitive and its piece artwork, not about the
pedagogical layer.

`python-chess`'s `chess.svg` module (GPL-3.0-or-later, same license as the
rest of the package) supports orientation, arrows, square fill/highlighting,
and coordinate labels, and produces plain SVG output. Its bundled default
piece set ("cburnett") is **triple/quadruple-licensed** (GFDL, CC-BY-SA 3.0,
BSD-3-clause, GPL v2+) — confirmed on the artist's own Wikimedia Commons file
page — meaning a redistributor may pick whichever single license suits them.

## Decision

- **Use `chess.svg.board()` as an isolated full-board SVG primitive**, behind
  a project-owned rendering-adapter module. `python-chess`'s GPL license is
  not vendored/statically combined into the MIT-licensed core's own
  distributed source; its types must not leak into the project's public
  domain model or MCP-facing API (mirroring the same "GPL tool, isolated
  behind a boundary" shape as `0002`/`0003`). Since `python-chess` is very
  likely already present dev-time (`0002`) and potentially process-isolated
  at runtime, this avoids adding a second, less-proven rendering dependency.
- **Exercise the BSD-3-clause option on the cburnett piece artwork**,
  explicitly, rather than the GFDL/CC-BY-SA options — this avoids
  share-alike/copyleft obligations on the artwork entirely, at the cost of
  retaining a copyright/attribution notice (to Colin M. L. Burnett, 2006),
  to be recorded in a `NOTICE`/`THIRD_PARTY_LICENSES` file once artwork is
  actually vendored into the repository.
- **The pedagogical viewport/cropping layer — arbitrary rank/file window
  crops via SVG `viewBox` math, key-square highlighting beyond what `fill`/
  `squares` already provide, arrow paths between arbitrary points (not just
  squares, for pawn-race lanes), and side-by-side before/after composition —
  is built as project-owned code** operating on the raw SVG output of the
  primitive above. This is the "Pedagogical View Specification → Renderer →
  SVG artifact" separation described in the bootstrap prompt: teaching
  intent (what to crop, highlight, compare) is a data structure the renderer
  consumes, not logic embedded in rendering code.
- **A generated board SVG is treated as the primitive's output, not as GPL
  code itself** — consistent with the FSF's general position that a
  program's output is not automatically covered by that program's license
  unless substantial program text is copied into the output (board
  coordinate/path data generated from a position is not "text copied from
  the program"). This is a reasoned, sourced position, not a certainty — see
  the gate below; the underlying FAQ quote was retrieved via a search-cache
  excerpt, not a direct fetch of the live page, because the live page
  rate-limited the research pass twice.

## Alternatives considered

- **Write a from-scratch SVG board renderer with self-drawn/geometric
  pieces**, avoiding any GPL dependency and the cburnett licensing question
  entirely. Rejected as the default: the licensing benefit is already
  captured by the BSD option above, so this alternative would only add real
  design/maintenance cost (owning piece-shape drawing) and arguably a worse
  learner experience (unfamiliar piece glyphs vs. the standard set widely
  recognized from lichess/Wikipedia) for no offsetting benefit. Left as a
  fallback if the isolation-boundary approach above is later judged
  insufficient for the project's MIT claim (see gate below).
- **Adopt a different, permissively-licensed FEN→SVG library instead.**
  Rejected: none found in the research pass are both (a) confirmed
  permissive by an actual `LICENSE` file (not just marketing/README text —
  one candidate, `chess-viewer-utils`, advertised itself as MIT but shipped
  an AGPL-3.0 `LICENSE` file, and was rejected specifically for that
  discrepancy) and (b) more capable than `chess.svg` for this project's
  needs. None support cropping either way, so switching primitives buys
  nothing on the one capability that actually matters most here.
- **Use lichess's `chessground`.** Rejected: GPL-3.0, client-side/browser
  widget, not a server-side SVG generator — wrong shape for this project's
  MCP/Markdown output regardless of license.

## Consequences

- Rendering code has a hard internal boundary: nothing outside the
  rendering-adapter module may import `python-chess`/`chess.svg` directly,
  and the adapter's own inputs/outputs must be plain data (FEN-like position
  representation, a pedagogical view-spec, resulting SVG string) — not
  `python-chess` objects — so the GPL surface stays contained and legible.
- The project takes on real, testable responsibility for cropping/annotation
  logic (SVG string/DOM manipulation) — bounded and deterministic, but not
  free.
- A `NOTICE`/`THIRD_PARTY_LICENSES` file recording the BSD-option exercise on
  the cburnett artwork is required once rendering code lands — tracked as a
  follow-up, not yet done (no rendering code exists at bootstrap time).
- **Open gate, not fully closed by this decision**: whether an adapter-module
  boundary is sufficient isolation for the project's actual MIT claim, versus
  requiring the stronger structural separation used for engine integration
  (separate optional-install process/subprocess rather than in-process
  import), is a licensing-risk-tolerance call, not a pure research question.
  This decision takes the adapter-boundary position as the working default;
  revisit with a superseding record if that tolerance is judged wrong once a
  firmer legal read (or a human with authority to accept the risk) weighs in.
- The GPL-FAQ "output isn't GPL" citation should be re-verified against the
  live `gnu.org/licenses/gpl-faq.html` page before this reasoning is relied
  on in anything more formal than internal architecture documentation.
