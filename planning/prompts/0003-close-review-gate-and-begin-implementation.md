---
date: 2026-09-30
purpose: Close the outstanding independent-review gate left open by the GPL relicensing phase (roadmap item 1b was marked done without its own retro's required independent review ever being recorded in the repository), then re-plan the first implementation work into small phases and implement Phase 2A (Python project and chess-state foundation) only.
resulting_phase: GPL-replanning review closeout, roadmap re-planning into small phases, and Phase 2A implementation (follows the GPL relicensing phase recorded in 0002-gpl-relicensing-and-simplification.md)
resulting_commits: see git log for the commits that followed this prompt in this repository's history
supersedes: does not edit or replace 0001 or 0002's own bodies; directs closing a process gap those phases left open and directs the start of implementation work neither of them began.
---

The prompt body below is quoted verbatim, exactly as given by the user in
their message. Nothing in the body has been rewritten, shortened, or
"cleaned up" — see `planning/prompts/README.md` for why.

---

You are the lead Claude Code orchestrator for:

Repository: https://github.com/ctosullivan/codecompass-chess-tutor

Assume no knowledge of prior conversation. Work from the repository’s current main and treat the repository itself as authoritative, especially:

* CLAUDE.md;
* README.md;
* docs/architecture.md;
* docs/research/;
* decisions/0001–0011;
* planning/ROADMAP.md;
* planning/CONTEXT.md;
* planning/retros/;
* planning/knowledge/;
* planning/context-gaps/;
* planning/prompts/;
* vendor.toml;
* LICENSE;
* NOTICE-THIRD-PARTY.md.

The project bootstrap and GPL-3.0-or-later architectural simplification are substantially complete. The objective now is to begin implementation and progress systematically toward the first usable MVP, without collapsing the remaining roadmap into one large build.

Current architectural intent

CodeCompass Chess Tutor is a GPL-3.0-or-later, Python-based, local-first chess-learning system.

The MVP is deliberately bounded:

* endgame-first tutor, initially focused on basic pawn endings;
* daily thematic tactical puzzles;
* MCP interface for use by an AI assistant;
* learner-owned Obsidian/Markdown notebook environment;
* SQLite-backed structured learner/concept/evidence state;
* python-chess as the normal runtime chess-state/rules/notation/Syzygy/chess.svg dependency;
* exact tablebase truth for bounded endgame correctness;
* optional Stockfish only if later tactical-validation evidence justifies it;
* visual pedagogy including partial-board/cutaway diagrams;
* CodeCompass used as a development tool only, never a required product/runtime dependency.

Preserve the hard distinction between:

* legal chess state;
* exact tablebase truth;
* optional engine evaluation;
* sourced claims/puzzle provenance;
* tutor interpretation;
* learner understanding.

An LLM is never the source of objective chess truth.

1. Preserve this prompt verbatim

Save this entire prompt verbatim as the next sequential record under:

planning/prompts/

Do not modify prior prompt bodies.

2. First close the outstanding GPL-replanning review gate

Before implementing new product code, resolve the process inconsistency left by the GPL-replanning phase.

The current repository marks roadmap item 1b as done, but its own retro states that an independent review still needed to follow. CLAUDE.md requires independent review for consequential architecture/licensing work.

Perform a fresh independent review of the GPL-replanning state, specifically checking:

* decisions/0010 and 0011;
* supersession/narrowing of 0002, 0003, 0004, 0007;
* GPL-3.0-or-later licensing consistency;
* LICENSE and NOTICE-THIRD-PARTY.md;
* direct runtime use of python-chess;
* removal of obsolete MIT-driven architecture;
* board-rendering wording and bounded-evidence claims;
* tactical-puzzle legality vs optimality distinction;
* README.md, docs/architecture.md, ROADMAP.md, CONTEXT.md consistency.

Fix any material contradictions found.

Only after the independent review passes should roadmap item 1b remain/return to done.

Record the review outcome and any fixes according to the project’s existing lightweight governance.

3. Re-plan the first implementation work into small phases

Do not execute the existing broad “next implementation phase” as one large unit.

Split the beginning of MVP implementation into at least these conceptual phases, adjusting numbering/naming to the repository’s actual conventions:

Phase 2A — Python project and chess-state foundation

Goal: establish the first real executable project state with the minimum infrastructure necessary for later domain work.

Scope should include:

* create the Python project/package structure;
* add and pin the minimum justified dependencies;
* adopt python-chess as the runtime chess-state primitive;
* add the official Python MCP SDK dependency if appropriate to establish the real dependency manifest, but do not build the broad MCP interface yet;
* basic tests proving:
    * FEN loading;
    * legal move handling;
    * applying moves/state transitions;
    * SAN/UCI round-tripping where relevant;
* establish test/tooling configuration only as needed;
* create the first real first-party source tree.

Explicitly out of scope:

* complete concept graph;
* tablebase lesson validation;
* broad pedagogy;
* daily puzzle workflow;
* visual cutaway implementation;
* MCP tool surface;
* Obsidian integration.

CodeCompass dogfooding requirement for Phase 2A

Once the real manifest and source tree exist:

* run the current supported CodeCompass discovery/sync workflow;
* allow it to populate/use vendor.toml as appropriate;
* use CodeCompass where it plausibly helps;
* record honestly whether its dependency/source context was useful;
* record actual missing/misleading context under planning/context-gaps/;
* record transferable process/tool learnings under planning/knowledge/;
* do not manufacture CodeCompass usage merely to produce a positive result.

This should be the project’s first genuine clean-slate test of the CodeCompass template.

Phase 2B — Endgame concept/state model

Goal: represent the smallest meaningful chess-learning domain on top of python-chess.

Start with a deliberately small slice such as:

* opposition;
* key squares;
* king-and-pawn versus king.

Design the smallest SQLite schema justified by real domain queries.

The model should begin exploring the interaction of:

* position/current state;
* concept/principle;
* typed relationships;
* applicability conditions;
* representative transformations/future states;
* evidence/provenance.

Do not implement a general graph platform.

Exercise the real queries the tutor will need, such as:

* what concepts apply to this position?
* what prerequisites does this concept have?
* what positions illustrate/counterexample it?
* what transformation changes its relevance?

Use typed relational tables/edges in SQLite as currently planned unless real evidence shows that design is inadequate.

Phase 3 — Tablebase-backed endgame truth

Keep this separate from concept representation.

Goal: prove that the bounded endgame material can be mechanically grounded.

Implement:

* tablebase abstraction/integration;
* initial remote Lichess tablebase path or current approved strategy;
* W/D/L lookup;
* exact successor-state verification where useful;
* tests showing the Phase 2B examples/claims agree with tablebase truth;
* clear handling of unavailable/network-failure cases.

Do not allow explanation prose to substitute for tablebase verification.

4. Continue toward the MVP incrementally

After Phases 2A/2B/3, continue planning and implementing small, independently reviewable phases covering the remaining MVP capabilities.

The required MVP ultimately includes:

Daily thematic tactics

Build a small daily tactical puzzle workflow using the approved Lichess CC0 source strategy.

Required eventual capabilities:

* select puzzles by tactical theme;
* prepare a small daily set;
* replay/validate stored moves through python-chess;
* track provenance;
* record learner outcomes;
* support learner-selected themes and later adaptive selection.

Do not falsely claim tactical optimality from python-chess.

Keep separate:

* move legality/state-transition verification — cheap with python-chess;
* best-move/tactical-optimality verification — requires evaluation not yet supplied by python-chess;
* theme purity / “dominant unrelated tactic” analysis — still an open design problem.

Verify the actual Lichess Themes vocabulary against real dataset data before hard-coding mappings.

Learner/pedagogical model

Implement the smallest model that supports evidence-backed adaptation.

Consider evidence for:

* concepts encountered;
* correct/incorrect attempts;
* recurring misconception;
* recognition vs candidate-generation vs calculation failures;
* prerequisites;
* review history;
* transfer to unfamiliar examples.

Avoid arbitrary gamification or complex scoring unless justified.

The learner workflow should remain broadly aligned with:

Map → Explore → Commit → Practice → Feedback → Revise

Visual pedagogy

Implement the existing architectural decision:

PedagogicalViewSpec → project-owned composition → chess.svg → SVG artifact

Support the pedagogically useful minimum, including:

* full board;
* bounded cutaways such as 3×3/4×4/5×5;
* orientation;
* highlighted squares;
* arrows/trajectories;
* comparison/minimal-pair diagrams;
* “now → then” views.

Treat crop size/content as part of teaching intent, not merely rendering configuration.

Do not overclaim that no external renderer can support this; the evidence only established that none of the surveyed candidates provided the required feature directly.

MCP

Expose the tutor through a deliberately small MCP surface.

Prefer coarse learner-facing capabilities over dozens of low-level tools.

Potential MVP capabilities may include:

* inspect/explain an endgame position;
* request/practise a concept;
* prepare daily tactical puzzles;
* submit/validate an answer;
* render a pedagogical board view;
* read/update learner progress;
* work with relevant notebook material.

Design the actual API only when the underlying domain operations exist.

Obsidian/vault integration

Preserve learner ownership.

Use the vault as ordinary files with strict path-root safety.

Prefer:

* Markdown;
* simple metadata/frontmatter where useful;
* relative links to generated SVG/artifacts;
* a dedicated tutor-managed subfolder;
* SQLite only for structured/regenerable system state.

Do not make Obsidian itself or an Obsidian plugin a hard runtime dependency unless later evidence demands it.

5. Define the first integrated MVP slice

The first integrated MVP should demonstrate an actual learning loop, not merely disconnected modules.

It should support at minimum something close to:

learner asks/studies an endgame concept
        ↓
tutor retrieves concept + current learner state
        ↓
shows appropriate position / cutaway
        ↓
learner predicts or explains
        ↓
learner plays/chooses
        ↓
python-chess validates legal transition
        ↓
tablebase establishes endgame truth
        ↓
tutor explains with provenance
        ↓
learner evidence is updated
        ↓
relevant Markdown/artifact is recorded in Obsidian

and, separately but sharing the same learner/concept/evidence architecture:

daily tactical session
        ↓
select thematic puzzles
        ↓
learner attempts
        ↓
python-chess checks legal stored line / state transitions
        ↓
record success/error category
        ↓
update learner evidence
        ↓
schedule/recommend later practice

The MVP does not need to solve every future pedagogical problem. It needs to prove these loops are coherent and useful.

6. Maintain evidence-first development

For each non-trivial phase:

* plan first;
* keep explicit scope/out-of-scope;
* use real evidence for dependencies/behaviour;
* keep docs synchronized;
* record meaningful ADRs;
* independently review consequential work;
* write a short retro;
* triage real learnings/context gaps;
* preserve substantial directing prompts verbatim.

Keep the agent model lightweight.

Do not copy CodeCompass’s large specialist roster. Use bounded subagents where they materially help and independent reviewers where required.

7. Keep the MVP bounded

Do not add, unless required by evidence to complete the defined MVP:

* opening training;
* general middlegame strategy;
* broad master-game mining;
* generated synthetic tactical puzzles;
* cloud services/accounts;
* web UI;
* mobile app;
* dedicated graph database;
* large permanent multi-agent system;
* broad Stockfish integration;
* general-purpose chess engine functionality.

If an attractive capability appears, record it as a later candidate rather than expanding MVP scope silently.

8. Roadmap and phase-management requirement

Before implementation:

1. reconcile ROADMAP.md so the first work is represented as small phases rather than one broad mixed phase;
2. update CONTEXT.md;
3. create the detailed plan for the first implementation phase;
4. ensure no unresolved human decision gate blocks it.

Then implement one phase at a time.

After each phase:

* verify;
* independently review where required;
* update docs;
* write retro;
* update knowledge/context gaps;
* update ROADMAP/CONTEXT;
* commit/push according to project rules.

Do not mark a phase done before its own required independent review has actually completed.

MVP completion criteria

The MVP programme is complete when a fresh learner can use the system through its intended MCP/Obsidian workflow and demonstrate:

* bounded pawn-endgame tutoring;
* objective tablebase-backed correctness;
* concept relationships/state-transformations represented explicitly;
* useful full-board and cutaway visual explanations;
* daily thematic tactical puzzles;
* legal tactical lines checked mechanically;
* learner history/evidence influencing subsequent practice in at least a basic way;
* learner-owned Markdown/Obsidian artifacts;
* a coherent MCP surface;
* CodeCompass absent from runtime requirements;
* tests covering core domain/integration behaviour;
* documentation explaining architecture and usage;
* at least one real end-to-end learning-scenario evaluation.

Do not require tactical engine-backed optimality/theme-purity verification to declare the first MVP complete unless implementation evidence shows the learner-facing feature is not trustworthy without it. If it remains deferred, provenance and limitations must be explicit.

Immediate execution instruction

Proceed now as follows:

1. preserve this prompt;
2. perform and close the missing independent review of the GPL-replanning phase;
3. reconcile any resulting fixes;
4. re-plan the first implementation work into small phases, using the Phase 2A → 2B → 3 structure above unless repository evidence justifies a better decomposition;
5. implement Phase 2A only;
6. independently verify/close Phase 2A;
7. stop and report before implementing Phase 2B.

At the end report:

* independent GPL-replanning review result;
* any corrections made;
* revised MVP roadmap;
* Phase 2A plan;
* Phase 2A implementation commits;
* tests/results;
* CodeCompass dogfooding outcome and any context gaps/learnings;
* current architecture/state;
* unresolved gates;
* recommended Phase 2B scope.

Do not begin Phase 2B in this task.
