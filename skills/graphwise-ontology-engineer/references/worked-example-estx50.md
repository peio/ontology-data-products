# Worked example: EURO STOXX 50 constituents

A complete, tested run of the nine steps on real data: the 50 EURO STOXX 50
companies, their country, ICB industry classification and FY2024 revenue. Use it
as a precedent when a modelling decision is not obvious. Each pattern below names
the general rule first, then what the example did and what it rejected.

Result: 3 minted classes, 6 minted properties, 1 reused SKOS taxonomy (ICB, 249
concepts), 50 companies; 22/22 robustness tests and 6/6 business questions pass.
Full sources, scripts and decision log:
https://github.com/peio/ontology-data-products/tree/main/tutorial

## Step 1: Scope and competency questions

- **Split the tests into two tracks.** Track A checks the model is built right
  (SHACL, SPARQL `ASK`, OWL RL). Track B checks it answers the business questions
  (SPARQL `SELECT` against an answer key). They fail for different reasons and need
  different fixes.
- **Compute the answer key from the source data, not from the graph.** A key derived
  from the graph only tests the graph against itself. The example computes it from
  the CSVs with a separate script.

## Step 2: Reuse

- **Align, don't import, when the import closure is heavy.** Minted classes are
  `rdfs:subClassOf` `schema:Corporation`, `schema:Country` and
  `fibo-ind-mkt-bas:EquityIndex`, with no `owl:imports`. FIBO's closure would swamp
  a 50-row dataset; the alignment still lets FIBO-aware tools classify the data.
