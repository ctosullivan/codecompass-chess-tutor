---
status: open
found_during: Phase 2A CodeCompass dogfooding (planning/ROADMAP.md)
---

# Gap: `codecompass query symbol` doesn't cover method-level symbols

**What I was trying to do**: while writing `src/chess_tutor/chess_state.py`,
I wanted to confirm what exception `python-chess`'s `Board.push_uci()` and
`Board.push_san()` raise for an illegal move, to decide what
`chess_tutor.chess_state.IllegalMoveError` should wrap. `python-chess` is
tracked in `vendor.toml` and had already been synced
(`.venv/bin/codecompass sync --budget 0`), so I tried the tool first:
`codecompass query symbol push_uci`.

**What I expected to find**: either the method's own docstring/signature,
or at least a pointer to the class it belongs to.

**What I actually found**: `no symbol named 'push_uci' found in
context-graph.db`. Following up with `codecompass query symbol Board`
returned `Board`'s own class-level docstring (a long one, 95 lines
rendered) but never mentions `push_uci` by name — the class-level symbol
entry doesn't enumerate its methods. Grepping the generated digest
artifacts directly (`vendor/chess/*.md`, `vendor/chess/*.json`) for
`push_uci` found nothing either. The only place `push_uci` actually
appears is the raw cloned source CodeCompass keeps at
`vendor/chess/src/__init__.py` (confirmed via `grep -n "def push_uci"` —
found at line 3271), which is a real, usable fallback, but not something
`query symbol` surfaces or points to.

**What this means in practice**: `codecompass query symbol` indexes
class/module/exception-level symbols (confirmed: `AmbiguousMoveError`,
`Board`, `BaseBoard`, etc. all appear with real docstrings), not individual
methods. For a method-level question, the working path is to query the
*class* the method belongs to (to confirm it exists at all and get
class-level context), then read the raw source directly under
`vendor/<name>/src/` — not to query the method name itself, which silently
returns "not found" rather than a hint to try the containing class or the
raw source.

**Resolution used for this task**: verified `push_uci`/`push_san`'s actual
exception-raising behavior empirically, by running python-chess directly
in a scratch interpreter (`chess.IllegalMoveError`, `chess.InvalidMoveError`,
`chess.AmbiguousMoveError`, all `ValueError` subclasses — see
`src/chess_tutor/chess_state.py`'s own comment on this). CodeCompass's
context did not block the work, but it also didn't answer the actual
question asked; the source-of-truth here ended up being direct empirical
verification, same practice as `planning/retros/0002-gpl-relicensing.md`'s
"fetch canonical text directly, don't trust memory or an intermediate
summary" lesson.

**Not filed as a knowledge-log rule yet** — one occurrence. Worth
promoting to a documented habit ("query the containing class, and fall
back to `vendor/<name>/src/` directly for method-level questions") if this
recurs on a later phase.
