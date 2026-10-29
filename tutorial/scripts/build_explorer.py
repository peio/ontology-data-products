"""Step 9: build the semantic-layer explorer.

Usage: python scripts/build_explorer.py [--variant fibo] [--fragment PATH]
(run from the project root, after map_csv.py, or map_csv_fibo.py and build_fibo_files.py
for the FIBO variant). Reads the source CSVs, the ontology, the ICB taxonomy, the
instance data and the shapes, runs the Track B queries and the SHACL demo, and embeds
the results as JSON in docs/explorer-template.html. Writes docs/estx50-explorer.html,
or docs/estx50-fibo-explorer.html for the FIBO variant. Nothing in the page is typed by
hand except the explanations in the variant configs below.
--fragment also writes the page without the <!doctype>/<html> wrapper (for publishing
as a claude.ai Artifact, which adds its own).
"""
import csv
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

sys.path.insert(0, str(Path(__file__).resolve().parent))
from map_csv import CSV_ICB, CSV_MAIN, ICB, slug  # noqa: E402
from run_tests import sections  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ONTO, DATA = ROOT / "ontology", ROOT / "data"
VOCABS = ROOT / "ontologies"
TEMPLATE = ROOT / "docs" / "explorer-template.html"
SH = Namespace("http://www.w3.org/ns/shacl#")
PROV = Namespace("http://www.w3.org/ns/prov#")
GW = Namespace("https://graphwise.ai/ontology/estx50/")
GWI = Namespace("https://graphwise.ai/instance/")
GWF = Namespace("https://graphwise.ai/ontology/estx50-fibo/")
GWFI = Namespace("https://graphwise.ai/instance/estx50-fibo/")
SCHEMA = Namespace("https://schema.org/")
CMNS_CLS = Namespace("https://www.omg.org/spec/Commons/Classifiers/")
CMNS_DSG = Namespace("https://www.omg.org/spec/Commons/Designators/")
CMNS_ID = Namespace("https://www.omg.org/spec/Commons/Identifiers/")
CMNS_ORG = Namespace("https://www.omg.org/spec/Commons/Organizations/")
FIBO_CUR = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/CurrencyAmount/")
FIBO_REL = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/")
LCC_CR = Namespace("https://www.omg.org/spec/LCC/Countries/CountryRepresentation/")

# Where a term's meaning comes from, by namespace (first match wins).
SOURCES = [
    ("https://graphwise.ai/ontology/", "gw"), ("https://graphwise.ai/instance/", "prov"),
    ("https://graphwise.ai/taxonomy/icb/", "icb"), ("https://schema.org/", "schema"),
    ("https://spec.edmcouncil.org/fibo/", "fibo"), ("https://www.omg.org/spec/Commons/", "cmns"),
    ("https://www.omg.org/spec/LCC/", "lcc"), ("http://www.wikidata.org/", "wd"),
    ("http://www.w3.org/ns/prov#", "prov"), ("http://www.w3.org/ns/dcat#", "prov"),
    ("http://www.w3.org/2004/02/skos/core#", "icb"),
]
# Terms that name a step in the mapping rather than a vocabulary term.
MAPPING_NOTES = {
    "skos:broader+": "Follow skos:broader one or more times, from narrower to broader concepts.",
    "skos:notation": "A code that identifies a concept within its scheme.",
    "skos:Concept": "An idea or notion; a unit of thought in a concept scheme.",
}
DERIVED = {
    "ICB Industry": dict(term="skos:broader+", source="icb", fate="derived",
                         adds="Not stored. Derived by walking up from the subsector, so it can never disagree with it."),
    "ICB code": dict(term="skos:notation", source="icb", fate="derived",
                     adds="Not stored. The notation of the industry concept reached through skos:broader+."),
    "ICB concept IRI": dict(term="skos:Concept", source="icb", fate="derived",
                            adds="Not stored. Used to cross-check that each subsector rolls up to this industry (50 of 50)."),
    "Country currency": dict(term="(dropped)", source="none", fate="dropped",
                             adds="Out of scope: implied by the country, and no business question needs it."),
}
TABLE_NOTES = {
    "B1": "The table has an industry column (Financials, 11 companies) but no subsector, so it cannot tell a bank from an insurer or an exchange.",
    "B2": "A spreadsheet pivot on \"ICB Industry\" would add EUR and USD figures together. The graph groups by currency because the currency is part of the model.",
    "B3": "Same as B2, by the index-assigned country. Ireland's two constituents both report in USD.",
    "B4": "Countable in the table only because the industry column is there; in the graph it is derived from one subsector link per company.",
    "B5": "Sorting the revenue column puts TotalEnergies (USD) above Allianz (EUR). Within each currency, each is the largest.",
    "B6": "A CSV cell has no memory of where it came from. Every company in the graph points to its source files, and the dataset says the figures are approximate.",
}
LEVEL = {2: "Industry", 4: "Supersector", 6: "Sector", 8: "Subsector"}


