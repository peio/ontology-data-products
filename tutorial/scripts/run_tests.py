"""Step 7: run Track A (robustness) and Track B (business) tests.

Usage: python scripts/run_tests.py [--variant fibo]   (run from the project root, after
map_csv.py and make_answer_key.py; for the FIBO variant, after map_csv_fibo.py and
build_fibo_files.py). Writes reports/test-report.md and reports/shacl-*.txt, or
reports/test-report-fibo.md and reports/shacl-fibo-*.txt for the FIBO variant.
Exits 1 if any check fails.
"""
import csv
import importlib
import re
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import owlrl
from pyshacl import validate
from rdflib import Graph, Literal, URIRef

ROOT = Path(__file__).resolve().parent.parent
ICB = ROOT / "ontology" / "icb-skos.ttl"
REPORTS = ROOT / "reports"

VARIANTS = {
    "default": {
        "title": "EURO STOXX 50 ontology",
        "ontology": [ROOT / "ontology" / "estx50-ontology.ttl"],
        "icb": [ICB],
        "instances": ROOT / "data" / "estx50-instances.ttl",
        "demo": ROOT / "data" / "violations-demo.ttl",
        "shapes": ROOT / "shapes" / "shapes.ttl",
        "tests": ROOT / "queries" / "robustness-tests.rq",
        "queries": ROOT / "queries" / "business-queries.rq",
        "answer_key": ROOT / "queries" / "answer-key.csv",
        "suffix": "",
        "mapper": "map_csv",
        "classified_by": "https://graphwise.ai/ontology/estx50/icbSubsector",
    },
    "fibo": {
        "title": "EURO STOXX 50 ontology, FIBO variant",
        "ontology": [ROOT / "ontology" / "estx50-fibo-ontology.ttl", ROOT / "ontology" / "fibo-extract.ttl"],
        "icb": [ICB, ROOT / "ontology" / "icb-fibo-alignment.ttl"],
        "instances": ROOT / "data" / "estx50-fibo-instances.ttl",
        "demo": ROOT / "data" / "violations-demo-fibo.ttl",
        "shapes": ROOT / "shapes" / "shapes-fibo.ttl",
        "tests": ROOT / "queries" / "robustness-tests-fibo.rq",
        "queries": ROOT / "queries" / "business-queries-fibo.rq",
        "answer_key": ROOT / "queries" / "answer-key-fibo.csv",
        "suffix": "-fibo",
        "mapper": "map_csv_fibo",
        "classified_by": "https://www.omg.org/spec/Commons/Classifiers/isClassifiedBy",
    },
}


def load(*paths) -> Graph:
    g = Graph()
    for p in paths:
        g.parse(p)
    return g


def sections(path: Path, tag: str):
    """Split a .rq file into (id, extra, description, query) by '# @<tag>' headers."""
    text = path.read_text(encoding="utf-8")
    prefixes = "\n".join(l for l in text.splitlines() if l.startswith("PREFIX"))
    parts = re.split(rf"^# @{tag} ", text, flags=re.M)[1:]
    for part in parts:
        header, _, body = part.partition("\n")
        fields = [f.strip() for f in header.split("|")]
        yield fields, prefixes + "\n" + body


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, Literal):
        v = v.toPython()
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (Decimal, float)):
        return f"{Decimal(str(v)):.1f}"
    return str(v)