- **Load a reused taxonomy alongside, not as an import,** when it has its own
  version and licence (ICB is FTSE Russell's).
- **Use global identifiers for well-known entities.** Countries are Wikidata IRIs,
  with the ISO 3166 code as `skos:notation`, rather than minted IRIs.
- **Verify every reused term against its source** before using it.
- **Never redeclare terms you do not own.** The ontology types and labels only its
  own terms; `schema:name` and `schema:url` are used, not declared (see Step 8,
  Revision 1).
- **Match the reused term's meaning to the data.** The CSV gives common names
  ("Stellantis"), not legal names (Stellantis N.V.), so they are `schema:name`,
  not `schema:legalName`.

## Step 3: Enumerate terms

- **List every term before classifying any.** The example collected 16: company,
  website, country, index, constituent, industry, supersector, sector, subsector, ICB
  code, revenue, fiscal year, source dataset, approximation, reporting currency,
  country currency.
- **Give every source column a fate, including the ones left out.** Five are mapped
  (company, website, country, revenue, reporting currency), three ICB industry columns
  are cross-checked and then derived rather than stored, and one (country currency) is
  dropped as out of scope. Keeping excluded terms in the list makes each exclusion
  explicit and testable: a test checks every column is either mapped or intentionally
  dropped. Reporting currency was on this list as excluded in 1.0.0, which is what made
  Revision 2 traceable (Step 8).
- **Record the relations between the terms, not just the terms.** Company is assigned
  to a country, classified in a subsector, a constituent of an index, and reports
  revenue for a fiscal year in a reporting currency; subsector → sector → supersector →
  industry each is part of the next level up; company and revenue come from a source
  dataset; revenue carries an approximation caveat. What is left (website, ICB code)
  are attributes. Steps 4 and 5 then read classes and properties off this list.

## Step 4: Classes

- **Keep the class definition free of relations you model separately.** A first draft
  defined `gw:Company` as "a constituent of the EURO STOXX 50", which put back the
  membership the model states with `gw:isConstituentOf`.
- **Mint a local subclass of the reused class** (`gw:Company` ⊑ `schema:Corporation`)
  so local disjointness and SHACL targets assert nothing about the external vocabulary.
- **Type instances with both the local and the reused class**
  (`a gw:Company, schema:Corporation`), so the reuse is visible without a reasoner
  (see Step 8, Revision 1).
- **Terminological hierarchies stay SKOS.** ICB industries, sectors and subsectors
  carry no distinct properties per level, so they are `skos:Concept`s, not 249 OWL
  classes. Rejected: making each company an instance of a class like "Banks", which
  blurs instance and class.
- **Membership that changes over time is a relation, not a class.** No
  `EuroStoxx50Company` class: index rebalancing would make instances migrate in and
  out. Use `gw:isConstituentOf` with inverse `gw:hasConstituent`.
- **Declare top-level classes pairwise disjoint** with `owl:AllDisjointClasses`.

## Step 5: Properties

- **Store the finest level, derive the rest.** Each company links only to its 8-digit
  subsector; sector, supersector and industry follow via `skos:broader+`. Storing
  every level is redundant and can contradict itself.
- **Pick the one reading of an ambiguous property that holds for all rows,** and
  document the edge case. `gw:country` means the index-assigned country; a
  `skos:scopeNote` records that Stellantis is domiciled in the Netherlands but
  assigned to Italy. Rejected: separate domicile and headquarters properties that no
  competency question needs.
- **A caveat about the numbers is a remark, not data.** Revenue is a plain
  `xsd:decimal`; "approximate, not FX-converted, not comparable across sectors" is an
  `rdfs:comment` on the property and in the dataset description. The currency is a
  separate property, so totals can be grouped by it. Rejected: an observation pattern
  with a fiscal period, which was out of scope for one figure per company.
- **Websites are IRIs** (`schema:url`), not strings.

## Step 6: Facets — OWL vs. SHACL

- **OWL for what a reasoner should infer or detect:** disjointness, functional
  properties, inverse pairs.
- **SHACL for "must have":** exact cardinalities, value ranges (revenue ≥ 0), at
  least one index, at least one source. OWL cannot require a value under the
  open-world assumption.
- **State intent directly in SHACL.** "Must be a subsector" is membership of the
  `icb:subsectors` collection (`sh:inversePath skos:member`), not a regex on the
  8-digit code.
- **Give every constraint a human-readable `sh:message`;** the validation report then
  doubles as documentation.

## Step 7: Instances and testing

- **Generate the instance data with a script; never edit it by hand.**
- **Cross-check redundant source columns, then drop them.** The CSV's industry
  columns are checked against the subsector's roll-up (50 of 50 consistent) and not
  stored.
- **Record provenance per entity:** each company has `prov:wasDerivedFrom` to the
  `dcat:Distribution`s it came from. Flag provisional inputs (the subsector
  assignments) on their own distribution with a `skos:editorialNote`.
- **Plant violations in a separate file** (missing country, negative revenue,
  industry-level classification) so the clean data stays clean, and assert that
  validation catches exactly those.
- **Count top-level SHACL results only.** pySHACL also reports nested `sh:node`
  failures as details; counting them double-counts.

## Step 8: Refine and iterate

- **A green test run proves only what the tests ask.** Both revisions fixed a model
  that passed every test; both mistakes were found by review. Trace each finding back
  to the step it came from, fix it there, and add a test so it cannot come back.
- **Revision 1: reuse invisible without a reasoner** (returns to Steps 2 and 7). The
  reuse decision was right; the instance typing hid it. Instances were typed only
  `gw:Company`, `gw:Country`, `gw:StockIndex`, so the plain data had 0
  `schema:Corporation`, `schema:Country` and `EquityIndex` instances; OWL RL inferred
  50, 8 and 1. A plain triple store, a schema.org-aware crawler or an LLM reading the
  Turtle saw no reuse. The ontology also declared `schema:legalName` and `schema:url`
  as OWL properties, claims about terms schema.org owns (and the `url` typing
  contradicted schema.org's `URL` range). Fix: dual typing in the mapping (59 triples)
  and the two declarations removed. New tests: A1f (on the plain data, every instance
  of a minted class carries the reused superclass, and at least one of each exists so
  the test cannot pass vacuously) and A1g (no external term is declared). Both were
  confirmed to fail before the fix. The existing A1e had passed: it checked that each
  class *has* a reused superclass, not that the reuse reaches the data. Rejected:
  relying on reasoning only (visibility depends on the consumer), and typing with the
  reused classes only (disjointness and SHACL targets would land on terms not owned).
- **Revision 2: EUR and USD summed together** (returns to Steps 1, 3 and 5). Reporting
  currency was enumerated in Step 3, put out of scope in Step 1, so Step 5 defined no
  property and the mapping dropped the column. 5 of 50 companies report in USD;
  revenue by industry and country summed dollars and euros, and "largest constituent"
  answered TotalEnergies (195.6 USD) over Allianz (179.8 EUR), a ranking that depends on
  the exchange rate. The test still passed, because the answer key was computed from
  the CSV with the same mistake: Track B checks the graph against the key, not against
  the truth. Fix: `gw:reportingCurrency` (ISO 4217, functional, required by SHACL);
  the queries group or rank within each currency. Leaving out FX conversion is a scope
  decision; hiding the unit is not. A column dropped as out of scope can hide a wrong
  answer from every test, because the key and the graph lose the same information.
- **Revision 2 also fixed three review findings,** each traced to its own step:
  `schema:legalName` held common names (Step 2, now `schema:name`); class definitions
  named the index (Step 4); and terms lived in the shared
  `https://graphwise.ai/ontology/` namespace, where `gw:Company` would clash with any
  other Graphwise ontology (a setup choice, now `https://graphwise.ai/ontology/estx50/`).
- **Term IRIs changed, so the version is major:** 1.0.0 → 2.0.0, with
  `owl:priorVersion` pointing back.
- **Log what was deferred, not just what was fixed.** `gw:revenueFY2024` puts the year
  in the property name; a second year would need an observation pattern with a fiscal
  period.

## Step 9: Document and deploy

- Ontology header: `owl:versionIRI`, `dcterms:title`, creator, publisher, licence,
  `vann:preferredNamespacePrefix`.
- HTML documentation with pyLODE (pin a working version; 3.3 had a dependency
  conflict, 3.2.1 works).
- GraphDB load order: ontology, reused taxonomy, instances, then shapes into the
  SHACL shape graph.