def lang_rank(v):
    """Sort key for literals: English first, then untagged, then other English variants."""
    lang = v.language if isinstance(v, Literal) else None
    return ({"en": 0, None: 1}.get(lang, 2 if lang and lang.lower().startswith("en") else 3), str(v))


def text(g, s, p):
    """One value of s p, chosen the same way on every run (rdflib's order is not stable)."""
    if s is None:
        return ""
    vals = sorted(g.objects(s, p), key=lang_rank)
    return str(vals[0]) if vals else ""


def first(g, s, p):
    """The smallest of several values, so a multi-valued property gives a stable result."""
    vals = sorted(g.objects(s, p))
    return vals[0] if vals else None


# ---------------------------------------------------------------------------
# Variant: default (2.0.0, gw:)
# ---------------------------------------------------------------------------
def default_record(g, co):
    ctry, cur = g.value(co, GW.country), text(g, co, GW.reportingCurrency)
    rev = g.value(co, GW.revenueFY2024)
    return dict(
        name=text(g, co, SCHEMA.name), url=text(g, co, SCHEMA.url),
        country=dict(iri=ctry, label=text(g, ctry, RDFS.label), code=text(g, ctry, SKOS.notation)),
        revenue=float(Decimal(str(rev))) if rev is not None else None, currency=dict(code=cur, iri=None),
        subsector=g.value(co, GW.icbSubsector), revenue_node=None)


DEFAULT = dict(
    title_iri=URIRef("https://graphwise.ai/ontology/estx50"),
    ontology=[ONTO / "estx50-ontology.ttl"],
    vocab=[VOCABS / "schemaorg-current-https.ttl", ONTO / "fibo-extract.ttl", VOCABS / "prov-o.ttl"],
    icb=[ONTO / "icb-skos.ttl"], base_extra=[],
    instances=DATA / "estx50-instances.ttl", demo=DATA / "violations-demo.ttl",
    shapes=ROOT / "shapes" / "shapes.ttl", queries=ROOT / "queries" / "business-queries.rq",
    out=ROOT / "docs" / "estx50-explorer.html", page_title="EURO STOXX 50 Semantic Layer", mapper="map_csv", inst_ns=GWI,
    record=default_record,
    sources=[("gw", "This ontology (gw:)"), ("schema", "schema.org"), ("fibo", "FIBO"), ("icb", "ICB taxonomy (SKOS)"),
             ("wd", "Wikidata"), ("prov", "PROV-O / DCAT")],
    columns={
        "Company": dict(term="schema:name", adds="Each row becomes a resource with its own IRI (gwi:company-<slug>), typed gw:Company and schema:Corporation."),
        "Website": dict(term="schema:url", adds="Stored as an IRI, not a string, so it links rather than just reads."),
        "Country": dict(term="gw:country", adds="The text \"Germany\" becomes the Wikidata entity wd:Q183, with ISO code DE. Any dataset using Wikidata joins on it."),
        "Revenue FY2024 (bn, approx.)": dict(term="gw:revenueFY2024", adds="Typed xsd:decimal, required to be 0 or more, and carries its comparability caveat."),
        "Reporting currency": dict(term="gw:reportingCurrency", adds="An ISO 4217 code that totals are grouped by, so EUR and USD are never added together."),
    },
    added=[
        dict(heading="ICB subsector", term="gw:icbSubsector", adds="One link to an 8-digit subsector gives all four ICB levels. Comes from a second, provisional file."),
        dict(heading="Index", term="gw:isConstituentOf", adds="Membership as a relation to the index, which is typed fibo-ind-mkt-bas:EquityIndex. Its inverse, hasConstituent, is inferred."),
        dict(heading="Source", term="prov:wasDerivedFrom", adds="Every company points to the two files it came from, described with DCAT."),
    ],
    heading_terms={
        "Company": ["gw:Company", "schema:name"], "Website": ["schema:url"], "Country": ["gw:country", "gw:Country"],
        "ICB Industry": ["gw:icbSubsector", "icb:industries"], "ICB code": ["gw:icbSubsector", "icb:industries"],
        "ICB concept IRI": ["gw:icbSubsector", "icb:industries"], "Revenue FY2024 (bn, approx.)": ["gw:revenueFY2024"],
        "Reporting currency": ["gw:reportingCurrency"], "Country currency": [],
        "ICB subsector": ["gw:icbSubsector", "icb:subsectors"], "Index": ["gw:isConstituentOf", "gw:StockIndex"],
        "Source": ["prov:wasDerivedFrom", "gwi:dataset-estx50", "gwi:distribution-icb-assignments"],
    },
    bad_paths={GW.country: "Country", GW.revenueFY2024: "Revenue", GW.icbSubsector: "ICB subsector"},
    graph=dict(width=760, company_sub="gw:Company · schema:Corporation",
               name=["schema:name", "schema"], url=["schema:url", "schema", "IRI"],
               revenue=["gw:revenueFY2024", "gw", "xsd:decimal"], currency=["gw:reportingCurrency", "gw", "ISO 4217"],
               revenue_node=None, index=["gw:isConstituentOf", "gw", "fibo:EquityIndex", "fibo"],
               country=["gw:country", "gw", "wd"], icb=["gw:icbSubsector", "icb"]),
    texts=dict(countries="Wikidata countries", mode_graph="Values as stored in the graph: IRIs, typed literals, links into ICB and Wikidata.",
               heat="Company counts. Countries are Wikidata entities, so this grid could be joined with any other dataset that uses them.",
               rules="A spreadsheet accepts any value in any cell. The shapes file states what a valid company looks like. The three rows below were planted to break one rule each; all three are caught, and the 50 real companies pass."),
)


