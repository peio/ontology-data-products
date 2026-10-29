# Decision log: FIBO mapping

This log records how the EURO STOXX 50 data was mapped to FIBO: which FIBO term was chosen for each concept, why, what was rejected, and which test guards each decision. The analysis behind it is in [`fibo-feasibility-study.md`](fibo-feasibility-study.md); the main tutorial log is [`decision-log.md`](decision-log.md).

- **Author:** Peio Popov · Graphwise
- **FIBO release:** 2026Q2 production (`ontologies/QuickFIBOProd.ttl`), with OMG Commons 1.3 and LCC 1.2
- **Ontology:** `https://graphwise.ai/ontology/estx50-fibo`, version 1.0.0 (`gwf:`); instances `gwfi:`
- **Commits:** `84783e3` FIBO variant (2026-10-28), `393b1cd` bridge from 2.0.0 (2026-10-29), `37e32b6` FIBO explorer (2026-10-29)

---

## At a glance

- **Result:** a standalone ontology next to 2.0.0 that uses FIBO, Commons and LCC terms directly and mints five terms.
- **Tests:** Track A 26/26, Track B 6/6 (`scripts/run_tests.py --variant fibo`); bridge 10/10 (`scripts/check_bridge.py`).
- **Reused directly:** 28 FIBO, Commons and LCC terms, plus 14 FIBO individuals: 8 countries, 2 currencies, 2 currency codes and the ICB scheme.
- **Minted:** `gwf:Revenue`, `gwf:hasRevenue`, `gwf:indexAssignedCountry`, `gwf:isConstituentOf`, `gwf:hasConstituent`.
- **Biggest caveats:** revenue amounts are in billions, against FIBO's convention, and the data is incomplete in FIBO's terms (no legal names, incorporation details or share data).

