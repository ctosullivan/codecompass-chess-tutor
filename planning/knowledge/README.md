# Knowledge

A lightweight log of things learned while working on this project — distinct
from `decisions/` (which records a specific choice made) and from
`planning/context-gaps/` (which records a specific missing piece of context,
see that directory's own `README.md`).

## The lifecycle

1. **Candidate** — something you noticed, written down with enough detail
   (what happened, what the evidence was, why it seemed worth noting) that
   someone else could evaluate it without having been there.
2. **Reviewed** — at a natural point (closing out a piece of work, noticing a
   pattern a second time), look back over recent candidates and decide, for
   each one:
   - **Promote** it — turn it into something durable: a test that would have
     caught the problem, a line in `docs/architecture.md`, a rule in
     `CLAUDE.md`, a new roadmap item. Once promoted, the candidate's job is
     done — the durable artifact is what matters going forward, not the log
     entry.
   - **Retain** it — genuinely useful context, but not yet ready to become a
     permanent rule (maybe it's only happened once, and you want to see if it
     recurs before treating it as a real pattern).
   - **Discard** it — on reflection, not actually generalizable, or already
     covered by something else.

## What belongs here

Something you'd want a future version of yourself (or a teammate) to know
before repeating a mistake, or before re-discovering something that worked
well. Concrete and specific, not a vague impression — for this project, that
might include things like "the lichess puzzle CSV's `Themes` column uses
space-separated tags, not the human-readable theme names" or "python-chess's
SAN parser rejects X" — not "chess libraries can be tricky."

## Format

A short entry per candidate: what happened, the evidence, why it seems worth
keeping, and (once reviewed) what happened to it. Keep entries in one running
file or one-file-per-candidate, whichever suits how much volume this project
actually generates — this doesn't prescribe which.
