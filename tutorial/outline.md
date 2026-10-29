# Tutorial outline (draft)

A draft structure for turning the decision logs into a hands-on tutorial. The logs stay the record of *why*; the tutorial tells the learner what to *do*, what they should see, and how to check it.

- Sources: [`decision-log.md`](decision-log.md) (2.0.0), [`fibo-decision-log.md`](fibo-decision-log.md) (FIBO variant), [`fibo-feasibility-study.md`](fibo-feasibility-study.md) (optional reading).
- Status: draft, 2026-10-29, superseded by [`guide/`](guide/README.md), where the core path and the FIBO module are written out. The guide renumbers the core modules to match the methodology steps (C1 is Step 1 … C9 is Step 9), so the C-numbers below are out of date. Timings assume a 90-minute core slot plus an optional 45-minute FIBO module; adjust to the agenda.

## The story in one line

Build a small ontology, test it, let the tests expose real mistakes, fix them, then build it a second time with FIBO and compare. The two variants differ in **how deeply they reuse**: 2.0.0 mints local terms and places them under schema.org (and one FIBO) class; the FIBO variant uses FIBO terms directly and mints only five.

## Format of each module

| Part | Content |
| --- | --- |
| Goal | One sentence |
| Do | The commands or edits, copy-pasteable |
| See | The expected output, with numbers (triples, test counts, rows) |
| Check | The test that proves it (Track A/B ID) |
| Why | Link to the decision-log entry, including what was rejected |
| Decided by | Person or AI-proposed, then approved (supports the "AI accelerates the work" message) |

## Checkpoints

The core path is told in the order it happened. Each stage is a commit that learners check out into its own worktree, so the main checkout stays on `main`.

| Stage | Commit | Ontology | Tests |
| --- | --- | --- | --- |
| First build | `760d31f` | 1.0.0 | Track A 20/20, Track B 6/6 |
| Revision 1: reuse made visible | `64207ac` | 1.0.0 | Track A 22/22, Track B 6/6 |
| Revision 2: currency, names, namespace | `dcc89b1` | 2.0.0 | Track A 22/22, Track B 6/6 |
| FIBO variant | `84783e3` | FIBO 1.0.0 | Track A 26/26, Track B 6/6 |
| Bridge | `393b1cd` | bridge 1.0.0 | Bridge 10/10 |

```bash
git worktree add ../estx50-first-build 760d31f
```

---

## Core path: a tested ontology (2.0.0)

### Part 1: First build (`760d31f`), about 50 minutes

