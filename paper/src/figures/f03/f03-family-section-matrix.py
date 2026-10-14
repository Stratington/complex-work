import csv
import json
import sqlite3
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "canonical.db"
HERE = Path(__file__).resolve().parent

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
ntype = dict(con.execute("SELECT id, type FROM nodes"))
attrs = dict(con.execute("SELECT id, attrs FROM nodes"))
cparent = {d: s for s, d in con.execute("SELECT src, dst FROM edges WHERE type='CONTAINS'")}


def top_section(node):
    while True:
        p = cparent.get(node)
        if p is None:
            return node
        if ntype[p] == "DocumentNode":
            return node
        node = p



families = {}
for fid, title, ordinal in con.execute(
    "SELECT id, json_extract(attrs,'$.title'), ordinal FROM nodes "
    "WHERE type='SectionNode' AND doc='GP' AND id LIKE 'GP:section:family-%'"
):
    num = int(fid.rsplit("-", 1)[1])
    families[num] = {"title": title, "ordinal": ordinal, "forms": []}

fam_of_section = {f"GP:section:family-{n}": n for n in families}
form_family = {}
for form, parent in cparent.items():
    if ntype[form] == "AdoptedFormNode" and parent in fam_of_section:
        num = fam_of_section[parent]
        form_family[form] = num
        families[num]["forms"].append(form)

clause_section = {}
for c, in con.execute("SELECT id FROM nodes WHERE type='ClauseNode'"):
    sec = top_section(c)
    num = json.loads(attrs[sec]).get("number")
    assert num is not None and num.isdigit(), f"clause {c} under non-numbered {sec}"
    clause_section[c] = int(num)

matrix = Counter()
for s, d in con.execute("SELECT src, dst FROM edges WHERE type='GROUNDED_IN'"):
    if ntype[s] == "ClauseNode" and ntype[d] == "AdoptedFormNode":
        matrix[(form_family[d], clause_section[s])] += 1

sections = sorted(set(clause_section.values()) | set(range(1, 17)))

with open(HERE / "f03-matrix.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "section", "brackets"])
    for fam in sorted(families):
        for sec in sections:
            w.writerow([fam, sec, matrix[(fam, sec)]])

with open(HERE / "f03-families.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["family", "label", "forms"])
    for num in sorted(families):
        title = families[num]["title"]
        label = title.split("—", 1)[1].strip() if "—" in title else title
        label = " ".join(label.replace(",", " ").split())
        w.writerow([num, label, len(families[num]["forms"])])

con.close()
print(f"wrote f03-matrix.csv ({len(families)}x{len(sections)} cells, "
      f"{sum(matrix.values())} brackets) and f03-families.csv")