| Concept | FIBO term | Fit | Decision |
| --- | --- | --- | --- |
| Company | `fibo-be-le-cb:PubliclyHeldCompany` | High | [M1](#m1-company) |
| Index | `fibo-ind-mkt-bas:EquityIndex`, `fibo-ind-mkt-bas:hasIndexName` | High | [M2](#m2-index) |
| Index membership | local `gwf:isConstituentOf` (flat link) | — | [M3](#m3-index-membership-flat-link) |
| Country | `lcc-cr:Country`, `lcc-3166-1:` individuals | High | [M4](#m4-country) |
| Index-assigned country | local `gwf:indexAssignedCountry` ⊑ `cmns-loc:hasCountry` | Medium | [M4](#m4-country) |
| ICB subsector | `cmns-cls:isClassifiedBy`; `fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier` | High | [M5](#m5-icb-classification) |
| Revenue | local `gwf:Revenue` ⊑ `fibo-fnd-acc-cur:MonetaryAmount` | Medium | [M6](#m6-revenue) |
| Currency | `fibo-fnd-acc-cur:hasCurrency`, `fibo-fnd-acc-4217:Euro`, `fibo-fnd-acc-4217:USDollar` | High | [M6](#m6-revenue) |
| Fiscal year | `fibo-fnd-arr-doc:hasReportingPeriod`, `cmns-dt:ExplicitDatePeriod` | Medium | [M6](#m6-revenue) |
| Name | `cmns-dsg:hasTextualName` | Medium | [M7](#m7-name-and-website) |
| Website | `cmns-org:hasWebsite` | High | [M7](#m7-name-and-website) |

---

## V: How terms were verified

**Goal:** never use a FIBO term from memory or from its label alone.

**Decisions**

- **Every term is checked twice.**
  1. In the AI Ontologist FIBO term index: definition, parents, the restrictions inherited from them, domain and range.
  2. In `ontologies/QuickFIBOProd.ttl` (`owl:versionIRI <https://spec.edmcouncil.org/fibo/ontology/master/2026Q2/QuickFIBOProd/>`): the term or individual exists.
  - Why: labels mislead. "Has constituent" and "EUR" both look right and are wrong (see M3, M6).
- **Read what a term commits you to, not just its definition.** For each candidate class, the inherited restrictions were read up to the top of the hierarchy. That is how M1's caveat (FIBO's expectations the data cannot meet) and M3's structure (an index is a measure, not a collection) were found.
- **The build repeats the existence check.** `scripts/build_fibo_files.py` collects every FIBO, Commons and LCC IRI used in the ontology, the alignment, the instances and the shapes. It fails if any is missing from QuickFIBOProd, and fails if the file's version is not 2026Q2.
- **Only Release terms.** None of the FIBO terms used is marked Provisional.

**Known gaps in the checking:**
- The term index does not cover named individuals, so the ICB scheme, currencies and countries were confirmed in QuickFIBOProd only.
- The term checker flags `skos:broader` in SPARQL property paths as "used as a class". This is a false positive.

**Checks:** A1h (every FIBO term used is declared in the extract with a label); the build-time existence check.

---

## M1: Company

**Decision:** constituents are typed `fibo-be-le-cb:PubliclyHeldCompany`, used directly with no local class.

- Why: FIBO defines it as a "corporation whose shares are traded and held publicly", which is exactly what an index constituent is.
- Rejected:
  - `fibo-be-le-cb:StockCorporation`: correct, but less specific.
  - `fibo-sec-eq-eq:ShareIssuer`: in FIBO this is a role a company plays (it descends from `cmns-pts:PartyRole`), not the company itself.
  - A local `gwf:Company` class: unlike 2.0.0, the variant has no local disjointness or shape that would need to be kept off FIBO.
- **Consequence: incomplete, not inconsistent.** Through inheritance, FIBO expects a publicly held company to have:
  - a legal name
  - an incorporation date
  - an incorporation jurisdiction
  - a legal address
  - issued capital

  The source has none of these. Under OWL's open world this is incompleteness, not a contradiction. The shapes deliberately do not require them.
- **Checks:** A2a (all 50 companies are inferred as `cmns-org:LegalEntity` and `cmns-org:Organization`); A3a.

---

## M2: Index

**Decision:** the index is a `fibo-ind-mkt-bas:EquityIndex`, named with `fibo-ind-mkt-bas:hasIndexName`.

- Why: FIBO defines it as a "benchmark whose constituents are exclusively equity instruments". 2.0.0 already used it as the superclass of `gw:StockIndex`.
- Rejected: a local index class, for the same reason as in M1.
- Note: in FIBO an equity index is a measure (`fibo-ind-mkt-bas:ReferenceIndex` ⊑ `fibo-fnd-utl-alx:ScopedMeasure` ⊑ `cmns-qtu:Measure`). This matters for M3.

---

## M3: Index membership (flat link)

**Decision (D1):** a local `gwf:isConstituentOf` / `gwf:hasConstituent` links each company directly to the index. It has no FIBO super-property.

- Why: FIBO links an index to *shares*, not companies. The full path is index `fibo-fbc-dae-dbt:isBasedOn` → `fibo-ind-mkt-bas:BasketOfEquities` → `cmns-col:hasMember` → `fibo-sec-sec-bsk:SecuritiesBasketConstituent` → `cmns-col:comprises` → `fibo-sec-eq-eq:ListedShare` → `fibo-fnd-rel-rel:isIssuedBy` → share issuer role → `cmns-rlcmp:isPlayedBy` → company. The source has no ISIN, share class or exchange, so every share node on that path would be invented.
- Rejected:
  - The full FIBO path: about 5 resources per company, all but the company assumed rather than sourced.
  - `cmns-col:isConstituentOf` / `cmns-col:hasConstituent`: meant for parts that are not discrete elements (substances, composites), and declared disjoint with `cmns-col:hasMember`.
  - `cmns-col:isMemberOf`: an equity index is a measure in FIBO, not a collection (M2). Its members belong to the basket.
- **Consequence:** the definition of `gwf:isConstituentOf` names the full FIBO path, so a share layer can be added later without renaming anything.
- **Checks:** A2b (`gwf:hasConstituent` materialised for all 50 companies).

---

## M4: Country

**Decision (D4):** countries are LCC individuals (`lcc-3166-1:Germany` and so on), typed `lcc-cr:Country` by FIBO itself. Companies link to them with a local `gwf:indexAssignedCountry` ⊑ `cmns-loc:hasCountry` (functional).

- Why LCC: these are FIBO's own country individuals. All 8 countries in the data exist, and FIBO itself links to them with `cmns-loc:hasCountry`.
- Why a local property: `cmns-loc:hasCountry` only "indicates a country". The basis here is the index provider's assignment, which is ours to state.
- Rejected:
  - `cmns-org:isDomiciledIn`: legal domicile is a different fact. Stellantis N.V. is domiciled in the Netherlands but assigned to Italy.
  - `cmns-loc:Country` as the type: FIBO's country individuals are `lcc-cr:Country`, and FIBO has no alignment between the two classes.
  - Keeping Wikidata IRIs: not FIBO's countries. 2.0.0 keeps them.
- **Consequence: country names.** LCC's `rdfs:label` is the local-language name ("Deutschland"@de). Queries read `lcc-cr:hasEnglishShortName`, which for the Netherlands is "Netherlands (the)". That is the only difference between `answer-key-fibo.csv` and `answer-key.csv`.
- **Consequence: two country classes.** Through the range of `cmns-loc:hasCountry`, the reasoner also types LCC countries as `cmns-loc:Country`.
- **Checks:** A1i (assigned countries are LCC countries); A2d (`cmns-loc:hasCountry` inferred for all 50 companies); B3, B4.

---

## M5: ICB classification

**Decision:** companies link to their subsector with `cmns-cls:isClassifiedBy`. A generated alignment file additionally types all 249 ICB concepts as `fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier`, with `cmns-dsg:isDefinedIn` `fibo-sec-sec-cls:IndustryClassificationBenchmarkScheme`.

- Why: FIBO already expects `cmns-org:LegalEntity` `cmns-cls:isClassifiedBy min 0 fibo-fnd-arr-cls:IndustrySectorClassifier`. It has an ICB classifier class (abbreviated "ICB code") and an ICB scheme individual.
- What FIBO lacks:
  - the ICB codes themselves
  - a property for the classifier hierarchy

  So `icb-skos.ttl` stays unchanged, and roll-ups still follow `skos:broader`.
- Rejected:
  - A local `gwf:icbSubsector` subproperty: FIBO's own property fits. "Exactly one subsector" is enforced by a qualified SHACL count instead.
  - Editing `icb-skos.ttl`: it is a separate artifact with its own version and FTSE Russell's rights.
- **Consequence:** `cmns-cls:isClassifiedBy` is generic. A company classified under another scheme too (GICS, say) would still pass, because the shape counts only ICB subsectors.
- **Checks:** A4e (every ICB concept is a FIBO ICB classifier, and nothing else is); A5c; A3b (an industry-level classification is rejected).

---

## M6: Revenue

**Decision:** each revenue figure is a node. A local `gwf:Revenue` ⊑ `fibo-fnd-acc-cur:MonetaryAmount`, linked from the company by a local `gwf:hasRevenue`, carries exactly one:
- `fibo-fnd-acc-cur:hasAmount` (xsd:decimal, **in billions**, D3)
- `fibo-fnd-acc-cur:hasCurrency` (a FIBO currency)
- `fibo-fnd-arr-doc:hasReportingPeriod` (one shared `cmns-dt:ExplicitDatePeriod` labelled FY2024)

- Why a monetary amount: FIBO requires exactly one amount and one currency on it, which makes mixing currencies impossible by construction. That was the 2.0.0 Revision 2 problem.
- Why local terms: FIBO has no corporate-revenue, turnover or fiscal-year term, and no property linking an organization to its revenue.
- Rejected:
  - `fibo-fnd-oac-own:Income`: "revenue received during a period of time", i.e. cash received; reported revenue is recognised, not received.
  - Full amounts (34200000000): the user chose billions, as in the source.
- **Currency:**
  - Decision: `fibo-fnd-acc-4217:Euro` and `fibo-fnd-acc-4217:USDollar`, typed `fibo-fnd-acc-cur:Currency`.
  - Rejected: `fibo-fnd-acc-4217:EUR` and `fibo-fnd-acc-4217:USD`, which are currency *identifiers* (`fibo-fnd-acc-cur:CurrencyIdentifier`) that `cmns-id:identifies` the currency.
  - Queries read the ISO code through the identifier's `fibo-fnd-rel-rel:hasTag`.
- **Reporting period:** company fiscal years differ (Infineon's ends in September) and the source has no dates, so the FY2024 period has no start or end date.
- **Consequence: billions.** FIBO reads `fibo-fnd-acc-cur:hasAmount` in currency units. The scale is stated in the definition and label of `gwf:Revenue`, and revenue nodes are always typed `gwf:Revenue` as well as `fibo-fnd-acc-cur:MonetaryAmount`, so the scale travels with the node.
- **Checks:** A1f (revenue nodes carry both types); A1i (currencies are FIBO currencies, not codes); A5a (one revenue per company); A6c (the caveat and the billions scale are attached); A3b (negative revenue is rejected); B2, B3, B5.

---

## M7: Name and website

**Decision:** short names with `cmns-dsg:hasTextualName` (D5, default). Websites with `cmns-org:hasWebsite`, as `xsd:anyURI` literals.

- Why: the CSV holds short names ("SAP", "Siemens"), not legal names. `cmns-org:hasWebsite` has range `xsd:anyURI`.
- Rejected: `fibo-fnd-rel-rel:hasLegalName`, which would mislabel short names as legal names. It becomes the right choice once real legal names are sourced.
- **Consequence:** websites change from IRIs (2.0.0, `schema:url`) to literals.

---

## AR: Architecture

**AR1: standalone file, 2.0.0 untouched (D2).** New namespace `gwf:` and instance namespace `gwfi:`, so both variants can share a repository.
- Rejected:
  - Version 3.0.0 of the existing ontology: it would rewrite the tutorial's nine steps.
  - A thin alignment file over 2.0.0: it cannot align a plain revenue number with FIBO's amount-plus-currency node (M6).

**AR2: reference FIBO, do not import it.** A generated extract (`ontology/fibo-extract.ttl`, about 480 triples) carries the labels, definitions, named parents, domains and ranges of the terms used, up to the top of each hierarchy, plus the needed individuals. Restrictions are left out, and the MIT copyright notice is kept.
- Rejected: `owl:imports` of FIBO, which adds about 132,600 triples to a 50-company dataset.

**AR3: FIBO types are asserted on the instances.** No reasoner is needed to see them. This is the same choice as Revision 1 of 2.0.0.

**AR4: the shapes check the source, not FIBO.** They enforce what the data provides and leave FIBO's own cardinalities alone (M1).

**AR5: no merge with 2.0.0.**
- Rejected: one file holding both ontologies. It would hold two models of the same facts with duplicate labels, fail each suite's "declares no terms it doesn't own" check, and fold two versions into one.

---

## B: Bridge from 2.0.0 (2026-10-29)

**Decision:** an optional, separate file (`ontology/estx50-fibo-bridge.ttl`, 1.0.0) that mints nothing and holds four one-way links:

| 2.0.0 term | Bridged to |
| --- | --- |
| `gw:Company` | ⊑ `fibo-be-le-cb:PubliclyHeldCompany` |
| `gw:icbSubsector` | ⊑ `cmns-cls:isClassifiedBy` |
| `gw:country` | ⊑ `cmns-loc:hasCountry` |
| `gw:isConstituentOf` | ⊑ `gwf:isConstituentOf` |

- Why: 2.0.0 data becomes readable in FIBO terms, and both ontologies and test suites stay unchanged.
- Rejected:
  - Equivalence: it pushes FIBO data into the 2.0.0 classes, so the 2.0.0 shapes would start checking FIBO companies. It would also make the reasoner merge Wikidata and LCC countries through the two functional country properties. Test C4b fails when equivalence is swapped in.
  - `gw:country` ⊑ `gwf:indexAssignedCountry`: its range would type Wikidata IRIs as LCC countries.
- **Revenue** is converted by a SPARQL rule (`queries/bridge-revenue.rq`), because OWL cannot map a value on the company onto a path through a node.
- **Consequence:** bridged 2.0.0 data answers FIBO questions B1, B2, B5 and B6. B3 and B4 return nothing, because 2.0.0 countries are not LCC countries.
- **Checks:** C1a–C4b in `queries/bridge-tests.rq`.

---

## Open items

| Item | Why open | What would close it |
| --- | --- | --- |
| Legal names (D5) | The source has short names only | Source legal names (for example from GLEIF); switch to `fibo-fnd-rel-rel:hasLegalName` |
| Share layer (M3) | No ISIN, share class or exchange in the source | Add ISINs; model the FIBO basket path under the existing `gwf:isConstituentOf` |
| Fiscal-year dates (M6) | Fiscal years differ; the source has no dates | One period per company with its start and end dates |
| ICB subsectors | Provisional, chosen from the taxonomy labels | Verify against FTSE Russell (applies to both variants) |
| FIBO release | Pinned to 2026Q2 | Replace `QuickFIBOProd.ttl`, update the expected version in `build_fibo_files.py`, rebuild; the build fails on any term that moved |
