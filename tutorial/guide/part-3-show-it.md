# Part 3: Document and deploy, Step 9

About 15 minutes, on `main`. The model is tested; now make it usable by people who were not in the room.

---

## C9. Document and deploy

> **Methodology step 9: Document and deploy.**
> **Objective:** documentation for each audience, and a deployment people can use: versioning, a changelog, loading notes.
> **Deliverables:** documentation, deployment plan, training material, success metrics and monitoring.
> **Covered here:** version metadata and changelog, reference documentation, the explorer for business users, GraphDB loading, the maintenance procedure, its owner, and success measures.

**Goal:** turn the ontology and data into something a business user can explore and an engineer can load.

**Do**

1. Build and open the semantic-layer explorer:

   ```bash
   python scripts/build_explorer.py
   ```

   Open `docs/estx50-explorer.html` in a browser. Look at the CSV next to its meaning, one company as a row and as a graph, the business questions, the validation rules and the ICB hierarchy.

2. Generate the reference documentation:

   ```bash
   python -m pylode ontology/estx50-ontology.ttl -o docs/estx50-ontology.html
   ```

   Open `docs/estx50-ontology.html` and find the metadata at the top: version, prior version, licence, creator, preferred prefix.

3. Optional, with GraphDB:
   1. Create a repository with the **OWL2-RL** ruleset.
   2. Import, in this order: `ontology/estx50-ontology.ttl`, `ontology/icb-skos.ttl`, `data/estx50-instances.ttl`.
   3. Optional: enable SHACL validation, load `shapes/shapes.ttl` into the SHACL shape graph (`http://rdf4j.org/schema/rdf4j#SHACLShapeGraph`), then try importing `data/violations-demo.ttl` and watch it be rejected.
   4. Run the queries in `queries/business-queries.rq` in the SPARQL editor.

**See**

- Step 1: `Wrote docs/estx50-explorer.html: 50 companies, 6 questions, 3 violations`.
- Step 2: an HTML page with every class and property, its definition and its links to schema.org and FIBO. The version is 2.0.0, prior version 1.0.0, licence CC BY 4.0.
- Step 3: with SHACL enabled, GraphDB rejects the import of the demo file. (Not yet run against GraphDB for this guide.)

**Check:** A6a (every company traces back to a source distribution), A6b (the ontology and the ICB taxonomy are both versioned), A6c (the revenue caveat is attached to the property and the dataset), B6 (ASML's figures trace to both source files, both flagged approximate).

**Why:** [Step 9](../decision-log.md#step-9-document-and-deploy).

- The explorer shows the result to people who will not read Turtle or SPARQL.
- GraphDB loading is documented, not run, so the workshop needs no server.
- The provenance (DCAT, PROV-O) and the caveats travel with the data, so a consumer who never reads this guide still learns that the figures are approximate and the subsector codes provisional.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Never load `violations-demo.ttl` into a real repository.
- With the pinned versions in `requirements.txt` the generated files reproduce byte for byte, apart from the date in `reports/test-report.md`. pyLODE is pinned to 3.2.1 because 3.3 fails on a dependency conflict.
- **Maintenance and success measures** are in [Step 9](../decision-log.md#step-9-document-and-deploy) of the log: every change runs the full pipeline and is accepted only if the tests pass; a change to a term IRI is a major version; success is Track A and Track B passing and a reproducible build. For a teaching example, success also means participants can run every module and get the stated results.

---

## Wrap-up

What the 90 minutes showed:

| Lesson | Step | Where |
| --- | --- | --- |
| Decide what the model must answer, and compute the expected answers independently | 1 | C1 |
| Reuse existing vocabularies, and make the reuse visible in the data | 2 | C2, C8a |
| List every term, including the ones you leave out | 3 | C3 |
| Model categories as a taxonomy and membership as a relation, not as classes | 4 | C4 |
| Store the fact you have, derive the rest | 5 | C5 |
| OWL infers, SHACL validates | 6 | C6 |
| Make the mapping refuse bad input; test every question | 7 | C7 |
| Tests prove only what they ask; review finds the rest, and each fix returns to the step it came from | 8 | C8a, C8b |
| Ship provenance and caveats with the data | 9 | C9 |

Next: [Part 4](part-4-fibo.md) takes apart the FIBO variant, which models the same data with FIBO terms used directly.
