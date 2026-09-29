# Project context

This file reflects the *current* state of the project — overwrite the
section below at each stopping point rather than appending to it. History
belongs in git log and `planning/retros/`, not here.

## Current state

Bootstrap phase (roadmap item 1) is in progress. The initial
codecompass-template-adapted structure (this file, `CLAUDE.md`,
`planning/ROADMAP.md`, `decisions/`, `planning/retros|knowledge|context-gaps/`,
`planning/prompts/`, `vendor.toml`, `.gitignore`) has been created and
committed. Five parallel research passes into `docs/research/` are
underway/complete, covering: chess engine/tablebase licensing, tactical
puzzle dataset licensing and validation, MCP SDK/protocol and language
choice, board rendering options, and Obsidian integration/learner storage.

Next: once all five research documents have landed, synthesize them into
`docs/architecture.md`, write the ADRs they justify (language/SDK choice,
chess-rules/engine/tablebase licensing boundary, board-rendering
build-vs-dependency, puzzle sourcing/validation, learner-storage/Obsidian
boundary, and the overall project license), write `README.md`, add `LICENSE`
if the evidence supports MIT cleanly, run an independent review against the
bootstrap prompt's "definition of success" question list, fix anything
material, then commit and push.

## Known gaps / rough edges

- No code exists yet — this is intentionally a research-and-architecture-only
  bootstrap, per `planning/prompts/0001-project-bootstrap.md`.
- Several research documents in `docs/research/` flag their own open
  uncertainties (things that couldn't be authoritatively verified in one
  pass, e.g. a live source page that returned a rate-limit error). Those are
  human decision gates, not settled facts — see each document's own "Open
  uncertainty" section, and `decisions/` for which ones got resolved into an
  actual ADR versus left open.
