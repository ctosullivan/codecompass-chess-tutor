# 0003. Remote lichess tablebase API for MVP correctness; engine deferred and process-isolated if ever added

## Status

Accepted (2026-09-30).

## Context

The endgame core needs an authoritative source of "what is actually the
correct/winning continuation" for the bounded pawn-ending curriculum under
consideration (K+P vs K, opposition, key squares, pawn races, zugzwang).
These are exactly the positions Syzygy tablebases solve perfectly — Syzygy
covers positions with up to 7 pieces total (confirmed in
`docs/research/chess-engine-tablebase-licensing.md`), and the bounded
pawn-ending curriculum under consideration (K+P vs K is 3 pieces; the other
named endings stay similarly small) sits comfortably within that range with
room to spare. See `docs/research/chess-engine-tablebase-licensing.md`.

Three genuinely different things were researched: the tablebase *data*
itself, tablebase *probing code* (bundled GPL vs. standalone
permissive-in-effect), and a *remote hosted lookup service*
(`tablebase.lichess.ovh`). A full evaluation engine (Stockfish, GPL-3.0) is a
separate concern from tablebases and is not obviously required for this
bounded endgame scope at all — it becomes relevant later for a different
purpose (tactical-puzzle generation quality: rejecting a candidate puzzle
whose apparent theme is dominated by an unrelated, stronger tactic), not for
the endgame core.

## Decision

- **Default to the remote lichess public tablebase API**
  (`https://tablebase.lichess.ovh`, via the `lila-tablebase` service) for
  tablebase lookups in the MVP. No install, no local licensing exposure (it's
  a network call to a third-party hosted service, not a dependency this
  project redistributes). Standard good-citizen API norms apply: no
  authentication required, but cache results and don't hammer the service;
  a follow-up design note on rate-limit handling and an offline fallback is
  needed if daily-puzzle volume ever makes this a real constraint.
- **Local Syzygy tablebase files are an explicitly optional, later addition**
  — not part of the MVP — for offline use or higher volume than the remote
  API comfortably supports. If added, use standalone probing code (reported
  permissive-in-effect, not yet independently license-verified — see gate
  below) rather than the GPL probing module bundled in python-chess, to keep
  the local-tablebase path itself out of GPL entirely.
- **A full evaluation engine (Stockfish or equivalent) is deferred entirely**
  for the MVP. It is not part of the endgame core (tablebases cover that
  scope). If and when a concrete need is reached (tactical-puzzle
  dominant-tactic rejection), it must be integrated as an **optional,
  separately-installed, subprocess/UCI-only** component — never vendored,
  never imported in-process — mirroring the standard, low-risk pattern the
  wider chess-software ecosystem already uses to keep GUIs and tools that
  invoke GPL engines from becoming GPL themselves.

## Alternatives considered

- **Bundle local Syzygy tablebases from day one.** Rejected for the MVP:
  adds install/storage weight and a licensing surface (probing code) not yet
  needed when a zero-install remote API covers the bounded curriculum
  adequately.
- **Take a Stockfish dependency now, speculatively, for the endgame core.**
  Rejected: tablebases already solve this scope perfectly and more cheaply;
  taking an engine dependency before there's a concrete need it serves would
  be exactly the kind of speculative architecture the bootstrap prompt asks
  to avoid.
- **Use python-chess's bundled `chess.syzygy` module if local tablebases are
  ever added.** Rejected as the default for that future case specifically
  because it shares python-chess's GPL license; standalone probing code is
  preferred if/when this is revisited, subject to the verification gate
  below.

## Consequences

- The MVP has a hard external-network dependency for tablebase lookups
  unless/until local Syzygy files are added — acceptable for a learning tool
  used interactively, but worth flagging in `docs/architecture.md` as a known
  operational constraint (no fully offline mode yet).
- Engine integration is explicitly deferred, not designed yet. When it is
  designed, it inherits this decision's subprocess/UCI-only constraint by
  default; a genuine reason to deviate would need its own decision record.
- Open verification gates carried over from research, not yet closed: the
  Syzygy data license and standalone-probing-code license were not
  independently confirmed against a signed license file (community-consensus
  confidence only); re-verify before this project starts locally bundling
  either.
