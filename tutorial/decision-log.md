# Decision log: EURO STOXX 50 ontology tutorial

This log records what was decided at each step of the Graphwise ontology-engineer methodology, why, and what was rejected. Each step maps to one or two slides.

- **Author:** Peio Popov · Graphwise
- **Built:** 2026-10-28
- **Version:** ontology 1.0.0

---

## At a glance

- **Result:** a small OWL ontology plus SKOS taxonomy describing the 50 EURO STOXX 50 constituents.
- **Tests:** Track A (robustness) 22/22 passed; Track B (business questions) 6/6 passed.
- **Size:** 2,430 triples (ontology + ICB taxonomy + instances); 3,915 after OWL RL reasoning.
- **Revision 1 (Step 8):** reuse made visible without a reasoner. Instances now carry the schema.org and FIBO types directly, and the ontology no longer redeclares schema.org terms.
- **Core model:** 3 minted classes, 5 minted properties, 2 reused properties, 1 reused taxonomy (ICB, 249 concepts).
- **Biggest caveat:** ICB subsector assignments are provisional. They were chosen from the taxonomy labels, not taken from FTSE Russell.

---

## Step 0: Setup

**Goal:** a reproducible project skeleton.

**Decisions**

- **Namespaces.** `gw:` `https://graphwise.ai/ontology/`, `gwi:` `https://graphwise.ai/instance/`, `icb:` `https://graphwise.ai/taxonomy/icb/`.
  - Why: follows the Graphwise prompt template; `icb:` matches the supplied taxonomy file.
- **Tooling: Python with rdflib, pySHACL, owlrl and pyLODE; GraphDB loading is documented, not executed.**
  - Why: everything runs locally in about two seconds, with no server needed during a workshop.
  - Rejected: a live GraphDB instance, because it adds an install step for every participant.
- **Layout.** `data/`, `ontology/`, `shapes/`, `queries/`, `scripts/`, `reports/`, `docs/`. Generated files are never edited by hand.

**Produced:** project skeleton, `README.md`.

---

## Step 1: Domain, scope and competency questions

**Goal:** fix what the ontology must answer before modeling anything.

**Decisions**

- **Domain:** the 50 constituents of the EURO STOXX 50, with country, ICB classification and FY2024 revenue.
- **Out of scope, by agreement:**
  - reporting currency vs country currency (the two currency columns are dropped)
  - index membership over time (snapshot only)
  - FX normalization
  - revenue comparability modeling (it is a remark on the numbers, not part of the data)
- **Two test tracks.**
  - Track A checks that the model is built correctly (SHACL, SPARQL `ASK`, OWL RL).
  - Track B checks that it answers business questions (SPARQL `SELECT` against an answer key).
  - Why: "is it built right" and "is it the right thing" fail for different reasons and need different fixes.
- **The answer key is computed from the CSV, not from the graph** (`scripts/make_answer_key.py`).
  - Why: a key derived from the graph would test the graph against itself.

**Business questions (Track B)**

| # | Question |
| --- | --- |
| B1 | Which constituents are banks? |
| B2 | Revenue by ICB industry, rolled up from subsectors |
| B3 | Revenue by country |
| B4 | Which countries' constituents span the most industries? |
| B5 | Largest constituent by revenue, with the comparability caveat |
| B6 | Where does a figure come from, and is it approximate? |

**Produced:** scope statement (README), `queries/answer-key.csv` (37 expected rows).

---

## Step 2: Reuse existing ontologies

**Goal:** mint as little as possible.

**Decisions**

| Need | Reused term | Rationale |
| --- | --- | --- |
| Industry classification | ICB SKOS taxonomy (`icb-skos.ttl`, 249 concepts) | Official structure; IRIs built from ICB codes are stable |
| Company | `schema:Corporation` (superclass) | Widely used; no import needed |
| Name, website | `schema:legalName`, `schema:url` | Direct fit |
| Country | `schema:Country` (superclass); Wikidata IRIs for the instances | Globally resolvable identifiers |
| Index | `fibo-ind-mkt-bas:EquityIndex` (superclass) | FIBO's equity index class, checked against the FIBO source on GitHub |
| Provenance | DCAT (`Dataset`, `Distribution`), PROV-O (`wasDerivedFrom`), Dublin Core | W3C standards for dataset metadata |

- **Align, don't import.** FIBO and schema.org are referenced with `rdfs:subClassOf`, with no `owl:imports`.
  - Why: FIBO's import closure is large and would swamp a 50-row tutorial.
  - Rejected: importing FIBO IND, because it is heavyweight for no gain in the competency questions.
