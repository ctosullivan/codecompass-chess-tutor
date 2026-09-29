# Research: tactical-puzzle & master-game sources, and mechanical validation

Checked 2026-09-30. Sources are primary (project's own site/docs/LICENSE) unless
marked otherwise. This file is evidence for a licensing/architecture decision,
not the decision itself — see `decisions/` once one is written.

## Summary table

| Source | License / terms | Usable for MVP? |
|---|---|---|
| Lichess puzzle DB (`lichess_db_puzzle.csv.zst`, database.lichess.org) | **CC0 1.0** (public-domain dedication), stated directly on the export page | **Yes** — cleanest option, no attribution required (though giving it anyway is good practice) |
| Lichess games DB / Elite Database (nikonoel filter of lichess CC0 exports) | **CC0 1.0** (derivative of CC0 source, itself stated CC0 on lichess.org/team page and the mirror site) | **Yes**, for master-game-style strong-player games |
| Lichess evaluations DB (`lichess_db_eval.jsonl.zst`) | CC0 1.0, same export page | Yes, useful as pre-computed Stockfish evals if depth is sufficient |
| ChessBase Mega Database | Commercial, paid, per-seat activation-locked product (shop.chessbase.com) — no evidence of a redistribution/derivative-use license | **No** — rule out for MVP |
| chess.com Public API (PubAPI) + chess.com User Agreement | API is free for public data, but the User Agreement prohibits reproducing/exploiting "any portion of the Services" for commercial purposes; account/API use is "solely for personal, non-commercial use" | **Caveat / avoid for now** — ambiguous fit for a tool that redistributes derived puzzles; see gate below |
| `ornicar/lichess-puzzler` (Lichess's own puzzle generator+validator) | **AGPL-3.0** (per repo) | Not usable as a dependency (AGPL, and copyleft mismatch with MIT goal) — usable only as a **methodology reference**, not code |
| `vitogit/pgn-tactics-generator` | **MIT** | Usable as a methodology reference and, license-wise, potentially as a code reference/starting point |
| `Leo-Y-Zhang/ChessPuzzleForge` | **MIT** | Usable as a methodology reference (engine re-proves every answer) |

## 1. Lichess open puzzle database

Verified directly on **database.lichess.org**: "Database exports are released
under the [Creative Commons CC0 license]... Use them for research, commercial
purpose, publication, anything you like. You can download, modify and
redistribute them, without asking for permission." This applies to the puzzle
export (`lichess_db_puzzle.csv.zst`, ~6.1M puzzles with `PuzzleId, FEN, Moves,
Rating, Themes, GameUrl` columns), the games exports, and the Stockfish
evaluation export (`lichess_db_eval.jsonl.zst`, 409.7M positions).

CC0 means no attribution is legally required, but the project should credit
Lichess anyway as a courtesy and for provenance (this project's own evidence/
provenance principle — §5 of the bootstrap — argues for recording the source
even when not legally compelled to).

Source: https://database.lichess.org/

## 2. Lichess's own puzzle-generation methodology

The generator/validator pipeline lives at **github.com/ornicar/lichess-puzzler**,
licensed **AGPL-3.0**. Its own README describes the architecture only at a high
level: a *generator* that uses "stockfish and database.lichess.org to produce
puzzle candidates" (built on `python-chess` for the chess logic), and a
*validator* that "stores puzzle candidates and lets people review them with a
web UI" (backed by a MongoDB schema with `game id, FEN, moves, score, rating,
topics` fields).

Lichess does **not** publicly document, at the level of detail this project
would want to cite with confidence, the exact algorithm for (a) forced-line
detection or (b) rejecting a candidate whose apparent theme is dominated by an
unrelated stronger tactic. What is verifiable is that: engine analysis
(Stockfish) is central, `python-chess` provides legality/PGN handling, and a
**human validation step** (the web UI) is explicitly part of their pipeline —
i.e. Lichess does not rely on engine analysis alone before a puzzle reaches
players. That human-in-the-loop step is a meaningful data point for this
project's own "must not trust an LLM/engine output blindly" stance.

Because it's AGPL-3.0, `lichess-puzzler` cannot be adopted as a code dependency
of an MIT project without that project also becoming AGPL for at least that
component — treat it as a **methodology reference only**, not a library.

Source: https://github.com/ornicar/lichess-puzzler

## 3. Master-game corpora

- **Lichess Elite Database**: CC0-licensed (both the source Lichess exports
  and the elite-filtered derivative, per lichess.org/team/lichess-elite-database
  and the mirror at database.nikonoel.fr). It's games by strong players
  (2400+ vs 2200+, tightened to 2500+ vs 2300+ from Dec 2021), not "master"
  games in the classical database sense, but freely licensed and large
  (26.3M games at last check).
- **ChessBase Mega Database**: a commercial, paid, activation-locked product
  (shop.chessbase.com, newinchess.com). No evidence of any license permitting
  redistribution or derivative/educational-tool use was found; treat as
  **out of scope** for an MVP that needs a freely redistributable corpus.
  This is sufficient to rule it out without needing to chase down its exact
  EULA text — a paid, per-seat product is categorically the wrong shape for
  an open MVP regardless of exact clause wording.

## 4. chess.com data

Chess.com's own **User Agreement** (chess.com/legal/user-agreement) states
users agree not to "reproduce, duplicate, copy, sell, trade, resell or
exploit for any commercial purposes, any portion of the Services... or access
to the Services," and that API/account use is "solely for personal,
non-commercial use." Their Help Center confirms a public API (PubAPI) exists
for anonymous-accessible data, but scraping beyond that API is explicitly
against ToS, and they direct anyone building a member-facing app to contact
them directly rather than assume the PubAPI licenses that use.

This is genuinely restrictive for a tool that would ingest chess.com puzzles/
games and re-serve them as part of a redistributable, MIT-licensed learning
product. **Do not use chess.com data for MVP puzzle sourcing** without
explicit written permission — flagged below as a decision gate if the project
ever wants chess.com data specifically (e.g. for something Lichess doesn't
cover).

Source: https://www.chess.com/legal/user-agreement,
https://support.chess.com/en/articles/9650547-what-is-the-pubapi-and-how-do-i-use-it

## 5. Other corpora

No other clearly-licensed, well-known tactical-puzzle corpus surfaced beyond
Lichess's own exports during this pass. Several small open-source puzzle
*generators* exist (see below) but they are tools, not datasets, and mostly
consume Lichess/PGN data themselves. This project should default to Lichess's
CC0 exports rather than chase a secondary corpus without a clear gap.

## 6. Generated/modified positions — mechanical validation pipeline precedent

Three concrete open-source reference points, all consuming `python-chess` for
legality:

- **`vitogit/pgn-tactics-generator`** (**MIT**) — extracts candidate tactics
  from PGN games via engine analysis, with a documented `--strict` flag: "Use
  False to generate more tactics but a little more ambiguous." This confirms
  the pattern this project should use — an engine-score-gap/strictness
  threshold between the best move and the next-best alternative, used to
  reject ambiguous or multi-solution positions — though the README does not
  spell out the exact gap formula; the mechanism (a strictness toggle keyed to
  ambiguity) is the citable fact, not a specific numeric threshold.
- **`Leo-Y-Zhang/ChessPuzzleForge`** (**MIT**) — "each puzzle's solution is
  re-derived and re-checked by a bundled forced-mate search, so the tool
  cannot serve a 'mate in 1' that is not actually mate," and for material-
  winning tactics, "a fork is emitted only when an engine capture search
  PROVES the material win." This is a clean precedent for the "never trust a
  claimed solution — mechanically re-derive it" principle the bootstrap prompt
  asks for. It does **not**, per its own docs, explicitly filter out puzzles
  whose theme is dominated by an unrelated stronger tactic — that check (step
  4 in the pipeline below) has no clean off-the-shelf precedent found here and
  would need to be designed by this project.
- **`ornicar/lichess-puzzler`** (AGPL — reference only, not a dependency) —
  confirms the generator→engine-analysis→human-review shape at production
  scale, and that Lichess itself does not skip human review even with engine
  backing.

### Recommended pipeline shape (grounded in the above, not invented from nothing)

```
theme
  → candidate position (from Lichess CC0 games/puzzles, or a constructed/modified position)
  → legality check (python-chess or equivalent — see chess-engine-tablebase-licensing.md)
  → engine (and, for endgames, tablebase) analysis of best move + best alternative
  → reject if score gap between best and next-best move is below a strictness threshold
      (precedented by pgn-tactics-generator's --strict flag; exact threshold is
      this project's own parameter to tune, not something borrowed)
  → reject if the "winning" line is dominated by a stronger unrelated tactic
      not matching the intended theme (no off-the-shelf precedent found —
      this is this project's own thing to design, likely: run engine analysis,
      then independently check whether the intended-theme motif detector fires
      on the actual best line, not just on some line)
  → re-derive/re-check the full solution mechanically before ever presenting it
      (precedented by ChessPuzzleForge's re-proving approach)
  → learner-facing puzzle, tagged with source + validation method (provenance)
```

## Recommendation

Start the MVP entirely on **Lichess's CC0 exports** (puzzle DB for sourced
puzzles, Elite Database or standard game exports for master-game-derived
positions, eval DB as an optional pre-computed hint). This needs zero
licensing negotiation, is legally the cleanest option found, and is large
enough (6.1M puzzles) to support a "daily thematic set" MVP without needing
generation at all for v1 — **generation/modification of positions can be a
later phase**, once selection-only is working, rather than a day-one
requirement. Do not use chess.com data or ChessBase Mega Database. Credit
Lichess in documentation even though CC0 doesn't require it.

For any future generated/modified positions, build validation around
`python-chess` (or the equivalent chosen in the engine/tablebase research) +
engine score-gap thresholding (precedented pattern) + a from-scratch
"dominant unrelated tactic" check (no precedent found — must be designed) +
mechanical re-derivation before serving (precedented pattern), never trusting
a generation step's own claimed solution.

## Open uncertainty / human decision gate

- **chess.com data**: if a future phase wants chess.com-sourced puzzles/games
  specifically, that requires either explicit written permission from
  chess.com or a legal read of whether "public API" use for a non-commercial,
  redistributable open project is distinguishable from the ToS's commercial-
  exploitation language. Not resolved here — flag as a gate, don't guess.
- **Exact score-gap threshold** for rejecting ambiguous tactics, and the
  design of the "dominant unrelated tactic" rejection check, have no
  authoritative off-the-shelf answer — these are this project's own design
  work in the tactical-puzzle-model phase, informed by but not copied from
  the precedents above.
- **Confidence**: high on all license findings (each checked against the
  source's own page/file); medium on "no better-documented theme-purity
  algorithm exists publicly" — it's possible Lichess has an internal
  algorithm not reflected in the public repo's README; this file only claims
  what's actually visible in `ornicar/lichess-puzzler`'s public documentation.
