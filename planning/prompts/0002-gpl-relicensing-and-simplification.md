---
date: 2026-09-30
purpose: Record the project owner's decision to relicense GPL-3.0-or-later instead of MIT, and direct the resulting architecture-simplification and replanning work (superseding the bootstrap's MIT-driven isolation machinery where no longer needed, while preserving the MVP boundary, the chess-truth/pedagogy boundary, and evidence-first process).
resulting_phase: GPL relicensing and architecture simplification (follows the bootstrap phase recorded in 0001-project-bootstrap.md)
resulting_commits: see git log for the commits that followed this prompt in this repository's history
supersedes: does not edit or replace 0001-project-bootstrap.md's own body; this prompt supersedes the *licensing conclusion* reached during that phase (MIT, decisions/0007) and the architecture built specifically to preserve it (parts of decisions/0002 and 0004) — see decisions/0010 for the resulting decision record.
---

The prompt body below is quoted verbatim, exactly as given by the user in
their message. Nothing in the body has been rewritten, shortened, or
"cleaned up" — see `planning/prompts/README.md` for why.

---

You are the lead Claude Code orchestrator for:

Repository: https://github.com/ctosullivan/codecompass-chess-tutor

Assume no knowledge of prior conversation. Work from the repository’s current main, especially:

* CLAUDE.md;
* README.md;
* docs/architecture.md;
* docs/research/;
* decisions/0001–0009;
* planning/ROADMAP.md;
* planning/CONTEXT.md;
* planning/retros/;
* planning/knowledge/;
* planning/context-gaps/;
* planning/prompts/;
* vendor.toml;
* the current LICENSE.

This task follows the completed initial bootstrap. It is a decision-recording, architecture-simplification and replanning task, not the next feature implementation phase.

User decision

The project owner has explicitly decided that CodeCompass Chess Tutor should be licensed GPL-3.0-or-later rather than MIT, because the available chess ecosystem dependencies make GPL a better fit and avoiding them would introduce unnecessary custom infrastructure.

Treat this as an intentional architectural simplification, not merely a licence-file change.

The project should still:

* use CodeCompass as a development/context tool but not require CodeCompass at runtime;
* use the CodeCompass template/development-process principles;
* remain an endgame-first chess tutor;
* include daily thematic tactical puzzles in the MVP;
* operate as an MCP-style tool/server alongside a learner’s Obsidian vault;
* preserve the learner/concept/pedagogical/state/evidence architecture;
* treat visual pedagogy, including variable-size board cutaways, as a first-class requirement;
* preserve prompt provenance and evidence-first development.

Do not broaden the MVP simply because GPL-compatible dependencies are now easier to use.

1. Preserve prompt provenance

Save this entire prompt verbatim under planning/prompts/ as the next sequential prompt record.

Do not rewrite or modify previous prompt bodies.

Minimal metadata may identify that this prompt supersedes the bootstrap’s MIT licensing assumption and caused an architectural replanning phase.

2. Record a superseding architectural decision

Create the next append-only ADR, likely 0010, recording:

* adoption of GPL-3.0-or-later;
* why the owner chose it;
* which earlier decisions or portions of decisions it supersedes;
* which previous architectural work existed only to preserve MIT;
* which architectural boundaries remain valuable for technical reasons;
* what this allows the project to delete, simplify or avoid building.

Do not rewrite historical ADRs to make it appear that GPL was always intended.

Explicitly reconcile at least:

* 0002 — bespoke bounded legal-move validator / python-chess isolation;
* 0003 — tablebase and engine strategy;
* 0004 — board-rendering / chess.svg isolation;
* 0007 — MIT project licence.

Expected direction, subject to repository evidence:

* 0007 is superseded.
* 0002’s MIT-driven bespoke runtime move-validator decision should normally be superseded. A mature chess library should be preferred unless there is an independent product reason to own chess move generation.
* 0004’s GPL-isolation reasoning should be superseded, while its PedagogicalViewSpec and project-owned crop/composition layer remain valuable.
* 0003 may remain substantially valid because exact tablebase truth and optional engine analysis are separate architectural concerns from licensing.

Make supersession relationships explicit in current documentation without editing the historical ADR bodies.

3. Simplify the chess-domain dependency architecture

Reassess python-chess as a normal runtime dependency now that GPL compatibility is intentional.

Evaluate using it directly for:

* FEN/board representation;
* legal move generation;
* applying state transitions;
* check/checkmate/stalemate and other relevant game-state checks;
* SAN/UCI notation;
* Syzygy support where appropriate;
* SVG board rendering.

The project should not maintain a bespoke legal-move generator merely because the bootstrap once planned one for MIT compatibility.

The initial bootstrap review identified permissively licensed alternatives such as ChessMG and smaller perft-verified move generators. Under the new GPL decision, do not spend project effort evaluating or adopting them solely to avoid python-chess. Only revisit an alternative if it offers a concrete product benefit such as materially better portability, performance, maintenance or capability.

Retain independent correctness testing where useful. Using python-chess does not remove the requirement to test the tutor’s own domain logic; it removes the need to recreate generic chess rules.

