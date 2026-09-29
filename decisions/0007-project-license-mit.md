# 0007. License this project MIT

## Status

Accepted (2026-09-30).

## Context

The bootstrap prompt's preferred license was MIT, conditional on dependency
research actually supporting it rather than assuming it. Five research
passes (`docs/research/*.md`) and five prior decisions (`0001`–`0006`)
examined every category of likely dependency the prompt asked about: chess
libraries/engines/tablebases, MCP SDKs, board-rendering/diagram libraries
and their bundled artwork, and tactical-puzzle/master-game data sources.

The recurring finding across all five areas: **every GPL/AGPL-licensed
component found (python-chess, Stockfish, lichess's chessground,
lichess-puzzler) has a credible isolation strategy** (dev-time-only use,
subprocess/UCI arm's-length invocation, an adapter-module boundary, or
"methodology reference, not dependency") that keeps it from being combined
into this project's own distributed source. The one clearly permissive
option among piece artwork (BSD-3-clause, one of cburnett's four offered
licenses) was found and adopted. The one clean, zero-friction data source
(Lichess's CC0 exports) was found and adopted, ruling out the two
problematic ones (chess.com ToS, ChessBase's commercial terms) without
needing them.

## Decision

**This project is licensed MIT**, on the strength of `0001`–`0006`'s
isolation strategies holding: no GPL/AGPL-licensed code is imported
in-process into this project's own distributed source; any GPL component
used at all (python-chess dev-time or process-isolated per `0002`;
Stockfish subprocess-only per `0003`; `chess.svg` behind a rendering-adapter
per `0004`) is isolated behind a boundary consistent with how the wider
chess-software ecosystem already treats exactly this kind of dependency;
piece artwork is used under its BSD option (`0004`); puzzle/game data is
CC0 (`0006`); CodeCompass itself (GPL-3.0-or-later) is a development-only
tool never imported by runtime code (`CLAUDE.md` §8, `docs/architecture.md`).
The `LICENSE` file (MIT, matching `codecompass-template`'s own license text)
is added in this same bootstrap.

## Alternatives considered

- **License the project GPL-3.0**, matching python-chess/Stockfish/
  CodeCompass and sidestepping the isolation-boundary question entirely.
  Rejected: the bootstrap prompt's explicit preference is MIT, and the
  isolation strategies in `0001`–`0006` make MIT achievable without giving
  up any dependency this project actually needs — there was no forcing
  function to accept the more restrictive license.
- **Defer the license decision entirely**, leaving the repository unlicensed
  until implementation reveals whether the isolation boundaries hold up in
  practice. Rejected: the research is specific and consistent enough across
  all five areas to support a defensible decision now, consistent with the
  bootstrap prompt's own instruction ("if the dependency review supports
  MIT, add the MIT license"). The open gates below are real, but each is a
  narrow verification task, not a reason to withhold the license entirely.

## Consequences

- **This decision rests on isolation boundaries that are not yet built.** No
  runtime code exists yet (this is a bootstrap). Each future implementation
  phase that touches a GPL-adjacent area (`0002`'s validator, `0003`'s engine
  integration, `0004`'s rendering adapter) must actually honor its decision's
  isolation boundary — an in-process `import chess` slipped into the runtime
  by a future change would quietly invalidate this decision's reasoning
  without anyone necessarily noticing at review time. `CLAUDE.md` §7's
  independent-review requirement for consequential architecture work is the
  intended safeguard; this should be treated as a standing thing to check,
  not a one-time bootstrap concern.
- **Open verification gates carried forward from research, none of which are
  believed likely to overturn this decision, but none fully closed either:**
  - The FSF GPL FAQ's exact current wording (on library-linking and on
    program-output licensing) was not re-fetched verbatim in research
    (rate-limited both times it was attempted) — re-verify against
    `gnu.org/licenses/gpl-faq.html` directly before relying on this
    project's GPL-isolation reasoning in anything more formal than internal
    architecture documentation.
  - Syzygy tablebase data/probing-code licenses were not independently
    confirmed against a signed license file (community-consensus confidence
    only) — only relevant if/when local tablebases are ever added (`0003`).
  - Whether an adapter-module boundary (vs. a stronger subprocess boundary)
    is sufficient isolation for `0004`'s rendering dependency is flagged in
    that decision as a licensing-risk-tolerance call, not fully closed.
  - The TypeScript MCP SDK's license was reported low-confidence and never
    mattered to this decision since Python was chosen (`0001`) — noted only
    for completeness.
- If any of the above verification steps later surface a real problem, the
  fix is a **new, superseding decision record** (isolate more strongly,
  swap a dependency, or reconsider the license) — not a silent edit to this
  one.
