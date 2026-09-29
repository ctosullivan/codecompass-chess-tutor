---
date: 2026-09-30
purpose: Initial project bootstrap — establish repository structure, development process, research the key architectural/domain questions, and produce an evidence-backed initial architecture and roadmap for codecompass-chess-tutor.
resulting_phase: Bootstrap (phase 1 of `planning/ROADMAP.md`)
resulting_commits: see git log for the commits that followed this prompt in this repository's initial history
superseded_by: (none yet)
---

The prompt body below is quoted verbatim, exactly as given by the user in
their message. Nothing in the body has been rewritten, shortened, or
"cleaned up" — see `planning/prompts/README.md` for why.

---

You are the lead Claude Code orchestrator for a new project:
Repository: `https://github.com/ctosullivan/codecompass-chess-tutor`
The repository is currently blank. Your task is to bootstrap the project, establish its development process, research the key architectural/domain questions, and produce an evidence-backed initial architecture and roadmap. Do not rush into implementing the tutor itself.
Project intent
CodeCompass Chess Tutor is an experimental AI-assisted chess-learning system.
Its initial MVP should be:

* an endgame-focused chess tutor;
* capable of preparing daily thematic tactical puzzles as a core learner-facing feature;
* exposed as an MCP-style tool/server usable from an AI assistant;
* designed to live alongside and work with a learner's Obsidian notebook/vault environment;
* capable eventually of adapting teaching to the learner rather than merely returning engine moves;
* developed using CodeCompass as a development/context tool, while CodeCompass must not be a runtime or required installation dependency of the finished tutor.

The project should investigate chess learning as a system involving multiple interacting models rather than treating chess as only an engine-evaluation problem.
Candidate conceptual layers include, but are not limited to:

1. Chess state and transformation
   * current board state;
   * legal transitions;
   * future/representative states;
   * strategic trajectories;
   * irreversible transformations;
   * concepts whose importance changes as the position changes.
2. Chess concepts and principles
   * concepts such as opposition, key squares, king activity, passed pawns, zugzwang, simplification, etc.;
   * tactical motifs such as forks, pins, skewers, discovered attacks, deflection, decoys, overloaded defenders, clearance, interference, zwischenzug, removal of defender and back-rank motifs;
   * relationships between principles;
   * applicability conditions, exceptions and conflicts;
   * avoid treating verbal principles as universally true rules.
3. Learner model
   * concepts encountered;
   * demonstrated understanding;
   * recurring errors;
   * prerequisites;
   * recognition versus calculation versus explanation failures;
   * tactical pattern-recognition versus candidate-generation versus calculation failures;
   * evidence that a concept transfers to unfamiliar positions.
4. Pedagogical model
   * how concepts should be introduced, explored, practised, contrasted and revisited;
   * examples, counterexamples, minimal pairs and transfer exercises;
   * progressive difficulty;
   * learner explanation before engine/tablebase revelation where pedagogically appropriate;
   * visual representation as part of the teaching model, not merely presentation;
   * daily thematic tactical practice as a recurring learning mechanism.
Specifically investigate whether some concepts are better taught using partial-board or cutaway visualisations rather than always showing a full 8×8 board. Examples may include:
   * 3×3, 4×4, 5×5 or other bounded board regions;
   * highlighted key squares;
   * pawn-race lanes;
   * opposition geometry;
   * promotion zones;
   * arrows, paths or transformed future positions;
   * side-by-side "now → then" positions;
   * minimal-pair diagrams where one piece or square changes;
   * full-board views where broader positional context matters.
Board size/crop should therefore be considered a potential pedagogical variable chosen according to what the learner is being asked to perceive.
5. Evidence/provenance
   * distinguish objective chess truth, source claims, tutor interpretation and learner understanding;
   * preserve provenance where knowledge comes from books, tablebases, engines, master games or generated examples;
   * do not allow LLM-generated explanations to silently become ground truth.

