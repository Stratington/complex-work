import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MATRIX = ROOT / "reports" / "evidence-audit" / "master-evidence-matrix.csv"
CANONICAL = ROOT / "subspec" / "canonical.db"
OUT = Path(__file__).with_suffix(".csv")

with open(MATRIX, newline="") as f:
    rows = list(csv.DictReader(f))

collected = len(rows)
kept = sum(1 for r in rows if r["phase2"] == "Keep")
rejected = collected - kept
reentry = sum(
    1 for r in rows if r["phase2"] == "Reject" and r["phase3"] in ("Adopted", "Discarded")
)
processed = sum(1 for r in rows if r["phase3"] in ("Adopted", "Discarded"))
adopted = sum(1 for r in rows if r["phase3"] == "Adopted")
subsumed = sum(1 for r in rows if r["phase3"] == "Discarded")
assert processed == kept + reentry == adopted + subsumed

con = sqlite3.connect(f"file:{CANONICAL}?mode=ro", uri=True)
clauses = con.execute(
    "SELECT count(*) FROM nodes WHERE type='ClauseNode'"
).fetchone()[0]
con.close()

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["y", "stage", "main", "reentry", "exit", "total"])
    w.writerow([3, "Collected", kept, 0, rejected, collected])
    w.writerow([2, "Processed", kept, reentry, 0, processed])
    w.writerow([1, "Outcome", adopted, 0, subsumed, processed])
    w.writerow([0, "Clauses", clauses, 0, 0, clauses])

print(f"wrote {OUT.name}: {collected} collected, {kept} kept, {rejected} rejected, "
      f"{reentry} re-entered, {processed} processed, {adopted} adopted, "
      f"{subsumed} subsumed, {clauses} clauses")
