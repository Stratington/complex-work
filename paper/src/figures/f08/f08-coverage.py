import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "e1-relation-ratified.db"
OUT = Path(__file__).with_suffix(".csv")

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
status = dict(con.execute("SELECT status, count(*) FROM logic_extractions GROUP BY status"))
gaps = dict(
    con.execute(
        "SELECT gap_classification, count(*) FROM extraction_coverage "
        "WHERE is_explicit_gap = 1 GROUP BY gap_classification"
    )
)
policy = con.execute(
    "SELECT value FROM meta WHERE key='evidence_policy'"
).fetchone()[0]
con.close()

compiled = status["COMPILED"]
total = sum(status.values())
assert compiled + sum(gaps.values()) == total
assert policy == "REVIEWED_SINGLE_LANE_RELATION_AI_RATIFIED_V1", policy

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["y", "row", "compiled", "ontology", "structural", "ambiguity"])
    w.writerow([1, "units", compiled, gaps["ONTOLOGY_GAP"],
                gaps["STRUCTURAL_ERROR"], gaps["SOURCE_AMBIGUITY"]])
    w.writerow([0, "gaps", 0, gaps["ONTOLOGY_GAP"],
                gaps["STRUCTURAL_ERROR"], gaps["SOURCE_AMBIGUITY"]])

print(f"wrote {OUT.name}: {compiled} compiled of {total} units; gaps "
      f"ontology={gaps['ONTOLOGY_GAP']} structural={gaps['STRUCTURAL_ERROR']} "
      f"ambiguity={gaps['SOURCE_AMBIGUITY']}")
