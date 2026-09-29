# Context gaps

A log of places where the context available to you — from CodeCompass, from
this project's own documentation, or from anywhere else — turned out to be
missing, wrong, or misleading for a real task you were doing.

This is deliberately narrower than `planning/knowledge/`'s general learnings
log: an entry here is specifically about *context that should have existed
but didn't*, not about "how we should work" observations (those belong in
`planning/knowledge/` instead).

## What belongs here

- A real dependency CodeCompass (or another tool) doesn't seem to know about,
  or knows about incorrectly.
- A relationship between two things in this project (a doc and the code it
  describes, one module and another) that had to be worked out by hand
  because nothing surfaced it.
- Context that was present but actively misleading — stale, or describing an
  earlier version of something that has since changed.
- For this project specifically: a licensing or provenance claim in
  `docs/research/` that later turned out to be wrong or outdated — those
  research documents are dated evidence snapshots, not living truth, and a
  gap between what they say and current reality belongs here.

## What doesn't belong here

- A straightforward bug in this project's own code (that's just a bug — file
  it wherever this project tracks bugs).
- A feature request for how a tool renders output, as opposed to what it
  knows.
- Anything that a fresh `codecompass sync` would simply fix — that's a
  freshness problem, not a genuine gap, and doesn't need a permanent record.

## What to do with an entry

Write down what you were trying to do, what context you expected to find, and
what you actually found (or didn't). If the same kind of gap shows up a
second time, independently, that's a real signal — worth raising as something
to actually fix, rather than working around silently every time it recurs.