**C0. Setup and first run** (5 min)
- Do: `pip install -r requirements.txt`, then the three scripts in the README.
- See: Track A 20/20, Track B 6/6.
- Why: [Step 0](decision-log.md#step-0-setup) (no server needed during a workshop).

**C1. Scope and two kinds of questions** (10 min)
- Do: read B1–B6; open `queries/answer-key.csv`; predict B1 before running it.
- See: 7 banks.
- Lesson: "built right" (Track A) and "right thing" (Track B) fail for different reasons. The answer key comes from the CSV, never from the graph.
- Why: [Step 1](decision-log.md#step-1-domain-scope-and-competency-questions).

**C2. Reuse before you mint** (10 min)
- Do: find each reused vocabulary in `ontology/estx50-ontology.ttl` and classify it by the three mechanisms (alignment, direct use, reuse as data).
- Lesson: align, don't import; ICB is loaded alongside, not imported.
- Why: [Step 2](decision-log.md#step-2-reuse-existing-ontologies).

**C3. Terms and classes** (10 min)
- Do: list every CSV column and its fate (mapped, cross-checked, dropped); A5b checks this.
- Lesson: three classes only. Discuss the two rejected designs: a `EuroStoxx50Company` class (instances migrate when the index rebalances) and 249 OWL classes for ICB (blurs instance and class).
- Why: [Steps 3–4](decision-log.md#step-4-classes-and-hierarchy).

**C4. Properties** (5 min)
- Lesson: link to the 8-digit subsector and derive the higher levels with `skos:broader+`; one country property meaning "index-assigned" (Stellantis is domiciled in the Netherlands, assigned to Italy).
- Why: [Step 5](decision-log.md#step-5-properties).

**C5. OWL infers, SHACL validates** (10 min)
- Do: run the tests with `data/violations-demo.ttl`; then break one company yourself (remove its country) and read the `sh:message`.
- See: exactly 3 top-level violations for the demo file.
- Why: [Step 6](decision-log.md#step-6-facets-and-constraints), and the first finding in [Step 8](decision-log.md#step-8-refine-and-iterate) (why 4 became 3).

### Part 2: The tests find real mistakes, about 25 minutes

**C6. Revision 1: reuse that nobody can see** (`760d31f` → `64207ac`, 10 min)
- Do: at `760d31f`, count `schema:Corporation` in `data/estx50-instances.ttl` without a reasoner.
- See: 0 (50 after Revision 1).
- Lesson: reuse that only appears after reasoning is invisible to a plain triple store, a crawler or an LLM. The fix is dual typing; the new tests A1f and A1g were confirmed to fail before the fix.
- Why: [Revision 1](decision-log.md#step-8-refine-and-iterate).

**C7. Revision 2: the wrong "largest company"** (`64207ac` → `dcc89b1`, 15 min)
- Do: at `64207ac`, run B5 and ask "in which currency?".
- See: TotalEnergies 195.6, which is USD, ranked against EUR figures.
- Lesson: a dropped column can hide a wrong answer from every test. Also covered: `schema:legalName` holding short names, definitions that built in index membership, a namespace shared with other ontologies. Term IRIs changed, so the version goes to 2.0.0.
- Why: [Revision 2](decision-log.md#step-8-refine-and-iterate).

### Part 3: Show it (`main`), about 15 minutes

**C8. Document and deploy**
- Do: open `docs/estx50-explorer.html`; generate the pyLODE docs; optionally load into GraphDB.
- Why: [Step 9](decision-log.md#step-9-document-and-deploy).

---

## Advanced module: the same data with FIBO, about 45 minutes (written out as [Part 4](guide/part-4-fibo.md), about 60)

Framing: Step 2 redone with a different reuse strategy. The Step 1 questions and the answer key stay the same; Steps 4–7 follow from the new reuse choice.

**F1. Checking a term** (10 min)
- Do: look up `fibo-fnd-acc-4217:EUR` and `fibo-fnd-acc-4217:Euro` in `ontologies/QuickFIBOProd.ttl`.
- Lesson: labels mislead; one is a currency identifier, the other the currency. Read what a term commits you to, not just its label.
- Why: [V](fibo-decision-log.md#v-how-terms-were-verified), [M6](fibo-decision-log.md#m6-revenue).

**F2. Company and index: what FIBO expects** (10 min)
- Lesson: `PubliclyHeldCompany` inherits expectations the source cannot meet (legal name, incorporation, issued capital): incomplete, not inconsistent. An equity index is a measure, not a collection.
- Why: [M1](fibo-decision-log.md#m1-company), [M2](fibo-decision-log.md#m2-index).

**F3. Where FIBO does not fit** (10 min)
- Lesson: index membership stays a flat local link, because FIBO's path goes through shares the source does not have. Revenue becomes a monetary-amount node, which rules out mixing currencies by construction (the Revision 2 problem), at the cost of the billions caveat.
- Why: [M3](fibo-decision-log.md#m3-index-membership-flat-link), [M6](fibo-decision-log.md#m6-revenue).

**F4. Run and compare** (10 min)
- Do: `python scripts/run_tests.py --variant fibo`; open both explorers side by side.
- See: Track A 26/26, Track B 6/6; the only answer-key difference is "Netherlands (the)".
- Why: [M4](fibo-decision-log.md#m4-country), the README comparison table.

**F5. Bridge (optional)** (5 min)
- Do: `python scripts/check_bridge.py`.
- See: 10/10; FIBO B3 and B4 return nothing on bridged 2.0.0 data.
- Lesson: why one-way links and not equivalence.
- Why: [B](fibo-decision-log.md#b-bridge-from-200-2026-10-29).

---

## To do before this can be taught

1. **Tag the checkpoints** (`git tag` on the commits above). The scripts were confirmed to run at `760d31f`, `64207ac` and `dcc89b1` with the pinned requirements (Python 3.14).
2. **Explain the mix in 2.0.0.** Add a line to Step 2 of the decision log on why the company is aligned to schema.org but the index to FIBO (schema.org has no index class).
3. **Mark who decided.** Add "Decided by" to each decision. Known from the logs: the user chose provisional ICB codes, billions for revenue, and D1–D4.
4. **Replace the term index in F1.** Participants do not have the AI Ontologist FIBO term index; F1 uses `QuickFIBOProd.ttl` instead.
5. **One home for the FIBO decisions.** Keep `fibo-decision-log.md` as the source; shorten the FIBO section of the main log and the feasibility study to summaries that link to it.
6. **Expected outputs per module.** Collect the numbers (triples, test counts, rows) from the logs and reports into the "See" lines, and recheck them at each checkpoint.
