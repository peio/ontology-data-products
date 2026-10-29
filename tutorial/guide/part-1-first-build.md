# Part 1: Build and test, Steps 1–7

About 65 minutes, on `main`. Learners run the pipeline, then walk through the finished model one methodology step at a time. Module numbers match the step numbers of the [Graphwise ontology-engineer methodology](../../skills/graphwise-ontology-engineer/SKILL.md#workflow): C1 is Step 1, C7 is Step 7.

Each module opens with a box naming the step, its objective as the methodology states it, its expected deliverables, and what this module covers of them.

---

## C0. Setup and first run

> **Methodology step:** none; this is preparation. The methodology starts at Step 1.
> **Objective:** a reproducible project that runs end to end, so every later module starts from a green test run.

**Goal:** run the whole pipeline once.

**Do**

```bash
python scripts/map_csv.py
```

```bash
python scripts/make_answer_key.py
```

```bash
python scripts/run_tests.py
```

**See**

- `map_csv.py`: `Wrote data/estx50-instances.ttl: 650 triples, 50 companies from 50 rows`, then the fate of each of the 9 CSV columns.
- `make_answer_key.py`: `45 expected rows`, twice (the second file is for the FIBO variant in Part 4).
- `run_tests.py`: one `PASS` line per check, ending in `Track A 22/22, Track B 6/6`. The full report is in `reports/test-report.md`.

On Windows the paths print with backslashes.

**Check:** `run_tests.py` exits with code 0 only if every check passes.

**Why:** [Step 0](../decision-log.md#step-0-setup). Everything runs locally in seconds, so no one needs a database server during the workshop.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Show the three inputs first: `data/EURO_STOXX_50_Constituents_CSV2.csv` (50 rows, 9 columns), `data/icb-subsector-assignments.csv` (one subsector per company, with a reason) and `ontology/icb-skos.ttl` (the ICB industry taxonomy, 249 concepts).
- Generated files are never edited by hand: `data/estx50-instances.ttl`, `queries/answer-key.csv` and everything in `reports/`.
- The pipeline runs Step 7 (instances and tests) in seconds. The modules below explain the decisions behind what just ran, in methodology order.

---

## C1. Domain, scope and competency questions

> **Methodology step 1: Domain and scope.**
> **Objective:** establish the foundation and boundaries of the ontology: what it covers, what it is for, which questions it must answer, and who uses and maintains it.
> **Deliverables:** domain definition, scope boundaries, 5–10 competency questions, stakeholders.
> **Covered here:** domain, intended use, users and maintainer, scope and out-of-scope list, six competency questions, plus how they will be tested.

**Goal:** decide what the ontology must answer before modelling anything, and how to tell whether it does.

**Do**

1. Read the six competency questions, which the tutorial calls business questions:

   | # | Question |
   | --- | --- |
   | B1 | Which constituents are banks? |
   | B2 | Revenue by ICB industry and reporting currency, rolled up from subsectors |
   | B3 | Revenue by country and reporting currency |
   | B4 | Which countries' constituents span the most industries? |
   | B5 | Largest constituent by revenue in each reporting currency, with the comparability caveat |
   | B6 | Where does a figure come from, and is it approximate? |

2. Before running anything, guess how many of the 50 companies are banks. Then run:

   ```bash
   python scripts/query.py guide/exercises/c1-banks.rq
   ```

3. Open `queries/answer-key.csv` and find the B1 rows. Then open `scripts/make_answer_key.py` and find where B1 is computed.

**See**

```text
company          subsector
---------------  ---------
BBVA             Banks
BNP Paribas      Banks
Banco Santander  Banks
ING Group        Banks
Intesa Sanpaolo  Banks
Nordea Bank      Banks
UniCredit        Banks
(7 rows)
```

The answer key has the same seven names. `make_answer_key.py` gets them from the CSVs alone, by subsector codes that start with `3010`. It never reads the graph.

**Check:** Track B, B1 in `reports/test-report.md`.

**Why:** [Step 1](../decision-log.md#step-1-domain-scope-and-competency-questions).

- Two test tracks, because "is it built right?" (Track A) and "is it the right thing?" (Track B) fail for different reasons and need different fixes. The methodology calls competency questions "the litmus test"; Track B is that test, and Track A adds checks the methodology puts in Steps 4–7.
- The answer key comes from the CSV, not from the graph. A key computed from the graph would test the graph against itself.
- Out of scope, by agreement: country currency, index membership over time, FX conversion, modelling how comparable revenue figures are.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask: "If the answer key were wrong, would the test notice?" No. Track B is only as good as its key. C8b shows this happening.
- The banks query needs the ICB hierarchy, because the data stores only the subsector. That sets up C5.
- **Use, users, maintainer:** a teaching example for this workshop, used by its participants, maintained by Peio Popov (Graphwise). Ask: "How would the scope change if this were a production semantic layer for analysts?" Legal names, share data and membership history would come back into scope.

---

## C2. Reuse existing ontologies

> **Methodology step 2: Reuse.**
> **Objective:** leverage existing work and ensure interoperability; mint as little as possible.
> **Deliverables:** relevant existing ontologies, reuse strategy, gap analysis, import plan.
> **Covered here:** the reuse table, the reuse strategy (three ways of reusing), the gap (what had to be minted), and the import plan, which is deliberately empty.

**Goal:** use existing vocabularies wherever they fit, and see the three ways reuse can be applied.

**Do**

1. Open `ontology/estx50-ontology.ttl`. Find every term that does not start with `gw:` and note which vocabulary it comes from.
2. Count how many resources carry each reused class, first as stored, then with reasoning:

   ```bash
   python scripts/query.py guide/exercises/c2-reused-types.rq
   ```

   ```bash
   python scripts/query.py guide/exercises/c2-reused-types.rq --reason
   ```

**See:** the same counts both times.

```text
reusedClass                   instances
----------------------------  ---------
schema:Corporation            50
schema:Country                8
fibo-ind-mkt-bas:EquityIndex  1
(3 rows)
```

They match because each instance carries both its local and its reused class in the data (`a gw:Company, schema:Corporation`), so the reasoner has nothing to add. Hold on to this result: C8a runs the same query on the first build.

**The reuse table and the gap**

| Need | Reused | Gap: minted |
| --- | --- | --- |
| Industry classification | ICB SKOS taxonomy (249 concepts) | — |
| Company, country | `schema:Corporation`, `schema:Country`; Wikidata IRIs for countries | Local subclasses `gw:Company`, `gw:Country` |
| Index | `fibo-ind-mkt-bas:EquityIndex` (schema.org has no index class) | Local subclass `gw:StockIndex` |
| Name, website | `schema:name`, `schema:url` | — |
| Provenance | DCAT, PROV-O, Dublin Core | — |
| Country link, subsector link, revenue, currency, index membership | — | Six `gw:` properties (C5) |

**The three ways of reusing**

| How | Terms | Visible without a reasoner? |
| --- | --- | --- |
| Alignment: a local class `rdfs:subClassOf` a reused class | `schema:Corporation`, `schema:Country`, `fibo-ind-mkt-bas:EquityIndex` | Yes, because instances carry both types |
| Direct use, no local term | `schema:name`, `schema:url`, DCAT, PROV-O, Dublin Core, SKOS | Yes |
| Reuse as data | ICB concepts, Wikidata country IRIs | Yes |

**Check:** A1e (every minted class specialises a reused class), A1f (instances carry the reused class without a reasoner), A1g (the ontology declares no terms it does not own).

**Why:** [Step 2](../decision-log.md#step-2-reuse-existing-ontologies).

- **Align, don't import.** The import plan is "none, by design": there is no `owl:imports`. FIBO's import closure is large (all of FIBO, in `ontologies/QuickFIBOProd.ttl`, is about 132,600 triples), against 2,491 for the whole tutorial graph.
- **Don't redeclare terms you don't own.** The ontology types and labels only `gw:` terms.
- **ICB is loaded alongside, not imported.** It is a separate artifact with its own version and FTSE Russell's rights.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Learners will ask why the company is aligned to schema.org but the index to FIBO. Schema.org is the first choice where it fits, and it has no stock-index class; FIBO does.
- Reference copies of schema.org, DCAT, Dublin Core, PROV-O and SKOS are in `ontologies/` for looking terms up. They are not loaded.
- Part 4 redoes this step with a different strategy: FIBO terms used directly instead of aligned.

---

## C3. Enumerate terms

> **Methodology step 3: Enumerate terms.**
> **Objective:** a comprehensive vocabulary of the domain: every term, its properties and its relationships, *before* deciding what is a class and what is a property.
> **Deliverables:** term list, property inventory, relationship mapping.
> **Covered here:** the term list, the relationships between the terms, and the fate of every source column.

**Goal:** list everything the domain talks about, without classifying it yet.

**Do**

1. Read the 16 terms collected in this step:

   > company, website, country, index, constituent, industry, supersector, sector, subsector, ICB code, revenue, fiscal year, source dataset, approximation, reporting currency, country currency

2. For each term, predict what it will become in the model: a class, a property, a value from a taxonomy, a note, or nothing. Keep your answers for the table below.
3. Look at the column map that `map_csv.py` printed in C0, or at `COLUMN_MAP` in `scripts/map_csv.py`. For each of the 9 columns, say whether it is mapped, cross-checked and derived, or dropped.

**See**

What the 16 terms became (by the end of Revision 2):

| Term | Became | Decided in |
| --- | --- | --- |
| company, country, index | Classes `gw:Company`, `gw:Country`, `gw:StockIndex` | Step 4 |
| constituent | A relation, `gw:isConstituentOf`, not a class | Step 4 |
| industry, supersector, sector, subsector | Levels of the ICB SKOS taxonomy: values, not classes | Step 4 |
| ICB code | `skos:notation` on each ICB concept | Step 2 (reused) |
| website, revenue | Properties `schema:url`, `gw:revenueFY2024` | Step 5 |
| reporting currency | Property `gw:reportingCurrency` (out of scope until Revision 2) | Step 8 |
| fiscal year | Part of the property name `revenueFY2024` (a deferred candidate) | Step 5 |
| source dataset | `dcat:Dataset` and two `dcat:Distribution`s | Step 7 |
| approximation | A caveat in the dataset description and on the revenue property | Step 5 |
| country currency | Nothing: out of scope | Step 1 |

| Column | Fate |
| --- | --- |
| Company, Website, Country, Revenue, Reporting currency | Mapped |
| ICB Industry, ICB code, ICB concept IRI | Cross-checked against the subsector, then not stored: they are derived |
| Country currency | Dropped: out of scope |

**Check:** A5b (every CSV column is either mapped or intentionally dropped).

**Why:** [Step 3](../decision-log.md#step-3-enumerate-terms). Excluded terms stay on the list so the exclusion is explicit and testable.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask: "Why list a column you are going to drop?" So the exclusion is explicit. A5b fails if a column appears in the CSV without a fate.
- The relationships between the terms (company is assigned to a country, is classified in a subsector, is a constituent of an index, reports revenue) are listed in [Step 3](../decision-log.md#step-3-enumerate-terms) of the log. Ask learners to draw them before showing the table: each relationship becomes a property in C5.

---

## C4. Classes and hierarchy

> **Methodology step 4: Classes and class hierarchy.**
> **Objective:** organise the concepts into a structured taxonomy: decide which terms are independent objects (classes), arrange them by "kind of", and declare which classes cannot share instances.
> **Deliverables:** class definitions, inheritance relationships, hierarchy validation.
> **Covered here:** the development approach (bottom-up); three classes, each under a reused class; disjointness; two rejected designs; SKOS for the terminological hierarchy.

**Goal:** keep the class model as small as the questions allow.

**Do**

```bash
python scripts/query.py guide/exercises/c4-classes.rq
```

**See**

```text
class          superclass                    definition
-------------  ----------------------------  ---------------------------------------------------------------
gw:Company     schema:Corporation            A company whose shares are listed on a stock exchange.
gw:Country     schema:Country                A sovereign country. Instances are Wikidata country IRIs.
gw:StockIndex  fibo-ind-mkt-bas:EquityIndex  An equity market index whose constituents are listed companies.
(3 rows)
```

The three classes are declared pairwise disjoint (`owl:AllDisjointClasses`): nothing can be both a company and a country.

**Check:** A1c (no cycles), A1d (every class is the domain or range of a property), A2a (no individual is in two disjoint classes after reasoning).

**Why:** [Step 4](../decision-log.md#step-4-classes-and-hierarchy). Two designs were rejected; each applies a rule from the methodology:

- **A `EuroStoxx50Company` class.** "A class to which an individual instance belongs should not change often" (methodology §4.5). Membership changes when the index rebalances, so companies would move in and out of the class. Membership is a relation instead (`gw:isConstituentOf`, C5). No class definition mentions the index.
- **249 OWL classes for ICB.** "Classes in terminological hierarchies do not have to introduce new properties" (§4.4), but turning ICB into classes would make each company an instance of a class like "Banks", blurring things and categories (§4.6). ICB stays a SKOS taxonomy: a hierarchy of concepts linked by `skos:broader`, as the skill prescribes for hierarchies that are not kind-of.

The three classes are minted, rather than using schema.org and FIBO directly, so that local rules (disjointness, SHACL targets) say nothing about terms other people own. Each adds no properties of its own; the methodology's quality bar accepts that when the subclass is justified, and the justification is recorded in each class's `rdfs:comment`.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- **Development approach: bottom-up.** The classes came from what the source rows describe (company, country, index) and were then placed under more general reused classes. Ask: "What would top-down have looked like?" Starting from a general class such as organization and specialising it, which the reused vocabularies already do.

---

## C5. Properties

> **Methodology step 5: Properties.**
> **Objective:** specify the attributes and relationships of each class, attached at the most general class that genuinely has them, with domain, range, inverses and functional properties declared.
> **Deliverables:** property definitions, domain and range, property characteristics.
> **Covered here:** six minted and two reused properties; domain and range for each; one inverse pair; four functional properties.

**Goal:** attach each fact at the right level, and store only what cannot be derived.

**Do**

1. Follow Siemens from its subsector up to its industry:

   ```bash
   python scripts/query.py guide/exercises/c5-siemens-path.rq
   ```

2. In `ontology/estx50-ontology.ttl`, read the `skos:scopeNote` of `gw:country`.

**See**

```text
code      label
--------  -----------------------------
50203000  Diversified Industrials
502030    General Industrials
5020      Industrial Goods and Services
50        Industrials
(4 rows)
```

Only the first row is stored. The other three are reached through `skos:broader`. The scope note says the country is the one the index provider assigns: Stellantis N.V. is legally domiciled in the Netherlands but assigned to Italy.

**The properties**

| Property | Links | Characteristics |
| --- | --- | --- |
| `schema:name`, `schema:url` | Company → name, website | Reused directly |
| `gw:country` | Company → Country | Functional; the index-assigned country |
| `gw:icbSubsector` | Company → ICB concept | Functional; always an 8-digit subsector |
| `gw:revenueFY2024` | Company → decimal | Functional; billions, as reported |
| `gw:reportingCurrency` | Company → ISO 4217 code | Functional; added in Revision 2 (C8b) |
| `gw:isConstituentOf` / `gw:hasConstituent` | Company ↔ Stock index | Inverse pair (methodology §5.1) |

**Check:** A1a (labels and definitions), A1b (domain and range declared, never `owl:Thing`), A5c (every subsector rolls up to the industry stated in the CSV), A2b (`hasConstituent` is inferred for all 50 companies).

**Why:** [Step 5](../decision-log.md#step-5-properties).

- Link to the subsector and derive the rest. Storing industry, sector and supersector too would be redundant and could contradict itself.
- One country property with one meaning, because it is the only reading that holds for all 50 rows. Separate domicile and headquarters properties were rejected: no question needs them (§4.7, limiting the scope).
- Revenue is a plain number next to its currency. An observation pattern with a fiscal period was rejected for one figure per company (a deferred candidate if a second year is added).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- **Naming conventions** (methodology §6, and a phase of its own in the Graphwise "Ontology Development 101" deck) are recorded in [Step 5](../decision-log.md#step-5-properties) of the log: classes in UpperCamelCase and singular, properties in lowerCamelCase, instance IRIs as `gwi:<kind>-<slug>`. Show them here, then discuss the one exception: `revenueFY2024` puts a value (the year) into a property name, a deferred candidate.

---

## C6. Facets and constraints

> **Methodology step 6: Facets and constraints.**
> **Objective:** specify cardinalities, value types, allowed values, ranges and patterns, as SHACL shapes, with OWL restrictions only where reasoning needs them.
> **Deliverables:** constraint definitions, value types, validation rules.
> **Covered here:** which rules go in OWL and which in SHACL; the SHACL shapes; seeing each kind of rule react to broken data.

**Goal:** see which rules belong in OWL and which in SHACL, by breaking the data.

**Do**

1. Open `shapes/shapes.ttl` and `data/violations-demo.ttl`: three companies, each broken in one way (no country, negative revenue, classified at industry level). Open `reports/shacl-violations-demo.txt`, which `run_tests.py` wrote in C0.
2. Experiment: a company with two countries. Ask first whether the reasoner thinks Germany and France are the same:

   ```bash
   python scripts/query.py guide/exercises/c6-same-country.rq --reason
   ```

3. Append the block in `guide/exercises/c6-two-countries.ttl` to the end of `data/violations-demo.ttl`. Ask again, and run the tests:

   ```bash
   python scripts/query.py guide/exercises/c6-same-country.rq --reason --add data/violations-demo.ttl
   ```

   ```bash
   python scripts/run_tests.py
   ```

4. Undo the experiment:

   ```bash
   git restore data/violations-demo.ttl
   ```

**See**

- Step 1: three violations, each with a plain-language message, for example `A company needs exactly one country, typed gw:Country.` The industry-level one also shows a nested detail explaining that `icb:30` is not in the subsector collection.
- Step 2: `False`.
- Step 3: `True`. `gw:country` is functional, so OWL concludes that the two countries must be the same individual. It raises no error. SHACL does: the tests end in `Track A 21/22`, with A3b failing on four focus nodes instead of three, and `reports/shacl-violations-demo.txt` shows `demo-two-countries` with the "exactly one country" message.

**Check:** A3a (the 50 companies conform), A3b (exactly 3 violations, one per demo company), A2a and A2c (no disjointness clashes or merged companies after reasoning).

**Why:** [Step 6](../decision-log.md#step-6-facets-and-constraints).

| Rule | Where | Why there |
| --- | --- | --- |
| Disjoint classes, functional properties, inverse pair | OWL | A reasoner uses them to infer facts or detect contradictions |
| Exactly one name, website, country, subsector, revenue, currency | SHACL | OWL's open world cannot say "must have"; SHACL checks the data as it is |
| Revenue ≥ 0; currency is three capital letters | SHACL | Value range and pattern facets |
| Classification is an ICB subsector | SHACL | Checked as membership of the subsector collection, which states the intent better than a pattern on 8-digit codes |

Every constraint has a human-readable `sh:message`, so the report can be read by people who don't know SHACL. All OWL used stays within OWL 2 RL, as the skill requires.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- `violations-demo.ttl` is a teaching aid. Never load it into a real repository.

---

## C7. Instances and testing

> **Methodology step 7: Instances and test.**
> **Objective:** populate the ontology with representative data and check it against the competency questions; find modelling errors.
> **Deliverables:** instance data, test results per competency question, validation report.
> **Covered here:** how the CSV becomes instances (identifiers, types, provenance, the subsector cross-check), and reading the results of both test tracks.

**Goal:** see the decisions inside the mapping, and read the test results as the methodology's validation report.

**Do**

1. Open `data/estx50-instances.ttl` and find SAP (`gwi:company-sap`).
2. Open `scripts/map_csv.py`. Find the country table (`COUNTRIES`), the identifier rule (`slug`) and the subsector cross-check (`industry_of`).
3. Break the cross-check: in `data/icb-subsector-assignments.csv`, change SAP's subsector from `10101015` (Software) to `30101010`, a Financials code. Run the mapping, then undo:

   ```bash
   python scripts/map_csv.py
   ```

   ```bash
   git restore data/icb-subsector-assignments.csv
   ```

4. Open `reports/test-report.md` and read Track B: each question with its actual and expected rows.

**See**

Step 1:

```turtle
gwi:company-sap a gw:Company,
        schema:Corporation ;
    rdfs:label "SAP" ;
    prov:wasDerivedFrom gwi:distribution-csv2,
        gwi:distribution-icb-assignments ;
    gw:country wd:Q183 ;
    gw:icbSubsector icb:10101015 ;
    gw:isConstituentOf gwi:index-euro-stoxx-50 ;
    gw:reportingCurrency "EUR"^^xsd:string ;
    gw:revenueFY2024 34.2 ;
    schema:name "SAP"^^xsd:string ;
    schema:url <https://www.sap.com> .
```

Step 3: the mapping refuses to write anything.

```text
Mapping errors:
  SAP: subsector 30101010 does not roll up to https://graphwise.ai/taxonomy/icb/10
```

**The instance decisions**

| Decision | Choice |
| --- | --- |
| Company identifiers | `gwi:company-<slug>`, an ASCII slug of the name (`company-loreal`) |
| Countries | Wikidata IRIs (`wd:Q183` is Germany), with the ISO code as `skos:notation` |
| Types | Local and reused class together (C2, C8a) |
| Subsectors | Provisional, from the taxonomy labels; refused unless they roll up to the industry in the CSV |
| Provenance | Every company links to both source files (`prov:wasDerivedFrom`); the provisional status is stated on the assignments file |
| Broken examples | In a separate file (`violations-demo.ttl`), so the clean data stays clean |

**Check:** A5a (exactly 50 companies), A5c (50 of 50 subsectors consistent), A6a (every company traces to a source distribution), and Track B 6/6: one result per competency question, as Step 7 asks.

**Why:** [Step 7](../decision-log.md#step-7-instances-and-testing).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- The methodology says "representative instances"; here the instances are the full dataset, all 50 companies. With real data there is no need to invent samples, and the answer key can be computed from it.
- Borderline subsector choices to verify against FTSE Russell are listed in the decision log (Siemens, Adyen, Prosus, Deutsche Börse, EssilorLuxottica, CRH, Air Liquide).
- The provisional subsectors are assumption AS1 in the log's [assumption register](../decision-log.md#assumption-register), next to the others the data depends on: approximate figures, the index-assigned country, differing fiscal years. Ask learners which assumption would hurt most if wrong.
- Everything passes. Part 2 shows that "everything passes" is where Step 8 starts, not where it ends.
