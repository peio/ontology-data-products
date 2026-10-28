"""FIBO variant: build the ICB-to-FIBO alignment and the FIBO extract.

Usage: python scripts/build_fibo_files.py   (run from the project root, after map_csv_fibo.py)
Needs ontologies/QuickFIBOProd.ttl (FIBO 2026Q2 production, all modules in one file).
Writes ontology/icb-fibo-alignment.ttl and ontology/fibo-extract.ttl.

The extract holds every FIBO, OMG Commons and LCC term the FIBO variant uses
(in the ontology, the alignment, the instances and the shapes), plus their named
parents, domains and ranges up to the top: type, label, definition and those
links only, with no restrictions. The build fails if a used term is not in
QuickFIBOProd, so the extract doubles as an existence check.
"""
import sys
from pathlib import Path

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS, XSD

ROOT = Path(__file__).resolve().parent.parent
FIBO_SRC = ROOT / "ontologies" / "QuickFIBOProd.ttl"
ICB_TTL = ROOT / "ontology" / "icb-skos.ttl"
ALIGN = ROOT / "ontology" / "icb-fibo-alignment.ttl"
EXTRACT = ROOT / "ontology" / "fibo-extract.ttl"
USERS = [ROOT / "ontology" / "estx50-fibo-ontology.ttl", ALIGN,
         ROOT / "data" / "estx50-fibo-instances.ttl", ROOT / "shapes" / "shapes-fibo.ttl"]

ICB = Namespace("https://graphwise.ai/taxonomy/icb/")
FIBO_CLS = Namespace("https://spec.edmcouncil.org/fibo/ontology/SEC/Securities/SecuritiesClassification/")
CMNS_DSG = Namespace("https://www.omg.org/spec/Commons/Designators/")
CMNS_ID = Namespace("https://www.omg.org/spec/Commons/Identifiers/")
FIBO_CUR = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/CurrencyAmount/")
FIBO_REL = Namespace("https://spec.edmcouncil.org/fibo/ontology/FND/Relations/Relations/")
LCC_CR = Namespace("https://www.omg.org/spec/LCC/Countries/CountryRepresentation/")
FIBO_VERSION = URIRef("https://spec.edmcouncil.org/fibo/ontology/master/2026Q2/QuickFIBOProd/")

COVERED = ("https://spec.edmcouncil.org/fibo/", "https://www.omg.org/spec/")
TERM_TYPES = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty,
              OWL.FunctionalProperty, OWL.TransitiveProperty, OWL.SymmetricProperty,
              OWL.InverseFunctionalProperty, RDFS.Datatype, OWL.NamedIndividual}
TERM_LINKS = [RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range, OWL.inverseOf]
# What is copied for a named individual (country, currency, scheme).
INDIVIDUAL_FACTS = [RDFS.label, SKOS.definition, LCC_CR.hasEnglishShortName, LCC_CR.hasEnglishFullName,
                    FIBO_CUR.hasNumericCode, FIBO_REL.hasTag, CMNS_ID.identifies]

PREFIXES = {
    "fibo-be-le-cb": "https://spec.edmcouncil.org/fibo/ontology/BE/LegalEntities/CorporateBodies/",
    "fibo-ind-mkt-bas": "https://spec.edmcouncil.org/fibo/ontology/IND/MarketIndices/BasketIndices/",
    "fibo-fnd-acc-cur": str(FIBO_CUR),
    "fibo-fnd-acc-4217": "https://spec.edmcouncil.org/fibo/ontology/FND/Accounting/ISO4217-CurrencyCodes/",
    "fibo-fnd-arr-cls": "https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/ClassificationSchemes/",
    "fibo-fnd-arr-doc": "https://spec.edmcouncil.org/fibo/ontology/FND/Arrangements/Documents/",
    "fibo-fnd-rel-rel": str(FIBO_REL),
    "fibo-sec-sec-cls": str(FIBO_CLS),
    "cmns-cls": "https://www.omg.org/spec/Commons/Classifiers/",
    "cmns-dsg": str(CMNS_DSG),
    "cmns-dt": "https://www.omg.org/spec/Commons/DatesAndTimes/",
    "cmns-id": str(CMNS_ID),
    "cmns-loc": "https://www.omg.org/spec/Commons/Locations/",
    "cmns-org": "https://www.omg.org/spec/Commons/Organizations/",
    "lcc-cr": str(LCC_CR),
    "lcc-3166-1": "https://www.omg.org/spec/LCC/Countries/ISO3166-1-CountryCodes/",
}


def covered(t) -> bool:
    return isinstance(t, URIRef) and str(t).startswith(COVERED)


def module_of(t: URIRef) -> URIRef:
    return URIRef(str(t).rsplit("/", 1)[0] + "/")


def build_alignment() -> Graph:
    icb = Graph().parse(ICB_TTL)
    g = Graph()
    g.bind("icb", ICB)
    g.bind("fibo-sec-sec-cls", FIBO_CLS)
    g.bind("cmns-dsg", CMNS_DSG)
    ont = URIRef("https://graphwise.ai/taxonomy/icb/fibo-alignment")
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, DCTERMS.title, Literal("ICB to FIBO alignment", lang="en")))
    g.add((ont, DCTERMS.description, Literal(
        "Types every concept of the ICB SKOS scheme as a FIBO ICB classifier defined in FIBO's ICB scheme, "
        "so companies classified with cmns-cls:isClassifiedBy point to FIBO classifiers. FIBO has the ICB "
        "classifier class and the scheme individual but no ICB codes; the codes and the skos:broader "
        "hierarchy stay in icb-skos.ttl, which is unchanged.", lang="en")))
    g.add((ont, OWL.versionIRI, URIRef("https://graphwise.ai/taxonomy/icb/fibo-alignment/1.0.0")))
    g.add((ont, OWL.versionInfo, Literal("1.0.0")))
    g.add((ont, DCTERMS.created, Literal("2026-10-28", datatype=XSD.date)))
    for c in sorted(set(icb.subjects(SKOS.inScheme, ICB.scheme))):
        g.add((c, RDF.type, FIBO_CLS.IndustryClassificationBenchmarkClassifier))
        g.add((c, CMNS_DSG.isDefinedIn, FIBO_CLS.IndustryClassificationBenchmarkScheme))
    return g


