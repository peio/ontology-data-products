"""FIBO variant: map the EURO STOXX 50 CSV (+ provisional ICB subsector assignments) to RDF
using FIBO, OMG Commons and LCC terms directly.

Usage: python scripts/map_csv_fibo.py   (run from the project root)
Writes data/estx50-fibo-instances.ttl
"""
import csv
import sys
from decimal import Decimal

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

from map_csv import CSV_ICB, CSV_MAIN, ICB, ICB_TTL, ROOT, industry_of, slug

OUT = ROOT / "data" / "estx50-fibo-instances.ttl"

GWF = Namespace("https://graphwise.ai/ontology/estx50-fibo/")
GWFI = Namespace("https://graphwise.ai/instance/estx50-fibo/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
PROV = Namespace("http://www.w3.org/ns/prov#")
FIBO_CB = Namespace("https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/CorporateBodies/")
FIBO_BAS = Namespace("https://spec.edmcouncil.org/fibo/ontology/IND/MarketIndices/BasketIndices/")
FIBO_CUR = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/CurrencyAmount/")
FIBO_4217 = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/")
FIBO_DOC = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Documents/")
CMNS_CLS = Namespace("https://www.omg.org/spec/Commons/Classifiers/")
CMNS_DSG = Namespace("https://www.omg.org/spec/Commons/Designators/")
CMNS_DT = Namespace("https://www.omg.org/spec/Commons/DatesAndTimes/")
CMNS_ORG = Namespace("https://www.omg.org/spec/Commons/Organizations/")
LCC_3166 = Namespace("https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/")

# Countries: LCC ISO 3166-1 individuals. Their English short names live in
# ontology/fibo-extract.ttl (lcc-cr:hasEnglishShortName), not here.
COUNTRIES = {name: LCC_3166[name] for name in
             ["Belgium", "Finland", "France", "Germany", "Ireland", "Italy", "Netherlands", "Spain"]}

# Reporting currency codes -> FIBO currency individuals (not the code individuals
# fibo-fnd-acc-4217:EUR / USD, which are currency identifiers).
CURRENCIES = {"EUR": FIBO_4217.Euro, "USD": FIBO_4217.USDollar}

# Columns of the main CSV and what happens to each (checked in Track A5).
COLUMN_MAP = {
    "Company": "cmns-dsg:hasTextualName, rdfs:label",
    "Website": "cmns-org:hasWebsite",
    "Country": "gwf:indexAssignedCountry",
    "ICB Industry": "derived via skos:broader+ (cross-checked, not stored)",
    "ICB code": "derived via skos:broader+ (cross-checked, not stored)",
    "ICB concept IRI": "derived via skos:broader+ (cross-checked, not stored)",
    "Revenue FY2024 (bn, approx.)": "gwf:hasRevenue / fibo-fnd-acc-cur:hasAmount (billions)",
    "Reporting currency": "gwf:hasRevenue / fibo-fnd-acc-cur:hasCurrency",
    "Country currency": "DROPPED: out of scope (implied by the country)",
}


def main() -> int:
    rows = list(csv.DictReader(open(CSV_MAIN, encoding="utf-8-sig")))
    assign = {r["Company"]: r for r in csv.DictReader(open(CSV_ICB, encoding="utf-8"))}
    icb = Graph().parse(ICB_TTL)

    missing_cols = set(rows[0].keys()) ^ set(COLUMN_MAP)
    if missing_cols:
        print(f"Unmapped or unexpected columns: {missing_cols}")
        return 1

    g = Graph()
    for p, ns in [("gwf", GWF), ("gwfi", GWFI), ("icb", ICB), ("dcat", DCAT), ("prov", PROV),
                  ("dcterms", DCTERMS), ("skos", SKOS), ("fibo-be-le-cb", FIBO_CB),
                  ("fibo-ind-mkt-bas", FIBO_BAS), ("fibo-fnd-acc-cur", FIBO_CUR),
                  ("fibo-fnd-acc-4217", FIBO_4217), ("fibo-fnd-arr-doc", FIBO_DOC),
                  ("cmns-cls", CMNS_CLS), ("cmns-dsg", CMNS_DSG), ("cmns-dt", CMNS_DT),
                  ("cmns-org", CMNS_ORG), ("lcc-3166-1", LCC_3166)]:
        g.bind(p, ns)

    # Dataset and its two source distributions (same metadata as the 2.0.0 mapping).
    ds, dist_main, dist_icb = GWFI["dataset-estx50"], GWFI["distribution-csv2"], GWFI["distribution-icb-assignments"]
    g.add((ds, RDF.type, DCAT.Dataset))
    g.add((ds, DCTERMS.title, Literal("EURO STOXX 50 constituents, FY2024", lang="en")))
    g.add((ds, DCTERMS.description, Literal(
        "Snapshot of the 50 EURO STOXX 50 constituents with country, ICB subsector and FY2024 revenue. "
        "Remark on the numbers: revenue figures are approximate, in billions of each company's reporting currency "
        "(recorded, not converted; do not sum across currencies), and not comparable across sectors. ICB subsector assignments are provisional, "
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

    # The index: a FIBO equity index, used directly (no local class).
    idx = GWFI["index-euro-stoxx-50"]
    g.add((idx, RDF.type, FIBO_BAS.EquityIndex))
    g.add((idx, RDFS.label, Literal("EURO STOXX 50", lang="en")))
    g.add((idx, FIBO_BAS.hasIndexName, Literal("EURO STOXX 50", datatype=XSD.string)))

    # One shared reporting period. Fiscal years differ between companies and the
    # source gives no dates, so the period has no start or end date.
    period = GWFI["period-fy2024"]
    g.add((period, RDF.type, CMNS_DT.ExplicitDatePeriod))
    g.add((period, RDFS.label, Literal("FY2024", lang="en")))
    g.add((period, SKOS.note, Literal(
        "Each company's own fiscal year 2024. Start and end dates differ between companies "
        "and are not in the source, so none are given.", lang="en")))

    errors = []
    for r in rows:
        name = r["Company"]
        co = GWFI["company-" + slug(name)]
        a = assign.get(name)
        if a is None:
            errors.append(f"{name}: no ICB subsector assignment")
            continue
        sub = ICB[a["ICB subsector code"]]
        if (ICB["subsectors"], SKOS.member, sub) not in icb:
            errors.append(f"{name}: {sub} is not an ICB subsector")
        if industry_of(icb, sub) != URIRef(r["ICB concept IRI"]):
            errors.append(f"{name}: subsector {a['ICB subsector code']} does not roll up to {r['ICB concept IRI']}")
        if r["Country"] not in COUNTRIES:
            errors.append(f"{name}: unknown country {r['Country']!r}")
            continue
        if r["Reporting currency"] not in CURRENCIES:
            errors.append(f"{name}: unknown reporting currency {r['Reporting currency']!r}")
            continue

        g.add((co, RDF.type, FIBO_CB.PubliclyHeldCompany))
        g.add((co, RDFS.label, Literal(name)))
        g.add((co, CMNS_DSG.hasTextualName, Literal(name, datatype=XSD.string)))
        g.add((co, CMNS_ORG.hasWebsite, Literal(r["Website"], datatype=XSD.anyURI)))
        g.add((co, GWF.indexAssignedCountry, COUNTRIES[r["Country"]]))
        g.add((co, CMNS_CLS.isClassifiedBy, sub))
        g.add((co, GWF.isConstituentOf, idx))
        g.add((co, PROV.wasDerivedFrom, dist_main))
        g.add((co, PROV.wasDerivedFrom, dist_icb))

        # Revenue as a FIBO monetary amount: exactly one amount and one currency.
        rev = GWFI["revenue-" + slug(name) + "-fy2024"]
        g.add((co, GWF.hasRevenue, rev))
        g.add((rev, RDF.type, GWF.Revenue))
        g.add((rev, RDF.type, FIBO_CUR.MonetaryAmount))
        g.add((rev, RDFS.label, Literal(f"{name} revenue FY2024", lang="en")))
        g.add((rev, FIBO_CUR.hasAmount, Literal(Decimal(r["Revenue FY2024 (bn, approx.)"]), datatype=XSD.decimal)))
        g.add((rev, FIBO_CUR.hasCurrency, CURRENCIES[r["Reporting currency"]]))
        g.add((rev, FIBO_DOC.hasReportingPeriod, period))
        g.add((rev, PROV.wasDerivedFrom, dist_main))

    if errors:
        print("Mapping errors:\n  " + "\n  ".join(errors))
        return 1

    OUT.write_text(
        "# Generated by scripts/map_csv_fibo.py from data/EURO_STOXX_50_Constituents_CSV2.csv\n"
        "# and data/icb-subsector-assignments.csv. Do not edit by hand.\n"
        + g.serialize(format="turtle"),
        encoding="utf-8",
    )
    n = len(set(g.subjects(RDF.type, FIBO_CB.PubliclyHeldCompany)))
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(g)} triples, {n} companies from {len(rows)} rows")
    for col, target in COLUMN_MAP.items():
        print(f"  {col:32} -> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