4. Preserve the chess-truth / pedagogy boundary

GPL adoption should simplify software boundaries, not collapse epistemic ones.

Keep a clear distinction between:

* legal chess state and move mechanics;
* exact tablebase truth;
* optional engine analysis;
* sourced tactical-puzzle claims;
* tutor interpretation/explanation;
* learner understanding.

An LLM must still never become the source of objective chess truth merely because chess infrastructure is now easier to use.

Reconcile docs/architecture.md accordingly.

5. Reassess tablebase and engine strategy

Review ADR 0003 under the simplified dependency model.

The likely shape remains:

* tablebases as the preferred exact oracle for bounded endgames;
* python-chess may provide convenient Syzygy integration if/when local tablebases are used;
* the remote Lichess tablebase service can remain useful if its operational tradeoffs are acceptable;
* Stockfish remains optional/deferred until a concrete tactical-analysis or validation requirement justifies it;
* if Stockfish is introduced, UCI/subprocess remains a clean architectural interface even though GPL isolation is no longer required for licensing.

Do not introduce Stockfish merely because GPL now permits it.

6. Simplify board rendering while preserving visual pedagogy

The bootstrap correctly identified visual pedagogy as a differentiating requirement.

Retain:

PedagogicalViewSpec → Renderer → SVG/notebook artifact

and project-owned teaching logic for:

* arbitrary 3×3 / 4×4 / 5×5 or other cutaways;
* key-square highlighting;
* arrows and trajectories;
* promotion lanes;
* side-by-side comparisons;
* minimal pairs;
* “now → then” state visualisations;
* concept-specific framing;
* full-board views when broader context matters.

Now reassess chess.svg as a normal base rendering primitive instead of treating it as something that must be artificially isolated for MIT purposes.

The likely architecture is:

position / board state
        ↓
PedagogicalViewSpec
        ↓
project-owned pedagogical composition
        ↓
python-chess / chess.svg primitive
        ↓
SVG artifact
        ↓
Obsidian / MCP consumer

The project-owned layer should answer what should the learner see?; the underlying renderer should answer how are squares and pieces drawn?

Correct the bootstrap evidence overstatement

The initial review identified a specific example of the project’s own recorded “hedge-rounding” failure mode.

The research established:

no surveyed candidate provided the required arbitrary partial-board rendering directly.

Some current architecture wording escalates this to a universal claim equivalent to:

no chess rendering library anywhere supports it.

That stronger claim was not established.

Correct current-state documentation to say “none of the surveyed candidates supported the requirement” or equivalent. Preserve uncertainty rather than turning a bounded search result into proof of absence.

Check other synthesis statements for the same failure mode while touching the affected documents.

7. Replace and canonicalise the project licence

Replace the current MIT licensing position with GPL-3.0-or-later.

Use a conventional canonical licence file. The repository’s LICENSE/COPYING should contain the standard applicable GPL licence text rather than project-specific architecture/dependency commentary appended to the licence.

Move explanatory material about:

* project licensing rationale;
* dependency licences;
* third-party artwork;
* attribution;
* optional components;

to the appropriate combination of:

* README.md;
* docs/architecture.md;
* ADRs;
* NOTICE / THIRD_PARTY_LICENSES.md if warranted.

Review the cburnett chess-piece artwork attribution requirement independently of the project’s GPL licence. GPL adoption does not erase third-party attribution obligations.

Avoid legal conclusions stronger than the evidence supports.

8. Simplify architecture documentation

Update current-state architecture so it no longer carries obsolete MIT-driven machinery.

Remove or supersede statements whose only purpose was:

* preventing an in-process python-chess import;
* maintaining a bespoke chess move generator for copyleft avoidance;
* treating chess.svg as requiring an artificial internal isolation boundary;
* framing every GPL dependency as a licensing hazard.

Preserve architectural boundaries that have independent technical value.

A likely simplified shape is:

AI assistant
      │
     MCP
      ↓
application/service layer
      ↓
chess-learning domain
      ├── concept/evidence model
      ├── learner model
      ├── endgame curriculum
      ├── daily thematic tactics
      └── PedagogicalViewSpec
              │
              ├── python-chess
              │    ├── board state
              │    ├── legal moves
              │    ├── notation/state transitions
              │    ├── Syzygy integration
              │    └── chess.svg
              │
              ├── exact tablebase source
              └── optional Stockfish when justified
persistence
      ├── SQLite structured state
      └── learner-owned Obsidian Markdown/artifacts

Reconcile this against actual project evidence rather than copying it blindly.

9. Re-plan the roadmap

Review planning/ROADMAP.md in light of this simplification.

Remove or shrink work that existed only because the project intended to recreate capabilities already available in python-chess.

In particular, the mechanically validated chess-core work should now focus on integration and verification, not implementing generic chess rules.

Preserve the MVP priorities:

* bounded pawn-ending domain/curriculum;
* current/future chess-state concepts and transformations;
* shared concept graph;
* tablebase-backed correctness;
* learner/pedagogical modelling;
* visual pedagogy;
* daily thematic tactical puzzles;
* MCP interface;
* Obsidian/vault integration;
* integrated learning loop;
* evaluation with real learning scenarios.