def build_extract(fibo: Graph, used: set) -> tuple[Graph, list]:
    g = Graph()
    for p, ns in PREFIXES.items():
        g.bind(p, ns)
    missing, done = [], set()
    todo = sorted(used)
    # Currency identifiers (e.g. fibo-fnd-acc-4217:EUR) carry the ISO code of a currency.
    for cur in [t for t in used if (t, RDF.type, FIBO_CUR.Currency) in fibo]:
        todo += [i for i in fibo.subjects(CMNS_ID.identifies, cur) if (i, RDF.type, FIBO_CUR.CurrencyIdentifier) in fibo]
    while todo:
        t = todo.pop()
        if t in done:
            continue
        done.add(t)
        types = set(fibo.objects(t, RDF.type))
        if not types:
            missing.append(t)
            continue
        individual = OWL.NamedIndividual in types
        for ty in types:
            if isinstance(ty, BNode):
                continue
            g.add((t, RDF.type, ty))
            if individual and covered(ty):
                todo.append(ty)
        facts = INDIVIDUAL_FACTS if individual else [RDFS.label, SKOS.definition] + TERM_LINKS
        for p in facts:
            for o in fibo.objects(t, p):
                if isinstance(o, BNode):
                    continue
                g.add((t, p, o))
                if covered(o):
                    todo.append(o)
                if covered(p):
                    todo.append(p)
        if not individual and (t, RDFS.isDefinedBy, None) not in fibo:
            g.add((t, RDFS.isDefinedBy, module_of(t)))
        for o in fibo.objects(t, RDFS.isDefinedBy):
            g.add((t, RDFS.isDefinedBy, o))
    return g, missing


def main() -> int:
    if not FIBO_SRC.exists():
        print(f"Missing {FIBO_SRC.relative_to(ROOT)}: download QuickFIBOProd.ttl (FIBO 2026Q2 production) first.")
        return 1
    align = build_alignment()
    ALIGN.write_text(
        "# Generated by scripts/build_fibo_files.py from ontology/icb-skos.ttl. Do not edit by hand.\n"
        + align.serialize(format="turtle"), encoding="utf-8")
    print(f"Wrote {ALIGN.relative_to(ROOT)}: {len(align)} triples")

    used = set()
    for f in USERS:
        if not f.exists():
            print(f"  (skipping {f.relative_to(ROOT)}: not built yet)")
            continue
        for triple in Graph().parse(f):
            used |= {t for t in triple if covered(t)}

    fibo = Graph().parse(FIBO_SRC)
    if (None, OWL.versionIRI, FIBO_VERSION) not in fibo:
        print(f"Unexpected FIBO version in {FIBO_SRC.name}: expected {FIBO_VERSION}")
        return 1
    extract, missing = build_extract(fibo, used)
    if missing:
        print("Not in QuickFIBOProd (invented, misspelled or moved?):\n  " + "\n  ".join(sorted(map(str, missing))))
        return 1

    ont = URIRef("https://graphwise.ai/ontology/estx50-fibo/fibo-extract")
    extract.add((ont, RDF.type, OWL.Ontology))
    extract.add((ont, DCTERMS.title, Literal("FIBO extract for the EURO STOXX 50 ontology (FIBO variant)", lang="en")))
    extract.add((ont, DCTERMS.description, Literal(
        "Labels, definitions, named parents, domains and ranges of the FIBO, OMG Commons and LCC terms the FIBO "
        "variant uses, up to the top of each hierarchy, plus the country, currency and scheme individuals it refers "
        "to. Copied unchanged from FIBO; restrictions are left out. Load it alongside the ontology instead of "
        "importing the whole of FIBO.", lang="en")))
    extract.add((ont, DCTERMS.source, FIBO_VERSION))
    extract.add((ont, DCTERMS.license, URIRef("https://opensource.org/licenses/MIT")))
    extract.add((ont, DCTERMS.rights, Literal(
        "Copyright (c) 2018-2026 EDM Association dba EDM Council, Inc. Copyright (c) 2018-2025 Object Management "
        "Group, Inc. Released under the MIT License.")))
    extract.add((ont, OWL.versionInfo, Literal("FIBO 2026Q2")))
    EXTRACT.write_text(
        "# Generated by scripts/build_fibo_files.py from ontologies/QuickFIBOProd.ttl. Do not edit by hand.\n"
        + extract.serialize(format="turtle"), encoding="utf-8")
    terms = {s for s in extract.subjects(RDF.type, None) if covered(s)}
    inds = {s for s in extract.subjects(RDF.type, OWL.NamedIndividual)}
    print(f"Wrote {EXTRACT.relative_to(ROOT)}: {len(extract)} triples, {len(used)} terms used directly, "
          f"{len(terms) - len(inds)} classes and properties with their parents, {len(inds)} individuals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
