# Data

Sample source data used in the tutorial.

For each dataset, record its source, licence, and any transformations applied.

## EURO STOXX 50 constituents

| | |
|---|---|
| File | [EURO STOXX 50 Constituents.csv](EURO%20STOXX%2050%20Constituents.csv) |
| Content | 50 rows, one per index constituent: company, website, country, ICB industry, ICB code, ICB concept IRI, revenue FY2024 (bn, approx.), reporting currency, country currency |
| Coverage | 8 countries, 11 ICB industries; revenue total 2,769.0 bn as reported |
| Source | Compiled from public company information; revenue figures are approximate and in each company's reporting currency |
| Licence | To be confirmed |
| Transformations | ICB concept IRIs point into [icb-skos.ttl](icb-skos.ttl) |

Known limitations:

- ICB classification is at **industry level only** (2-digit code, e.g. `10` Technology). The tutorial needs the 8-digit subsector code and IRI for each company, taken from FTSE Russell's classification; that version (CSV2) is not yet available.
- Revenue figures are not FX-normalized and are not directly comparable across reporting currencies.

## ICB taxonomy (SKOS)

| | |
|---|---|
| File | [icb-skos.ttl](icb-skos.ttl) |
| Content | Industry Classification Benchmark as a SKOS concept scheme `icb:scheme`: 249 concepts (11 industries, 20 supersectors, 45 sectors, 173 subsectors), with one `skos:Collection` per level |
| Namespace | `icb:` `https://graphwise.ai/taxonomy/icb/` |
| Version | 1.0.0 (`owl:versionIRI <https://graphwise.ai/taxonomy/icb/1.0.0>`), created 2026-10-28 |
| Source | `icb-codes-description.xlsx`, sheet "New ICB Codes and Description" (FTSE Russell) |
| Licence | ICB codes and names are the intellectual property of FTSE International Limited (FTSE Russell). This file only re-expresses them in SKOS; FTSE Russell's licence terms apply. |
| Transformations | Hierarchy derived from the code structure: each level appends two digits to its parent's code (`skos:broader` / `skos:narrower`). Concept IRI = namespace + ICB code; the code is also kept as `skos:notation`. |
