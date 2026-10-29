# Part 2: Refine and iterate, Step 8

About 25 minutes. Learners go back to two earlier commits, where every test passed and the model was still wrong. Set up both stages first, as described in [Stages](README.md#stages).

> **Methodology step 8: Refine and iterate.**
> **Objective:** improve the ontology based on testing and feedback: find modelling problems and missing concepts, fix them, and "return to the step where the problem originated". Log each decision.
> **Deliverables:** refined ontology, updated documentation, version control.
> **Covered here:** two revisions, each traced to the step it came from, with a new test so the mistake cannot come back, and a new version where term IRIs changed.

The point of this part: a green test run only proves what the tests ask. Both mistakes were found by review, not by the tests.

---

## C8a. Revision 1: reuse nobody can see

> **Step 8, returning to Step 2 (reuse) and Step 7 (instances).** The reuse decision was right; the way the instances were typed hid it.

**Stage:** first build, `760d31f`, in `../estx50-first-build`.

**Goal:** see that reuse which exists only after reasoning is invisible to most consumers of the data.

**Do**

1. Run the first build's pipeline in its own folder:

   ```bash
   cd ../../estx50-first-build/tutorial
   ```

   ```bash
   python scripts/map_csv.py
   ```

   ```bash
   python scripts/run_tests.py
   ```

2. Go back to `main`'s tutorial folder, and run the C2 query against the first build, without and with reasoning:

   ```bash
   cd ../../ontology-data-products/tutorial
   ```

   ```bash
   python scripts/query.py guide/exercises/c2-reused-types.rq --root ../../estx50-first-build/tutorial
   ```

   ```bash
   python scripts/query.py guide/exercises/c2-reused-types.rq --root ../../estx50-first-build/tutorial --reason
   ```

**See**

- Step 1: `541 triples, 50 companies`, and `Track A 20/20, Track B 6/6`. Everything passes.
- Step 2, without reasoning: 0 for every reused class.

  ```text
  reusedClass                   instances
  ----------------------------  ---------
  schema:Corporation            0
  schema:Country                0
  fibo-ind-mkt-bas:EquityIndex  0
  (3 rows)
  ```

- Step 2, with reasoning: 50, 8 and 1, the same as `main`.

**What went wrong.** The instances were typed only `gw:Company`, `gw:Country` and `gw:StockIndex`. The link to schema.org and FIBO lived in `rdfs:subClassOf` axioms. GraphDB with OWL2-RL would infer the reused types; a plain triple store, a schema.org-aware crawler or an LLM reading the Turtle would not. To them, the data reused nothing. A second problem was found at the same time: the ontology declared `schema:legalName` and `schema:url` as OWL properties, which are claims about terms schema.org owns (and the `url` typing contradicted schema.org's own range).

**The fix**

- **Dual typing.** The mapping asserts the reused class next to the local one:

  ```turtle
  gwi:company-sap           a gw:Company , schema:Corporation .
  wd:Q183                   a gw:Country , schema:Country .
  gwi:index-euro-stoxx-50   a gw:StockIndex , fibo-ind-mkt-bas:EquityIndex .
  ```

  The `rdfs:subClassOf` axioms stay, so the two agree. Cost: 59 triples (541 → 600).
- **No declarations of terms we do not own.** The two `schema:` declarations were removed.
- **Rejected:** relying on reasoning only (visibility depends on the consumer's setup), and typing with the reused classes only (disjointness and SHACL targets would land on terms we do not own).

**Check:** two new tests, A1f (instances carry the reused class without a reasoner, and at least one of each exists, so the test cannot pass on empty data) and A1g (no external term is declared). Both were confirmed to fail on the first build before the fix. Track A goes from 20/20 to 22/22.

**Why:** [Step 8, Revision 1](../decision-log.md#step-8-refine-and-iterate).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask before showing the result: "Where would a crawler find out that SAP is a corporation?" Most people assume it is in the data.
- A1e already passed on the first build: it checked that each class *has* a reused superclass, not that the reuse reaches the data. A test can be true and still miss the point.

---

## C8b. Revision 2: the wrong "largest company"

> **Step 8, returning to Step 1 (scope), Step 3 (terms) and Step 5 (properties).** Reporting currency was enumerated in Step 3, put out of scope in Step 1, so no property was defined in Step 5. Revision 2 reversed the scope decision and added the property. The other three findings return to Step 2 (a reused term with the wrong meaning), Step 4 (class definitions) and Step 0 (the namespace).

**Stage:** Revision 1, `64207ac`, in `../estx50-revision-1`.

**Goal:** see a business question answered wrongly with every test green, and trace it to a column that was dropped.

**Do**

1. Run the Revision 1 pipeline:

   ```bash
   cd ../../estx50-revision-1/tutorial
   ```

   ```bash
   python scripts/map_csv.py
   ```

   ```bash
   python scripts/make_answer_key.py
   ```

   ```bash
   python scripts/run_tests.py
   ```

2. In `reports/test-report.md`, read B5 ("Which is the largest constituent by revenue?") and B2's row for Energy.
3. Find TotalEnergies in `data/EURO_STOXX_50_Constituents_CSV2.csv` and read the last two columns.
4. Back on `main`, list the five largest companies with their currencies:

   ```bash
   cd ../../ontology-data-products/tutorial
   ```

   ```bash
   python scripts/query.py guide/exercises/c8-largest.rq
   ```

**See**

- Step 1: `600 triples`, `Track A 22/22, Track B 6/6`.
- Step 2: B5 answers **TotalEnergies, 195.6**, and passes. B2 reports Energy as **284.4**.
- Step 3: `TotalEnergies,...,195.6,USD,EUR`. TotalEnergies reports in US dollars. The `Reporting currency` column was dropped by the mapping, so the graph could not show this.
- Step 4, on `main`:

  ```text
  company              revenue  currency
  -------------------  -------  --------
  TotalEnergies        195.6    USD
  Allianz              179.8    EUR
  Stellantis           156.9    EUR
  Mercedes-Benz Group  145.6    EUR
  BMW                  142.4    EUR
  (5 rows)
  ```

**What went wrong.** 5 of the 50 companies report in USD. B2, B3 and B5 summed and ranked dollars and euros together: Energy's 284.4 is 195.6 USD plus 88.8 EUR. TotalEnergies at 195.6 USD and Allianz at 179.8 EUR are close enough that which is "largest" depends on the exchange rate. The test still passed, because the answer key was computed from the CSV with the same mistake. Track B checks the graph against the key, not against the truth.

Review found three more problems in the same revision:

| Problem | Fix |
| --- | --- |
| `schema:legalName` held short names such as "Adidas", not legal names such as adidas AG | Use `schema:name`; real legal names can come later from a registry such as GLEIF |
| The `gw:Company` definition said "a constituent of the EURO STOXX 50", which builds in the membership that C4 keeps out of the class model | General definitions; membership stays in `gw:isConstituentOf` |
| Terms lived in the shared `https://graphwise.ai/ontology/` namespace, where they would clash with any other Graphwise ontology | Terms moved to `https://graphwise.ai/ontology/estx50/` |

**The fix**

- A new property, `gw:reportingCurrency` (ISO 4217 code, functional, required by SHACL as three capital letters).
- B2 and B3 group by currency. B5 ranks within each currency: Allianz 179.8 for EUR, TotalEnergies 195.6 for USD. The answer key was changed the same way, which is why it grows from 37 to 45 rows.
- Term IRIs changed, so the version goes from 1.0.0 to 2.0.0, with `owl:priorVersion` pointing back. Instance triples 600 → 650.
- FX conversion stays out of scope; the data says what it cannot answer instead of answering wrongly.

**Check:** SHACL requires exactly one reporting currency per company (A3a); B2, B3 and B5 are compared per currency. Track A 22/22, Track B 6/6.

**Why:** [Step 8, Revision 2](../decision-log.md#step-8-refine-and-iterate).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask before step 3: "The test passed. Is the answer right?" Let people find the currency column themselves.
- The lesson that carries over: a column dropped as "out of scope" can hide a wrong answer from every test, because the key and the graph lose the same information.
- Revision 2 changed one decision from Step 1: reporting currency moved from out of scope to in scope. Scope is a decision that can be revisited, and the log records both versions.
