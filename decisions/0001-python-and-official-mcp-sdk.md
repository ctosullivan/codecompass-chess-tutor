# 0001. Implement in Python, on the official MCP Python SDK, over stdio

## Status

Accepted (2026-09-30).

## Context

The tutor must be exposed as an MCP-style tool/server usable from an AI
assistant, and must eventually operate on a learner's local Obsidian vault.
Two decisions were open: implementation language, and which MCP SDK/transport
to build on. See `docs/research/mcp-protocol-and-language-choice.md` for the
underlying evidence.

The chess-domain dependencies this project needs regardless of MCP choice —
legal-move/state handling, tablebase probing, engine invocation, puzzle data
handling — are overwhelmingly Python-native (see
`docs/research/chess-engine-tablebase-licensing.md`). MCP itself offers
first-party SDKs for both Python and TypeScript.

## Decision

- **Language: Python.**
- **MCP binding: the official `modelcontextprotocol/python-sdk` (PyPI: `mcp`),
  confirmed MIT-licensed** (medium-high confidence — confirmed from the
  repo's README and PyPI's license classifier; the raw `LICENSE` file text
  itself was not opened in the research pass and should be spot-checked once
  the dependency is actually pinned).
- **Transport: stdio.** The tutor is a locally-spawned server invoked by a
  desktop AI-assistant host, not a standalone network service; stdio is the
  standard MCP binding for that deployment shape. Streamable HTTP is not
  needed for the MVP.
- **Filesystem-access safety for the Obsidian vault**, modeled on the
  official filesystem reference server's pattern: the server is configured
  at startup with exactly one explicit vault-root path, refuses to start
  without one, and routes every vault-touching read/write through a single
  path-resolution helper that resolves symlinks and rejects any path that
  escapes the vault root (`..`-escapes and symlink escapes alike). Generated
  artifacts (diagrams, etc.) are written only under a dedicated tutor
  subfolder within the vault — see `decisions/0005-obsidian-vault-integration.md`.

## Alternatives considered

- **TypeScript + the official TypeScript MCP SDK.** Rejected: would mean
  either reimplementing Python's chess-domain ecosystem or shelling out to a
  Python subprocess anyway — strictly more moving parts for no identified
  benefit. Its license was also reported (low confidence) as a dual
  Apache-2.0/MIT split, which is one more thing to verify for no offsetting
  gain. Nothing in the MVP (endgame tutoring, tactics, Obsidian file I/O, SVG
  rendering) is performance-sensitive in a way that favors Node.
- **Streamable HTTP transport.** Rejected for the MVP: adds complexity
  (network exposure, auth) with no requirement driving it; revisit only if
  the tutor ever needs to run as a standalone network service.
- **An unbounded/general filesystem allow-list** (multiple roots, dynamically
  supplied). Rejected: this project only ever needs one vault at a time: a
  single fixed root, refused-if-absent, is simpler and easier to reason
  about than the general case the official reference server supports.

## Consequences

- Chess-domain licensing decisions (0002–0004) can assume a Python runtime.
- The exact `mcp` SDK API surface (class/decorator names) was not verified
  against a pinned version in research — implementation must pin an exact
  version and read that version's own docs before writing server code; do
  not trust example code sketches from the research document literally.
- MCP's spec is versioned by date and only bumped on breaking changes (current
  revision 2026-07-28 at research time), with a documented backward-compat
  path — but this project has no first-hand experience yet of living through
  a breaking change. Pin the SDK version and re-check before upgrading.
- If this project ever needs a standalone network-accessible deployment, the
  transport choice will need revisiting (a new ADR, not an edit to this one).
