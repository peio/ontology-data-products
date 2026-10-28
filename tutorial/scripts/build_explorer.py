"""Step 9: build the semantic-layer explorer, docs/estx50-explorer.html.

Usage: python scripts/build_explorer.py [--fragment PATH]   (run from the project root,
after map_csv.py). Reads the source CSVs, the ontology, the ICB taxonomy, the instance
data and the shapes, runs the Track B queries and the SHACL demo, and embeds the
results as JSON in docs/explorer-template.html. Nothing in the page is typed by hand.
--fragment also writes the page without the <!doctype>/<html> wrapper (for publishing
as a claude.ai Artifact, which adds its own).
"""
import csv
import json
import sys
from decimal import Decimal
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from map_csv import COLUMN_MAP, COUNTRIES, CSV_ICB, CSV_MAIN, GW, GWI, ICB, SCHEMA, slug  # noqa: E402
from run_tests import sections  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ONT = ROOT / "ontology" / "estx50-ontology.ttl"
ICB_TTL = ROOT / "ontology" / "icb-skos.ttl"
INST = ROOT / "data" / "estx50-instances.ttl"
DEMO = ROOT / "data" / "violations-demo.ttl"
SHAPES = ROOT / "shapes" / "shapes.ttl"
SCHEMA_TTL = ROOT / "ontologies" / "schemaorg-current-https.ttl"
TEMPLATE = ROOT / "docs" / "explorer-template.html"
OUT = ROOT / "docs" / "estx50-explorer.html"
SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
FIBO_EQUITY_INDEX = ("A financial index whose constituents are equities (FIBO IND, "
                     "MarketIndices/BasketIndices).")

# What each CSV heading becomes in the semantic layer. "term" is the CURIE shown;
# its definition is read from the ontology (gw:), the bundled schema.org file, or ICB.
COLUMNS = {
    "Company": dict(term="schema:name", source="schema", fate="mapped",
                    adds="Each row becomes a resource with its own IRI (gwi:company-<slug>), typed gw:Company and schema:Corporation."),
    "Website": dict(term="schema:url", source="schema", fate="mapped",
                    adds="Stored as an IRI, not a string, so it links rather than just reads."),
    "Country": dict(term="gw:country", source="gw", fate="mapped",
                    adds="The text \"Germany\" becomes the Wikidata entity wd:Q183, with ISO code DE. Any dataset using Wikidata joins on it."),
    "ICB Industry": dict(term="skos:broader+", source="icb", fate="derived",
                         adds="Not stored. Derived by walking up from the subsector, so it can never disagree with it."),
    "ICB code": dict(term="skos:notation", source="icb", fate="derived",
                     adds="Not stored. The notation of the industry concept reached through skos:broader+."),
    "ICB concept IRI": dict(term="skos:Concept", source="icb", fate="derived",
                            adds="Not stored. Used to cross-check that each subsector rolls up to this industry (50 of 50)."),
    "Revenue FY2024 (bn, approx.)": dict(term="gw:revenueFY2024", source="gw", fate="mapped",
                                         adds="Typed xsd:decimal, required to be 0 or more, and carries its comparability caveat."),
    "Reporting currency": dict(term="gw:reportingCurrency", source="gw", fate="mapped",
                               adds="An ISO 4217 code that totals are grouped by, so EUR and USD are never added together."),
    "Country currency": dict(term="(dropped)", source="none", fate="dropped",
                             adds="Out of scope: implied by the country, and no business question needs it."),
}
# Columns the semantic layer adds that the CSV does not have.
ADDED = [
    dict(heading="ICB subsector", term="gw:icbSubsector", source="icb",
         adds="One link to an 8-digit subsector gives all four ICB levels. Comes from a second, provisional file."),
    dict(heading="Index", term="gw:isConstituentOf", source="fibo",
         adds="Membership as a relation to the index, which is typed fibo-ind-mkt-bas:EquityIndex. Its inverse, hasConstituent, is inferred."),
    dict(heading="Source", term="prov:wasDerivedFrom", source="prov",
         adds="Every company points to the two files it came from, described with DCAT."),
]


