"""Step 7: run Track A (robustness) and Track B (business) tests.

Usage: python scripts/run_tests.py   (run from the project root, after map_csv.py
and make_answer_key.py). Writes reports/test-report.md and reports/shacl-*.txt.
Exits 1 if any check fails.
"""
import csv
import re
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

import owlrl
from pyshacl import validate
from rdflib import Graph, Literal, URIRef

ROOT = Path(__file__).resolve().parent.parent
ONT = ROOT / "ontology" / "estx50-ontology.ttl"
ICB = ROOT / "ontology" / "icb-skos.ttl"
INST = ROOT / "data" / "estx50-instances.ttl"
DEMO = ROOT / "data" / "violations-demo.ttl"
SHAPES = ROOT / "shapes" / "shapes.ttl"
REPORTS = ROOT / "reports"


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


def main() -> int:
    REPORTS.mkdir(exist_ok=True)
    base = load(ONT, ICB, INST)
    icb = load(ICB)
    reasoned = Graph()
    for t in base:
        reasoned.add(t)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(reasoned)
    graphs = {"base": base, "reasoned": reasoned, "icb": icb}

    results_a = []  # (id, description, passed, detail)

    # Track A: SPARQL ASK tests.
    for (tid, gname, desc), q in sections(ROOT / "queries" / "robustness-tests.rq", "test"):
        ok = bool(graphs[gname].query(q).askAnswer)
        results_a.append((tid, desc, ok, f"ASK on {gname} graph"))

    # Track A3: SHACL on the clean data.
    conforms, _, text = validate(load(INST, ICB), shacl_graph=load(SHAPES), ont_graph=load(ONT),
                                 inference="none", allow_warnings=False)
    (REPORTS / "shacl-clean.txt").write_text(text, encoding="utf-8")
    results_a.append(("A3a", "SHACL: the 50 companies conform to all shapes", conforms,
                      "0 violations" if conforms else "see reports/shacl-clean.txt"))

    # Track A3: SHACL on the planted violations (teaching aid) must fail exactly 3 times.
    _, rg, text = validate(load(INST, ICB, DEMO), shacl_graph=load(SHAPES), ont_graph=load(ONT),
                           inference="none")
    (REPORTS / "shacl-violations-demo.txt").write_text(text, encoding="utf-8")
    SH = "http://www.w3.org/ns/shacl#"
    # Top-level results only (sh:result of the report); nested sh:detail results are not counted.
    top = list(rg.objects(None, URIRef(SH + "result")))
    focus = sorted(str(rg.value(r, URIRef(SH + "focusNode"))).rsplit("/", 1)[-1] for r in top)
    expected = ["demo-industry-level", "demo-negative-revenue", "demo-no-country"]
    results_a.append(("A3b", "SHACL: the planted violations are caught (3 expected, 1 per demo company)",
                      focus == expected, f"focus nodes: {', '.join(focus) or 'none'}"))

    # Track A5b: mapping completeness against the CSV (outside SPARQL).
    rows = list(csv.DictReader(open(ROOT / "data" / "EURO_STOXX_50_Constituents_CSV2.csv", encoding="utf-8-sig")))
    from map_csv import COLUMN_MAP, industry_of  # noqa: E402
    cols_ok = set(rows[0]) == set(COLUMN_MAP)
    results_a.append(("A5b", "Every CSV column is either mapped or intentionally dropped", cols_ok,
                      f"{len(COLUMN_MAP)} columns accounted for"))
    GW ="https://graphwise.ai/ontology/"
    mismatch = []
    for r in rows:
        co = next(base.subjects(URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(r["Company"])))
        sub = base.value(co, URIRef(GW + "icbSubsector"))
        if industry_of(icb, sub) != URIRef(r["ICB concept IRI"]):
            mismatch.append(r["Company"])
    results_a.append(("A5c", "Every subsector rolls up (skos:broader+) to the industry stated in CSV2", not mismatch,
                      "50 of 50 consistent" if not mismatch else f"mismatches: {mismatch}"))

    # Track B.
    key = {}
    for r in csv.DictReader(open(ROOT / "queries" / "answer-key.csv", encoding="utf-8")):
        key.setdefault(r["query"], []).append((r["key"], r["value"]))
    results_b = []
    for (qid, question), q in sections(ROOT / "queries" / "business-queries.rq", "query"):
        res = base.query(q)
        got = [(fmt(row[0]), "|".join(fmt(v) for v in row[1:])) for row in res]
        exp = key.get(qid, [])
        ok = sorted(got) == sorted(exp)
        results_b.append((qid, question, ok, got, exp))

    # Report.
    a_pass = sum(r[2] for r in results_a)
    b_pass = sum(r[2] for r in results_b)
    lines = [
        "# Test report: EURO STOXX 50 ontology",
        "",
        f"Generated by `scripts/run_tests.py` on {date.today().isoformat()}.",
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
        "Value formats: revenue sums in billions as reported, `revenue|companies`; booleans as `true`/`false`; "
        "`✓` = the row is present (no value to compare).",
        "",
    ]
    (REPORTS / "test-report.md").write_text("\n".join(lines), encoding="utf-8")

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
    sys.exit(main())