def default_cells(rec, row, headings):
    sub = rec["icb"][3]
    graph = {
        "Company": [[rec["name"], "txt"], [f"gwi:{rec['id']}", "iri muted"]],
        "Website": [[f"<{rec['url']}>", "iri"]],
        "Country": [[rec["country"]["curie"], "iri"], [rec["country"]["code"], "txt"]],
        "Revenue FY2024 (bn, approx.)": [[f"{rec['revenue']:.1f}", "txt"], ["^^xsd:decimal", "iri muted"]],
        "Reporting currency": [[rec["currency"]["code"], "cur"]],
    }
    return graph


def default_adds(rec, row):
    return [
        ["Two types, one asserted each", f"{' and '.join('`' + t + '`' for t in rec['types'])}. Tools that know schema.org see a Corporation without running a reasoner."],
        ["Four ICB levels from one link", f"{' › '.join(l['label'] for l in rec['icb'])}. The file only says \"{row['ICB Industry']}\". Basis for the subsector: {rec['basis']}."],
        ["A country you can join on", f"`{rec['country']['curie']}` is {rec['country']['label']} in Wikidata, ISO code {rec['country']['code']}. The file has the text \"{row['Country']}\"."],
        ["Where it came from", f"{' and '.join(rec['sources'])}. The dataset description says the figures are approximate and the subsectors provisional."],
    ]


def default_examples(a):
    return {
        "Company": f'"{a["name"]}" names the resource gwi:{a["id"]}, typed gw:Company and schema:Corporation.',
        "Website": f'<{a["url"]}> is a link, not a string.',
        "Country": f'"{a["country"]["label"]}" is {a["country"]["curie"]}, ISO 3166 code {a["country"]["code"]}.',
        "Revenue FY2024 (bn, approx.)": f'{a["revenue"]} is an xsd:decimal, in {a["currency"]["code"]}, approximate.',
        "Reporting currency": f'"{a["currency"]["code"]}" is an ISO 4217 code, required to be three capital letters.',
        "Index": "gwi:index-euro-stoxx-50, typed gw:StockIndex and fibo-ind-mkt-bas:EquityIndex.",
    }


DEFAULT.update(cells=default_cells, adds=default_adds, examples=default_examples)


# ---------------------------------------------------------------------------
# Variant: FIBO (gwf:)
# ---------------------------------------------------------------------------
def fibo_record(g, co):
    ctry, rev = g.value(co, GWF.indexAssignedCountry), g.value(co, GWF.hasRevenue)
    amount = g.value(rev, FIBO_CUR.hasAmount) if rev is not None else None
    cur = g.value(rev, FIBO_CUR.hasCurrency) if rev is not None else None
    ident = next(g.subjects(CMNS_ID.identifies, cur), None) if cur is not None else None
    return dict(
        name=text(g, co, CMNS_DSG.hasTextualName), url=text(g, co, CMNS_ORG.hasWebsite),
        country=dict(iri=ctry, label=text(g, ctry, LCC_CR.hasEnglishShortName), code=""),
        revenue=float(Decimal(str(amount))) if amount is not None else None,
        currency=dict(code=text(g, ident, FIBO_REL.hasTag) if ident is not None else "", iri=cur),
        subsector=g.value(co, CMNS_CLS.isClassifiedBy), revenue_node=rev)


