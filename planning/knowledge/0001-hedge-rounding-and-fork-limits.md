---
status: retained
source: planning/retros/0001-project-bootstrap.md
---

# Candidate: summarizing a hedged research finding tends to round the hedge away

**What happened**: during the project bootstrap, `docs/research/tactical-puzzle-datasets.md`
carefully stated it had only confirmed that Lichess's puzzle export has a
`Themes` column, not what its actual tag vocabulary is. When that finding
was summarized one level up, in `decisions/0009-mvp-curriculum-boundary.md`,
the summary named specific tag spellings (`discoveredAttack`,
`removeDefender`, etc.) as if they'd been verified — they hadn't. A similar
thing happened with the Lichess Elite Database being labeled "master-game
sourcing" in `docs/architecture.md`'s dependency table, when the research
document had explicitly distinguished "strong-player games" from classical
master-game corpora.

**Evidence**: both caught by an independent review pass reading the
research documents and the decisions/architecture docs that cite them side
by side (see `planning/retros/0001-project-bootstrap.md`).

**Why it seems worth keeping**: the failure mode wasn't fabrication — the
underlying research was accurate and appropriately hedged. It was that
*restating* a hedged finding one level up tends to lose the hedge, because
a specific-sounding example (an actual tag name) or a familiar label ("master
game") reads as more authoritative than the vaguer, correctly-hedged
original ("the column exists," "strong-player games"). This is a
generalizable risk for any project that does research → synthesis in
separate passes, not specific to chess data.

**What happened to it**: retained, not yet promoted to a rule, since this
is (so far) one incident, not a recurring pattern in this project yet. If
it recurs on a future research→synthesis pass, promote to a `CLAUDE.md`
rule: "when a decision record or architecture doc restates a specific
example, name, or figure from a cited research document, quote it exactly
or mark it as reasoned-beyond-the-source, rather than restating it more
confidently than the source supports."

---

# Candidate: a forked agent cannot spawn further sub-forks

**What happened**: during the same bootstrap, one of five parallel research
forks (the tactical-puzzle-datasets one) attempted, on its own initiative,
to spawn the other four research forks itself rather than trusting they'd
already been launched independently by the orchestrator. Those spawn
attempts failed silently (agent forking is not available from inside an
already-forked agent) with no user-visible error and no harm done, since
the other four were in fact already running from the orchestrator's own
parallel launch in the same turn.

**Evidence**: reported directly in that fork's own completion summary.

**Why it seems worth keeping**: a fork assuming it needs to fan out further
work itself, rather than trusting the orchestrator already has, is a
coordination assumption that happened to be harmless here but could cause
duplicated or missing work in a case where the orchestrator *hadn't*
already covered the same ground. Worth knowing this constraint exists
before designing any workflow that relies on a fork delegating further.

**What happened to it**: retained as a known tooling constraint. Not
promoted to a rule yet — one incident, no actual harm — but worth
mentioning explicitly in any future prompt to a fork that might be tempted
to delegate: "you cannot spawn further sub-agents from inside this fork;
if more parallel work is needed, say so in your report rather than
attempting it."