def main(variant: str = "default") -> int:
    cfg = VARIANTS[variant]
    sfx = cfg["suffix"]
    REPORTS.mkdir(exist_ok=True)
    ont = load(*cfg["ontology"][:1])
    base = load(*cfg["ontology"], *cfg["icb"], cfg["instances"])
    icb = load(*cfg["icb"])
    reasoned = Graph()
    for t in base:
        reasoned.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(reasoned)
    graphs = {"ontology": ont, "base": base, "reasoned": reasoned, "icb": icb}

    results_a = []  # (id, description, passed, detail)

    # Track A: SPARQL ASK tests.
    for (tid, gname, desc), q in sections(cfg["tests"], "test"):
        ok = bool(graphs[gname].query(q).askAnswer)
        results_a.append((tid, desc, ok, f"ASK on {gname} graph"))

    # Track A3: SHACL on the clean data. The FIBO variant needs the extract and the
    # ICB alignment in the data graph, for the types of countries, currencies and classifiers.
    data_extra = [*cfg["icb"], *cfg["ontology"][1:]]
    conforms, _, text = validate(load(cfg["instances"], *data_extra), shacl_graph=load(cfg["shapes"]),
                                 ont_graph=load(*cfg["ontology"][:1]), inference="none", allow_warnings=False)
    (REPORTS / f"shacl{sfx}-clean.txt").write_text(text, encoding="utf-8")
    results_a.append(("A3a", "SHACL: the 50 companies conform to all shapes", conforms,
                      "0 violations" if conforms else f"see reports/shacl{sfx}-clean.txt"))

    # Track A3: SHACL on the planted violations (teaching aid) must fail exactly 3 times.
    _, rg, text = validate(load(cfg["instances"], *data_extra, cfg["demo"]), shacl_graph=load(cfg["shapes"]),
                           ont_graph=load(*cfg["ontology"][:1]), inference="none")
    (REPORTS / f"shacl{sfx}-violations-demo.txt").write_text(text, encoding="utf-8")
    SH = "http://www.w3.org/ns/shacl#"
    # Top-level results only (sh:result of the report); nested sh:detail results are not counted.
    top = list(rg.objects(None, URIRef(SH + "result")))
    focus = sorted(str(rg.value(r, URIRef(SH + "focusNode"))).rsplit("/", 1)[-1] for r in top)
    expected = ["demo-industry-level", "demo-negative-revenue", "demo-no-country"]
    results_a.append(("A3b", "SHACL: the planted violations are caught (3 expected, 1 per demo company)",
                      focus == expected, f"focus nodes: {', '.join(focus) or 'none'}"))

    # Track A5b: mapping completeness against the CSV (outside SPARQL).
    rows = list(csv.DictReader(open(ROOT / "data" / "EURO_STOXX_50_Constituents_CSV2.csv", encoding="utf-8-sig")))
    COLUMN_MAP = importlib.import_module(cfg["mapper"]).COLUMN_MAP
    from map_csv import industry_of  # noqa: E402
    cols_ok = set(rows[0]) == set(COLUMN_MAP)
    results_a.append(("A5b", "Every CSV column is either mapped or intentionally dropped", cols_ok,
                      f"{len(COLUMN_MAP)} columns accounted for"))
    mismatch = []
    for r in rows:
        co = next(base.subjects(URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(r["Company"])))
        sub = base.value(co, URIRef(cfg["classified_by"]))
        if industry_of(icb, sub) != URIRef(r["ICB concept IRI"]):
            mismatch.append(r["Company"])
    results_a.append(("A5c", "Every subsector rolls up (skos:broader+) to the industry stated in CSV2", not mismatch,
                      "50 of 50 consistent" if not mismatch else f"mismatches: {mismatch}"))

    # Track B.
    key = {}
    for r in csv.DictReader(open(cfg["answer_key"], encoding="utf-8")):
        key.setdefault(r["query"], []).append((r["key"], r["value"]))
    results_b = []
    for (qid, question), q in sections(cfg["queries"], "query"):
        res = base.query(q)
        got = [(fmt(row[0]), "|".join(fmt(v) for v in row[1:])) for row in res]
        exp = key.get(qid, [])
        ok = sorted(got) == sorted(exp)
        results_b.append((qid, question, ok, got, exp))

    # Report.
    a_pass = sum(r[2] for r in results_a)
    b_pass = sum(r[2] for r in results_b)
    script = "scripts/run_tests.py" + (f" --variant {variant}" if variant != "default" else "")
    lines = [
        f"# Test report: {cfg['title']}",
        "",
        f"Generated by `{script}` on {date.today().isoformat()}.",
        "",
        f"**Track A (robustness): {a_pass}/{len(results_a)} passed. "
        f"Track B (business): {b_pass}/{len(results_b)} passed.**",
        "",
        "Graph sizes: base {} triples; after OWL RL closure {} triples.".format(len(base), len(reasoned)),
        "",
        "## Track A: robustness",
        "",
        "| Test | Check | Result | Detail |",
        "| --- | --- | --- | --- |",
    ]
    for tid, desc, ok, detail in sorted(results_a):
        lines.append(f"| {tid} | {desc} | {'PASS' if ok else 'FAIL'} | {detail} |")
    lines += ["", "## Track B: business questions", ""]
    for qid, question, ok, got, exp in results_b:
        lines += [f"### {qid}: {question} ({'PASS' if ok else 'FAIL'})", "",
                  "| Key | Actual | Expected |", "| --- | --- | --- |"]
        exp_d = dict(exp)
        keys = [k for k, _ in got] + [k for k, _ in exp if k not in dict(got)]
        got_d = dict(got)
        for k in keys:
            lines.append(f"| {k} | {got_d.get(k, '—') or '✓'} | {exp_d.get(k, '—') or '✓'} |")
        lines.append("")
    lines += [
        "Value formats: revenue sums in billions as reported, per reporting currency, `revenue|companies`; booleans as `true`/`false`; "
        "`✓` = the row is present (no value to compare).",
        "",
    ]
    (REPORTS / f"test-report{sfx}.md").write_text("\n".join(lines), encoding="utf-8")

    for tid, desc, ok, detail in sorted(results_a):
        print(f"{'PASS' if ok else 'FAIL'}  {tid}  {desc}  [{detail}]")
    for qid, question, ok, got, exp in results_b:
        print(f"{'PASS' if ok else 'FAIL'}  {qid}  {question}")
        if not ok:
            print("   got:", got, "\n   exp:", exp)
    print(f"\nTrack A {a_pass}/{len(results_a)}, Track B {b_pass}/{len(results_b)}")
    return 0 if a_pass == len(results_a) and b_pass == len(results_b) else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    args = sys.argv[1:]
    variant = args[1] if args[:1] == ["--variant"] and len(args) == 2 else "default"
    if args and variant == "default":
        sys.exit(f"Usage: python scripts/run_tests.py [--variant {'|'.join(v for v in VARIANTS if v != 'default')}]")
    sys.exit(main(variant))
