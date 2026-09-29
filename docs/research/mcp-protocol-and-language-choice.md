# Research: MCP SDK/protocol options and implementation-language choice

Checked 2026-09-30. Primary sources: `modelcontextprotocol.io` spec site, the
`modelcontextprotocol/python-sdk` and `modelcontextprotocol/typescript-sdk`
GitHub repos, and the `mcp` PyPI package page. Fetched via automated
page-summarization (WebFetch), not by opening raw source/LICENSE files
directly — see confidence notes below; anything load-bearing for a licensing
decision should get a direct source-file check before being treated as final.

## Summary table

| Component | License | Maturity (as of 2026-09-30) | Confidence |
|---|---|---|---|
| `modelcontextprotocol/python-sdk` (PyPI: `mcp`) | MIT (per repo README + PyPI classifier `OSI Approved :: MIT License`) | v2.2.0, released 2026-09-07; README describes v2 as "the current stable release line" | Medium-high — license confirmed from two independent pages (GitHub README, PyPI metadata), but I did not open the raw `LICENSE` file text itself |
| `modelcontextprotocol/typescript-sdk` | Reported as "Apache License 2.0 for new contributions, with existing code under MIT" | v2, implementing the 2026-07-28 spec revision; exact package version not surfaced | **Low** — this dual-license claim is unusual enough that it should be treated as unverified until someone opens the actual `LICENSE`/`NOTICE` files; it may be a summarization artifact |
| MCP protocol/spec itself | Spec text license not checked in this pass | Current revision **2026-07-28**; versioned as `YYYY-MM-DD`, only bumped on backwards-incompatible changes; official backward-compatibility path documented for older `initialize`-handshake-based clients/servers (2025-11-25 and earlier) | Medium — versioning page read directly, this is a good sign of a spec that treats stability as a first-class concern rather than churning silently |
| Official filesystem reference server (`modelcontextprotocol/servers`, `src/filesystem`) | Not checked in this pass (same org, presumably MIT like the SDKs — **unverified**) | Actively documented as the reference pattern for scoping local filesystem access | Medium |

## Recommendation: Python + the official Python MCP SDK

Use **Python** with the official `mcp` SDK (`pip install mcp`, MIT-licensed)
as the implementation language and MCP binding for the chess-tutor server.

Reasoning:

- The chess-domain dependencies this project will need regardless — legal
  move/state validation, tablebase probing, engine (UCI) invocation, puzzle
  data handling — are overwhelmingly Python-native (`python-chess` and its
  ecosystem; see the companion research doc on chess libraries). Choosing
  TypeScript/Node would mean either reimplementing that domain logic or
  shelling out to a separate Python process anyway, which is strictly more
  moving parts for no benefit.
- The MCP SDK licensing is not a differentiator either way in principle (both
  first-party SDKs are permissively licensed at the top line), but the Python
  SDK's license is the one I could confirm with reasonable confidence from two
  independent sources; the TypeScript SDK's reported dual-license split is a
  flag, not a blocker, but adds friction to an MIT-license review for no
  offsetting benefit here.
- Nothing in this project's MVP (endgame tutoring, daily tactics, Obsidian
  file I/O, board SVG rendering) is performance-critical in a way that would
  favor Node's event loop or any other runtime property over Python.
- This is not a hard technical constraint — a TypeScript server could in
  principle proxy to a Python chess-logic subprocess — but that's added
  complexity with no identified requirement driving it.

**Confidence: high** on "Python over TypeScript for this project specifically"; the reasoning rests on the chess-ecosystem asymmetry (verified independently — see `chess-libraries-engines-tablebases.md`) more than on any difference between the two MCP SDKs themselves.

## What a minimal server looks like (SDK-level sketch)

Per the Python SDK's own documentation, the shape is: instantiate a server
object, then register tools with a decorator; resources (URI-addressable
readable data, e.g. `greeting://{name}`-style templates) are a distinct
primitive from tools (callable actions), and prompts are a third, separate
primitive. A representative shape:

```python
from mcp.server import MCPServer  # exact import path — VERIFY against
                                    # installed package before writing code;
                                    # see confidence note below

mcp = MCPServer("codecompass-chess-tutor")

@mcp.tool()
def prepare_daily_puzzles(theme: str | None = None) -> dict:
    """Prepare today's thematic tactical puzzle set."""
    ...

@mcp.resource("vault-note://{path}")
def read_vault_note(path: str) -> str:
    ...
```