- **Reuse is applied in three ways.** Each way decides whether the reused term shows up in the files or only after reasoning.

  | Mechanism | Terms | Visible in the plain data? |
  | --- | --- | --- |
  | Alignment: local class `rdfs:subClassOf` reused class | `schema:Corporation`, `schema:Country`, `fibo-ind-mkt-bas:EquityIndex` | Yes, through dual typing (Revision 1); before that, only after reasoning |
  | Direct use, no local wrapper | `schema:legalName`, `schema:url`, DCAT, PROV-O, Dublin Core, SKOS | Yes |
  | Reuse as data | ICB concepts, Wikidata country IRIs | Yes |

- **Do not redeclare terms we do not own** (Revision 1). The ontology types and labels only `gw:` terms; reused classes and properties are referenced, never declared.
- **ICB is loaded alongside the ontology, not imported.** It is a separate artifact with its own version (1.0.0) and FTSE Russell licensing.

**Produced:** reuse table (above), no `owl:imports` by design.

---

## Step 3: Enumerate terms

**Goal:** list the vocabulary before classifying anything.

**Terms collected:** company, website, country, index, constituent, industry, supersector, sector, subsector, ICB code, revenue, fiscal year, source dataset, approximation, reporting currency, country currency.

**Decisions**

- Every CSV column is listed with its fate: four are mapped, three ICB columns are cross-checked and then derived rather than stored, and two are dropped (see Step 7).
- Reporting currency and country currency were enumerated, then excluded by scope.
  - Why keep them in the list: so the exclusion is explicit and testable (A5b).

**Produced:** the term list above; the column map in `scripts/map_csv.py`.

---

## Step 4: Classes and hierarchy

**Goal:** the smallest class model that answers B1–B6.

**Decisions**

- **Three minted classes, each a subclass of a reused class.**

  | Class | Superclass |
  | --- | --- |
  | `gw:Company` | `schema:Corporation` |
  | `gw:Country` | `schema:Country` |
  | `gw:StockIndex` | `fibo-ind-mkt-bas:EquityIndex` |

  - Why minted: local constraints (disjointness, SHACL targets) should not assert anything about schema.org or FIBO.
  - Instances are typed with both the local and the reused class, e.g. `a gw:Company, schema:Corporation` (Revision 1).
- **Industry is a SKOS concept scheme, not an OWL class hierarchy** (methodology §4.4, §4.6).
  - Why: ICB is a terminological hierarchy; its levels carry no distinct properties.
  - Rejected: 249 OWL classes, which would make each company an instance of a class like "Banks" and blur instance and class.
- **No `EuroStoxx50Company` class** (methodology §4.5).
  - Why: membership changes when the index rebalances, so a class would have instances migrating in and out.
  - Instead: an `isConstituentOf` relation.
- **`gw:Company`, `gw:Country` and `gw:StockIndex` are pairwise disjoint** (`owl:AllDisjointClasses`).

**Produced:** classes in `ontology/estx50-ontology.ttl`.

**Checks:**
- A1c: no cycles.
- A1d: every class is justified.
- A1e: every class specialises a reused class.
- A1f: every instance also carries the reused superclass as an asserted type.
- A1g: no external terms are redeclared.

---

## Step 5: Properties

**Goal:** attach each property at the most general domain that is still correct.

**Decisions**

| Property | Kind | Domain → Range | Notes |
| --- | --- | --- | --- |
| `schema:legalName` | data, reused | Company → `xsd:string` | Also copied to `rdfs:label` for display |
| `schema:url` | reused | Company → IRI | Website as an IRI, not a string |
| `gw:country` | object, functional | Company → Country | Index-assigned country (see below) |
| `gw:icbSubsector` | object, functional | Company → `skos:Concept` | Always an 8-digit subsector |
| `gw:revenueFY2024` | data, functional | Company → `xsd:decimal` | Billions, as reported |
| `gw:isConstituentOf` / `gw:hasConstituent` | object, inverse pair | Company ↔ StockIndex | Methodology §5.1 example |

- **One country property, meaning the index-assigned country.**
  - Why: it is the only reading that holds for all 50 rows. CSV2 resolves Stellantis to Italy, and a `skos:scopeNote` records that Stellantis N.V. is legally domiciled in the Netherlands.
  - Rejected: separate domicile and headquarters properties, which no competency question needs.
