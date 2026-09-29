# 0005. Direct filesystem vault access, dedicated subfolder, SQLite as a regenerable evidence index

## Status

Accepted (2026-09-30).

## Context

The learner must retain ownership of their learning material: the vault
should stay ordinary portable Markdown, not become dependent on a
proprietary database as its sole source of truth, and the tutor is
explicitly not an Obsidian plugin — it must work whether or not Obsidian is
even installed. See
`docs/research/obsidian-integration-and-learner-storage.md`.

Obsidian's own vault format is confirmed portable (plain Markdown files plus
a `.obsidian/` config folder that is off-limits to external tools). Two
existing precedents were found: `obsidian-spaced-repetition` (MIT), which
embeds review-scheduling state as inline HTML comments directly in notes;
and `obsidian-local-rest-api` (MIT), a *plugin* exposing a local REST API and
built-in MCP server for external processes — but that requires Obsidian to
be running with the plugin installed, a materially different integration
shape than this project's "works with a folder on disk" requirement.

Two genuinely different kinds of state exist: the learner's own qualitative
notes (must stay in the vault as plain Markdown), and the tutor's own
structured evidence/learner-model state (concepts encountered, puzzle
history, error classifications, spaced-review scheduling) which needs real
querying ("what's due for review," "what's recently been failed") that plain
frontmatter handles poorly at volume.

## Decision

- **The MVP accesses the vault directly as a folder on disk** — no
  dependency on Obsidian running or on `obsidian-local-rest-api` — via the
  single fixed vault-root + path-resolution-helper pattern established in
  `decisions/0001-python-and-official-mcp-sdk.md`.
- **All tutor-generated artifacts (diagrams, generated puzzle-set notes,
  etc.) are written to a dedicated, clearly-named subfolder** at a
  learner-configurable path (default e.g. `CodeCompassChessTutor/`) —
  never interleaved with the learner's own notes, and `.obsidian/` is never
  touched.
- **The MVP does not rewrite the learner's existing notes.** It reads them
  (for "current study" context) but does not perform wholesale rewrites; if
  a future need requires adding tutor-relevant frontmatter to an
  learner-owned note, that edit must be surgical (parse and preserve all
  existing keys, add/update only a single namespaced key, e.g. under a
  `codecompass` key) — not attempted in the MVP.
- **Writes use write-then-rename for atomicity** (temp file in the same
  directory, atomic rename over the target) to avoid Obsidian's file watcher
  ever observing a half-written file.
- **The tutor's own structured learner-evidence state lives in a small,
  project-owned SQLite file**, inside the tutor's vault subfolder (or
  configurably outside it), treated as a regenerable working index — not
  the learner's only copy of anything meaningful. This mirrors the boundary
  CodeCompass itself draws for `context-graph.db`: a tool-owned artifact
  safe to delete and rebuild, not something migration/versioning needs to
  preserve perfectly at this stage. Human-readable derived summaries the
  tutor generates from it (e.g. "your puzzle history this week") may be
  rendered out to Markdown in the tutor's subfolder, clearly marked as
  generated, but SQLite remains the queryable source for the tutor's own
  operation.
- **`obsidian-local-rest-api` integration is explicitly deferred to
  post-MVP**, as an optional, richer integration path for learners who
  already run Obsidian with that plugin (real-time updates, safer
  partial-PATCH edits) — not required, and not built, for the MVP.

## Alternatives considered

- **Depend on `obsidian-local-rest-api` (even optionally) for the MVP.**
  Rejected for MVP: requires Obsidian running plus a plugin install plus a
  network hop, which conflicts with "usable without extra Obsidian plugins."
  Left open as a credible post-MVP addition, not dismissed permanently.
- **Store learner-evidence state as inline HTML comments per note**
  (the `obsidian-spaced-repetition` pattern). Rejected as the primary store:
  that approach requires re-parsing every note for any bulk query and was
  judged a worse fit than SQLite for the querying this project's learner
  model actually needs (spaced review due-dates, cross-concept transfer
  evidence), though it remains a reasonable pattern to reuse for narrow,
  single-note-scoped state if that need arises later.
- **Store all learner-model state as vault frontmatter.** Rejected: property
  types are effectively vault-global per key name (Obsidian's own docs), and
  frontmatter has no real query engine — workable for a handful of
  learner-visible tags, not for the tutor's own operational state.
- **A general-purpose external database (not SQLite)**, e.g. a client-server
  DB. Rejected: unjustified operational weight for a single-learner local
  tool; SQLite gives real querying with zero install/service footprint.

## Consequences

- The tutor has a genuine, if believed-low-risk, unresolved question: true
  concurrent-write safety with a live Obsidian instance editing the exact
  same file has not been empirically validated (Obsidian's and
  `obsidian-local-rest-api`'s own docs don't fully specify this). The
  mitigation (tutor writes only to its own subfolder) is expected to make
  this a non-issue in practice, but this should be validated empirically
  before the tutor is ever given write access outside its own subfolder.
- SQLite becomes a real dependency of the tutor's own runtime (not GPL,
  not a licensing concern — noted here only as an architectural commitment).
  Its schema should be designed from the start to remain regenerable from
  other sources of truth (the vault's Markdown, the tutor's own puzzle/
  position data) rather than accumulating learner data with no other
  record — even though building the actual reconstruction path is not
  required for the MVP.
- Post-MVP `obsidian-local-rest-api` integration, if pursued, would need its
  own decision record (a new ADR, not an edit to this one) once evaluated
  against real learner demand.