FIBO = dict(
    title_iri=URIRef("https://graphwise.ai/ontology/estx50-fibo"),
    ontology=[ONTO / "estx50-fibo-ontology.ttl"],
    vocab=[ONTO / "fibo-extract.ttl", VOCABS / "prov-o.ttl"],
    icb=[ONTO / "icb-skos.ttl", ONTO / "icb-fibo-alignment.ttl"], base_extra=[ONTO / "fibo-extract.ttl"],
    instances=DATA / "estx50-fibo-instances.ttl", demo=DATA / "violations-demo-fibo.ttl",
    shapes=ROOT / "shapes" / "shapes-fibo.ttl", queries=ROOT / "queries" / "business-queries-fibo.rq",
    out=ROOT / "docs" / "estx50-fibo-explorer.html", page_title="EURO STOXX 50 FIBO Semantic Layer", mapper="map_csv_fibo", inst_ns=GWFI,
    record=fibo_record,
    sources=[("gw", "This ontology (gwf:)"), ("fibo", "FIBO"), ("cmns", "OMG Commons"), ("lcc", "LCC countries"),
             ("icb", "ICB taxonomy (SKOS)"), ("prov", "PROV-O / DCAT")],
    columns={
        "Company": dict(term="cmns-dsg:hasTextualName", adds="Each row becomes gwfi:company-<slug>, typed fibo-be-le-cb:PubliclyHeldCompany. The name is a Commons textual name."),
        "Website": dict(term="cmns-org:hasWebsite", adds="Typed xsd:anyURI, the datatype OMG Commons expects for a website."),
        "Country": dict(term="gwf:indexAssignedCountry", adds="The text \"Germany\" becomes the LCC individual lcc-3166-1:Germany, the country IRI FIBO data shares. The property specialises cmns-loc:hasCountry."),
        "Revenue FY2024 (bn, approx.)": dict(term="gwf:hasRevenue", adds="The number becomes a revenue node: a FIBO monetary amount with fibo-fnd-acc-cur:hasAmount in billions, a currency and a reporting period."),
        "Reporting currency": dict(term="fibo-fnd-acc-cur:hasCurrency", adds="\"EUR\" becomes the FIBO currency fibo-fnd-acc-4217:Euro, which the ISO 4217 identifier EUR identifies. Totals group by it."),
    },
    added=[
        dict(heading="ICB subsector", term="cmns-cls:isClassifiedBy", adds="One Commons classification link to an 8-digit subsector, which is also typed as a FIBO ICB classifier. All four ICB levels follow."),
        dict(heading="Index", term="gwf:isConstituentOf", adds="A shortcut for FIBO's path from the index through its basket, constituent, listed share and issuer role to the company. The source has no share data."),
        dict(heading="Source", term="prov:wasDerivedFrom", adds="Every company and every revenue node points to the files it came from, described with DCAT."),
    ],
    heading_terms={
        "Company": ["fibo-be-le-cb:PubliclyHeldCompany", "cmns-dsg:hasTextualName"], "Website": ["cmns-org:hasWebsite"],
        "Country": ["gwf:indexAssignedCountry", "lcc-cr:Country"],
        "ICB Industry": ["cmns-cls:isClassifiedBy", "fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier", "icb:industries"],
        "ICB code": ["cmns-cls:isClassifiedBy", "fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier", "icb:industries"],
        "ICB concept IRI": ["cmns-cls:isClassifiedBy", "fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier", "icb:industries"],
        "Revenue FY2024 (bn, approx.)": ["gwf:hasRevenue", "gwf:Revenue", "fibo-fnd-acc-cur:hasAmount"],
        "Reporting currency": ["fibo-fnd-acc-cur:hasCurrency", "fibo-fnd-acc-cur:Currency"], "Country currency": [],
        "ICB subsector": ["cmns-cls:isClassifiedBy", "fibo-sec-sec-cls:IndustryClassificationBenchmarkClassifier", "icb:subsectors"],
        "Index": ["gwf:isConstituentOf", "fibo-ind-mkt-bas:EquityIndex"],
        "Source": ["prov:wasDerivedFrom", "gwfi:dataset-estx50", "gwfi:distribution-icb-assignments"],
    },
    bad_paths={GWF.indexAssignedCountry: "Country", GWF.hasRevenue: "Revenue", CMNS_CLS.isClassifiedBy: "ICB subsector"},
    graph=dict(width=840, company_sub="fibo-be-le-cb:PubliclyHeldCompany",
               name=["cmns-dsg:hasTextualName", "cmns"], url=["cmns-org:hasWebsite", "cmns", "xsd:anyURI"],
               revenue=["fibo-fnd-acc-cur:hasAmount", "fibo", "billions"], currency=["fibo-fnd-acc-cur:hasCurrency", "fibo", "fibo-fnd-acc-4217"],
               revenue_node=["gwf:hasRevenue", "gw", "gwf:Revenue · MonetaryAmount"],
               index=["gwf:isConstituentOf", "gw", "fibo-ind-mkt-bas:EquityIndex", "fibo"],
               country=["gwf:indexAssignedCountry", "gw", "lcc"], icb=["cmns-cls:isClassifiedBy", "cmns"]),
    texts=dict(countries="LCC countries", mode_graph="Values as stored in the graph: FIBO, Commons and LCC terms, typed literals, links into ICB.",
               heat="Company counts. Countries are LCC individuals, the country IRIs FIBO itself uses, so this grid joins with any FIBO dataset.",
               rules="A spreadsheet accepts any value in any cell. The FIBO shapes state what a valid company looks like, and deliberately skip FIBO expectations the source cannot meet, such as legal name and incorporation date. The three rows below were planted to break one rule each; all three are caught, and the 50 real companies pass."),
)