def text(g, s, p):
    v = g.value(s, p)
    return str(v) if v is not None else ""


def main() -> int:
    ont = Graph().parse(ONT)
    icb = Graph().parse(ICB_TTL)
    inst = Graph().parse(INST)
    base = ont + icb + inst
    schema = Graph().parse(SCHEMA_TTL)

    def curie_iri(curie):
        pfx, local = curie.split(":", 1)
        return {"gw": GW, "schema": SCHEMA, "skos": SKOS, "prov": PROV}[pfx][local]

    def definition(curie):
        if curie.startswith("gw:"):
            return text(ont, curie_iri(curie), SKOS.definition)
        if curie.startswith("schema:"):
            return text(schema, curie_iri(curie), RDFS.comment)
        return {
            "skos:broader+": "Follow skos:broader one or more times, from narrower to broader concepts.",
            "skos:notation": "A code that identifies a concept within its scheme.",
            "skos:Concept": "An idea or notion; a unit of thought in a concept scheme.",
            "prov:wasDerivedFrom": "A transformation of one entity into another.",
        }.get(curie, "")

    shape_msgs = {}
    shapes = Graph().parse(SHAPES)
    for ps in shapes.objects(None, SH.property):
        path, msg = shapes.value(ps, SH.path), shapes.value(ps, SH.message)
        if isinstance(path, URIRef) and msg is not None:
            shape_msgs[path] = str(msg)

    rows = list(csv.DictReader(open(CSV_MAIN, encoding="utf-8-sig")))
    headings = list(rows[0].keys())
    assign = {r["Company"]: r for r in csv.DictReader(open(CSV_ICB, encoding="utf-8"))}

    columns = []
    for h in headings:
        c = dict(COLUMNS[h], heading=h, mapping=COLUMN_MAP[h])
        c["definition"] = definition(c["term"]) if c["fate"] != "dropped" else ""
        c["rule"] = shape_msgs.get(curie_iri(c["term"]), "") if c["term"].split(":")[0] in ("gw", "schema") and "+" not in c["term"] else ""
        columns.append(c)
    for a in ADDED:
        c = dict(a, fate="added", mapping=a["term"])
        c["definition"] = definition(c["term"])
        c["rule"] = shape_msgs.get(curie_iri(c["term"]), "")
        columns.append(c)

    level = {2: "Industry", 4: "Supersector", 6: "Sector", 8: "Subsector"}
    companies = []
    for r in rows:
        co = GWI["company-" + slug(r["Company"])]
        sub = inst.value(co, GW.icbSubsector)
        path, node = [], sub
        while node is not None:
            code = text(icb, node, SKOS.notation)
            path.append(dict(code=code, label=text(icb, node, SKOS.prefLabel), level=level[len(code)]))
            node = icb.value(node, SKOS.broader)
        ctry = inst.value(co, GW.country)
        companies.append(dict(
            id=str(co).rsplit("/", 1)[-1],
            row=[r[h] for h in headings],
            name=text(inst, co, SCHEMA.name),
            url=text(inst, co, SCHEMA.url),
            revenue=float(Decimal(str(inst.value(co, GW.revenueFY2024)))),
            currency=text(inst, co, GW.reportingCurrency),
            country=dict(iri=str(ctry), qid=str(ctry).rsplit("/", 1)[-1], label=text(inst, ctry, RDFS.label),
                         iso=text(inst, ctry, SKOS.notation)),
            icb=list(reversed(path)),
            basis=assign[r["Company"]]["Basis"],
            sources=sorted(text(inst, d, DCTERMS.title) for d in inst.objects(co, PROV.wasDerivedFrom)),
            types=sorted(str(t).replace(str(GW), "gw:").replace(str(SCHEMA), "schema:") for t in inst.objects(co, RDF.type)),
            triples=len(list(inst.triples((co, None, None)))),
        ))

    # Track B: run the real queries over the graph.
    table_notes = {
        "B1": "The table has an industry column (Financials, 11 companies) but no subsector, so it cannot tell a bank from an insurer or an exchange.",
        "B2": "A spreadsheet pivot on \"ICB Industry\" would add EUR and USD figures together. The graph groups by currency because the currency is part of the model.",
        "B3": "Same as B2, by the index-assigned country. Ireland's two constituents both report in USD.",
        "B4": "Countable in the table only because the industry column is there; in the graph it is derived from one subsector link per company.",
        "B5": "Sorting the revenue column puts TotalEnergies (USD) above Allianz (EUR). Within each currency, each is the largest.",
        "B6": "A CSV cell has no memory of where it came from. Every company in the graph points to its source files, and the dataset says the figures are approximate.",
    }
    questions = []
    for (qid, question), q in sections(ROOT / "queries" / "business-queries.rq", "query"):
        res = base.query(q)
        vars_ = [str(v) for v in res.vars]
        out = []
        for row in res:
            vals = []
            for v in row:
                v = v.toPython() if isinstance(v, Literal) else (str(v) if v is not None else None)
                vals.append(float(v) if isinstance(v, Decimal) else v)
            out.append(vals)
        body = q.split("\n", 1)[1]
        sparql = "\n".join(l for l in body.splitlines() if not l.startswith("PREFIX")).strip()
        questions.append(dict(id=qid, question=question, table=table_notes[qid], sparql=sparql, vars=vars_, rows=out))

    # SHACL demo: the three planted violations with their messages.
    _, rg, _ = validate(Graph().parse(INST) + icb + Graph().parse(DEMO), shacl_graph=shapes,
                        ont_graph=ont, inference="none")
    demo = Graph().parse(DEMO)
    violations = []
    for res in rg.objects(None, SH.result):
        focus = rg.value(res, SH.focusNode)
        violations.append(dict(
            id=str(focus).rsplit("/", 1)[-1], label=text(demo, focus, RDFS.label),
            name=text(demo, focus, SCHEMA.name), url=text(demo, focus, SCHEMA.url),
            country=COUNTRY_LABEL.get(text(demo, focus, GW.country), ""),
            icb=text(demo, focus, GW.icbSubsector).rsplit("/", 1)[-1],
            revenue=text(demo, focus, GW.revenueFY2024), currency=text(demo, focus, GW.reportingCurrency),
            path=str(rg.value(res, SH.resultPath)).replace(str(GW), "gw:"),
            message=text(rg, res, SH.resultMessage)))
    violations.sort(key=lambda v: v["id"])

    data = dict(
        title=text(ont, URIRef("https://graphwise.ai/ontology/estx50"), DCTERMS.title),
        version=text(ont, URIRef("https://graphwise.ai/ontology/estx50"), URIRef("http://www.w3.org/2002/07/owl#versionInfo")),
        headings=headings, columns=columns, companies=companies, questions=questions, violations=violations,
        stats=dict(rows=len(rows), cells=len(rows) * len(headings), triples=len(base), instance_triples=len(inst),
                   icb_concepts=len(set(icb.subjects(RDF.type, SKOS.Concept))), countries=len(COUNTRIES)),
        fibo=FIBO_EQUITY_INDEX,
    )
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
    note = "<!-- Generated by scripts/build_explorer.py from docs/explorer-template.html. Do not edit by hand. -->\n"
    OUT.write_text("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                   "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                   "</head>\n<body>\n" + note + page + "\n</body>\n</html>\n", encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(companies)} companies, {len(questions)} questions, "
          f"{len(violations)} violations")
    if "--fragment" in sys.argv:
        frag = Path(sys.argv[sys.argv.index("--fragment") + 1])
        frag.write_text(page, encoding="utf-8", newline="\n")
        print(f"Wrote fragment {frag}")
    return 0


COUNTRY_LABEL = {f"http://www.wikidata.org/entity/{q}": name for name, (q, _) in COUNTRIES.items()}

if __name__ == "__main__":
    sys.exit(main())
