---
status: reviewed
found_during: Phase 2A CodeCompass dogfooding (planning/ROADMAP.md)
---

# Candidate: CodeCompass must be installed into the project's own environment, not run from a separately-installed global binary

**What happened**: this project's first real CodeCompass dogfooding run
(`~/.local/bin/codecompass` — a pre-existing, separately-installed global
binary, not installed into this project) crashed with
`PackageNotFoundError: No package metadata was found for chess` while
trying to sync the newly-discovered `chess`/`mcp` vendors, even though both
were correctly declared in `pyproject.toml` and correctly installed in
this project's own `.venv`. The traceback showed the crash came from
`importlib.metadata.version("chess")` inside CodeCompass's own Python
adapter — which necessarily resolves against *whatever Python environment
the `codecompass` process itself is running in*, not the target project's
virtualenv. The global binary's own environment had never heard of
`chess` or `mcp`, so it failed opaquely rather than with a "you're running
me from the wrong environment" message.

**Fix**: installed the local `codecompass-context` wheel
(`/home/cormac/projects/codecompass/dist/codecompass_context-1.0.0-py3-none-any.whl`)
into this project's own `.venv`, then re-ran via `.venv/bin/codecompass`.
Worked immediately — auto-discovery found both vendors, `vendor.toml` was
populated, and (once re-run as `sync --budget 0`) real digests were
generated under `vendor/chess/` and `vendor/mcp/`.

**Why it seems worth keeping**: `codecompass-template`'s own README
already says to `pip install codecompass-context` (into the project) —
the crash was a self-inflicted deviation from the documented workflow
(using a pre-existing global install instead), not a genuine defect. But
the *failure mode* is worth remembering precisely: running the tool from
the wrong Python environment doesn't produce a clear "wrong environment"
error, it produces a generic `PackageNotFoundError` that looks like the
dependency itself is the problem. A future session (or a less careful
one) could easily misdiagnose this as "the project's dependency isn't
really installed" and go debug the wrong thing.

**What happened to it**: **retained**, not promoted to a `CLAUDE.md` rule
yet — one occurrence, and the underlying fix (install into the project's
own venv, as already documented) doesn't need a new rule, just remembering
that this specific crash signature means "wrong environment," not "broken
dependency," the next time it's seen.

---

# Candidate: `--budget 0` genuinely prevents any AI-enrichment spend, confirmed empirically

**What happened**: running bare `codecompass --budget 0` and
`codecompass sync --budget 0` against this real project both correctly
estimated Phase B (AI-enrichment) cost (~$0.02 for a small batch of
relationship descriptions) and aborted *before* making any API call,
printing `error: estimated cost $0.02 ... exceeds --budget $0.00`. Phase A
(mechanical work — vendor discovery, `vendor.toml` population, cloning
dependency source, building `context-graph.db`, generating per-vendor
`DEPTREE.md`/`FILETREE.md`/`CLAUDE.md` digests, and injecting a routing
table into this project's own root `CLAUDE.md` inside a clearly marked
`<!-- codecompass:start/end -->` block) completed fully and for free in
both runs.

**Why it seems worth keeping**: this is exactly the safety property an
agent-run dogfooding session needs — real, useful mechanical work happens
with zero risk of unexpected spend, and the tool's own advertised
`--budget` gate holds up under actual use, not just as documentation.
Confirms it's safe to run CodeCompass in future automated/agentic
sessions on this project with `--budget 0` (or an explicit small cap) as
a matter of course.

**What happened to it**: **retained** as a confirmed, safe default
practice for this project's future CodeCompass use — not promoted to a
`CLAUDE.md` rule since it's really just "use the tool's own documented
safety flag," not a new project-specific rule.

---

# Candidate: CodeCompass correctly distinguished a genuinely-used dependency from a merely-declared one

**What happened**: after Phase 2A's code imported and used `chess` but
only *declared* (never imported) `mcp` in `pyproject.toml`,
`codecompass query vendors` correctly reported `chess` as `Used: yes` and
`mcp` as `Used: no`. This is real, source-grounded usage detection, not
just "is it in the manifest."

**Why it seems worth keeping**: a small, concrete confirmation that the
tool's usage-tracking is trustworthy for exactly the kind of question
this project cares about ("is this dependency actually load-bearing yet,
or just declared for a future phase") — relevant again once the MCP tool
surface (roadmap item 7) actually starts importing and using `mcp`.

**What happened to it**: **retained**, no action needed — just a positive
data point worth having on record given this project deliberately added
`mcp` to Phase 2A's manifest *before* writing any code that uses it (see
`planning/ROADMAP.md`'s Phase 2A plan: "establish the real dependency
manifest... but do not build the broad MCP interface yet").