def fibo_cells(rec, row, headings):
    return {
        "Company": [[rec["name"], "txt"], [f"gwfi:{rec['id']}", "iri muted"]],
        "Website": [[f"\"{rec['url']}\"", "iri"], ["^^xsd:anyURI", "iri muted"]],
        "Country": [[rec["country"]["curie"], "iri"]],
        "Revenue FY2024 (bn, approx.)": [[rec["revenue_curie"], "iri"], [f"hasAmount {rec['revenue']:.1f}", "iri muted"]],
        "Reporting currency": [[rec["currency"]["curie"], "iri"], [rec["currency"]["code"], "cur"]],
    }


def fibo_adds(rec, row):
    return [
        ["A FIBO company, no local class", f"Typed `{rec['types'][0]}`: a corporation whose shares are traded and held publicly. Any FIBO-aware tool reads it as such, with no alignment axiom in between."],
        ["Revenue with its unit attached", f"`{rec['revenue_curie']}` is a FIBO monetary amount: {rec['revenue']:.1f} billion `{rec['currency']['curie']}`, for the reporting period FY2024. The file has two separate cells, \"{row['Revenue FY2024 (bn, approx.)']}\" and \"{row['Reporting currency']}\"."],
        ["Four ICB levels from one link", f"{' › '.join(l['label'] for l in rec['icb'])}. The file only says \"{row['ICB Industry']}\". Basis for the subsector: {rec['basis']}."],
        ["The country FIBO uses", f"`{rec['country']['curie']}` is the LCC individual for {rec['country']['label']}. The file has the text \"{row['Country']}\"."],
    ]


def fibo_examples(a):
    return {
        "Company": f'"{a["name"]}" names gwfi:{a["id"]}, typed fibo-be-le-cb:PubliclyHeldCompany.',
        "Website": f'"{a["url"]}" is typed xsd:anyURI.',
        "Country": f'"{a["country"]["label"]}" is {a["country"]["curie"]}, an LCC country.',
        "Revenue FY2024 (bn, approx.)": f'{a["revenue"]} is the fibo-fnd-acc-cur:hasAmount of {a["revenue_curie"]}, a gwf:Revenue, read as billions of {a["currency"]["code"]}.',
        "Reporting currency": f'"{a["currency"]["code"]}" is {a["currency"]["curie"]}, a FIBO currency identified by the ISO 4217 code {a["currency"]["code"]}.',
        "Index": "gwfi:index-euro-stoxx-50, typed fibo-ind-mkt-bas:EquityIndex, used directly.",
    }


FIBO.update(cells=fibo_cells, adds=fibo_adds, examples=fibo_examples)
VARIANTS = {"default": DEFAULT, "fibo": FIBO}


# ---------------------------------------------------------------------------
def load(*paths):
    g = Graph()
    for p in paths:
        g.parse(p)
    return g


