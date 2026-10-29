"""Run one SPARQL query over the tutorial graph and print the result as a table.

Usage: python scripts/query.py QUERY.rq [--variant fibo|bridge] [--reason] [--add FILE ...] [--root PATH]
  --variant which graph to load (see VARIANTS below; default: the 2.0.0 ontology and data)
  --reason  add the OWL RL closure first (what GraphDB's OWL2-RL ruleset would infer)
  --add     also load these Turtle files, for example data/violations-demo.ttl
  --root    the tutorial folder to read the graph from (default: this one), for
            example the tutorial folder of an earlier stage checked out as a worktree
"""
import argparse
import re
import sys
from pathlib import Path

import owlrl
from rdflib import Graph, URIRef

ROOT = Path(__file__).resolve().parent.parent

VARIANTS = {
    "default": ["ontology/estx50-ontology.ttl", "ontology/icb-skos.ttl", "data/estx50-instances.ttl"],
    "fibo": ["ontology/estx50-fibo-ontology.ttl", "ontology/fibo-extract.ttl", "ontology/icb-skos.ttl",
             "ontology/icb-fibo-alignment.ttl", "data/estx50-fibo-instances.ttl"],
    # 2.0.0 data read through the optional bridge; the links only take effect with --reason.
    "bridge": ["ontology/estx50-ontology.ttl", "ontology/icb-skos.ttl", "data/estx50-instances.ttl",
               "ontology/estx50-fibo-bridge.ttl", "ontology/estx50-fibo-ontology.ttl", "ontology/fibo-extract.ttl",
               "ontology/icb-fibo-alignment.ttl"],
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Run a SPARQL query over the tutorial graph.")
    ap.add_argument("query", type=Path)
    ap.add_argument("--variant", choices=VARIANTS, default="default")
    ap.add_argument("--reason", action="store_true")
    ap.add_argument("--add", type=Path, nargs="+", default=[])
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()

    files = [args.root / f for f in VARIANTS[args.variant]]
    g = Graph()
    for f in files + args.add:
        g.parse(f)
    if args.reason:
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)

    text = args.query.read_text(encoding="utf-8")
    # Print IRIs with the prefixes the query declares, as well as those of the loaded files.
    for prefix, iri in re.findall(r"^PREFIX\s+([\w-]*):\s*<([^>]*)>", text, flags=re.M | re.I):
        g.bind(prefix, iri, override=True, replace=True)
    sys.stdout.reconfigure(encoding="utf-8")
    res = g.query(text)
    if res.type == "ASK":
        print(res.askAnswer)
        return 0
    if res.type != "SELECT":
        print(res.serialize(format="turtle").decode())
        return 0
    rows = [[g.namespace_manager.normalizeUri(v) if isinstance(v, URIRef) else ("" if v is None else str(v))
             for v in row] for row in res]
    head = [str(v) for v in res.vars]
    widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h) for i, h in enumerate(head)]
    print("  ".join(h.ljust(w) for h, w in zip(head, widths)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(c.ljust(w) for c, w in zip(r, widths)))
    print(f"({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
