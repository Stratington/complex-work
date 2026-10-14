import csv
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "canonical.db"
HERE = Path(__file__).resolve().parent

ABBREV = {
    "DocumentNode": "Doc", "SectionNode": "Sect", "ParagraphNode": "Para",
    "ListNode": "List", "ListItemNode": "Item", "TableNode": "Tbl",
    "TableRowNode": "TRow", "SentenceNode": "Sent", "FormPartNode": "FPart",
    "TermNode": "Term", "ClauseNode": "Cls", "AdoptedFormNode": "AForm",
    "DiscardedFormNode": "DForm", "GoalUnitNode": "Goal", "PrincipleNode": "Prin",
    "ThematicBreakNode": "TBrk",
}
CHIP_W, CHIP_PITCH_X, ROW_PITCH_Y = 9.4, 10.4, 8.6

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
ntype = dict(con.execute("SELECT id, type FROM nodes"))
cparent = {d: s for s, d in con.execute("SELECT src, dst FROM edges WHERE type='CONTAINS'")}
con.close()

depth = {}
def depth_of(n):
    if n not in depth:
        p = cparent.get(n)
        depth[n] = 0 if p is None else depth_of(p) + 1
    return depth[n]

for n in ntype:
    depth_of(n)

nodes = defaultdict(int)
edges = Counter()
totals = Counter()
for n, t in ntype.items():
    nodes[(depth[n], t)] += 1
    totals[t] += 1
for child, par in cparent.items():
    edges[((depth[par], ntype[par]), (depth[child], ntype[child]))] += 1

levels = defaultdict(list)
for k in nodes:
    levels[k[0]].append(k)
for d in levels:
    levels[d].sort(key=lambda k: (-nodes[k], k[1]))

parents_of = defaultdict(list)
children_of = defaultdict(list)
for (a, b) in edges:
    parents_of[b].append(a)
    children_of[a].append(b)

for _ in range(40):

    for d in range(1, 8):
        pos = {k: i for i, k in enumerate(levels[d - 1])}
        levels[d].sort(key=lambda k: (
            sum(pos[p] for p in parents_of[k]) / len(parents_of[k])
            if parents_of[k] else float("inf"), -nodes[k]))

    for d in range(6, -1, -1):
        pos = {k: i for i, k in enumerate(levels[d + 1])}
        levels[d].sort(key=lambda k: (
            sum(pos[c] for c in children_of[k]) / len(children_of[k])
            if children_of[k] else pos.get(k, 0.0), -nodes[k]))

key = lambda k: f"d{k[0]}-{k[1]}"

with open(HERE / "f05-nodes.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["key", "id", "depth", "type", "abbrev", "count", "x", "y"])
    for d in range(8):
        row = levels[d]
        x0 = -(len(row) - 1) * CHIP_PITCH_X / 2.0
        for i, k in enumerate(row):
            w.writerow([key(k), f"d{k[0]}:{k[1]}", k[0], k[1], ABBREV[k[1]],
                        nodes[k], f"{x0 + i * CHIP_PITCH_X:.2f}", f"{-d * ROW_PITCH_Y:.2f}"])

with open(HERE / "f05-edges.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["src", "dst", "weight"])
    for (a, b), wt in sorted(edges.items()):
        w.writerow([key(a), key(b), wt])

with open(HERE / "f05-legend.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["abbrev", "type", "total"])
    for t, c in totals.most_common():
        w.writerow([ABBREV[t], t, c])


with open(HERE / "f05-levels.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["depth", "total", "xmin", "y"])
    for d in range(8):
        row = levels[d]
        x0 = -(len(row) - 1) * CHIP_PITCH_X / 2.0
        w.writerow([d, sum(nodes[k] for k in row),
                    f"{x0 - CHIP_W / 2.0:.2f}", f"{-d * ROW_PITCH_Y:.2f}"])

print(f"wrote f05-nodes.csv ({sum(nodes.values())} graph nodes -> "
      f"{len(nodes)} chips over {len(levels)} levels), "
      f"f05-edges.csv ({len(edges)} edges), f05-legend.csv ({len(totals)} types)")
