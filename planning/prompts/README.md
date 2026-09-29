# Prompts

A record of the substantial prompts that initiated or materially redirected a
phase of work on this project — provenance, not current-state documentation.

## Why this exists

The project's *current* state lives in `CLAUDE.md`, `docs/architecture.md`,
`decisions/`, and `planning/ROADMAP.md` / `planning/CONTEXT.md`. Those describe
what's true now. This directory instead preserves *why work happened when it
did*: the actual wording a human (or a lead orchestrator acting on a human's
behalf) used to direct a phase of work, at the time they wrote it.

This matters for a project developed largely through instructions to an AI
agent: the instructions themselves are part of the historical record, and
paraphrasing them after the fact loses information — tone, emphasis, what was
explicitly left open versus decided, what was asked for but not delivered.

## What belongs here

Every substantial prompt that **initiates or materially redirects** a phase of
project work. Not every message in every session — routine follow-ups,
clarifying questions, and small corrections don't need their own record. A
prompt belongs here when it sets or changes direction for a meaningful chunk
of work (a new phase, a scope change, a reversal of an earlier instruction).

## Rules

- **Verbatim.** The prompt's body is quoted exactly as given — no rewriting,
  shortening, or "cleaning up." Typos and all.
- **Append-only.** Once recorded, a prompt file's quoted body is never edited.
  If a later prompt supersedes or redirects an earlier one, record the new
  prompt in its own file and note the relationship (in the new file, and as a
  short added note — not a rewrite — in the old one's metadata section).
- **Numbered sequentially**, `NNNN-short-slug.md`, in the order they were
  received.
- **Minimal metadata outside the quoted body**: date, a one-line statement of
  purpose, and the phase/commit(s) that resulted, where useful. This metadata
  can be corrected or extended later (e.g. to add "superseded by 0004"); the
  quoted prompt body itself cannot.

## What this is not

Not a session transcript, not a changelog, not a substitute for
`planning/CONTEXT.md` or `decisions/`. A reader wanting to know the project's
current state should go there first; this directory is for a reader asking
"why did this phase of work happen, and what exactly was asked for."
