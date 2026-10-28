"""Step 7: map the EURO STOXX 50 CSV (+ provisional ICB subsector assignments) to RDF.

Usage: python scripts/map_csv.py   (run from the project root)
Writes data/estx50-instances.ttl
"""
import csv
import re
import sys
import unicodedata
from decimal import Decimal
from pathlib import Path

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

ROOT = Path(__file__).resolve().parent.parent
CSV_MAIN = ROOT / "data" / "EURO_STOXX_50_Constituents_CSV2.csv"
CSV_ICB = ROOT / "data" / "icb-subsector-assignments.csv"
ICB_TTL = ROOT / "ontology" / "icb-skos.ttl"
OUT = ROOT / "data" / "estx50-instances.ttl"

GW = Namespace("https://graphwise.ai/ontology/")
GWI = Namespace("https://graphwise.ai/instance/")
ICB = Namespace("https://graphwise.ai/taxonomy/icb/")
SCHEMA = Namespace("https://schema.org/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
PROV = Namespace("http://www.w3.org/ns/prov#")
WD = Namespace("http://www.wikidata.org/entity/")
FIBO_BAS = Namespace("https://spec.edmcouncil.org/fibo/ontology/IND/MarketIndices/BasketIndices/")

# Countries: Wikidata IRIs, ISO 3166-1 alpha-2 as skos:notation.
COUNTRIES = {
    "Belgium": ("Q31", "BE"),
    "Finland": ("Q33", "FI"),
    "France": ("Q142", "FR"),
    "Germany": ("Q183", "DE"),
    "Ireland": ("Q27", "IE"),
    "Italy": ("Q38", "IT"),
    "Netherlands": ("Q55", "NL"),
    "Spain": ("Q29", "ES"),
}

# Columns of the main CSV and what happens to each (checked in Track A5).
COLUMN_MAP = {
    "Company": "schema:legalName, rdfs:label",
    "Website": "schema:url",
    "Country": "gw:country",
    "ICB Industry": "derived via skos:broader+ (cross-checked, not stored)",
    "ICB code": "derived via skos:broader+ (cross-checked, not stored)",
    "ICB concept IRI": "derived via skos:broader+ (cross-checked, not stored)",
    "Revenue FY2024 (bn, approx.)": "gw:revenueFY2024",
    "Reporting currency": "DROPPED: out of scope",
    "Country currency": "DROPPED: out of scope",
}


def slug(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = s.replace("'", "")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def industry_of(icb: Graph, concept: URIRef) -> URIRef:
    """Follow skos:broader to the top concept (the ICB industry)."""
    while True:
        parent = icb.value(concept, SKOS.broader)
        if parent is None:
            return concept
        concept = parent


def main() -> int:
    rows = list(csv.DictReader(open(CSV_MAIN, encoding="utf-8-sig")))
    assign = {r["Company"]: r for r in csv.DictReader(open(CSV_ICB, encoding="utf-8"))}
    icb = Graph().parse(ICB_TTL)

    missing_cols = set(rows[0].keys()) ^ set(COLUMN_MAP)
    if missing_cols:
        print(f"Unmapped or unexpected columns: {missing_cols}")
        return 1

    g = Graph()
    for p, ns in [("gw", GW), ("gwi", GWI), ("icb", ICB), ("schema", SCHEMA), ("dcat", DCAT),
                  ("prov", PROV), ("dcterms", DCTERMS), ("skos", SKOS), ("wd", WD),
                  ("fibo-ind-mkt-bas", FIBO_BAS)]:
        g.bind(p, ns)

    # Dataset and its two source distributions (Step 7 / A6 provenance).
    ds, dist_main, dist_icb = GWI["dataset-estx50"], GWI["distribution-csv2"], GWI["distribution-icb-assignments"]
    g.add((ds, RDF.type, DCAT.Dataset))
    g.add((ds, DCTERMS.title, Literal("EURO STOXX 50 constituents, FY2024", lang="en")))
    g.add((ds, DCTERMS.description, Literal(
        "Snapshot of the 50 EURO STOXX 50 constituents with country, ICB subsector and FY2024 revenue. "
        "Remark on the numbers: revenue figures are approximate, in each company's reporting currency "
        "(not converted), and not comparable across sectors. ICB subsector assignments are provisional, "
        "derived from the taxonomy labels, and must be verified against FTSE Russell's classification.",
        lang="en")))
    g.add((ds, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((ds, DCAT.distribution, dist_main))
    g.add((ds, DCAT.distribution, dist_icb))
    for d, title, f in [(dist_main, "EURO STOXX 50 constituents CSV (CSV2)", CSV_MAIN.name),
                        (dist_icb, "Provisional ICB subsector assignments", CSV_ICB.name)]:
        g.add((d, RDF.type, DCAT.Distribution))
        g.add((d, DCTERMS.title, Literal(title, lang="en")))
        g.add((d, DCAT.mediaType, URIRef("https://www.iana.org/assignments/media-types/text/csv")))
        g.add((d, DCTERMS.identifier, Literal(f)))
    g.add((dist_icb, SKOS.editorialNote, Literal(
        "Provisional: each subsector was chosen from the ICB taxonomy labels based on the company's main "
        "business. Verify against FTSE Russell before production use.", lang="en")))

    # The index.
    idx = GWI["index-euro-stoxx-50"]
    # Reused classes are asserted alongside the local ones (dual typing), so the
    # schema.org / FIBO alignment is visible without a reasoner.
    g.add((idx, RDF.type, GW.StockIndex))
    g.add((idx, RDF.type, FIBO_BAS.EquityIndex))
    g.add((idx, RDFS.label, Literal("EURO STOXX 50", lang="en")))

    # Countries.
    for name, (qid, iso) in COUNTRIES.items():
        c = WD[qid]
        g.add((c, RDF.type, GW.Country))
        g.add((c, RDF.type, SCHEMA.Country))
        g.add((c, RDFS.label, Literal(name, lang="en")))
        g.add((c, SKOS.notation, Literal(iso)))

    errors = []
    for r in rows:
        name = r["Company"]
        co = GWI["company-" + slug(name)]
        a = assign.get(name)
        if a is None:
            errors.append(f"{name}: no ICB subsector assignment")
            continue
        sub = ICB[a["ICB subsector code"]]
        if (ICB["subsectors"], SKOS.member, sub) not in icb:
            errors.append(f"{name}: {sub} is not an ICB subsector")
        # Cross-check: the subsector must roll up to the industry given in CSV2.
        if industry_of(icb, sub) != URIRef(r["ICB concept IRI"]):
            errors.append(f"{name}: subsector {a['ICB subsector code']} does not roll up to {r['ICB concept IRI']}")
        if r["Country"] not in COUNTRIES:
            errors.append(f"{name}: unknown country {r['Country']!r}")
            continue

        g.add((co, RDF.type, GW.Company))
        g.add((co, RDF.type, SCHEMA.Corporation))
        g.add((co, RDFS.label, Literal(name)))
        g.add((co, SCHEMA.legalName, Literal(name, datatype=XSD.string)))
        g.add((co, SCHEMA.url, URIRef(r["Website"])))
        g.add((co, GW.country, WD[COUNTRIES[r["Country"]][0]]))
        g.add((co, GW.icbSubsector, sub))
        g.add((co, GW.revenueFY2024, Literal(Decimal(r["Revenue FY2024 (bn, approx.)"]), datatype=XSD.decimal)))
        g.add((co, GW.isConstituentOf, idx))
        g.add((co, PROV.wasDerivedFrom, dist_main))
        g.add((co, PROV.wasDerivedFrom, dist_icb))

    if errors:
        print("Mapping errors:\n  " + "\n  ".join(errors))
        return 1

    OUT.write_text(
        "# Generated by scripts/map_csv.py from data/EURO_STOXX_50_Constituents_CSV2.csv\n"
        "# and data/icb-subsector-assignments.csv. Do not edit by hand.\n"
        + g.serialize(format="turtle"),
        encoding="utf-8",
    )
    n = len(set(g.subjects(RDF.type, GW.Company)))
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(g)} triples, {n} companies from {len(rows)} rows")
    for col, target in COLUMN_MAP.items():
        print(f"  {col:32} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
