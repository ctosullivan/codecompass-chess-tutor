# Research: Obsidian vault integration and learner-evidence storage

Checked 2026-09-30. Sources are Obsidian's own official help docs and the
source repos/docs of two widely-used, actively-maintained community
plugins, cited inline. This document is evidence for an architecture
decision, not the decision itself — see `decisions/` for the resulting
ADR(s).

## Summary table

| Mechanism / precedent | What it does | License | Relevance here |
|---|---|---|---|
| Obsidian vault format ([obsidian.md/help](https://obsidian.md/help/Files+and+folders/How+Obsidian+stores+data)) | Vault = plain folder of Markdown files + subfolders; hidden `.obsidian/` holds app config (hotkeys, themes, workspace layout); some transient UI state also cached in IndexedDB | N/A (Obsidian app itself is proprietary/freemium; vault *content format* is open) | Confirms note content is portable plain text — supports "learner retains ownership" requirement |
| Obsidian Properties/frontmatter ([obsidian.md/help](https://obsidian.md/help/Editing+and+formatting/Properties)) | YAML frontmatter block (`---`) at top of a note; 7 typed property kinds (text, list, number, checkbox, date, datetime, tags) | N/A | Defines the safe, native metadata channel a well-behaved external tool should write into |
| **obsidian-spaced-repetition** plugin ([st3v3nmw/obsidian-spaced-repetition](https://github.com/st3v3nmw/obsidian-spaced-repetition), [docs](https://stephenmwangi.com/obsidian-spaced-repetition/)) | Closest functional precedent: per-flashcard/per-note spaced-review scheduling embedded directly in the Markdown file | MIT ([LICENSE](https://raw.githubusercontent.com/st3v3nmw/obsidian-spaced-repetition/master/LICENSE), Stephen Mwangi, 2021–2024) | Precedent for "learning-progress state living in the vault itself," and for *which* storage layer (frontmatter vs. inline) a mature plugin actually chose |
| **obsidian-local-rest-api** plugin ([coddingtonbear/obsidian-local-rest-api](https://github.com/coddingtonbear/obsidian-local-rest-api)) | Obsidian plugin exposing an authenticated local HTTPS REST API *and, as of recent versions, a built-in MCP server at `/mcp/`* for external processes to read/write the live vault through Obsidian itself | MIT ([LICENSE](https://raw.githubusercontent.com/coddingtonbear/obsidian-local-rest-api/master/LICENSE), Adam Coddington, 2023) | Closest precedent for "external process ↔ live vault," but requires Obsidian to be running and the plugin installed — a materially different integration shape than direct filesystem access |
| Derivative MCP wrappers (`mcp-obsidian`, `obsidian-mcp-server`, etc. — see search results below) | Multiple independent MCP servers built on top of `obsidian-local-rest-api` | Varies (mostly MIT-style; not verified individually) | Confirms "Obsidian + MCP" is already a populated ecosystem niche, not a novel idea — worth scanning before building a bespoke vault adapter |

## 1. Vault format and portability

Per Obsidian's own docs: notes are "Markdown-formatted plain text files in
a vault," where a vault is "a folder on your local file system, including
any subfolders." Because of this, "you can use other text editors and
file managers to edit and manage notes." A hidden `.obsidian/` folder at
the vault root holds app/vault configuration (hotkeys, themes, community
plugin settings, `workspace.json`/`workspaces.json` for layout) — this is
Obsidian's own state, not learner content, and an external tool must
treat it as off-limits. Obsidian also caches some transient
metadata/session state in IndexedDB, which is irrelevant to files on
disk and not something an external process needs to interact with.
[Source](https://obsidian.md/help/Files+and+folders/How+Obsidian+stores+data),
checked 2026-09-30.

**Conclusion:** note *content* is genuinely portable (plain Markdown);
the *application* is proprietary/freemium but does not lock in the data.
This directly supports the project requirement that the learner owns
their material independent of any specific tool, including this tutor.

## 2. Frontmatter/properties conventions

Obsidian stores structured metadata as YAML frontmatter delimited by
`---` at the top of a file. Property names must be unique per note;
order doesn't matter. Seven typed kinds exist (text, list, number,
checkbox, date `YYYY-MM-DD`, date&time `YYYY-MM-DDTHH:MM:SS`, and the
special `tags` list type) and *all properties sharing a name across the
vault share one type* — i.e. type is effectively vault-global per key,
not per-file. Obsidian's own docs explicitly bless external editing:
"bulk-editing tools like VSCode, scripts, and community plugins" are the
suggested route for programmatic property edits, and JSON-shaped
frontmatter is accepted on write but is always normalized to YAML on
save. [Source](https://obsidian.md/help/Editing+and+formatting/Properties),
checked 2026-09-30.

**Implication for a well-behaved external writer:**
- Only ever add/update well-namespaced keys (e.g. a single `codecompass:`
  nested key, or a small flat set of clearly-prefixed keys) — never
  reuse a generic key name the learner might already be using for
  something else, since type is vault-global per key name.
- Never touch `.obsidian/`.
- Preserve any existing frontmatter keys/values verbatim when rewriting
  a file's frontmatter block; a naive "regenerate the whole file"
  approach risks clobbering the learner's own properties.
- Prefer a dedicated subfolder for tool-generated content over
  interleaving with arbitrary learner notes (see Recommendation).

## 3. Precedent: obsidian-spaced-repetition

This plugin is the closest functional analogue to "a tool that tracks
per-item learning/review state inside a learner's own vault." Its own
documentation states scheduling info is stored as an **inline HTML
comment embedded directly in the Markdown file**, next to the
flashcard/note content it applies to — not in frontmatter, and not in a
separate plugin data file, for the per-card case.
[Docs](https://stephenmwangi.com/obsidian-spaced-repetition/), checked
2026-09-30 (exact wording: "The plugin stores scheduling info within
this HTML comment").

This is a real, shipped precedent for embedding learning-progress state
*inside* the learner's own note, keeping single-file portability, at the
cost of that state being somewhat opaque/fragile to hand-editing and not
easily queryable in bulk without re-parsing every note. It is MIT
licensed, so its approach can be studied and adapted freely, though this
project should design its own schema rather than reusing its exact
comment format.

## 4. External-process vault access: obsidian-local-rest-api

`obsidian-local-rest-api` is an Obsidian **plugin** (i.e. it only works
while Obsidian is running with the plugin installed and enabled) that
exposes a local, certificate-secured, API-key-authenticated HTTPS REST
API, and — in current versions — a **built-in MCP server at `/mcp/`**
specifically so "AI agents and MCP-compatible clients can interact with
your vault without hand-crafting HTTP requests." It supports full
CRUD on notes/attachments, targeted PATCH edits to specific headings,
block references, or frontmatter fields, full-text/structured search,
event streaming (SSE) for vault changes, and optimistic concurrency via
an `ifMatch` parameter carrying a prior document version.
[Source](https://github.com/coddingtonbear/obsidian-local-rest-api),
checked 2026-09-30. MIT licensed. A live ecosystem of thin MCP wrappers
around it already exists (`mcp-obsidian`, `obsidian-mcp-server`,
`obsidian-mcp-rest`, and others found via GitHub search, 2026-09-30),
confirming "MCP talks to Obsidian via this plugin" is a populated,
non-novel pattern.

**Important distinction for this project:** the bootstrap brief is
explicit that the chess tutor is *not* an Obsidian plugin — it should
work with the vault as an ordinary folder on disk, usable whether or not
Obsidian is even installed. `obsidian-local-rest-api` is a plugin-based
integration route (requires Obsidian running + plugin installed +
network round-trip) and is therefore **not** the primary integration
mechanism for this project's MVP. It is, however, a credible **optional,
richer integration** for a learner who already runs Obsidian with that
plugin (e.g. real-time SSE updates, safer PATCH-based partial edits,
built-in MCP surface reusable directly) — worth revisiting post-MVP
rather than building now.

Its own documentation does not fully specify safe-write behavior when
Obsidian is *simultaneously* editing the same file live (it only
describes optimistic concurrency via `ifMatch`, not what happens under a
true race). This is a genuine open question, not something resolvable
from docs alone — see the human-decision-gate section below.

## 5. Direct-filesystem write pattern for this project's MVP

Given the tutor is a standalone process/MCP server reading and writing
vault files directly (no plugin, no REST API dependency for MVP), the
realistic safe-write pattern, informed by (1)-(4) above plus ordinary
POSIX file-safety practice:

- **Never write inside `.obsidian/`.** That's Obsidian's own state.
- **Use a dedicated, clearly-named subfolder** for all tutor-generated
  artifacts (e.g. `CodeCompassChessTutor/` at the vault root, or a
  learner-configurable path) so tool output is trivially distinguishable
  from — and never interleaved with — the learner's own notes. The
  learner's pre-existing notes are read (for "current study" context)
  but never rewritten wholesale by the tool.
- **Write-then-rename for atomicity:** write new/updated content to a
  temp file in the same directory, then atomically rename over the
  target. This avoids any window where Obsidian's file watcher sees a
  half-written file (relevant because Obsidian re-indexes on file
  change events).
- **Frontmatter edits are surgical, not wholesale.** When adding
  tutor-relevant metadata to an existing learner note (should this ever
  be needed — the MVP should prefer *not* to do this at all, writing
  only to its own subfolder instead), parse and preserve all existing
  frontmatter keys and only add/update a single namespaced key.
- **No polling/locking scheme for MVP.** Building real mutual-exclusion
  with a live Obsidian instance is out of scope for the MVP; the
  practical mitigation is "the tool only writes to its own subfolder,"
  which makes the collision surface with the learner's live editing
  session effectively zero.

## 6. Storage format for the tutor's own learner-evidence state

Two genuinely different kinds of state exist here, and they should not
be forced into one format:

**(a) The learner's own qualitative notes and understanding** (what they
wrote about a concept, their own words, their study material) — this
must stay in the vault as ordinary Markdown+frontmatter. It is the
learner's property, must remain readable/editable with zero tooling,
and Obsidian's own conventions (Section 2) are the right schema to reuse
for the small amount of tutor-relevant frontmatter that touches these
files at all (e.g. a `codecompass-concepts` tag/list on a note the
learner explicitly links to a lesson).

**(b) The tutor's own structured evidence/learner-model state**
(concepts encountered with timestamps, puzzle attempt history, error
classifications, spaced-review scheduling, difficulty estimates) needs
to support queries like "what's due for review," "what motifs has this
learner recently failed," and "what's the transfer evidence for concept
X" — exactly the kind of relational/temporal querying that plain
Markdown frontmatter (per Section 2, vault-global-per-key, no query
engine) handles poorly at any real volume, and that the
spaced-repetition plugin's inline-HTML-comment approach (Section 3)
handles only by re-parsing every note on every operation.

**Recommendation:** a small, project-owned **SQLite** file (one file,
zero external service, trivially backed up, portable, has a real query
engine) as the tutor's evidence store, kept *inside the tutor's own
subfolder in the vault* (or configurably outside it) rather than
scattered across learner notes. This mirrors the boundary CodeCompass
itself already draws for `context-graph.db` — a regenerable, tool-owned
artifact, not the learner's primary copy of anything. Concretely:

- The SQLite file is the tutor's working index — fast to query, easy to
  rebuild.
- Anything a learner should be able to read/edit without the tool (their
  own understanding, their own notes) never lives *only* in SQLite —
  it's either the learner's own Markdown (source of truth) or, for
  human-readable summaries the tool generates *from* SQLite (e.g. "your
  puzzle history this week"), rendered out to Markdown in the tutor's
  vault subfolder as a derived, regeneratable artifact, clearly marked
  as generated.
- This boundary should be stated explicitly in `docs/architecture.md`
  and enforced by never treating the SQLite file as something the
  learner needs to hand-edit or that migration/versioning needs to
  preserve perfectly — it should be safe to delete and regenerate from
  the vault's Markdown + the tutor's own puzzle/position sources, though
  the initial MVP does not need to build that reconstruction path on day
  one; it just needs to avoid architectural choices that would make it
  impossible later (e.g. don't put learner data in SQLite that has no
  other source of truth at all).
- JSON/JSONL is worth keeping as a possible **import/export**
  interchange format for the SQLite content (for portability/backup),
  not as the primary store — SQLite already gives that plus real query
  support for free.

## Open uncertainty / human decision gate

- **Live-write conflict with Obsidian itself is not fully resolved by
  documentation.** Neither Obsidian's own docs nor
  `obsidian-local-rest-api`'s docs specify guaranteed-safe behavior for
  a true concurrent write race between an external process and Obsidian
  editing the *same* file at the *same* instant. The mitigation proposed
  above (tool writes only to its own subfolder, never learner notes) is
  believed to make this a non-issue in practice, but this has not been
  empirically tested against a running Obsidian instance and should be
  validated before the tutor is ever given write access to a learner's
  live vault outside of its own subfolder.
- **Whether MVP should depend on `obsidian-local-rest-api` at all**
  (even optionally) is a genuine open call, not resolved here — it would
  give real-time SSE updates and a ready-made MCP surface, but adds a
  plugin-install dependency and a second network hop, which conflicts
  with "learner should be able to use this without extra Obsidian
  plugins" for the MVP. Recommendation above treats it as post-MVP;
  a human should confirm that framing rather than have it decided
  implicitly by omission.
