# Guide: a tested ontology for the EURO STOXX 50

A hands-on walk through the tutorial: build a small ontology for the 50 EURO STOXX 50 constituents, test it, watch the tests miss two real mistakes, and fix them. Then take apart a second model of the same data, built with FIBO.

The [decision log](../decision-log.md) records *why* each choice was made. This guide tells you what to *do*, what you should see, and which test proves it. Each module links to the decision it teaches.

- **Audience:** data and analytics people who know tables and SQL; no RDF experience needed.
- **Time:** about 105 minutes for the core (Parts 1–3), plus about 60 for the FIBO part (Part 4).
- **Status:** draft for review, 2026-10-29. Every command and every number below was run against the commits named in [Stages](#stages).
- **Method:** the nine steps of the [Graphwise ontology-engineer methodology](../../skills/graphwise-ontology-engineer/SKILL.md#workflow), based on Noy and McGuinness, *Ontology Development 101*. In Parts 1–3 the module number is the step number.

## Modules

| Part | Module | Methodology step | Time | Stage |
| --- | --- | --- | --- | --- |
| [1. Build and test](part-1-first-build.md) | [C0. Setup and first run](part-1-first-build.md#c0-setup-and-first-run) | Preparation | 5 min | `main` |
| | [C1. Domain, scope and competency questions](part-1-first-build.md#c1-domain-scope-and-competency-questions) | 1. Domain and scope | 10 min | `main` |
| | [C2. Reuse existing ontologies](part-1-first-build.md#c2-reuse-existing-ontologies) | 2. Reuse | 10 min | `main` |
| | [C3. Enumerate terms](part-1-first-build.md#c3-enumerate-terms) | 3. Enumerate terms | 5 min | `main` |
| | [C4. Classes and hierarchy](part-1-first-build.md#c4-classes-and-hierarchy) | 4. Classes and hierarchy | 10 min | `main` |
| | [C5. Properties](part-1-first-build.md#c5-properties) | 5. Properties | 5 min | `main` |
| | [C6. Facets and constraints](part-1-first-build.md#c6-facets-and-constraints) | 6. Facets and constraints | 10 min | `main` |
| | [C7. Instances and testing](part-1-first-build.md#c7-instances-and-testing) | 7. Instances and test | 10 min | `main` |
| [2. Refine and iterate](part-2-revisions.md) | [C8a. Revision 1: reuse nobody can see](part-2-revisions.md#c8a-revision-1-reuse-nobody-can-see) | 8. Refine and iterate, back to 2 and 7 | 10 min | first build |
| | [C8b. Revision 2: the wrong "largest company"](part-2-revisions.md#c8b-revision-2-the-wrong-largest-company) | 8. Refine and iterate, back to 1, 3 and 5 | 15 min | Revision 1 |
| [3. Document and deploy](part-3-show-it.md) | [C9. Document and deploy](part-3-show-it.md#c9-document-and-deploy) | 9. Document and deploy | 15 min | `main` |
| [4. The same data with FIBO](part-4-fibo.md) | [F0. Setup and first run](part-4-fibo.md#f0-setup-and-first-run) | 7 (3 unchanged) | 5 min | `main` |
| | [F1. Checking a term](part-4-fibo.md#f1-checking-a-term) | 2 | 10 min | `main` |
| | [F2. What FIBO expects of a company](part-4-fibo.md#f2-what-fibo-expects-of-a-company) | 2, 4, 6 | 10 min | `main` |
| | [F3. Where FIBO does not fit: index membership](part-4-fibo.md#f3-where-fibo-does-not-fit-index-membership) | 2, 5 | 5 min | `main` |
| | [F4. Revenue as a node](part-4-fibo.md#f4-revenue-as-a-node) | 4, 5, 6 | 10 min | `main` |
| | [F5. Countries and their names](part-4-fibo.md#f5-countries-and-their-names) | 2, 7 | 5 min | `main` |
| | [F6. The two models side by side](part-4-fibo.md#f6-the-two-models-side-by-side) | 8 (and 9) | 5 min | `main` |
| | [F7. Optional: a bridge between the two](part-4-fibo.md#f7-optional-a-bridge-between-the-two) | 9 (and 2) | 10 min | `main` |

Part 1 walks through the finished model in methodology order, so learners see good design before they see mistakes. Part 2 goes back in history to the two revisions, the most instructive moments of the build, and traces each one to the step it came from. Part 4 re-enters the methodology at Step 2 with a different reuse strategy and compares the result with Parts 1–3 on the same questions.

## The nine steps and where the guide covers them

The objective of each step is taken from the methodology ([SKILL.md](../../skills/graphwise-ontology-engineer/SKILL.md#workflow) and [methodology.md](../../skills/graphwise-ontology-engineer/references/methodology.md)). "Conformance" says how far the guide covers the step's expected deliverables.

| Step | Objective | Expected deliverables | Module | Conformance |
| --- | --- | --- | --- | --- |
| 1. Domain and scope | Fix what the ontology covers, what it is for, which questions it must answer, and who uses and maintains it | Domain, scope, 5–10 competency questions, stakeholders | C1 | **Full.** Domain, intended use (teaching example), users, maintainer, scope, and six questions with an answer key |
| 2. Reuse | Reuse existing vocabularies; mint as little as possible | Reuse list, strategy, gap analysis, import plan | C2; F1–F3, F5 | **Full.** The import plan is deliberately empty (align, don't import), and the log says so |
| 3. Enumerate terms | List every term, its attributes and relations, before classifying | Term list, property inventory, relationships | C3 | **Full.** 16 terms, their relationships, and every column's fate |
| 4. Classes and hierarchy | Choose the classes and their kind-of hierarchy; declare disjointness; SKOS for terminological hierarchies | Class definitions, hierarchy, validation | C4; F2, F4 | **Full.** Development approach: bottom-up |
| 5. Properties | Attach each property at the most general class; domain, range, inverses, functional | Property definitions, domain and range | C5; F3–F5 | **Full,** including naming conventions |
| 6. Facets and constraints | Cardinalities, value types, ranges, patterns, as SHACL; OWL only where reasoning needs it | Constraints, value types, validation rules | C6; F2, F4 | **Full** |
| 7. Instances and test | Populate with data; test against the competency questions; find modelling errors | Instances, results per question, validation report | C7; F0, F5 | **Full** |
| 8. Refine and iterate | Fix what testing and review find, returning to the step where the problem originated; log each decision | Refined ontology, updated docs, version control | C8a, C8b; F6 | **Full.** Each revision names the step it returns to and adds a test |
| 9. Document and deploy | Documentation, versioning and changelog, deployment notes | Documentation, deployment plan, training, success metrics | C9; F6, F7 | **Full.** Maintenance procedure, owner and success measures recorded; this guide is the training material |

### Gaps and deviations

| # | Step | Finding | Status |
| --- | --- | --- | --- |
| G1 | 1 | Intended use, users and maintainers were not recorded | Closed: a teaching example for workshop participants, maintained by Peio Popov (Graphwise); the log's Step 1 and C1 |
| G2 | 2 | The methodology asks for an `owl:imports` plan; the build imports nothing | Closed: "import plan: none, by design" in the log's Step 2 and in C2 |
| G3 | 2 | Why schema.org for the company but FIBO for the index | Closed: the log's Step 2 (schema.org has no stock-index class) |
| G4 | 3 | Relations were not enumerated | Closed: a relationship table in the log's Step 3, used in C3 |
| G5 | 4 | The development approach was not stated | Closed: bottom-up, recorded after the fact in the log's Step 4 and in C4 |
| G6 | 5 | Naming conventions were not taught | Closed: recorded in the log's Step 5 and shown in C5 |
| G7 | 8, 9 | No maintenance plan or success measures | Closed: the log's Step 9 and C9 |
| G8 | — | No assumption register | Closed: [assumption register](../decision-log.md#assumption-register) in the log (AS1–AS8), used in C7. The skill's `DESIGN.md` is the tutorial's `decision-log.md` |

G4 and G5 were recorded after the fact, on 2026-10-29, and the log says so.

Two findings concern the skill rather than the guide:

- The skill's default namespace (`gw: <https://graphwise.ai/ontology/>`) is the shared namespace that Revision 2 (C8b) moved away from, and the skill's own worked example says to give each ontology its own namespace.
- The skill's worked example (`references/worked-example-estx50.md`) has no Step 3 or Step 8 section, although Step 8 holds the tutorial's two most useful lessons.

## How each module is laid out

| Part | What it holds |
| --- | --- |
| **Methodology box** | The step, its objective as the methodology states it, its expected deliverables, and what the module covers of them |
| **Goal** | What the learner achieves in this module, in one sentence |
| **Do** | Commands to run and files to open |
| **See** | The expected output |
| **Check** | The test that proves it |
| **Why** | The decision-log entry, including what was rejected |
| **Decided by** | Who made the decisions in this module: the Subject Matter Expert |
| **Instructor notes** | Questions to ask and points that tend to come up |

## Setup

You need Python 3.10 or later and git. Run everything from the `tutorial/` folder.

```bash
pip install -r requirements.txt
```

`scripts/query.py` runs one SPARQL query over the graph and prints a table. The exercises use it:

```bash
python scripts/query.py guide/exercises/c1-banks.rq
```

Options: `--variant fibo` loads the FIBO variant and `--variant bridge` the 2.0.0 data with the bridge (Part 4); `--reason` adds what an OWL RL reasoner (such as GraphDB's OWL2-RL ruleset) would infer; `--add FILE` loads extra Turtle files; `--root PATH` reads the graph from another copy of the tutorial folder, such as an earlier stage.

## Stages

Part 2 (Step 8) needs the repository as it was at two earlier commits. Check each one out into its own folder next to the repository with `git worktree`, so your main checkout stays on `main`. Run these from the repository root:

```bash
git worktree add ../estx50-first-build 760d31f
```

```bash
git worktree add ../estx50-revision-1 64207ac
```

| Stage | Commit | Ontology | Instance triples | Tests |
| --- | --- | --- | --- | --- |
| First build | `760d31f` | 1.0.0 | 541 | Track A 20/20, Track B 6/6 |
| Revision 1 | `64207ac` | 1.0.0 | 600 | Track A 22/22, Track B 6/6 |
| Revision 2 | `dcc89b1` | 2.0.0 | 650 | Track A 22/22, Track B 6/6 |
| `main` | | 2.0.0 | 650 | Track A 22/22, Track B 6/6 |

The earlier stages use the same pinned `requirements.txt`. When you are done, remove the folders with `git worktree remove ../estx50-first-build` and `git worktree remove ../estx50-revision-1`.

## Files used in the guide

| Path | What it is |
| --- | --- |
| `guide/exercises/*.rq` | The exercise queries: `c*` for Parts 1–3 (numbered by step), `f*` for Part 4 |
| `guide/exercises/c6-two-countries.ttl` | A broken company for the C6 experiment |
| `guide/exercises/f7-equivalence.ttl` | An equivalence link for the F7 experiment |
| `scripts/query.py` | Runs one query and prints a table |