- **Link to the 8-digit subsector; derive the higher levels.**
  - Why: one link supports every level through `skos:broader+`. This makes "which are banks?" (B1) and the industry roll-up (B2) real queries.
  - Rejected: storing industry, sector and supersector as well, which is redundant and can contradict itself.
- **Revenue is a plain decimal; comparability is a remark, not data.**
  - The caveat is an `rdfs:comment` on the property and part of the dataset's `dcterms:description`.
  - Rejected: an observation pattern with currency and fiscal period, which is out of scope.
- **Every minted term has `rdfs:label` and `skos:definition`.**

**Produced:** properties in `ontology/estx50-ontology.ttl`.

**Checks:** A1a labels and definitions; A1b domain and range declared, never `owl:Thing`.

---

## Step 6: Facets and constraints

**Goal:** decide which rules belong in OWL (open-world inference) and which in SHACL (closed-world validation).

**Decisions**

- **OWL:**
  - disjoint classes
  - functional `gw:country`, `gw:icbSubsector` and `gw:revenueFY2024`
  - the `isConstituentOf` / `hasConstituent` inverse pair
  - Why: these let a reasoner infer new facts or detect contradictions.
- **SHACL** (`shapes/shapes.ttl`), for each company:
  - exactly one name, website, country, subsector and revenue
  - revenue of 0 or more
  - at least one index
  - at least one source distribution
  - Why: OWL cannot say "must have" under the open-world assumption; SHACL can.
- **"Must be a subsector" is pure SHACL.** The classification must be a member of the `icb:subsectors` collection (`sh:inversePath skos:member`) and in `icb:scheme`.
  - Rejected: a regex on the 8-digit notation, because the collection membership states the intent directly.
- **Every constraint carries a human-readable `sh:message`,** so validation output works as teaching material.

**Produced:** `shapes/shapes.ttl`.

**Checks:** A2a–A2c on the OWL RL closure; A3a SHACL on the clean data.

---

## Step 7: Instances and testing

**Goal:** populate the model from CSV2 and prove it against both tracks.

**Decisions**

- **ICB subsector codes are provisional.** The user chose this option, since CSV2 carries only the 2-digit industry.
  - Each company was assigned the subsector matching its main business (`data/icb-subsector-assignments.csv`, one line of rationale each).
  - The mapping refuses any assignment that does not roll up to the industry stated in CSV2: 50 of 50 consistent.
  - The provisional status is recorded twice: in the dataset description, and as a `skos:editorialNote` on its own `dcat:Distribution`.
  - Borderline cases to verify against FTSE Russell:

    | Company | Assigned subsector | Note |
    | --- | --- | --- |
    | Siemens | Diversified Industrials | |
    | Adyen | Transaction Processing Services | Industrials |
    | Prosus | Consumer Digital Services | Technology |
    | Deutsche Börse | Investment Services | |
    | EssilorLuxottica | Medical Supplies | |
    | CRH | Building Materials: Other | |
    | Air Liquide | Specialty Chemicals | |

- **Instance IRIs.**
  - Companies: `gwi:company-<slug>` (ASCII slug of the name, e.g. `company-loreal`).
  - Index: `gwi:index-euro-stoxx-50`.
  - Countries: Wikidata (`wd:Q183` Germany, etc.) with the ISO 3166 alpha-2 code as `skos:notation`.
- **Columns:**
  - Mapped: Company, Website, Country, Revenue.
  - Cross-checked, then not stored: the three ICB industry columns, since they are derived.
  - Dropped: the two currency columns (out of scope).
- **Two source distributions** (the constituents CSV and the subsector assignments). Every company links to both with `prov:wasDerivedFrom`.
- **Planted violations live in a separate file** (`data/violations-demo.ttl`) so the clean data stays clean:
  1. missing country
  2. negative revenue
  3. classification at the industry level (`icb:30`) instead of a subsector

**Results**

- 50 rows → 50 companies; 600 instance triples (541 before Revision 1 added 59 type triples).
- **Track A: 22/22 passed.** The planted-violation file produces exactly 3 top-level SHACL violations, one per demo company.
- **Track B: 6/6 passed**, against the CSV-derived answer key:

  | # | Result |
  | --- | --- |
  | B1 | 7 banks: Banco Santander, BBVA, BNP Paribas, ING Group, Intesa Sanpaolo, Nordea Bank, UniCredit |
  | B2 | Consumer Discretionary 638.3 (9 companies), Financials 588.7 (11) … Real Estate 5.1 (1) |
  | B3 | Germany 1,000.2 (14), France 928.8 (17), Italy 369.9 (5) … |
  | B4 | France and Germany span 8 industries each; Belgium 1 |
  | B5 | TotalEnergies, 195.6, returned with the comparability caveat attached |
  | B6 | ASML traces to both distributions, both flagged approximate |