**Confidence note:** the exact class name (`MCPServer` vs. the historically
documented `FastMCP` from `mcp.server.fastmcp`) and decorator surface were
pulled from an automated page summary, not from reading the SDK's actual
source or a pinned version of its README. Before implementation starts,
pin an exact `mcp` version in the project's dependency manifest and read
that version's own quickstart directly — do not trust this sketch's literal
names, only its shape (tool/resource/prompt as three distinct primitives,
decorator-based registration).

## Transport: stdio for a local server

The spec defines two standard transport bindings: **stdio** (newline-delimited
JSON-RPC over the standard streams of a client-launched subprocess) and
**Streamable HTTP** (HTTP POST plus optional SSE for streaming replies).
stdio is the standard binding for exactly this project's deployment shape — a
server launched locally by a desktop AI-assistant host, not one accessed
remotely over a network — since the host process spawns the server as a
child process and talks to it over its stdin/stdout. This project should
default to stdio and treat Streamable HTTP as unnecessary for the MVP (it
would only matter if the tutor needed to run as a standalone network service
rather than a locally-spawned tool).

## Filesystem-access safety: the Obsidian-vault boundary

The official filesystem reference server (`modelcontextprotocol/servers`,
`src/filesystem`) is the closest official precedent for "an MCP server that
touches local files safely," and its documented model is directly
applicable to this project's vault access:

- The server is configured with an explicit **allow-list of root
  directories**, supplied either as command-line arguments at launch or
  dynamically via the MCP "roots" protocol feature from the connecting
  client. If neither is provided, the server refuses to start rather than
  defaulting to an unbounded filesystem.
- Every filesystem operation is checked against that allow-list; nothing
  outside the configured roots is reachable.
- The reference implementation keeps this enforcement in dedicated
  path-validation code (referenced as `path-validation.ts`/`path-utils.ts` in
  that repo), which is the shape to imitate even though this project's own
  implementation will be Python: a single, well-tested "is this resolved
  path inside an allowed root" check that every vault-touching tool call
  goes through, rather than ad hoc path handling scattered across tool
  implementations.

**Recommended shape for this project:** the chess-tutor MCP server should be
configured at startup with exactly one explicit **vault root** path (the
learner's Obsidian vault folder), refuse to start without one being
configured, and route every read/write through a single path-resolution
helper that: (1) resolves the requested relative path against the vault
root, (2) resolves symlinks, (3) rejects any resolved path that is not a
descendant of the vault root (rejecting `..`-escapes and symlink escapes
alike), and (4) — if an attachments subfolder convention is adopted (see the
companion Obsidian-integration research doc) — writes generated diagrams only
under that subfolder, never elsewhere in the vault. This keeps the trust
boundary identical in shape to the official reference server's, adapted to a
single fixed root rather than a general allow-list, since this project only
ever needs one vault at a time.

## Open uncertainty / human decision gates

1. **TypeScript SDK license claim is unverified and should not be relied
   on** — if a future decision ever revisits the language choice, someone
   must open the actual `LICENSE`/`NOTICE` files in that repo rather than
   trusting the summary above.
2. **Exact Python SDK API surface (class/decorator names) is unverified
   against a pinned version** — resolve this at implementation time by
   reading the installed package's own docs/source, not from this document.
3. **Protocol stability risk:** the spec's versioning scheme (only bump the
   date on backwards-incompatible changes, with a documented compatibility
   path for older `initialize`-handshake-based implementations) is a good
   sign, but this project has no first-hand history of living through an MCP
   breaking change yet. Treat "pin the SDK version, re-check before
   upgrading" as an ongoing operational practice rather than a one-time
   decision.
4. **Filesystem reference server's exact traversal-guard implementation**
   was described at a summary level ("path-validation utilities exist") but
   not read line-by-line. Before implementing the vault path-resolution
   helper, it would be worth reading that file directly as a design
   reference rather than reinventing the check from first principles alone —
   flagged here as a good use of a future bounded research task rather than
   something to resolve in this bootstrap pass.
