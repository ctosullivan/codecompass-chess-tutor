# Decisions

Architecture decision records (ADRs) — one file per significant, non-obvious
tradeoff, numbered sequentially starting from `0001`.

## Why bother

A decision record isn't a design doc. It exists so that six months from now,
when someone (possibly you) wonders "why did we do it this way instead of the
obviously simpler alternative," the answer is written down instead of having
to be reconstructed from a commit message or a half-remembered conversation.

## What belongs here

A record for any choice where a reasonable person could have picked
differently, and the reasoning for picking what you picked is worth
preserving. Not every change needs one — a straightforward bug fix or an
obviously-correct implementation doesn't. If you're not sure, a quick test:
could someone later look at the code and reasonably ask "why not the other
way?" If yes, write it down.

For this project specifically, licensing boundaries (what's a runtime
dependency vs. an isolated/optional GPL component vs. a dev-only tool),
build-vs-dependency calls (e.g. board rendering), and anything that fixes a
human decision gate raised during research all belong here.

## Format

Use `TEMPLATE.md` as a starting shape: Status, Context, Decision,
Alternatives considered, Consequences. Keep it short — a page is usually
plenty.

## Append-only

Once written, a decision record's own original content is never edited. If a
decision is later reversed or superseded, write a **new**, higher-numbered
record that says so explicitly (e.g. "`0007` is superseded by this record") —
the old one stays exactly as it was, now readable as history rather than
current truth. This preserves an honest trail: you can always see not just
what's true now, but what was believed true at each point along the way, and
why it changed.

Decisions are distinct from `planning/prompts/` (which preserves the
*instructions* that directed work) — a decision record captures the *outcome
and reasoning*, and may be informed by several prompts and by research in
`docs/research/`.
