# Ontology bundle

Local reference copies of the standard vocabularies the tutorial reuses.

They are **not imported**: the tutorial references reused terms directly and aligns its own classes with `rdfs:subClassOf`, without `owl:imports` (see the [decision log, Step 2](../decision-log.md#step-2-reuse-existing-ontologies)). Use these files to:

- check that every reused term exists and is used as its vocabulary intends (for example, the range of `schema:url` is `schema:URL`);
- load them into GraphDB alongside the tutorial's ontology, to get labels and definitions for the reused terms.

| Prefix | Namespace | File | Version | Source |
|---|---|---|---|---|
| skos | http://www.w3.org/2004/02/skos/core# | skos.ttl | W3C Recommendation 2009-08-18 (converted from official RDF/XML; no official TTL is published) | http://www.w3.org/2004/02/skos/core.rdf |
| skos | http://www.w3.org/2004/02/skos/core# | skos.rdf | W3C Recommendation 2009-08-18, the official RDF/XML that `skos.ttl` was converted from | http://www.w3.org/2004/02/skos/core.rdf |
| dcat | http://www.w3.org/ns/dcat# | dcat.ttl | DCAT 3 (W3C Recommendation 2024-08-22) | https://www.w3.org/ns/dcat.ttl |
| dcterms | http://purl.org/dc/terms/ | dublin_core_terms.ttl | DCMI Metadata Terms (2020-01-20 release) | https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl |
| prov | http://www.w3.org/ns/prov# | prov-o.ttl | PROV-O core, W3C Recommendation 2013-04-30 | https://www.w3.org/ns/prov-o.ttl |
| prov | http://www.w3.org/ns/prov# | prov.ttl | Full PROV namespace (PROV-O + extensions: dictionary, links, AQ, DC mapping) | https://www.w3.org/ns/prov.ttl |
| schema | https://schema.org/ | schemaorg-current-https.ttl | Schema.org V30.1 (released 2026-09-16), https IRIs | https://schema.org/version/latest/schemaorg-current-https.ttl |
| fibo-*, cmns-*, lcc-* | https://spec.edmcouncil.org/fibo/ontology/, https://www.omg.org/spec/Commons/, https://www.omg.org/spec/LCC/ | QuickFIBOProd.ttl | FIBO production 2026Q2 (`owl:versionIRI <https://spec.edmcouncil.org/fibo/ontology/master/2026Q2/QuickFIBOProd/>`, modified 2026-07-07): all FIBO production modules with OMG Commons and LCC in one file, 132,594 triples. MIT licence, EDM Council / OMG | https://spec.edmcouncil.org/fibo/ |

Added to the repository on 2026-10-28.

**FIBO** is used by the FIBO variant only, and is not loaded by default: `scripts/build_fibo_files.py` copies the terms the variant uses into `../ontology/fibo-extract.ttl` (about 480 triples) and fails if a term is missing from this file. Load the extract, not this file, unless you need the whole of FIBO.

## Which files to load

- **SKOS:** load `skos.ttl`. `skos.rdf` is the same vocabulary in RDF/XML, kept as the conversion source.
- **PROV:** load `prov-o.ttl`; it covers everything the tutorial uses (`prov:wasDerivedFrom`). `prov.ttl` is a superset with the PROV extensions. Load one or the other, not both, or the PROV-O triples are duplicated.

## Not in the bundle

The tutorial also uses terms from:

| Vocabulary | Terms used | Why not bundled |
|---|---|---|
| FIBO (`fibo-ind-mkt-bas:`) in 2.0.0 | `EquityIndex`, the superclass of `gw:StockIndex` | Now also in `QuickFIBOProd.ttl` (above). 2.0.0 does not load it: one class does not justify the whole of FIBO. |
| VANN (`vann:`) | `preferredNamespacePrefix`, `preferredNamespaceUri` | Ontology header annotations only. |
| Wikidata (`wd:`) | Country IRIs, e.g. `wd:Q183` for Germany | Used as data (instance identifiers), not as a vocabulary. |

## Refresh

To update the bundle, download the files again from their sources and record the new versions in the table above. Run these commands from this folder:

```bash
curl -L -o dcat.ttl https://www.w3.org/ns/dcat.ttl
curl -L -o dublin_core_terms.ttl https://www.dublincore.org/specifications/dublin-core/dcmi-terms/dublin_core_terms.ttl
curl -L -o prov-o.ttl https://www.w3.org/ns/prov-o.ttl
curl -L -o prov.ttl https://www.w3.org/ns/prov.ttl
curl -L -o schemaorg-current-https.ttl https://schema.org/version/latest/schemaorg-current-https.ttl
curl -L -o skos.rdf http://www.w3.org/2004/02/skos/core.rdf
```

`skos.ttl` is then converted from `skos.rdf`, for example with rdflib:

```bash
python -c "import rdflib; rdflib.Graph().parse('skos.rdf').serialize('skos.ttl', format='turtle')"
```
