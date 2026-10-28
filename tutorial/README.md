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
| [5. Properties](decision-log.md#step-5-properties) | Country, ICB subsector, revenue and its currency, index membership | Properties in `ontology/estx50-ontology.ttl` |
| [6. Facets and constraints](decision-log.md#step-6-facets-and-constraints) | OWL for inference, SHACL for validation | Facets in `ontology/estx50-ontology.ttl`, `shapes/shapes.ttl` |
| [7. Instances and testing](decision-log.md#step-7-instances-and-testing) | Map CSV to RDF, plant violations, run both tracks | `data/estx50-instances.ttl`, `data/violations-demo.ttl`, `queries/*.rq`, `scripts/run_tests.py`, `reports/` |
| [8. Refine and iterate](decision-log.md#step-8-refine-and-iterate) | Fix what the tests exposed; Revision 1 makes reuse visible without a reasoner; Revision 2 stops mixing currencies and fixes names, definitions and the namespace | Changelog and Revision 1 in the decision log |
| [9. Document and deploy](decision-log.md#step-9-document-and-deploy) | Ontology metadata, HTML docs, GraphDB load | `docs/estx50-ontology.html`, this README |

## Contents

| Path | What it is |
| --- | --- |
| `ontology/estx50-ontology.ttl` | The ontology (TBox): 3 classes, 6 properties, metadata |
| `ontology/icb-skos.ttl` | ICB taxonomy as SKOS (249 concepts), reused unchanged |
| `ontologies/` | Reference copies of the reused standard vocabularies (schema.org, DCAT, Dublin Core, PROV-O, SKOS); not imported, see its [README](ontologies/README.md) |
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
| `docs/estx50-explorer.html` | Semantic-layer explorer: the CSV next to its meaning, one company as a row and a graph, the business questions, rules and ICB hierarchy. Open in a browser |
| `docs/explorer-template.html` | Page template for the explorer |
| `scripts/build_explorer.py` | Builds the explorer from the repository files |

## Run it

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python scripts/map_csv.py          # CSV -> data/estx50-instances.ttl
python scripts/make_answer_key.py  # CSV -> queries/answer-key.csv
python scripts/run_tests.py        # Track A + B -> reports/test-report.md
python -m pylode ontology/estx50-ontology.ttl -o docs/estx50-ontology.html
python scripts/build_explorer.py   # -> docs/estx50-explorer.html
```

Run from the `tutorial/` folder. `run_tests.py` exits non-zero if any check fails. Expected: Track A 22/22, Track B 6/6. With the pinned versions in `requirements.txt` the generated files reproduce byte for byte, apart from the date in `reports/test-report.md`. pyLODE is pinned to 3.2.1 because 3.3 fails on a `kurra` dependency conflict.

Reused classes are asserted directly on the instances (`a gw:Company, schema:Corporation`), so schema.org and FIBO types are visible even without a reasoner.

## Load into GraphDB

1. Create a repository with the **OWL2-RL** ruleset. This materialises `gw:hasConstituent` from `gw:isConstituentOf`; the schema.org and FIBO types are already asserted.
2. Import, in this order: `ontology/estx50-ontology.ttl`, `ontology/icb-skos.ttl`, `data/estx50-instances.ttl`.
3. Optional: enable SHACL validation on the repository and load `shapes/shapes.ttl` into the SHACL shape graph (`http://rdf4j.org/schema/rdf4j#SHACLShapeGraph`). Then try importing `data/violations-demo.ttl` to see it rejected.
4. Run the queries in `queries/business-queries.rq` in the SPARQL editor.

Never load `violations-demo.ttl` into a production repository.

## FIBO variant

A second, standalone ontology models the same data with FIBO, OMG Commons and LCC terms used directly. It sits next to 2.0.0, which is unchanged. The plan, every term choice and the terms that were rejected are in [`fibo-feasibility-study.md`](fibo-feasibility-study.md); the decisions are in the [decision log](decision-log.md#fibo-variant).

| Concept | 2.0.0 | FIBO variant |
| --- | --- | --- |
| Company | `gw:Company` ⊑ `schema:Corporation` | `fibo-be-le-cb:PubliclyHeldCompany` |
| Index | `gw:StockIndex` ⊑ `fibo-ind-mkt-bas:EquityIndex` | `fibo-ind-mkt-bas:EquityIndex`, named with `fibo-ind-mkt-bas:hasIndexName` |
| Country | Wikidata IRI via `gw:country` | LCC country (`lcc-3166-1:Germany`) via `gwf:indexAssignedCountry` ⊑ `cmns-loc:hasCountry` |
| ICB subsector | `gw:icbSubsector` | `cmns-cls:isClassifiedBy`; ICB concepts are also FIBO ICB classifiers |
| Revenue | `gw:revenueFY2024` + `gw:reportingCurrency` | a `gwf:Revenue` ⊑ `fibo-fnd-acc-cur:MonetaryAmount` node: `fibo-fnd-acc-cur:hasAmount` (**in billions**), `fibo-fnd-acc-cur:hasCurrency` (`fibo-fnd-acc-4217:Euro`), `fibo-fnd-arr-doc:hasReportingPeriod` |
| Name, website | `schema:name`, `schema:url` | `cmns-dsg:hasTextualName`, `cmns-org:hasWebsite` |
| Index membership | `gw:isConstituentOf` | `gwf:isConstituentOf` (local: FIBO only links an index to shares in a basket, which the source does not have) |

Only five terms are minted (`gwf:Revenue`, `gwf:hasRevenue`, `gwf:indexAssignedCountry`, `gwf:isConstituentOf`, `gwf:hasConstituent`). FIBO is referenced, not imported: `ontology/fibo-extract.ttl` carries the labels, definitions and parents of the 28 FIBO terms used and their ancestors, plus the 14 country, currency and scheme individuals, copied from FIBO 2026Q2.

| Path | What it is |
| --- | --- |
| `ontology/estx50-fibo-ontology.ttl` | The FIBO-variant ontology: 5 minted terms, metadata |
| `ontology/fibo-extract.ttl` | Generated FIBO extract (MIT, EDM Council / OMG) — do not edit by hand |
| `ontology/icb-fibo-alignment.ttl` | Generated: types the 249 ICB concepts as FIBO ICB classifiers — do not edit by hand |
| `data/estx50-fibo-instances.ttl` | Generated instance data — do not edit by hand |
| `data/violations-demo-fibo.ttl` | The three broken demo companies, in the FIBO model |
| `shapes/shapes-fibo.ttl` | SHACL shapes for the FIBO variant |
| `queries/robustness-tests-fibo.rq`, `queries/business-queries-fibo.rq` | Track A and Track B for the FIBO variant |
| `queries/answer-key-fibo.csv` | Track B expected results (as `answer-key.csv`, with LCC country names) |
| `reports/test-report-fibo.md` | Test report for the FIBO variant |
| `scripts/map_csv_fibo.py`, `scripts/build_fibo_files.py` | CSV → FIBO RDF; ICB alignment and FIBO extract |

Run it (after the main pipeline):

```bash
python scripts/map_csv_fibo.py          # CSV -> data/estx50-fibo-instances.ttl
python scripts/build_fibo_files.py      # -> ontology/icb-fibo-alignment.ttl, ontology/fibo-extract.ttl
python scripts/run_tests.py --variant fibo  # -> reports/test-report-fibo.md
python -m pylode ontology/estx50-fibo-ontology.ttl -o docs/estx50-fibo-ontology.html
```

`build_fibo_files.py` needs `ontologies/QuickFIBOProd.ttl` (FIBO 2026Q2) and fails if any FIBO term used in the ontology, data or shapes is not in it. The other steps do not need it. Expected: Track A 26/26, Track B 6/6.

To load it into GraphDB, use an OWL2-RL repository and import `ontology/estx50-fibo-ontology.ttl`, `ontology/fibo-extract.ttl`, `ontology/icb-skos.ttl`, `ontology/icb-fibo-alignment.ttl` and `data/estx50-fibo-instances.ttl`; the shapes are `shapes/shapes-fibo.ttl`. You can load `ontologies/QuickFIBOProd.ttl` instead of the extract, at the cost of about 132,000 extra triples. The two variants use different namespaces, so both can share a repository.

Caveats specific to the FIBO variant:

- **Billions.** FIBO reads `fibo-fnd-acc-cur:hasAmount` in currency units; here it is in billions, and this is stated only on `gwf:Revenue`. Never copy a `gwf:Revenue` amount onto a plain FIBO monetary amount.
- **Incomplete, not inconsistent.** FIBO expects a legal name, an incorporation date and jurisdiction, a legal address and issued capital for a publicly held company. The source has none of them, and the shapes do not require them.
- **Country names.** LCC's `rdfs:label` is in the local language ("Deutschland"@de); query the English name with `lcc-cr:hasEnglishShortName`. For the Netherlands it is "Netherlands (the)".

## Scope

- **In:** company, website, index-assigned country, ICB subsector (rolling up to industry), FY2024 revenue and its reporting currency, dataset provenance.
- **Out:** country currency, index membership over time, FX normalisation.
- **Remark on the numbers:** revenue is approximate, in each company's reporting currency (not converted), and not comparable across sectors. Sums are per currency, as reported.

## Caveats

- **ICB subsector codes are provisional.** They were chosen from the taxonomy labels based on each company's main business, not taken from FTSE Russell. To replace them, edit `data/icb-subsector-assignments.csv` and re-run the three scripts; the mapping refuses any code that does not roll up to the industry stated in CSV2.
## Namespaces

| Prefix | IRI |
| --- | --- |
| `gw:` | `https://graphwise.ai/ontology/estx50/` |
| `gwi:` | `https://graphwise.ai/instance/` |
| `icb:` | `https://graphwise.ai/taxonomy/icb/` |
| `wd:` | `http://www.wikidata.org/entity/` |
| `gwf:` | `https://graphwise.ai/ontology/estx50-fibo/` (FIBO variant) |
| `gwfi:` | `https://graphwise.ai/instance/estx50-fibo/` (FIBO variant) |

Ontology IRI `https://graphwise.ai/ontology/estx50`, version 2.0.0, licensed CC BY 4.0. FIBO variant: `https://graphwise.ai/ontology/estx50-fibo`, version 1.0.0, CC BY 4.0. Author: Peio Popov, Graphwise.
