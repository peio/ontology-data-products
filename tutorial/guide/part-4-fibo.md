# Part 4: The same data with FIBO

About 60 minutes, on `main`; F7 is optional. Learners rebuild nothing: the FIBO variant is already in the repository. They take it apart and compare it with 2.0.0.

**Framing.** Parts 1–3 reused vocabularies lightly: local terms placed under schema.org and FIBO classes. This part reuses deeply: FIBO, OMG Commons and LCC terms are used directly, and only five terms are minted. The business questions B1–B6 and the answer key stay the same, so the two models can be compared answer by answer.

**Where this sits in the methodology.** Part 4 re-enters the methodology at Step 2 with a different reuse strategy, the way Step 8 sends you back to the step a change belongs to. Step 1 (the competency questions) and Step 3 (the terms and columns) are reused unchanged. Steps 4–7 follow from the new reuse choice, and F6–F7 evaluate and connect the result.

| Step | Objective | Module |
| --- | --- | --- |
| 1. Domain and scope | Unchanged: the same six questions and answer key | — |
| 2. Reuse | Choose and verify FIBO terms; find the gaps | F1, F2, F3, F5 |
| 3. Enumerate terms | Unchanged: the same columns, new targets | F0 |
| 4. Classes | Use FIBO classes directly; mint only `gwf:Revenue` | F2, F4 |
| 5. Properties | Mint the properties FIBO lacks, under FIBO parents where one fits | F3, F4, F5 |
| 6. Facets and constraints | Shapes that check the source, not FIBO's own expectations | F2, F4 |
| 7. Instances and test | Map the CSV to FIBO terms; run both tracks | F0, F5 |
| 8. Refine and iterate | Compare the two models on the same questions | F6 |
| 9. Document and deploy | Explorer for the variant; connect it to 2.0.0 | F6, F7 |

The decisions behind this part are in the [FIBO decision log](../fibo-decision-log.md); the analysis that came first is in the [feasibility study](../fibo-feasibility-study.md).

**Prefixes you will meet**

| Prefix | Vocabulary |
| --- | --- |
| `fibo-…` | FIBO, the Financial Industry Business Ontology (EDM Council), release 2026Q2 |
| `cmns-…` | OMG Commons: organizations, classifiers, designators, locations, dates |
| `lcc-…` | OMG Languages, Countries and Codes: countries |
| `gwf:` | The five minted terms of the FIBO variant |
| `gwfi:` | Instances of the FIBO variant |

---

## F0. Setup and first run

> **Methodology step 7, for the variant (Step 3 unchanged).** Objective: populate the FIBO model from the same CSV and test it against the same questions.

**Goal:** build the FIBO variant and see it pass the same business questions.

**Do** (after the C0 pipeline)

```bash
python scripts/map_csv_fibo.py
```

```bash
python scripts/build_fibo_files.py
```

```bash
python scripts/run_tests.py --variant fibo
```

**See**

- `map_csv_fibo.py`: `871 triples, 50 companies from 50 rows`, then the fate of each column. Compare it with the column map from C0: the same columns, different targets. Revenue and currency now go to a node: `gwf:hasRevenue / fibo-fnd-acc-cur:hasAmount (billions)`.
- `build_fibo_files.py` (about 10 seconds, because it reads all of FIBO):
  - `icb-fibo-alignment.ttl: 504 triples`
  - `fibo-extract.ttl: 485 triples, 28 terms used directly, 76 classes and properties with their parents, 14 individuals`
- `run_tests.py --variant fibo`: `Track A 26/26, Track B 6/6`. The report is `reports/test-report-fibo.md`.

**Check:** the build fails if any FIBO, Commons or LCC term used in the ontology, data or shapes is missing from `ontologies/QuickFIBOProd.ttl`, or if that file is not FIBO 2026Q2. A1h checks that the extract declares every term used.

