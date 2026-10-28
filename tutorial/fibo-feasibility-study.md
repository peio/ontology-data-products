# Feasibility study: a FIBO-based EURO STOXX 50 ontology

Status: **implemented** on 2026-10-28 (decisions D1–D5 below); see the [README](README.md#fibo-variant) and the [decision log](decision-log.md#fibo-variant). Track A 26/26, Track B 6/6. Prefixes: `gwf:` for the five minted terms, `gwfi:` for instances.

Question: can the EURO STOXX 50 tutorial (CSV data + `ontology/estx50-ontology.ttl` 2.0.0) be rebuilt as a new ontology that reuses as much of FIBO as possible?

Answer: **yes, feasible.** Every concept in the data has a FIBO or OMG Commons/LCC home except three: revenue, the index-assigned country and (with the flat link chosen in D1) index membership. These need small local terms, two of them under FIBO parents.

## Decisions taken

| # | Question | Decision | Consequence |
|---|---|---|---|
| D1 | Depth of reuse | **Flat company-to-index link** | No basket, share, issuer-role or basket-constituent nodes. Index membership stays a local property (see "Index membership" below). FIBO is used for company, index, country, classification, money and website. |
| D2 | Namespace and version | **Separate file, named and namespaced as the FIBO-aligned version** | New file `ontology/estx50-fibo-ontology.ttl`, namespace `https://graphwise.ai/ontology/estx50-fibo/`, version 1.0.0. The 2.0.0 ontology, its data, tests and docs stay untouched. |
| D3 | Revenue amount | **Amounts in billions** | `fibo-fnd-acc-cur:hasAmount 34.2` means 34.2 billion. The scale goes in the definition of `gwf:Revenue` (see risk R5). |
| D4 | Countries | **Switch to FIBO (LCC) countries** | `lcc-3166-1:` individuals replace the Wikidata IRIs as country values. |
| D5 | Company name | *Not yet decided.* Default: `cmns-dsg:hasTextualName` for the short name | Change only if real legal names are sourced (then `fibo-fnd-rel-rel:hasLegalName`). |

D2 confirmed: a new, standalone ontology that uses FIBO terms directly. A thin alignment file over the unchanged 2.0.0 terms was considered and rejected: it would work for classes but not for revenue, because 2.0.0 stores revenue as a plain number on the company, and that number cannot be aligned to FIBO's amount-plus-currency node.

## How the terms were checked

Every term below was confirmed twice:

1. In the AI Ontologist FIBO term index (FIBO 2026Q2, Commons 1.3, LCC 1.2): definition, parents, inherited restrictions, domain and range.
2. In the bundled `ontologies/QuickFIBOProd.ttl` (versionIRI `.../master/2026Q2/QuickFIBOProd/`, 132,594 triples, 2,717 classes, 14,797 named individuals; parses in about 5 s with rdflib). All terms and individuals named below are present in that file.

All FIBO terms below are marked Release (stable). None are Provisional. The term index does not cover named individuals, so `fibo-sec-sec-cls:IndustryClassificationBenchmarkScheme` and the currency and country individuals were confirmed in `QuickFIBOProd.ttl` only.

## Term map

| Today (2.0.0) | New file (FIBO-aligned) | What FIBO means by it | Fit |
|---|---|---|---|
| `gw:Company` (⊑ `schema:Corporation`) | `fibo-be-le-cb:PubliclyHeldCompany` | "corporation whose shares are traded and held publicly" | High |
| `gw:StockIndex` (⊑ `fibo-ind-mkt-bas:EquityIndex`) | `fibo-ind-mkt-bas:EquityIndex` (used directly) | "benchmark whose constituents are exclusively equity instruments" | High |
| index name (`schema:name`) | `fibo-ind-mkt-bas:hasIndexName` | formal name of the index, domain `fibo-ind-mkt-bas:ReferenceIndex` | High |
| `gw:isConstituentOf` / `gw:hasConstituent` | **local** `gwf:isConstituentOf` / `gwf:hasConstituent`, no FIBO parent | see "Index membership" below | — |
| `gw:Country` (Wikidata IRIs) | `lcc-cr:Country`, individuals from `lcc-3166-1:` (all 8 exist: Belgium, Finland, France, Germany, Ireland, Italy, Netherlands, Spain) | country or dependent territory; FIBO itself links to these individuals with `cmns-loc:hasCountry` | High |
| `gw:country` (index-assigned country) | **local** `gwf:indexAssignedCountry` ⊑ `cmns-loc:hasCountry` | `cmns-loc:hasCountry` only says "indicates a country"; the index-provider basis is ours | Medium |
| `gw:icbSubsector` | `cmns-cls:isClassifiedBy` | FIBO already expects `cmns-org:LegalEntity` `cmns-cls:isClassifiedBy min 0 fibo-fnd-arr-cls:IndustrySectorClassifier` | High |
| ICB concepts (`icb:` SKOS) | additionally typed `fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier`, `cmns-dsg:isDefinedIn` `fibo-sec-sec-cls:IndustryClassificationBenchmarkScheme` (an individual in FIBO) | FIBO has an ICB classifier class and an ICB scheme individual, but **no ICB codes** and **no classifier hierarchy property** | High; keep `skos:broader` for roll-ups |
| `gw:revenueFY2024` + `gw:reportingCurrency` | **local** `gwf:Revenue` ⊑ `fibo-fnd-acc-cur:MonetaryAmount`, with `fibo-fnd-acc-cur:hasAmount` (xsd:decimal, in billions), `fibo-fnd-acc-cur:hasCurrency` (`fibo-fnd-acc-4217:Euro`, `fibo-fnd-acc-4217:USDollar`), `fibo-fnd-arr-doc:hasReportingPeriod` a `cmns-dt:ExplicitDatePeriod` | FIBO has no corporate-revenue or fiscal-year term. `fibo-fnd-acc-cur:MonetaryAmount` requires exactly one amount and one currency, which stops currencies being mixed by construction | Medium |
| company → revenue | **local** `gwf:hasRevenue` (range `gwf:Revenue`) | no FIBO property links an organization to its revenue | — |
| `schema:name` on companies | `cmns-dsg:hasTextualName` (D5 default) | a name or appellation. The CSV holds short names ("SAP"), so `fibo-fnd-rel-rel:hasLegalName` would be wrong | Medium |
| `schema:url` | `cmns-org:hasWebsite` | range `xsd:anyURI` (a literal, not an IRI: a data change) | High |
| DCAT / PROV-O provenance, ICB SKOS scheme | unchanged | FIBO does not replace these | — |

### Index membership (flat link, D1)

No FIBO or Commons property fits a direct company-to-index link, so `gwf:isConstituentOf` stays local and gets no FIBO super-property:

- In FIBO an equity index is a *measure* (`fibo-ind-mkt-bas:EquityIndex` ⊑ `fibo-ind-mkt-bas:ReferenceIndex` ⊑ `fibo-fnd-utl-alx:ScopedMeasure` ⊑ `cmns-qtu:Measure`), not a collection. Its members belong to the basket it is based on (`fibo-ind-mkt-bas:BasketOfEquities`), and those members are shares, not companies.
- `cmns-col:isMemberOf` ("is a discrete element of") would therefore say the company is an element of a measure, which contradicts FIBO's model.
- `cmns-col:isConstituentOf` is for parts that are not discrete elements, and its inverse is declared disjoint with `cmns-col:hasMember`.

The definition of `gwf:isConstituentOf` should say it is a shortcut for FIBO's path (index → basket of equities → basket constituent → listed share → issuer role → company), so the new file can be extended later without renaming anything.

### Terms looked at and rejected

| Term | Why not |
|---|---|
| `cmns-col:hasConstituent` / `cmns-col:isConstituentOf` | For parts that are *not* discrete elements; disjoint with `cmns-col:hasMember`. |
| `cmns-col:isMemberOf` | An equity index is a measure in FIBO, not a collection (see above). |
| `fibo-fnd-oac-own:Income` | "revenue **received** during a period of time" (cash received); reported revenue is recognised, not received. |
| `cmns-org:isDomiciledIn` | Domicile is a legal fact; Stellantis is domiciled in NL but assigned to IT by the index provider. |
| `fibo-fnd-acc-4217:EUR`, `fibo-fnd-acc-4217:USD` | Currency *identifiers* (`fibo-fnd-acc-cur:CurrencyIdentifier`). The currencies are `fibo-fnd-acc-4217:Euro` and `fibo-fnd-acc-4217:USDollar`. |
| `fibo-be-le-cb:StockCorporation` | Correct but less specific than `fibo-be-le-cb:PubliclyHeldCompany`. |
| `cmns-loc:Country` for the class | FIBO's country individuals are typed `lcc-cr:Country`; the file has no alignment between the two classes. |
| `fibo-sec-eq-eq:ShareIssuer`, `fibo-sec-eq-eq:ListedShare`, `fibo-ind-mkt-bas:BasketOfEquities`, `fibo-sec-sec-bsk:SecuritiesBasketConstituent` | Correct, but only needed for the full path, which D1 ruled out. |

## Proposed shape for one company

```text
gwfi:index-euro-stoxx-50  a fibo-ind-mkt-bas:EquityIndex
    fibo-ind-mkt-bas:hasIndexName "EURO STOXX 50"

gwfi:company-sap  a fibo-be-le-cb:PubliclyHeldCompany
    cmns-dsg:hasTextualName "SAP"
    cmns-org:hasWebsite "https://www.sap.com"^^xsd:anyURI
    gwf:indexAssignedCountry lcc-3166-1:Germany
    cmns-cls:isClassifiedBy icb:10101015
    gwf:isConstituentOf gwfi:index-euro-stoxx-50
    gwf:hasRevenue gwfi:revenue-sap-fy2024           (gwf:Revenue ⊑ fibo-fnd-acc-cur:MonetaryAmount)
        fibo-fnd-acc-cur:hasAmount 34.2                          (billions, D3)
        fibo-fnd-acc-cur:hasCurrency fibo-fnd-acc-4217:Euro
        fibo-fnd-arr-doc:hasReportingPeriod gwfi:period-fy2024    (cmns-dt:ExplicitDatePeriod)
```

Node count: 2 resources per company (company and revenue), so about 100, plus the index and one period.

## Risks and limits

- **R1. FIBO expects facts the data does not have.** Through inheritance, `fibo-be-le-cb:PubliclyHeldCompany` expects a legal name, an incorporation date, an incorporation jurisdiction, a legal address and issued capital. `fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier` expects membership of a code set. Under OWL's open world this causes no inconsistency, only incompleteness. It must be documented, and the SHACL shapes must not enforce FIBO's cardinalities.
- **R2. Country labels change.** LCC's `rdfs:label` is the local-language name ("Deutschland"@de). The English name is `lcc-cr:hasEnglishShortName`, and for the Netherlands it is "Netherlands (the)". Query B3 and the answer key must use that property and expect that value.
- **R3. ICB alignment lives outside FIBO.** FIBO has the ICB classifier class and the scheme individual but no codes. The ICB concepts get FIBO typing in a separate alignment file, so `icb-skos.ttl` stays unchanged. Roll-ups still use `skos:broader`.
- **R4. Revenue fiscal year.** `fibo-fnd-arr-doc:hasReportingPeriod` needs a period. Company fiscal years differ (Infineon's, for example, ends in September), and the CSV gives no dates, so the shared "FY2024" period node has no start or end date.
- **R5. Billions are not FIBO's convention.** FIBO reads `fibo-fnd-acc-cur:hasAmount` as the amount in the currency's units, so a FIBO-aware tool or LLM would read 34.2 as 34.2 euros. Mitigations: state the scale in the definitions of `gwf:Revenue` and `gwf:hasRevenue`, label the class "revenue (billions)", and add a Track A test that every revenue node is a `gwf:Revenue`, so no revenue amount ever appears on a plain `fibo-fnd-acc-cur:MonetaryAmount`.
- **R6. Import size.** `owl:imports` of the full FIBO adds 132k triples to a 50-row dataset. Keep "reference, don't import": the new file uses FIBO IRIs without `owl:imports`, and a small extract of the reused FIBO terms is loaded alongside for docs, the explorer and the tests.
- **R7. Parallel test suite.** Because 2.0.0 stays, the FIBO version needs its own mapping output, shapes, Track A tests and Track B queries. The answer-key values stay the same, apart from the country label (R2).

## Implementation plan

1. **Requirements.** Reuse the existing Track A/B competency questions as the acceptance test; no new CQs are needed with the flat link.
2. **FIBO extract.** A script that pulls the reused terms (labels, definitions, parents) and the needed individuals (2 currencies, 8 countries, the ICB scheme) from `QuickFIBOProd.ttl` into `ontology/fibo-extract.ttl`, each term confirmed with the term-index `check`.
3. **Ontology.** `ontology/estx50-fibo-ontology.ttl` (namespace `https://graphwise.ai/ontology/estx50-fibo/`, 1.0.0), containing only the local terms `gwf:Revenue`, `gwf:hasRevenue`, `gwf:indexAssignedCountry`, `gwf:isConstituentOf` and `gwf:hasConstituent`. Everything else is used directly from FIBO.
4. **ICB alignment.** `ontology/icb-fibo-alignment.ttl`, which types the ICB concepts as FIBO ICB classifiers defined in the FIBO ICB scheme.
5. **Mapping.** A FIBO output mode for `map_csv.py` (or a sibling script) that maps country names to LCC IRIs and currency codes to FIBO currency individuals, and creates the revenue nodes. It writes `data/estx50-fibo-instances.ttl`.
6. **Validation.** `shapes/shapes-fibo.ttl`: exactly one revenue with exactly one amount and currency, exactly one ICB subsector (a qualified `cmns-cls:isClassifiedBy` count), exactly one assigned country.
7. **Tests and docs.** FIBO variants of the Track A and Track B queries, run by `run_tests.py`, pyLODE docs for the new file, and a decision-log section for this variant.

Rough effort: about one day, most of it in steps 5–7.
