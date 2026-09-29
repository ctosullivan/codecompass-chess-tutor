# 0008. One lightweight concept graph in SQLite, not separate graph databases per layer

## Status

Accepted (2026-09-30).

## Context

The bootstrap prompt describes five candidate conceptual layers (chess
state/transformation, chess concepts/principles, learner model, pedagogical
model, evidence/provenance) and explicitly frames them as **research
hypotheses, not a requirement to immediately implement five physical graph
databases** — asking instead for the smallest architecture that represents
the useful relationships cleanly. It also asks directly whether tactical
motifs, endgame principles, and broader chess concepts should share one
concept model or use related but distinct models, and whether graph
relationships need a graph database at all initially.

`decisions/0005-obsidian-vault-integration.md` already commits to a small,
project-owned SQLite file as the tutor's structured-evidence store. The
concept/relationship model (principles, motifs, prerequisites, applicability
conditions, learner-concept evidence links) is exactly the kind of
many-to-many, queryable-by-relationship data SQLite can represent as
ordinary tables (nodes + typed edges), without needing a dedicated graph
database engine.

## Decision

- **One concept model, not five separate ones.** Tactical motifs (forks,
  pins, skewers, ...) and endgame principles (opposition, key squares,
  zugzwang, ...) are represented as the same kind of entity — a "concept"
  row with a `kind` discriminator (e.g. `motif` vs. `principle`) — rather
  than as structurally distinct models. This is justified because the
  bootstrap prompt's own relationship requirements (prerequisites,
  applicability conditions/exceptions/conflicts, relationships between
  principles, concept transfer evidence) are structurally identical whether
  the concept is "opposition" or "the fork motif": both need
  prerequisite/relationship edges to other concepts, both need
  applicability-condition metadata, and both need learner-evidence links.
  Splitting them into separate models would duplicate that structure for no
  benefit visible at MVP scale.
- **Relationships are represented as typed edges in ordinary SQLite tables**
  (a `concepts` table plus a `concept_relations` table with a `relation_type`
  column — e.g. `prerequisite_of`, `related_to`, `applies_under`,
  `conflicts_with`), not a dedicated graph-database engine. SQLite's
  recursive CTEs are sufficient for the traversal queries this project
  actually needs at MVP scale (e.g. "what are this concept's prerequisites,
  transitively"); nothing in the bootstrap prompt's requirements needs
  graph-database-specific features (e.g. distributed graph queries,
  built-in graph algorithms at scale) that plain relational tables with
  typed edges can't express for a single-learner local tool.
- **This single SQLite store also holds the learner-evidence and
  puzzle-history data from `0005`** — one project-owned database, not
  separate databases per conceptual layer. The "five candidate conceptual
  layers" from the bootstrap prompt are a way of *thinking about* the
  domain (and should stay legible as such in `docs/architecture.md` and in
  how tables are named/grouped), not a mandate for five separate storage
  systems.
- **Provenance (source of a concept claim: book, tablebase, engine, master
  game, generated example, or LLM interpretation) is a field/edge on the
  same model**, not a sixth separate system — e.g. a `provenance` column or
  linked table recording where a specific concept-instance claim or
  worked-example came from, per the evidence/provenance layer's
  requirements.

## Alternatives considered

- **A dedicated graph database (e.g. Neo4j or similar) for the concept
  model.** Rejected for MVP: adds a real operational dependency (a service
  to run, or an embedded graph engine to bundle) for graph-traversal
  capability that SQLite's recursive CTEs already cover at this project's
  actual scale (a bounded set of chess concepts/motifs, one learner). Worth
  revisiting only if a concrete traversal need is reached that SQLite
  genuinely can't express reasonably — not speculatively.
- **Five separate models/stores, one per conceptual layer**, mirroring the
  bootstrap prompt's five-layer framing literally. Rejected: the prompt
  itself frames this as a hypothesis to test, not a requirement, and the
  actual relationship structure needed (typed edges between concept-like
  entities, evidence links, provenance tags) is shared enough across layers
  that separate models would mean re-solving the same schema problem five
  times for no clear benefit at MVP scale.
- **Distinct motif-model vs. principle-model with different schemas** (e.g.
  because tactical motifs feel more "pattern-recognition" and endgame
  principles feel more "positional judgment"). Rejected: that distinction is
  real at the *pedagogical* level (how a concept is taught, practiced,
  assessed — see `docs/architecture.md`'s pedagogical-model section) but
  doesn't require a different *data* representation; a `kind` discriminator
  plus kind-specific optional fields is sufficient.

## Consequences

- The concept-model schema must be designed to comfortably hold both motifs
  and principles from day one (shared core fields: name, kind, description,
  applicability conditions, source/provenance; relationship edges keyed by
  concept id on both ends) — a future need to genuinely split them would be
  a schema migration, not a clean addition.
- SQLite's recursive-CTE traversal must actually be exercised/tested once
  real prerequisite chains exist (roadmap item 2) — this decision assumes
  it's adequate but that assumption is untested against real query patterns
  yet, since no domain model exists at bootstrap time.
- If a genuine graph-database-specific need is discovered later (traversal
  patterns SQLite handles poorly at the scale this project actually
  reaches), that would need its own superseding decision record with the
  concrete evidence for why plain tables stopped being adequate — not a
  speculative upgrade.