**Why:** [V](../fibo-decision-log.md#v-how-terms-were-verified) and [AR2](../fibo-decision-log.md#ar-architecture). FIBO is referenced, not imported: the extract carries the labels, definitions and parents of the terms used (485 triples) instead of all of FIBO (about 132,600).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- The FIBO variant is a separate ontology with its own namespace and version (1.0.0). 2.0.0 is untouched, and both can share one GraphDB repository ([AR1](../fibo-decision-log.md#ar-architecture)).
- `ontologies/QuickFIBOProd.ttl` is all of FIBO 2026Q2 in one file. Several exercises below load it with `--add`; each takes about 10 seconds.

---

## F1. Checking a term

> **Methodology step 2: Reuse.** Objective here: verify each candidate term against the standard itself, and find what it does not cover (the gap analysis).

**Goal:** never use a FIBO term on the strength of its label.

**Do**

1. Two FIBO individuals both look like "the euro". Which one is the currency?

   ```bash
   python scripts/query.py guide/exercises/f1-eur-or-euro.rq --variant fibo
   ```

2. Does FIBO have a term for a company's revenue? Search every class label in FIBO:

   ```bash
   python scripts/query.py guide/exercises/f1-revenue-in-fibo.rq --variant fibo --add ontologies/QuickFIBOProd.ttl
   ```

**See**

```text
individual              type                                 label
----------------------  -----------------------------------  -----
fibo-fnd-acc-4217:EUR   fibo-fnd-acc-cur:CurrencyIdentifier  EUR
fibo-fnd-acc-4217:Euro  fibo-fnd-acc-cur:Currency            Euro
(2 rows)
```

`EUR` is the code that identifies the currency; `Euro` is the currency. A revenue figure is in euros, not in a code.

```text
class                         label
----------------------------  ------------
fibo-sec-dbt-bnd:RevenueBond  revenue bond
fibo-fnd-oac-own:Income       income
(2 rows)
```

Neither fits. A revenue bond is a security. FIBO defines income as revenue *received* during a period, which is cash; reported revenue is recognised, whether or not the cash has arrived. So revenue gets a local term (F4).

**Check:** A1i (revenue currencies are FIBO currencies, not codes); the build-time existence check from F0.

**Why:** [V](../fibo-decision-log.md#v-how-terms-were-verified), [M6](../fibo-decision-log.md#m6-revenue).

- Every term was checked twice: in the AI Ontologist FIBO term index (definition, parents, inherited restrictions, domain and range) and in `QuickFIBOProd.ttl` (the term exists in this release).
- Read what a term commits you to, not only its definition. F2 shows what that means.
- Only Release terms are used; none is marked Provisional.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Participants do not have the AI Ontologist term index; `QuickFIBOProd.ttl` and the extract are enough for these exercises.
- Ask: "Which other label would you have trusted?" `cmns-col:hasConstituent` is the classic one, covered in F3.

---

## F2. What FIBO expects of a company

> **Methodology steps 2, 4 and 6.** Objective here: understand what a reused class commits you to (Step 2), use it as the class (Step 4), and decide which of its expectations the shapes enforce (Step 6).

**Goal:** see what a FIBO class commits you to, and why the data is incomplete but not wrong.

**Do**

1. Ask what SAP is once a reasoner follows FIBO's class hierarchy:

   ```bash
   python scripts/query.py guide/exercises/f2-companies-inferred.rq --variant fibo --reason
   ```

2. List what FIBO says every publicly held company must have, through every class above it:

   ```bash
   python scripts/query.py guide/exercises/f2-what-fibo-expects.rq --variant fibo --add ontologies/QuickFIBOProd.ttl
   ```

3. Compare that list with the columns of the CSV.

**See**

Step 1: the data says only `fibo-be-le-cb:PubliclyHeldCompany`; the reasoner adds eight more types.

```text
type
---------------------------------
fibo-be-le-cb:Corporation
fibo-be-le-cb:PubliclyHeldCompany
fibo-be-le-cb:StockCorporation
cmns-org:FormalOrganization
cmns-org:LegalEntity
cmns-org:LegalPerson
cmns-org:Organization
cmns-pts:Agent
cmns-pts:Party
(9 rows)
```

Step 2: eight facts FIBO expects, inherited from four of those classes.

```text
from                            property
------------------------------  ------------------------------------
fibo-be-le-cb:Corporation       fibo-be-le-cb:isIncorporatedIn
fibo-be-le-cb:Corporation       fibo-fnd-rel-rel:hasLegalName
fibo-be-le-cb:StockCorporation  fibo-be-le-cb:hasDateOfIncorporation
fibo-be-le-cb:StockCorporation  fibo-be-le-cb:hasIssuedCapital
fibo-be-le-cb:StockCorporation  cmns-rga:isGovernedBy
cmns-org:LegalEntity            fibo-be-le-lei:hasLegalAddress
cmns-org:LegalEntity            cmns-rga:isOrganizedIn
cmns-org:LegalPerson            cmns-rga:isRecognizedIn
(8 rows)
```

Step 3: the CSV has none of them.

**Why it is not an error.** OWL makes the open-world assumption: a missing legal name is unknown, not absent, so the data is *incomplete*, not *inconsistent*. A reasoner raises nothing. The SHACL shapes (`shapes/shapes-fibo.ttl`) check what the source provides and deliberately do not require these facts.

**Check:** A2a (all 50 companies are inferred as `cmns-org:LegalEntity` and `cmns-org:Organization`), A3a (the 50 companies conform to the shapes).

**Why:** [M1](../fibo-decision-log.md#m1-company), [AR4](../fibo-decision-log.md#ar-architecture).

- `PubliclyHeldCompany` is FIBO's "corporation whose shares are traded and held publicly", which is what an index constituent is.
- Rejected: `StockCorporation` (correct but less specific); `ShareIssuer` (in FIBO a role a company plays, not the company); a local company class (nothing local needs to be kept off FIBO, unlike in 2.0.0).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- This is the hidden cost of deep reuse: you inherit a model of what a complete company looks like. That is useful as a to-do list (legal names from GLEIF, for example), but it must be documented so nobody mistakes the data for complete.
- For the author: the decision log lists five expectations (legal name, incorporation date and jurisdiction, legal address, issued capital). FIBO 2026Q2 has eight; the log misses `isGovernedBy`, `isOrganizedIn` and `isRecognizedIn`.

---

## F3. Where FIBO does not fit: index membership

> **Methodology steps 2 and 5.** Objective here: recognise a gap in the reused model (Step 2) and fill it with the smallest local property that does not contradict it (Step 5).

**Goal:** recognise when a standard models the world differently from your data, and stop short of inventing facts.

**Do**

1. List every class above FIBO's equity index:

   ```bash
   python scripts/query.py guide/exercises/f3-what-an-index-is.rq --variant fibo
   ```

2. In `ontology/estx50-fibo-ontology.ttl`, read the `skos:scopeNote` and `rdfs:comment` of `gwf:isConstituentOf`.

**See**

```text
class                                label
-----------------------------------  -------------------
fibo-ind-mkt-bas:ReferenceIndex      reference index
fibo-fnd-utl-alx:ScopedMeasure       scoped measure
fibo-fnd-utl-alx:QualifiedMeasure    qualified measure
fibo-fnd-utl-alx:StatisticalMeasure  statistical measure
cmns-qtu:Measure                     measure
(5 rows)
```

In FIBO an equity index is a *measure*, not a collection. Its members belong to the basket it is based on, and those members are listed shares, not companies. FIBO's full path from the index to a company is:

index → basket of equities → basket constituent → listed share → share issuer role → company

**The decision (D1).** The source has no ISIN, share class or exchange, so every node between the index and the company would be invented. The variant mints a flat shortcut, `gwf:isConstituentOf`, with no FIBO parent, and writes the full path into its scope note so a share layer can be added later without renaming anything.

Rejected:

- The full FIBO path: about five resources per company, all but the company assumed rather than sourced.
- `cmns-col:isMemberOf`: it would make a company an element of a measure.
- `cmns-col:isConstituentOf`: meant for parts that are not discrete elements (substances, composites), and declared disjoint with `cmns-col:hasMember`. The label looks perfect; the definition rules it out.

**Check:** A2b (`gwf:hasConstituent` is inferred for all 50 companies).

**Why:** [M2](../fibo-decision-log.md#m2-index), [M3](../fibo-decision-log.md#m3-index-membership-flat-link).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask: "Would you add the share nodes with made-up identifiers to stay 'fully FIBO'?" The answer in this build is no: a standard is not a reason to state facts you do not have.

---

## F4. Revenue as a node

> **Methodology steps 4, 5 and 6.** Objective here: mint the one class FIBO lacks under a FIBO parent (Step 4), link it from the company (Step 5), and constrain it to exactly one amount, currency and period (Step 6).

**Goal:** see how FIBO's monetary amount prevents the Revision 2 mistake by construction, and what it costs.

**Do**

1. Look at SAP's revenue in the FIBO variant:

   ```bash
   python scripts/query.py guide/exercises/f4-revenue-node.rq --variant fibo
   ```

2. Compare it with 2.0.0, where SAP's revenue is two values on the company: `gw:revenueFY2024 34.2` and `gw:reportingCurrency "EUR"` (see C5).
3. In `ontology/estx50-fibo-ontology.ttl`, read the label, definition and scope note of `gwf:Revenue`.

**See**

```text
revenue                  amount  currency                code  period
-----------------------  ------  ----------------------  ----  ------
gwfi:revenue-sap-fy2024  34.2    fibo-fnd-acc-4217:Euro  EUR   FY2024
(1 rows)
```

The revenue is its own resource, typed both `gwf:Revenue` and `fibo-fnd-acc-cur:MonetaryAmount`, with exactly one amount, one currency and one reporting period. The ISO code is read through FIBO's currency identifier (F1).

**What it fixes.** FIBO's monetary amount always carries its currency, and the shapes require exactly one. An amount without a currency cannot pass validation, so the 2.0.0 Revision 2 mistake (C8b) cannot happen here.

**What it costs: billions.** FIBO reads `hasAmount` in the currency's units, so a FIBO-aware tool or an LLM would read 34.2 as 34.2 euros. The source gives billions, and the variant keeps them (D3). The scale is stated in the label ("revenue (billions)"), definition and scope note of `gwf:Revenue`, and every revenue node carries that type, so the scale travels with the figure.

**Check:** A1f (revenue nodes carry both types), A1i (currencies are FIBO currencies), A5a (exactly one revenue per company), A6c (the comparability caveat and the billions scale are attached), A3b (a negative amount is rejected).

**Why:** [M6](../fibo-decision-log.md#m6-revenue).

- `gwf:Revenue` and `gwf:hasRevenue` are local because FIBO has no corporate-revenue term and no property linking an organization to its revenue (F1).
- The FY2024 period has no start or end date: fiscal years differ (Infineon's ends in September) and the source gives no dates.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask: "Never copy a `gwf:Revenue` amount onto a plain FIBO monetary amount. Why?" Because the plain one would be read in euros, a factor of a billion off.
- This is the one place the variant goes against FIBO's convention. Discuss whether storing full amounts (34200000000) would have been better; it is listed as rejected in M6.

---

## F5. Countries and their names

> **Methodology steps 2 and 7.** Objective here: reuse a standard's own individuals as data (Step 2), and adapt the queries and answer key to them (Step 7).

**Goal:** see the small, practical cost of switching identifiers.

**Do**

1. List the names of the LCC countries in the data:

   ```bash
   python scripts/query.py guide/exercises/f5-country-names.rq --variant fibo
   ```

2. Compare the two answer keys:

   ```bash
   git diff --no-index queries/answer-key.csv queries/answer-key-fibo.csv
   ```

**See**

```text
country                 label          language  englishShortName
----------------------  -------------  --------  -----------------
lcc-3166-1:Belgium      Belgien        de        Belgium
lcc-3166-1:Belgium      Belgique (la)  fr        Belgium
lcc-3166-1:Belgium      België         nl        Belgium
lcc-3166-1:Finland      Suomi          fi        Finland
lcc-3166-1:Finland      Finland        sv        Finland
lcc-3166-1:France       France (la)    fr        France
lcc-3166-1:Germany      Deutschland    de        Germany
lcc-3166-1:Ireland      Ireland        en        Ireland
lcc-3166-1:Ireland      Éire           ga        Ireland
lcc-3166-1:Italy        Italia (l')    it        Italy
lcc-3166-1:Netherlands  Nederland      nl        Netherlands (the)
lcc-3166-1:Spain        España         es        Spain
(12 rows)
```

LCC's `rdfs:label` is the name in each country's own languages. Queries read `lcc-cr:hasEnglishShortName` instead, which for the Netherlands is "Netherlands (the)". The diff shows that this is the only difference between the two answer keys: three rows, all Netherlands.

**Check:** A1i (assigned countries are LCC countries), A2d (`cmns-loc:hasCountry` is inferred for every company), B3, B4.

**Why:** [M4](../fibo-decision-log.md#m4-country).

- LCC countries are FIBO's own country individuals, and all 8 in the data exist (D4). Wikidata IRIs, used in 2.0.0, are not FIBO's.
- The link is a local `gwf:indexAssignedCountry` under `cmns-loc:hasCountry`, because the basis (the index provider's assignment) is ours to state. `cmns-org:isDomiciledIn` was rejected: Stellantis is domiciled in the Netherlands but assigned to Italy.

**Decided by:** Subject Matter Expert.

**Instructor notes**

- A display label is not a stable key. Any query or report that matched "Netherlands" by name would silently lose a country.

---

## F6. The two models side by side

> **Methodology step 8 (and 9).** Objective here: evaluate the alternatives against the same questions. The methodology's first rule: there is no single correct way to model a domain; the best choice depends on the application.

**Goal:** compare the two ways of reusing on the same data.

**Do**

1. Build the FIBO explorer and open both explorers in a browser, side by side:

   ```bash
   python scripts/build_explorer.py --variant fibo
   ```

   `docs/estx50-explorer.html` (2.0.0) and `docs/estx50-fibo-explorer.html` (FIBO variant).

2. Pick one company and compare its row and its graph in the two pages.

**See:** `Wrote docs/estx50-fibo-explorer.html: 50 companies, 6 questions, 3 violations`, and the same answers to B1–B6 in both pages, apart from the Netherlands' name.

| Concept | 2.0.0 | FIBO variant |
| --- | --- | --- |
| Company | `gw:Company` ⊑ `schema:Corporation` | `fibo-be-le-cb:PubliclyHeldCompany` |
| Index | `gw:StockIndex` ⊑ `fibo-ind-mkt-bas:EquityIndex` | `fibo-ind-mkt-bas:EquityIndex` |
| Country | Wikidata IRI via `gw:country` | LCC country via `gwf:indexAssignedCountry` ⊑ `cmns-loc:hasCountry` |
| ICB subsector | `gw:icbSubsector` | `cmns-cls:isClassifiedBy`; ICB concepts are also FIBO ICB classifiers |
| Revenue | `gw:revenueFY2024` + `gw:reportingCurrency` on the company | a `gwf:Revenue` node with amount (billions), currency and period |
| Name, website | `schema:name`, `schema:url` (an IRI) | `cmns-dsg:hasTextualName`, `cmns-org:hasWebsite` (a literal) |
| Index membership | `gw:isConstituentOf` | `gwf:isConstituentOf` (local in both) |

| | 2.0.0 | FIBO variant |
| --- | --- | --- |
| Minted terms | 9 (3 classes, 6 properties) | 5 (1 class, 4 properties) |
| Instance triples | 650 | 871 |
| Track A / Track B | 22/22, 6/6 | 26/26, 6/6 |
| Needs FIBO to build | No | Yes, `QuickFIBOProd.ttl` |

**Check:** both test suites, `reports/test-report.md` and `reports/test-report-fibo.md`.

**Why:** [FIBO variant summary](../decision-log.md#fibo-variant), [AR1–AR5](../fibo-decision-log.md#ar-architecture).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Neither model is "right". Light reuse is quicker to build and easier to read; deep reuse speaks the industry's language and fixes the currency problem by construction, at the price of inherited expectations, a billions caveat and a FIBO release to track.
- The ICB taxonomy is the same file in both. FIBO has an ICB classifier class and an ICB scheme but no ICB codes and no hierarchy property, so roll-ups still use `skos:broader` ([M5](../fibo-decision-log.md#m5-icb-classification)).

---

## F7. Optional: a bridge between the two

> **Methodology step 9 (and 2).** Objective here: answer Step 9's "what integration is needed?" for two models of the same data, keeping Step 2's interoperability without merging them.

**Goal:** let 2.0.0 data be read in FIBO terms without merging the ontologies, and see why the links go one way only.

**Do**

1. Ask the banks question in FIBO terms only, on 2.0.0 data read through the bridge, first without and then with reasoning:

   ```bash
   python scripts/query.py guide/exercises/f7-banks-fibo.rq --variant bridge
   ```

   ```bash
   python scripts/query.py guide/exercises/f7-banks-fibo.rq --variant bridge --reason
   ```

2. Ask for companies per country, named the FIBO way, on the FIBO variant and then on the bridged 2.0.0 data:

   ```bash
   python scripts/query.py guide/exercises/f7-country-names-fibo.rq --variant fibo --reason
   ```

   ```bash
   python scripts/query.py guide/exercises/f7-country-names-fibo.rq --variant bridge --reason
   ```

3. Experiment: what if the bridge used equivalence? Load both datasets, count companies of each kind, then add `guide/exercises/f7-equivalence.ttl` and count again:

   ```bash
   python scripts/query.py guide/exercises/f7-count-companies.rq --variant bridge --reason --add data/estx50-fibo-instances.ttl
   ```

   ```bash
   python scripts/query.py guide/exercises/f7-count-companies.rq --variant bridge --reason --add data/estx50-fibo-instances.ttl guide/exercises/f7-equivalence.ttl
   ```

4. Run the full bridge checks:

   ```bash
   python scripts/check_bridge.py
   ```

**See**

- Step 1: 0 rows without reasoning; the same 7 banks with it. The bridge is four `rdfs:subClassOf` / `rdfs:subPropertyOf` links, which only take effect when a reasoner applies them.
- Step 2: 8 countries on the FIBO variant (France 17 … Belgium 1); 0 rows on bridged 2.0.0 data. Its countries stay Wikidata IRIs, which have no LCC English short name.
- Step 3: `gw:Company` 50 and `PubliclyHeldCompany` 100 with the one-way link; `gw:Company` 100 with equivalence. Equivalence pulls the FIBO variant's companies into the 2.0.0 class, so the 2.0.0 shapes would start checking companies that were never built for them.
- Step 4: `Bridge 10/10`. FIBO Track B on bridged 2.0.0 data: B1, B2, B5 and B6 give the FIBO answers; B3 and B4 return nothing, as expected.

**The bridge** (`ontology/estx50-fibo-bridge.ttl`) mints nothing and holds four one-way links:

| 2.0.0 term | Bridged to |
| --- | --- |
| `gw:Company` | ⊑ `fibo-be-le-cb:PubliclyHeldCompany` |
| `gw:icbSubsector` | ⊑ `cmns-cls:isClassifiedBy` |
| `gw:country` | ⊑ `cmns-loc:hasCountry` |
| `gw:isConstituentOf` | ⊑ `gwf:isConstituentOf` |

Revenue cannot be bridged in OWL: a number on the company cannot be mapped onto a path through a node. `queries/bridge-revenue.rq` converts it with a SPARQL rule instead, keeping the billions scale.

**Check:** C1a–C4b in `queries/bridge-tests.rq`, run by `check_bridge.py`. C4b checks that nothing in the FIBO variant's data becomes 2.0.0 data, which is what step 3 breaks.

**Why:** [B](../fibo-decision-log.md#b-bridge-from-200-2026-10-29).

- Rejected: equivalence (step 3; it would also make the reasoner merge Wikidata and LCC countries through the two functional country properties), and `gw:country` ⊑ `gwf:indexAssignedCountry` (its range would type Wikidata IRIs as LCC countries).
- Rejected: merging the two ontologies into one file, which would hold two models of the same facts and fold two versions into one ([AR5](../fibo-decision-log.md#ar-architecture)).

**Decided by:** Subject Matter Expert.

**Instructor notes**

- Ask: "Is a bridge that answers four of six questions a failure?" It does exactly what it says, and its test report says which questions it cannot answer and why. Compare with C8b, where a wrong answer passed silently.

---

## Wrap-up

| Lesson | Where |
| --- | --- |
| Check a term against the standard itself, not its label | F1 |
| A class brings expectations with it; under the open world, missing facts mean incomplete, not wrong | F2 |
| When the standard's model needs facts you don't have, use a documented shortcut instead of inventing them | F3 |
| A better structure can rule out a whole class of mistakes, and can bring its own caveats | F4 |
| Display names are not keys | F5 |
| Light and deep reuse are both valid; choose by audience and cost | F6 |
| Link models one way, and test that the link stays one way | F7 |