**Produced:** `scripts/map_csv.py`, `data/estx50-instances.ttl`, `data/violations-demo.ttl`, `scripts/run_tests.py`, `reports/test-report.md`, `reports/shacl-*.txt`.

---

## Step 8: Refine and iterate

**Goal:** fix what testing exposed.

**Findings and fixes**

| Finding | Cause | Fix |
| --- | --- | --- |
| The planted-violation test first reported 4 violations instead of 3 | pySHACL also reports the nested `sh:node` failure for `icb:30` as a detail result | Count only the report's top-level `sh:result`s. The nested detail stays in the report, where it explains *why* `icb:30` fails. |
| pyLODE 3.3 failed to start | Version conflict with its `kurra` dependency | Pinned `pylode==3.2.1` (recorded in the README) |
| No mapping defects found | The roll-up cross-check in the mapping script caught consistency up front | None needed |
| **Revision 1:** reuse was invisible without a reasoner. The plain data had 0 instances of `schema:Corporation`, `schema:Country` and `EquityIndex`; OWL RL inferred 50, 8 and 1. | Instances were typed only with the `gw:` classes; the reused classes were reachable only through `rdfs:subClassOf` | Dual typing in the mapping (see below) |
| **Revision 1:** the ontology contradicted its own rationale. It declared `schema:legalName a owl:DatatypeProperty` and `schema:url a owl:ObjectProperty`, which are claims about terms schema.org owns. The `url` typing was also wrong: schema.org's range is the `URL` datatype. | Declarations added "for documentation" | Removed both declarations |
| **Revision 1:** no test checked that reuse actually reaches the data | A1e checked only that a superclass exists | Added A1f and A1g |

**Revision 1: reuse made visible without a reasoner**

- **Problem.** The reuse depended on reasoning. GraphDB with OWL2-RL would infer the schema.org and FIBO types. A plain triple store, a schema.org-aware crawler, or an LLM reading the TTL would not, so to them the data looked like it reused nothing.
- **Decision.** The mapping asserts the reused class next to the local one:

  ```turtle
  gwi:company-sap           a gw:Company , schema:Corporation .
  wd:Q183                   a gw:Country , schema:Country .
  gwi:index-euro-stoxx-50   a gw:StockIndex , fibo-ind-mkt-bas:EquityIndex .
  ```

  - The `rdfs:subClassOf` axioms stay, so the two are consistent, and a reasoner adds nothing new for these types.
  - Cost: 59 triples (50 + 8 + 1).
  - Rejected:
    - relying on reasoning only, which makes visibility depend on the consumer's setup
    - typing with the reused classes only, which would put disjointness and SHACL targets back on terms we do not own
- **Decision.** Remove the two `schema:` property declarations. The ontology now declares only `gw:` terms. Ontology triples: 68 → 64.
- **New tests.**
  - **A1f** runs on the plain data, with no reasoner. Every instance of a minted class must also carry that class's reused superclass, and at least one Corporation, Country and EquityIndex must exist, so the test cannot pass vacuously.
  - **A1g** checks that no external term is typed as a class or property in our files.
  - Both tests were confirmed to fail on the pre-revision state before the fix was applied.
- **Result.** Track A 22/22 (was 20/20); Track B unchanged at 6/6.

**Deferred candidates**

- `skos:altLabel` and definitions for ICB concepts: the taxonomy has none, and no competency question needs them yet.
- Verify the provisional subsector codes against FTSE Russell. Only `data/icb-subsector-assignments.csv` changes; re-run the pipeline.
- B7, natural-language versions of B1–B4 over GraphDB: needs a live endpoint and agent.

**Produced:** this changelog entry.

---

## Step 9: Document and deploy

**Goal:** make the result usable without this conversation.

**Decisions**

- **Ontology metadata:**
  - `owl:versionIRI` `https://graphwise.ai/ontology/estx50/1.0.0`
  - creator Peio Popov, publisher Graphwise, license CC BY 4.0
  - `vann:preferredNamespacePrefix` `gw`
- **HTML documentation** generated with pyLODE: `docs/estx50-ontology.html`.
- **GraphDB deployment is documented in the README, not executed.** Load order: ontology, ICB, instances, then shapes as a SHACL graph.

**Produced:** `README.md`, `docs/estx50-ontology.html`, this log.