Treat these as research hypotheses, not a requirement to immediately implement five physical graph databases. Determine the smallest architecture that can represent the useful relationships cleanly.
Development-process requirements
Use `https://github.com/ctosullivan/codecompass-template` as the primary bootstrap guide.
Adopt its lightweight principles:
`understand → research/evidence → plan → design → implement → verify → retro → update knowledge`
Start from the template's conventions for:

* `CLAUDE.md`;
* `planning/ROADMAP.md`;
* `planning/CONTEXT.md`;
* `planning/retros/`;
* `planning/knowledge/`;
* `planning/context-gaps/`;
* `decisions/`;
* `docs/architecture.md`;
* `.gitignore`;
* `vendor.toml`.

Adapt them to this project rather than copying CodeCompass's accumulated governance wholesale.
Also inspect CodeCompass's current development process for useful patterns, especially:

* explicit planning before implementation;
* evidence-first design;
* human decision gates for unresolved architectural choices;
* independent verification for material work;
* current-state documentation;
* retrospectives and durable learnings;
* explicit context-gap recording.

Do not reproduce CodeCompass's large specialist-agent roster. This project is starting from zero and should have the smallest workable process.
Initially prefer:

* the lead orchestrator;
* bounded research/development subagents only where they materially help;
* an independent reviewer/verifier for consequential architecture or implementation decisions.

Add permanent specialist agents only after repeated work demonstrates that a stable role is justified.
Prompt provenance
The project should preserve the development prompts that materially direct orchestrator work.
Create an appropriate location such as:
`planning/prompts/`
with a short README describing its purpose.
Every substantial user/orchestrator prompt that initiates or materially redirects a phase of project work should be stored verbatim, without rewriting, shortening or "cleaning up" the original wording.
For this initial bootstrap:

* once the repository/template structure exists, save this entire prompt verbatim as the first prompt record, for example:
`planning/prompts/0001-project-bootstrap.md`;
* include minimal metadata outside the quoted/verbatim body where useful, such as date, purpose and resulting phase/commit;
* never silently modify a historical prompt after it has been recorded;
* if a later prompt supersedes an earlier one, preserve both and record the relationship.

These prompt records are provenance/history, not current-state instructions. `CLAUDE.md`, `ROADMAP.md`, `CONTEXT.md`, ADRs and architecture documents remain the authoritative current project state.
CodeCompass relationship
CodeCompass is a development tool, not part of the tutor product architecture.
Set the project up so that:

* developers may install and run `codecompass-context`;
* `vendor.toml` may be used to track important dependencies;
* first-party source and dependency context may be indexed during development;
* CodeCompass-generated databases, vendor digests, generated skills and other reproducible artifacts remain uncommitted where appropriate;
* production/runtime code does not import or depend upon CodeCompass;
* someone must be able to clone, install, test and run the chess tutor without having CodeCompass installed.

Record this boundary explicitly in project architecture/decision documentation.
Licensing
The preferred project license is MIT.
However, do not assume MIT compatibility before examining likely dependencies.
During bootstrap:

1. identify likely runtime and development dependencies;
2. verify their current licenses from authoritative sources;
3. distinguish:
   * runtime dependencies,
   * optional integrations,
   * development-only tools,
   * external services/data sources;
4. assess whether the proposed architecture permits the project itself to remain MIT licensed.

Particular attention should be paid to likely:

* chess libraries;
* engines;
* tablebase integrations;
* MCP libraries/SDKs;
* board rendering / chess-diagram libraries;
* image/SVG generation libraries;
* tactical-puzzle data sources or APIs;
* master-game databases or corpora;
* any other data corpus considered.

Prefer architectural separation of optional components where that preserves clean licensing boundaries.
If the dependency review supports MIT, add the MIT license. If a material uncertainty prevents a defensible licensing decision, document the issue and human decision gate rather than guessing.
CodeCompass's GPL license alone must not cause the tutor to become GPL merely because CodeCompass is used externally as a development tool.
MVP direction
The first functional milestone should be deliberately narrow: an endgame tutor with daily thematic tactical practice, not a general chess coach.
Research and propose the smallest useful initial endgame curriculum. A likely starting area is pawn endings, for example:

* king and pawn versus king;
* opposition;
* key squares;
* pawn races;
* king activity;
* zugzwang;
* basic passed-pawn concepts.

Do not assume that exact scope if research shows a better bounded starting slice.
The MVP must also support preparation of a daily set of thematic tactical puzzles.
The tactical component should not become a disconnected generic puzzle feed. It should test whether tactical training can use the same conceptual, learner and evidence architecture as the endgame tutor.
Research an MVP shape in which daily puzzles can be selected or generated around themes such as:

* forks;
* pins;
* skewers;
* discovered attacks;
* removal of defender;
* deflection;
* decoys;
* clearance;
* interference;
* overloaded pieces;
* back-rank motifs;
* forcing-move recognition;
* loose/undefended pieces.

The learner should be able to receive a small daily puzzle set selected according to one or more of:

* a specified theme;
* the learner's current study;
* concepts recently encountered;
* demonstrated weaknesses;
* spaced review;
* transfer to unfamiliar positions.

Puzzle generation/selection must be mechanically validated. The project must not trust an LLM simply because it claims a tactical solution works.
Research whether the MVP should source tactical positions from:

* suitably licensed/public puzzle datasets;
* master games;
* generated or modified positions;
* combinations of these.

Any dataset/API licensing or attribution requirements must be included in the licensing analysis.
For generated or modified tactical positions, investigate a pipeline such as:
`theme → candidate position → legality → tactical solution verification → reject unrelated dominant tactics → learner-facing puzzle`
Strongly investigate the use of objective mechanical validation, such as:

* chess move-legality libraries;
* endgame tablebases;
* engine analysis where appropriate.

The intended separation should roughly be:

```
LLM / AI assistant
        │
        │ MCP
        ▼
Chess Tutor
        │
        ├── learner/pedagogical model
        ├── concepts/evidence
        ├── endgame lesson/exercise selection
        ├── daily thematic tactical puzzles
        ├── visualisation / board rendering
        │
        └── chess validation layer
                 ├── legal chess state
                 ├── tablebase
                 └── engine where justified
```

The AI should explain, teach and interact. Objective chess tooling should validate facts that can be mechanically established.
Daily thematic tactical-puzzle requirement
Treat the daily puzzle workflow as a required MVP capability, not an optional future enhancement.
The bootstrap must design how the learner can request or receive a daily thematic puzzle session through the MCP interface and have the resulting work recorded in the learner's notebook environment.
Explore a minimal workflow such as:

```
learner state / chosen theme
        ↓
select daily theme(s)
        ↓
retrieve or construct candidate positions
        ↓
mechanically validate solution
        ↓
prepare small daily puzzle set
        ↓
learner attempts before solution reveal
        ↓
classify errors / successes
        ↓
update learner evidence
        ↓
write/refer to Obsidian learning record
```

Determine an appropriate MVP daily set size and difficulty progression rather than assuming a large volume.
Puzzle records should be able to retain useful metadata such as:

* position/FEN;
* side to move;
* theme/motif;
* expected solution or principal tactical line;
* validation source;
* difficulty estimate;
* concept/prerequisite links;
* learner outcome;
* error classification;
* date/review history.

Do not require all of these fields if a simpler representation is sufficient, but design for evidence-backed learner adaptation rather than an ephemeral puzzle response.
The architectural design should consider whether tactical motifs, endgame principles and broader chess concepts should share one concept model or use related but distinct models.
Visual pedagogy and board rendering
Treat chess-board rendering as part of the learning architecture, not merely UI polish.
The bootstrap should investigate how the tutor could produce visual teaching artifacts suitable for:

* Obsidian notes;
* AI/MCP responses where supported;
* printable or static study material;
* generated exercises;
* daily tactical puzzles;
* minimal-pair comparisons;
* "current state → transformed state" explanations.

Determine whether the MVP should:

1. use an existing chess-diagram/rendering dependency;
2. build a small project-owned renderer;
3. use a hybrid approach where a library handles chess representation but this project owns the pedagogical composition/cropping layer.

Evaluate candidate approaches against:

* license compatibility;
* dependency weight;
* maintenance burden;
* deterministic/reproducible output;
* SVG versus PNG or other formats;
* support for arbitrary board cutaways/crops;
* orientation;
* coordinates;
* highlighting;
* arrows;
* annotations;
* custom piece sets where useful;
* accessibility;
* embedding cleanly in Markdown/Obsidian;
* ability to generate visual minimal pairs;
* usefulness for tactical puzzle presentation;
* ease of testing generated output.

Do not implement a bespoke image renderer merely because doing so is possible. Equally, do not take a large dependency if a small deterministic renderer would better fit the project's needs.
This investigation should produce an explicit build-versus-dependency recommendation before the visualisation implementation phase begins.
Where useful, consider separating:

```
Position
    ↓
Pedagogical View Specification
    ├── full board / cutaway bounds
    ├── orientation
    ├── highlighted squares
    ├── arrows / trajectories
    ├── annotations
    └── comparison state
    ↓
Renderer
    ↓
SVG / image / notebook artifact
```

so teaching intent is not embedded directly inside rendering code.
Obsidian/MCP environment
The learner should retain ownership of their learning material.
Research an architecture in which the tutor can operate with an Obsidian vault using ordinary portable files where practical, preferably Markdown plus simple metadata rather than a proprietary database becoming the sole source of learner knowledge.
Explore a workflow such as:
`Map → Explore → Commit → Practice → Feedback → Revise`
where:

* Map identifies concepts and relationships from the learner's current study;
* Explore uses examples, questions, contrasts, visualisations and relevant positions;
* Commit records the learner's own current understanding in their notebook;
* Practice supplies mechanically validated endgame exercises and daily thematic tactical puzzles;
* Feedback diagnoses the type of misunderstanding;
* later evidence can cause the learner to revise prior understanding.

Visual artifacts generated by the tutor should, where practical, be storable alongside the learner's Markdown notes using portable relative links rather than requiring a proprietary viewer.
Consider how the MCP surface should expose capabilities such as:

* analyse or register a position;
* explain an endgame concept;
* generate/find a related exercise;
* prepare a daily thematic tactical puzzle set;
* request puzzles for a specified motif;
* select puzzles based on learner weaknesses/review needs;
* validate a tactical answer/line;
* render an appropriate pedagogical board view;
* generate a full-board or cutaway diagram;
* compare two positions visually;
* validate a learner answer;
* identify a useful contrast/counterexample;
* update/read learner progress;
* work with relevant notes in the learner's vault.

These are candidate capabilities, not a fixed API. Design the smallest coherent MCP interface for the MVP.
Do not tightly couple the core chess/pedagogy domain to MCP, Obsidian or any specific renderer. Prefer boundaries resembling:

```
core chess-learning domain
        ↑
application/service layer
        ↑
MCP adapter
        ↑
learner's AI + Obsidian environment

visual teaching specification
        ↓
renderer adapter
        ↓
SVG / image artifact
```

so other interfaces and renderers could be added later.
Research questions to resolve before implementation
Research enough to make defensible initial choices around:

* Python versus other implementation languages;
* current MCP SDK/protocol options and their licensing;
* how an MCP server should safely interact with an Obsidian vault;
* chess board/state representation;
* legal-move validation;
* endgame tablebases;
* optional engine integration;
* tactical puzzle sources/datasets and their licensing;
* whether thematic tactical puzzles should initially be selected, generated or both;
* how tactical positions and solutions can be mechanically verified;
* how to reject generated puzzles whose apparent teaching theme is dominated by an unrelated tactic;
* how generated or modified positions can be mechanically validated;
* representation of concepts, state transitions and learner knowledge;
* whether graph relationships initially require a graph database or can be represented more simply;
* storage format for learner state;
* boundaries between objective chess truth, pedagogical claims and LLM interpretation;
* dependency licensing;
* appropriate visual representations for chess learning;
* whether different concept types benefit from different board cutaway sizes;
* whether board cropping should be automatic, explicit in lesson metadata, or both;
* whether visualisation should initially be SVG, raster or another portable representation;
* whether an existing board-rendering dependency adequately supports the pedagogical requirements;
* whether a small custom board-image/diagram generator is justified instead.

Prefer authoritative upstream documentation and primary sources. Record evidence and uncertainty rather than silently filling gaps.
Bootstrap deliverables
Create and commit an initial project foundation containing, at minimum:

* adapted CodeCompass-template structure;
* appropriate `.gitignore`;
* provisional/final license decision as supported by dependency research;
* `README.md` explaining the project vision and its deliberately narrow initial MVP;
* `CLAUDE.md` with lightweight project governance;
* `docs/architecture.md`;
* one or more ADRs for consequential early decisions;
* `planning/ROADMAP.md`;
* `planning/CONTEXT.md`;
* `planning/prompts/README.md`;
* `planning/prompts/0001-project-bootstrap.md` containing this prompt verbatim;
* research/evidence documents sufficient to support the initial architecture;
* initial knowledge/context-gap structure inherited from the template;
* `vendor.toml` prepared for CodeCompass development use;
* minimal dependency/project configuration only where justified.

The roadmap should separate at least:

1. project/bootstrap and evidence gathering;
2. endgame-domain model;
3. mechanically validated endgame core;
4. tactical motif / daily-puzzle model;
5. learner/pedagogical model;
6. visual pedagogy and rendering;
7. MCP interface;
8. Obsidian/vault integration;
9. first integrated endgame-learning and daily-tactics loop;
10. evaluation with real learning scenarios.

These are roadmap themes, not mandated phase boundaries. Combine or split them where evidence supports doing so, and keep early phases small.
Definition of success for this bootstrap
The bootstrap is complete when a fresh developer or agent can read the repository and answer:

* What problem is this project trying to solve?
* What is explicitly in and out of the first MVP?
* Why is an endgame tutor the starting point?
* Why are daily thematic tactical puzzles also an MVP requirement?
* How will those puzzles be selected/generated and mechanically validated?
* How are objective chess truth and AI explanation separated?
* How might the learner, chess-state, tactical, concept and pedagogical models interact?
* What role does visual representation play in the pedagogy?
* Why might a 3×3/4×4/etc. cutaway sometimes be preferable to a full chessboard?
* How will visual teaching intent be separated from rendering implementation?
* Should board rendering initially be built by the project or supplied by a dependency, and why?
* How will Obsidian participate without becoming tightly coupled to the domain core?
* What does MCP provide?
* What role does CodeCompass play, and why is it not a product dependency?
* What licensing constraints exist, including any tactical-puzzle datasets?
* Where are the original prompts that directed project development preserved?
* What is the next concrete phase of work?
* What questions remain genuinely unresolved?

Before concluding, perform an independent review of the bootstrap architecture against these questions and fix material inconsistencies.
Do not implement a broad chess tutor in this initial task. Prefer a small, evidence-backed foundation over speculative architecture.
Commit the bootstrap in logical commits and push it to the blank `codecompass-chess-tutor` repository.
At the end, report:

* commits created;
* key architectural decisions;
* proposed MVP boundary;
* dependency/licensing conclusion;
* tactical-puzzle sourcing/validation conclusion, or explicit unresolved gate;
* board-rendering build-versus-dependency conclusion, or the explicit gate if not yet resolvable;
* unresolved human-decision gates;
* next recommended phase.
