"""Step 1/7: compute the Track B answer key directly from the source CSVs.

The key is computed WITHOUT the RDF graph, so Track B tests the graph against an
independent calculation. Writes queries/answer-key.csv.
"""
import csv
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader(open(ROOT / "data" / "EURO_STOXX_50_Constituents_CSV2.csv", encoding="utf-8-sig")))
assign = {r["Company"]: r for r in csv.DictReader(open(ROOT / "data" / "icb-subsector-assignments.csv", encoding="utf-8"))}
REV = "Revenue FY2024 (bn, approx.)"
CUR = "Reporting currency"

key = []  # (query_id, key, value)

# B1: banks = subsector code starting with the Banks supersector code 3010.
for name in sorted(r["Company"] for r in rows if assign[r["Company"]]["ICB subsector code"].startswith("3010")):
    key.append(("B1", name, ""))

# B2 / B3: revenue sums and counts by industry / by country, per reporting currency.
for qid, col in [("B2", "ICB Industry"), ("B3", "Country")]:
    total, count = defaultdict(Decimal), defaultdict(int)
    for r in rows:
        k = f"{r[col]} ({r[CUR]})"
        total[k] += Decimal(r[REV])
        count[k] += 1
    for k in sorted(total, key=lambda k: -total[k]):
        key.append((qid, k, f"{total[k]:.1f}|{count[k]}"))

# B4: distinct industries per country.
inds = defaultdict(set)
for r in rows:
    inds[r["Country"]].add(r["ICB Industry"])
for k in sorted(inds, key=lambda k: (-len(inds[k]), k)):
    key.append(("B4", k, str(len(inds[k]))))

# B5: largest constituent within each reporting currency; the caveat must be attached.
for cur in sorted({r[CUR] for r in rows}):
    top = max((r for r in rows if r[CUR] == cur), key=lambda r: Decimal(r[REV]))
    key.append(("B5", top["Company"], f"{Decimal(top[REV]):.1f}|{cur}|true"))

# B6: ASML's two source distributions, both flagged as approximate.
for title in sorted(["EURO STOXX 50 constituents CSV (CSV2)", "Provisional ICB subsector assignments"]):
    key.append(("B6", title, "true"))

out = ROOT / "queries" / "answer-key.csv"
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["query", "key", "value"])
    w.writerows(key)
print(f"Wrote {out.relative_to(ROOT)}: {len(key)} expected rows")