def main(variant: str, fragment) -> int:
    cfg = VARIANTS[variant]
    column_map = __import__(cfg["mapper"]).COLUMN_MAP
    ont, vocab, icb = load(*cfg["ontology"]), load(*cfg["vocab"]), load(*cfg["icb"])
    inst, demo, shapes = load(cfg["instances"]), load(cfg["demo"]), load(cfg["shapes"])
    lookup = ont + vocab + icb + inst            # everything a label or definition can come from
    base = ont + load(*cfg["base_extra"]) + icb + inst   # the same graph run_tests.py queries

    prefixes = {}
    for g in (ont, vocab, inst, shapes, demo):
        for pfx, ns in g.namespaces():
            if pfx and pfx not in prefixes:
                prefixes[pfx] = str(ns)
    # The FIBO release declares the standard prefix of every module; read only its
    # header, since the full file is 222,000 lines. Without it, a few inherited FIBO
    # and Commons terms show as full IRIs.
    quick = VOCABS / "QuickFIBOProd.ttl"
    if quick.exists():
        with open(quick, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"@prefix ([\w-]+): <([^>]+)> \.", line)
                if m:
                    prefixes.setdefault(m[1], m[2])
                elif line.strip() and not line.startswith(("#", "@")):
                    break
    by_len = sorted(prefixes.items(), key=lambda kv: -len(kv[1]))

    def short(iri):
        s = str(iri)
        for pfx, ns in by_len:
            if s.startswith(ns) and re.fullmatch(r"[\w.-]*", s[len(ns):]):
                return f"{pfx}:{s[len(ns):]}"
        return s

    def iri(curie):
        pfx, local = curie.split(":", 1)
        return URIRef(prefixes[pfx] + local)

    def src(x):
        s = str(x)
        return next((k for ns, k in SOURCES if s.startswith(ns)), "none")

    shape_msgs = {}
    for ps in shapes.objects(None, SH.property):
        path, msg = shapes.value(ps, SH.path), shapes.value(ps, SH.message)
        if isinstance(path, URIRef) and msg is not None:
            shape_msgs[path] = str(msg)

    def definition(t):
        if t in MAPPING_NOTES:
            return MAPPING_NOTES[t]
        x = iri(t)
        return (text(lookup, x, SKOS.definition) or text(lookup, x, PROV.definition)
                or (text(lookup, x, RDFS.comment) if src(x) == "schema" else ""))

    # Columns.
    rows = list(csv.DictReader(open(CSV_MAIN, encoding="utf-8-sig")))
    headings = list(rows[0].keys())
    assign = {r["Company"]: r for r in csv.DictReader(open(CSV_ICB, encoding="utf-8"))}
    columns = []
    for h in headings:
        spec = DERIVED.get(h) or dict(cfg["columns"][h], fate="mapped")
        c = dict(spec, heading=h, mapping=column_map[h])
        if "source" not in c:
            c["source"] = src(iri(c["term"]))
        mapped = c["fate"] == "mapped"
        c["definition"] = definition(c["term"]) if c["fate"] != "dropped" else ""
        c["rule"] = shape_msgs.get(iri(c["term"]), "") if mapped else ""
        columns.append(c)
    for a in cfg["added"]:
        c = dict(a, fate="added", mapping=a["term"], source=src(iri(a["term"])))
        if a["heading"] == "ICB subsector":
            c["source"] = "icb"
        c["definition"] = definition(c["term"])
        c["rule"] = shape_msgs.get(iri(c["term"]), "")
        columns.append(c)

    # Companies.
    def icb_path(sub):
        path, node = [], sub
        while node is not None:
            code = text(icb, node, SKOS.notation)
            path.append(dict(code=code, label=text(icb, node, SKOS.prefLabel), level=LEVEL[len(code)]))
            node = icb.value(node, SKOS.broader)
        return list(reversed(path))

    companies = []
    g_rec = inst + vocab
    for r in rows:
        co = cfg["inst_ns"]["company-" + slug(r["Company"])]
        rec = cfg["record"](g_rec, co)
        rec["country"]["curie"] = short(rec["country"]["iri"])
        rec["country"]["iri"] = str(rec["country"]["iri"])
        rec["currency"]["curie"] = short(rec["currency"]["iri"]) if rec["currency"]["iri"] is not None else ""
        rec["currency"]["iri"] = str(rec["currency"]["iri"] or "")
        rev = rec.pop("revenue_node")
        rec["revenue_curie"] = short(rev) if rev is not None else ""
        rec.update(id=str(co).rsplit("/", 1)[-1], row=[r[h] for h in headings], icb=icb_path(rec.pop("subsector")),
                   basis=assign[r["Company"]]["Basis"],
                   sources=sorted(text(inst, d, DCTERMS.title) for d in inst.objects(co, PROV.wasDerivedFrom)),
                   types=sorted(short(t) for t in inst.objects(co, RDF.type)),
                   triples=len(list(inst.triples((co, None, None)))) + (len(list(inst.triples((rev, None, None)))) if rev is not None else 0))
        graph = cfg["cells"](rec, r, headings)
        sub = rec["icb"][3]
        added = {
            "ICB subsector": (sub["label"], [[f"icb:{sub['code']}", "iri"], [sub["label"], "txt"]]),
            "Index": ("EURO STOXX 50", [[f"{short(cfg['inst_ns'])}index-euro-stoxx-50", "iri"]]),
            "Source": (f"{len(rec['sources'])} files", [[f"{short(cfg['inst_ns'])}distribution-csv2", "iri"], ["+1", "txt"]]),
        }
        cells = []
        for c in columns:
            h = c["heading"]
            if c["fate"] == "added":
                csv_text, parts = added[h]
            else:
                csv_text = r[h]
                parts = (graph.get(h) or ([[f"↑ from icb:{sub['code']}", "derived"]] if c["fate"] == "derived" else [["not mapped", "muted"]]))
            cells.append(dict(csv=csv_text, graph=parts))
        rec["cells"] = cells
        rec["adds"] = cfg["adds"](rec, r)
        companies.append(rec)

    # Track B: run the real queries over the graph.
    questions = []
    for (qid, question), q in sections(cfg["queries"], "query"):
        res = base.query(q)
        out = []
        for row in res:
            vals = []
            for v in row:
                v = v.toPython() if isinstance(v, Literal) else (str(v) if v is not None else None)
                vals.append(float(v) if isinstance(v, Decimal) else v)
            out.append(vals)
        body = q.split("\n", 1)[1]
        sparql = "\n".join(l for l in body.splitlines() if not l.startswith("PREFIX")).strip()
        questions.append(dict(id=qid, question=question, table=TABLE_NOTES[qid], sparql=sparql,
                              vars=[str(v) for v in res.vars], rows=out))

    # SHACL demo: the three planted violations with their messages.
    _, rg, _ = validate(inst + icb + vocab + demo, shacl_graph=shapes, ont_graph=ont, inference="none")
    g_demo = demo + inst + vocab
    violations = []
    for res in rg.objects(None, SH.result):
        focus = rg.value(res, SH.focusNode)
        rec = cfg["record"](g_demo, focus)
        path = rg.value(res, SH.resultPath)
        violations.append(dict(
            id=str(focus).rsplit("/", 1)[-1], label=text(demo, focus, RDFS.label), name=rec["name"], url=rec["url"],
            country=rec["country"]["label"] if rec["country"]["iri"] is not None else "",
            icb=str(rec["subsector"]).rsplit("/", 1)[-1] if rec["subsector"] is not None else "",
            revenue=f"{rec['revenue']:.1f}" if rec["revenue"] is not None else "", currency=rec["currency"]["code"],
            path=short(path), column=cfg["bad_paths"].get(path, ""), message=text(rg, res, SH.resultMessage)))
    violations.sort(key=lambda v: v["id"])

    # Meaning: the labels, definitions and notes behind each heading, with the
    # definitions inherited through named superclasses and superproperties.
    note_kinds = [("definition", SKOS.definition), ("definition", PROV.definition), ("scope note", SKOS.scopeNote),
                  ("comment", RDFS.comment), ("description", DCTERMS.description), ("editorial note", SKOS.editorialNote),
                  ("note", SKOS.note)]

    def parents(x):
        for p in (RDFS.subClassOf, RDFS.subPropertyOf):
            named = sorted(o for o in lookup.objects(x, p) if isinstance(o, URIRef) and o != OWL.Thing)
            labelled = [o for o in named if text(lookup, o, RDFS.label)]
            if labelled or named:
                return (labelled or named)[0]
        return None

    def term_info(curie):
        x = iri(curie)
        s = src(x)
        info = dict(curie=curie, source=s, notes=[], inherited=[], facets=[],
                    label=text(lookup, x, RDFS.label) or text(lookup, x, SKOS.prefLabel) or text(lookup, x, DCTERMS.title))
        for kind, p in note_kinds:
            for v in sorted(lookup.objects(x, p)):
                if isinstance(v, Literal) and v.language not in (None, "en"):
                    continue
                info["notes"].append(dict(kind="definition" if s == "schema" and p == RDFS.comment else kind, text=str(v)))
        if s == "icb":
            info["notes"].append(dict(kind="scheme", text=text(icb, ICB["scheme"], DCTERMS.description)))
        types = set(lookup.objects(x, RDF.type))
        info["kind"] = ("class" if types & {OWL.Class, RDFS.Class} else "collection" if SKOS.Collection in types
                        else "property" if types & {OWL.ObjectProperty, OWL.DatatypeProperty, RDF.Property}
                        else "record" if str(x).startswith("https://graphwise.ai/instance/") else "property")
        if OWL.FunctionalProperty in types:
            info["facets"].append("one value per company (functional)")
        d, r = first(lookup, x, RDFS.domain), first(lookup, x, RDFS.range)
        if isinstance(d, URIRef) or isinstance(r, URIRef):
            info["facets"].append(f"from {short(d) if isinstance(d, URIRef) else 'anything'} to {short(r) if isinstance(r, URIRef) else 'anything'}")
        inv = first(lookup, x, OWL.inverseOf)
        if inv is not None:
            info["facets"].append(f"inverse: {short(inv)}, inferred by the reasoner")
        if x in shape_msgs:
            info["facets"].append("rule: " + shape_msgs[x])
        node, seen = parents(x), set()
        while node is not None and node not in seen and len(info["inherited"]) < 8:
            seen.add(node)
            step = dict(curie=short(node), source=src(node), label=text(lookup, node, RDFS.label),
                        definition=text(lookup, node, SKOS.definition) or text(lookup, node, PROV.definition)
                        or (text(lookup, node, RDFS.comment) if src(node) == "schema" else ""))
            if step["label"] or step["definition"]:   # skip steps the bundled files say nothing about
                info["inherited"].append(step)
            node = parents(node)
        return info

    terms = {}
    for curies in cfg["heading_terms"].values():
        for t in curies:
            terms.setdefault(t, term_info(t))
    a = next(c for c in companies if c["id"] == "company-asml-holding")
    sub, top = a["icb"][3], a["icb"][0]
    examples = {
        "ICB Industry": f'"{top["label"]}" is icb:{top["code"]}, reached from icb:{sub["code"]} {sub["label"]}.',
        "ICB code": f'"{top["code"]}" is the skos:notation of icb:{top["code"]}, the ICB industry {top["label"]}.',
        "ICB concept IRI": f'Cross-checked against the industry reached from icb:{sub["code"]}.',
        "Country currency": "Not mapped. Its meaning stays in the heading.",
        "ICB subsector": f'icb:{sub["code"]} {sub["label"]}, a member of the subsector level.',
        "Source": "Two dcat:Distributions: the constituents CSV and the provisional subsector assignments.",
        **cfg["examples"](a),
    }
    meaning = dict(terms=terms, headings=[dict(heading=c["heading"], fate=c["fate"], terms=cfg["heading_terms"][c["heading"]],
                                               example=examples[c["heading"]]) for c in columns])

    data = dict(
        variant=variant, title=text(ont, cfg["title_iri"], DCTERMS.title), version=text(ont, cfg["title_iri"], OWL.versionInfo),
        headings=headings, columns=columns, companies=companies, questions=questions, violations=violations,
        sources=cfg["sources"], graph=cfg["graph"], texts=cfg["texts"], meaning=meaning,
        stats=dict(rows=len(rows), cells=len(rows) * len(headings), triples=len(base), instance_triples=len(inst),
                   icb_concepts=len(set(icb.subjects(RDF.type, SKOS.Concept))),
                   countries=len({c["country"]["iri"] for c in companies})),
    )
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (TEMPLATE.read_text(encoding="utf-8").replace("/*__DATA__*/null", payload)
            .replace("<title>EURO STOXX 50 Semantic Layer</title>", f"<title>{cfg['page_title']}</title>"))
    script = "scripts/build_explorer.py" + (f" --variant {variant}" if variant != "default" else "")
    note = f"<!-- Generated by {script} from docs/explorer-template.html. Do not edit by hand. -->\n"
    out = cfg["out"]
    out.write_text("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
                   "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
                   "</head>\n<body>\n" + note + page + "\n</body>\n</html>\n", encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}: {len(companies)} companies, {len(questions)} questions, "
          f"{len(violations)} violations")
    if fragment:
        Path(fragment).write_text(page, encoding="utf-8", newline="\n")
        print(f"Wrote fragment {fragment}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    variant, fragment = "default", None
    while args:
        flag = args.pop(0)
        if flag == "--variant" and args:
            variant = args.pop(0)
        elif flag == "--fragment" and args:
            fragment = args.pop(0)
        else:
            sys.exit("Usage: python scripts/build_explorer.py [--variant fibo] [--fragment PATH]")
    if variant not in VARIANTS:
        sys.exit(f"Unknown variant {variant!r}; choose one of {', '.join(VARIANTS)}")
    sys.exit(main(variant, fragment))
