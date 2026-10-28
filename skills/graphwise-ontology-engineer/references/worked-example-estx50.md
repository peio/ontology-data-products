# Worked example: EURO STOXX 50 constituents

A complete, tested run of the nine steps on real data: the 50 EURO STOXX 50
companies, their country, ICB industry classification and FY2024 revenue. Use it
as a precedent when a modelling decision is not obvious. Each pattern below names
the general rule first, then what the example did and what it rejected.

Result: 3 minted classes, 5 minted properties, 1 reused SKOS taxonomy (ICB, 249
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
- **Make exclusions explicit.** Currency columns were enumerated, then excluded by
  scope; a test checks every source column is either mapped or intentionally dropped.

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
  own terms; `schema:legalName` and `schema:url` are used, not declared. An early
  draft declared `schema:url a owl:ObjectProperty`, which was both a claim about
  schema.org and wrong (schema.org's range is the `URL` datatype).

## Step 4: Classes

- **Mint a local subclass of the reused class** (`gw:Company` ⊑ `schema:Corporation`)
  so local disjointness and SHACL targets assert nothing about the external vocabulary.
- **Type instances with both the local and the reused class**
  (`a gw:Company, schema:Corporation`). With `rdfs:subClassOf` alone, the reused
  types appear only after reasoning: the first version had 0 asserted
  `schema:Corporation` instances and needed OWL RL to infer all 50. Test it: every
  instance of a minted class also carries the reused superclass as an asserted type.
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
  `rdfs:comment` on the property and in the dataset description. Rejected: an
  observation pattern with currency and fiscal period, which was out of scope.
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

## Step 9: Document and deploy

- Ontology header: `owl:versionIRI`, `dcterms:title`, creator, publisher, licence,
  `vann:preferredNamespacePrefix`.
- HTML documentation with pyLODE (pin a working version; 3.3 had a dependency
  conflict, 3.2.1 works).
- GraphDB load order: ontology, reused taxonomy, instances, then shapes into the
  SHACL shape graph.