Keep early phases small.

Do not collapse everything into a single implementation phase simply because some infrastructure becomes easier.

10. Reconcile tactical-puzzle validation

The bootstrap’s independent review correctly narrowed an earlier overclaim: the project does not yet independently re-derive every Lichess tactical puzzle solution.

Reassess this now that python-chess can be a normal runtime/development dependency.

Determine whether the GPL decision materially lowers the cost of:

* replaying Lichess puzzle solution lines;
* independently verifying move legality;
* checking puzzle state transitions;
* later adding engine-backed solution/best-move verification.

Do not claim that python-chess alone establishes tactical optimality; move legality and best-move correctness are separate questions.

Preserve the existing open gate around:

* independent tactical-solution revalidation;
* exact Lichess theme vocabulary;
* detection of puzzles dominated by a different motif than the intended teaching theme.

Update planning if some of these can now be addressed earlier or more simply.

11. Reconcile all open gates

Audit docs/architecture.md, ADR consequences, planning/CONTEXT.md, and research notes for gates created by the old MIT assumption.

Classify each as:

* resolved by GPL adoption;
* superseded;
* still relevant;
* requires future evidence.

Likely resolved/superseded:

* whether in-process python-chess threatens the preferred project licence;
* whether chess.svg must sit behind a licence-isolation boundary;
* whether a custom legal-move validator is necessary purely to maintain MIT;
* FSF GPL-linking/output questions that were relevant only to preserving MIT.

Likely still relevant:

* Lichess theme-tag verification;
* tactical puzzle optimality/revalidation;
* tablebase service operational dependency/offline mode;
* pedagogical crop-selection rules;
* concept/state/learner model design;
* Obsidian concurrent-write behaviour;
* whether/when Stockfish adds enough value;
* local Syzygy operational/storage choices if later introduced.

Remove obsolete gates rather than keeping them indefinitely as historical clutter. Their history remains visible in git and ADRs.

12. Operationalise CodeCompass on the first real implementation phase

The bootstrap correctly left vendor.toml empty because no actual source/dependency manifest existed yet.

The next implementation phase will create real source and likely a pyproject.toml with dependencies such as python-chess and the MCP SDK.

Make that phase the project’s first genuine clean-slate CodeCompass/template dogfooding exercise:

* once the real dependency manifest/source exists, run CodeCompass discovery/sync according to current supported workflow;
* use it as a development aid, never a runtime requirement;
* record whether its source/dependency context was actually useful;
* file any real missing/misleading context under the template’s planning/context-gaps/;
* capture general process/tooling learnings under planning/knowledge/;
* do not create artificial CodeCompass usage simply to generate positive evidence.

Update the next-phase plan to include this development-tool validation explicitly.

13. Reconsider the next implementation phase

After all reconciliation, determine the smallest sensible next implementation phase.

The prior plan identified Roadmap Item 2: endgame-domain model / SQLite concept schema.

Reassess whether that remains the right first code phase given python-chess can now provide the chess-state primitive.

A plausible phase shape is:

* establish the Python project/package and pinned dependencies;
* integrate python-chess as the chess-state representation;
* define the smallest concept/state model needed for the bounded pawn-ending curriculum;
* introduce the initial SQLite schema only to the extent required by real domain queries;
* establish the first few mechanically grounded endgame concepts/examples;
* run CodeCompass against the resulting real project state.

However, verify this against the revised architecture rather than assuming it.

Do not implement that phase in this task.

Definition of Done

This replanning task is complete when:

* this prompt is preserved verbatim;
* a new superseding GPL decision exists;
* GPL-3.0-or-later is the canonical project licence;
* the licence file contains conventional licence text without project-specific commentary appended to it;
* affected historical ADRs are explicitly superseded/narrowed rather than silently rewritten;
* the bespoke legal-move-validator plan has been removed or justified by a non-licensing product reason;
* python-chess’s runtime role is explicit;
* tablebase/engine responsibilities remain correctly separated;
* board rendering is simplified while preserving PedagogicalViewSpec and cutaway/composition requirements;
* the universal “no renderer supports cutaways” overclaim has been corrected to the bounded evidence actually established;
* tactical-puzzle validation claims remain precise;
* obsolete MIT-specific gates have been retired;
* the roadmap reflects reduced infrastructure work without expanding MVP scope;
* ROADMAP.md, CONTEXT.md, README and architecture agree;
* the next implementation phase includes real CodeCompass dogfooding once source/dependencies exist;
* the next phase is clearly identified but not implemented;
* an independent reviewer checks the reconciled repository for contradictions, stale MIT assumptions, and synthesis claims stronger than their cited evidence.

Commit the replanning work in logical commits and push it.

At the end report:

* commit SHA(s);
* new/superseding ADR;
* which earlier decisions were superseded or narrowed;
* architectural simplifications made;
* roadmap changes;
* corrected bootstrap-review issues;
* remaining open gates;
* recommended next implementation phase.

Do not begin implementation of that next phase.
