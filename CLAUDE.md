# CLAUDE.md

This file governs how work on this project proceeds. If it disagrees with
anything else, it wins.

## 1. Plan before implementing

Before starting any non-trivial piece of work, write a short plan describing
what you intend to do, what's explicitly out of scope, and how you'll know
it's actually done. For a genuinely small change (a typo, a one-line config
fix), skip this — use judgment, and if in doubt, write the short plan anyway.

If planning surfaces a real, unresolved question only a human can answer,
stop and ask before proceeding, rather than guessing and moving on. Record it
as a human decision gate in the relevant document (an ADR under `decisions/`,
or `docs/architecture.md`) rather than letting it live only in
conversation.

## 2. Evidence before architecture

Before committing to a non-obvious dependency, license position, or
build-vs-buy call, write down what you actually verified and where
(`docs/research/`), not what seemed likely. Cite primary/authoritative
sources. If something can't be verified, say so plainly and treat it as an
open gate rather than filling it in with a plausible guess — see
`decisions/README.md` and the Licensing section of `docs/architecture.md`.

## 3. Keep documentation in sync, same change

When a change affects `docs/architecture.md`, a decision recorded under
`decisions/`, or anything else described elsewhere in this project, update
that description in the same change — not as a follow-up "when I get to it"
item. Documentation that describes the current system should never describe
a past version of it.

## 4. Record real decisions

When a change involves a non-obvious tradeoff — a choice that isn't simply
"the only reasonable option" — write a short decision record under
`decisions/` (see `decisions/README.md` for the format). Decision records are
append-only: if a past decision is later reversed, write a new one that
supersedes it; don't edit the old one's own content.

## 5. Keep a running context file

`planning/CONTEXT.md` should always reflect the current state of the
project: what's being worked on, what was just finished, what's next.
Overwrite its current-state section at each stopping point — don't let it
grow into an undifferentiated history. `planning/ROADMAP.md` is the
at-a-glance table of what's done, in progress, or planned; keep the two in
agreement.

## 6. Preserve prompt provenance

A substantial prompt that initiates or materially redirects a phase of work
gets recorded verbatim under `planning/prompts/` (see that directory's
`README.md`) — not paraphrased, not cleaned up. This is separate from, and
does not replace, `decisions/` or `planning/CONTEXT.md`.

## 7. Independent review for consequential work

Architecture-level decisions (a new dependency boundary, a licensing
position, a data-flow that crosses the chess-truth/AI-explanation line) and
any implementation phase materially larger than a single small change should
get an independent review pass — a fresh reading against
`docs/architecture.md` and the relevant ADRs, ideally by an agent that didn't
do the original work — before being considered done. Note the review, and
any resulting fixes, in the relevant `planning/retros/` entry.

## 8. CodeCompass is a development tool, not a product dependency

This project may use CodeCompass (`codecompass-context`) during development
for dependency/source context — see `vendor.toml` and
`docs/architecture.md`. Runtime/production code must never import or depend
on CodeCompass. Anyone must be able to clone, install, test, and run this
project's own tutor without CodeCompass installed. This is a deployability
rule, not a licensing one — it would hold regardless of what license either
project carries (they currently both happen to be GPL-3.0-or-later; see
`docs/architecture.md`'s "On this project's relationship to CodeCompass" and
`decisions/0010`).

## 9. Small process, added to only when justified

Start from the lead orchestrator plus bounded, single-purpose research or
implementation subagents. Don't stand up a permanent specialist-agent roster
speculatively — add a stable role only after repeated work has actually
demonstrated it's needed (see `docs/architecture.md`'s note on this, and
compare against CodeCompass's own much larger accumulated agent roster,
which reflects that project's different age and scale, not a template to
copy from day one).

## 10. Commits

One logical change per commit, with a message that says what changed and
why. Don't hold unrelated changes for a single large commit. Don't
force-push, rewrite shared history, or skip commit hooks without being
explicitly asked to.
