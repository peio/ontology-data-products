# EURO STOXX 50 ontology tutorial

A small, tested OWL ontology for the 50 EURO STOXX 50 constituents, built step by step with the Graphwise ontology-engineer methodology. Each company is linked to its country (Wikidata) and to its ICB subsector (SKOS). Industry roll-ups follow `skos:broader`.

Design decisions for every step are in [`decision-log.md`](decision-log.md). The [graphwise-ontology-engineer skill](../skills/graphwise-ontology-engineer/SKILL.md) carries a condensed version of these decisions as reusable patterns in [`worked-example-estx50.md`](../skills/graphwise-ontology-engineer/references/worked-example-estx50.md).

## Steps

| Step | What happens | Produces |
| --- | --- | --- |
| [0. Setup](decision-log.md#step-0-setup) | Namespaces, tooling, folder layout | This README |
| [1. Domain, scope and competency questions](decision-log.md#step-1-domain-scope-and-competency-questions) | Fix scope; define Track A (robustness) and Track B (business questions) | Scope (below), `scripts/make_answer_key.py`, `queries/answer-key.csv` |
| [2. Reuse existing ontologies](decision-log.md#step-2-reuse-existing-ontologies) | Reuse ICB, schema.org, FIBO, DCAT, PROV-O, Dublin Core; align, don't import | Reuse table in the decision log, `ontology/icb-skos.ttl` |
| [3. Enumerate terms](decision-log.md#step-3-enumerate-terms) | List the vocabulary and the fate of every CSV column | Term list in the decision log, column map in `scripts/map_csv.py` |
| [4. Classes and hierarchy](decision-log.md#step-4-classes-and-hierarchy) | Three classes, each a subclass of a reused class; industry stays SKOS | Classes in `ontology/estx50-ontology.ttl` |
| [5. Properties](decision-log.md#step-5-properties) | Country, ICB subsector, revenue, index membership | Properties in `ontology/estx50-ontology.ttl` |
| [6. Facets and constraints](decision-log.md#step-6-facets-and-constraints) | OWL for inference, SHACL for validation | Facets in `ontology/estx50-ontology.ttl`, `shapes/shapes.ttl` |
| [7. Instances and testing](decision-log.md#step-7-instances-and-testing) | Map CSV to RDF, plant violations, run both tracks | `data/estx50-instances.ttl`, `data/violations-demo.ttl`, `queries/*.rq`, `scripts/run_tests.py`, `reports/` |
| [8. Refine and iterate](decision-log.md#step-8-refine-and-iterate) | Fix what the tests exposed; Revision 1 makes reuse visible without a reasoner | Changelog and Revision 1 in the decision log |
| [9. Document and deploy](decision-log.md#step-9-document-and-deploy) | Ontology metadata, HTML docs, GraphDB load | `docs/estx50-ontology.html`, this README |

## Contents

| Path | What it is |
| --- | --- |
| `ontology/estx50-ontology.ttl` | The ontology (TBox): 3 classes, 5 properties, metadata |
| `ontology/icb-skos.ttl` | ICB taxonomy as SKOS (249 concepts), reused unchanged |
| `requirements.txt` | Pinned Python dependencies |
| `data/README.md` | Source, licence and mapping notes for each data file |
| `data/EURO_STOXX_50_Constituents_CSV2.csv` | Source data |
| `data/icb-subsector-assignments.csv` | **Provisional** ICB subsector per company, with rationale |
| `data/estx50-instances.ttl` | Generated instance data (ABox) — do not edit by hand |
| `data/violations-demo.ttl` | Three deliberately broken companies for the validation demo |
| `shapes/shapes.ttl` | SHACL shapes (Track A3) |
| `queries/robustness-tests.rq` | Track A: SPARQL `ASK` tests |
| `queries/business-queries.rq` | Track B: SPARQL `SELECT` business questions |
| `queries/answer-key.csv` | Track B expected results, computed from the CSVs |
| `scripts/map_csv.py` | CSV → RDF mapping |
| `scripts/make_answer_key.py` | Builds the answer key independently of the graph |
| `scripts/run_tests.py` | Runs both tracks and writes `reports/test-report.md` |
| `reports/` | Test report and SHACL reports |
| `docs/estx50-ontology.html` | HTML documentation (pyLODE) |

## Run it

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python scripts/map_csv.py          # CSV -> data/estx50-instances.ttl
python scripts/make_answer_key.py  # CSV -> queries/answer-key.csv
python scripts/run_tests.py        # Track A + B -> reports/test-report.md
python -m pylode ontology/estx50-ontology.ttl -o docs/estx50-ontology.html
```

Run from the `tutorial/` folder. `run_tests.py` exits non-zero if any check fails. Expected: Track A 22/22, Track B 6/6. With the pinned versions in `requirements.txt` the generated files reproduce byte for byte, apart from the date in `reports/test-report.md`. pyLODE is pinned to 3.2.1 because 3.3 fails on a `kurra` dependency conflict.

Reused classes are asserted directly on the instances (`a gw:Company, schema:Corporation`), so schema.org and FIBO types are visible even without a reasoner.

## Load into GraphDB

1. Create a repository with the **OWL2-RL** ruleset. This materialises `gw:hasConstituent` from `gw:isConstituentOf`; the schema.org and FIBO types are already asserted.
2. Import, in this order: `ontology/estx50-ontology.ttl`, `ontology/icb-skos.ttl`, `data/estx50-instances.ttl`.
3. Optional: enable SHACL validation on the repository and load `shapes/shapes.ttl` into the SHACL shape graph (`http://rdf4j.org/schema/rdf4j#SHACLShapeGraph`). Then try importing `data/violations-demo.ttl` to see it rejected.
4. Run the queries in `queries/business-queries.rq` in the SPARQL editor.

Never load `violations-demo.ttl` into a production repository.

## Scope

- **In:** company, website, index-assigned country, ICB subsector (rolling up to industry), FY2024 revenue, dataset provenance.
- **Out:** reporting vs country currency, index membership over time, FX normalisation.
- **Remark on the numbers:** revenue is approximate, in each company's reporting currency (not converted), and not comparable across sectors. Sums are as reported.

## Caveats

- **ICB subsector codes are provisional.** They were chosen from the taxonomy labels based on each company's main business, not taken from FTSE Russell. To replace them, edit `data/icb-subsector-assignments.csv` and re-run the three scripts; the mapping refuses any code that does not roll up to the industry stated in CSV2.
## Namespaces

| Prefix | IRI |
| --- | --- |
| `gw:` | `https://graphwise.ai/ontology/` |
| `gwi:` | `https://graphwise.ai/instance/` |
| `icb:` | `https://graphwise.ai/taxonomy/icb/` |
| `wd:` | `http://www.wikidata.org/entity/` |

Ontology IRI `https://graphwise.ai/ontology/estx50`, version 1.0.0, licensed CC BY 4.0. Author: Peio Popov, Graphwise.
