import csv
import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "e1-relation-ratified.db"
HERE = Path(__file__).resolve().parent


LBL_L_X = 24.0
BLK_L_X0, BLK_L_X1 = 25.0, 27.5
BLK_R_X0, BLK_R_X1 = 60.5, 63.0
LBL_R_X = 64.5
COL_TOP = 84.0
COL_H = 84.0
GAP = 1.6

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
ntype = dict(con.execute("SELECT id, type FROM nodes"))
attrs = dict(con.execute("SELECT id, attrs FROM nodes"))
cparent = {d: s for s, d in con.execute("SELECT src, dst FROM edges WHERE type='CONTAINS'")}
implements = list(con.execute("SELECT src, dst FROM edges WHERE type='IMPLEMENTS'"))
policy = con.execute("SELECT value FROM meta WHERE key='evidence_policy'").fetchone()[0]
assert policy == "REVIEWED_SINGLE_LANE_RELATION_AI_RATIFIED_V1", policy


def top_section(node):
    while True:
        p = cparent.get(node)
        if p is None or ntype[p] == "DocumentNode":
            return node
        node = p


clause_sec = {}
sec_clauses = defaultdict(list)
for c, in con.execute("SELECT id FROM nodes WHERE type='ClauseNode'"):
    s = top_section(c)
    clause_sec[c] = s
    sec_clauses[s].append(c)

sec_meta = {}
for s in sec_clauses:
    a = json.loads(attrs[s])
    sec_meta[s] = (int(a["number"]), a["title"])

goal_sec = {}
goal_ord = {}
for g, t, o in con.execute(
        "SELECT id, json_extract(attrs,'$.title'), ordinal FROM nodes "
        "WHERE type='GoalUnitNode'"):
    goal_sec[g] = top_section(g)
    goal_ord[g] = o

gsec_meta = {}
for s in {goal_sec[g] for g in goal_sec}:
    a = json.loads(attrs[s])
    gsec_meta[s] = (int(a.get("number") or 0), a.get("title") or "?",
                    con.execute("SELECT ordinal FROM nodes WHERE id=?",
                                (s,)).fetchone()[0])
con.close()

edges = Counter()
for s, d in implements:
    edges[(clause_sec[s], goal_sec[d])] += 1
covered_clauses = {s for s, _ in implements}
cov_by_sec = Counter(clause_sec[c] for c in covered_clauses)
uncovered_units = [g for g in goal_sec
                   if not any(d == g for _, d in implements)]

lefts = sorted(sec_clauses, key=lambda s: sec_meta[s][0])
rights = sorted(gsec_meta, key=lambda s: gsec_meta[s][2])
out_w = {s: sum(w for (ss, _), w in edges.items() if ss == s) for s in lefts}
in_w = {s: sum(w for (_, ss), w in edges.items() if ss == s) for s in rights}


r_idx = {s: i for i, s in enumerate(rights)}
for _ in range(40):
    lefts.sort(key=lambda s: (
        sum(r_idx[g] * w for (ss, g), w in edges.items() if ss == s)
        / max(out_w[s], 1), sec_meta[s][0]))

scale = (COL_H - GAP * (len(lefts) - 1)) / sum(out_w.values())
ly = COL_TOP
ly0 = {}
for s in lefts:
    h = max(out_w[s] * scale, 0.5)
    ly0[s] = ly - h
    ly -= h + GAP

rh = {s: in_w[s] * scale for s in rights}
r_total = sum(rh.values()) + GAP * (len(rights) - 1)
ry = COL_TOP - (COL_H - r_total) / 2.0
ry0 = {}
for s in rights:
    ry0[s] = ry - rh[s]
    ry -= rh[s] + GAP



l_idx = {s: i for i, s in enumerate(lefts)}
l_cur = {s: ly0[s] + out_w[s] * scale for s in lefts}
r_cur = {s: ry0[s] + in_w[s] * scale for s in rights}
bands = []
for s in lefts:
    for g in sorted((g for (ss, g) in edges if ss == s), key=lambda x: r_idx[x]):
        w = edges[(s, g)] * scale
        bands.append({"L": s, "R": g, "w": w,
                      "yt0": l_cur[s], "yb0": l_cur[s] - w,
                      "yt1": r_cur[g], "yb1": r_cur[g] - w,
                      "weight": edges[(s, g)]})
        l_cur[s] -= w
        r_cur[g] -= w

def tex_escape(t):
    t = " ".join(t.replace(",", " ").split())
    return (t.replace("\\", "\\textbackslash{}").replace("&", "\\&")
             .replace("%", "\\%").replace("#", "\\#").replace("_", "\\_"))


nodes = []
for i, s in enumerate(lefts):
    num, title = sec_meta[s]
    h = max(out_w[s] * scale, 0.5)
    nodes.append({
        "key": f"L-{num}", "side": "L",
        "x": (BLK_L_X0 + BLK_L_X1) / 2, "y": ly0[s] + h / 2,
        "w": BLK_L_X1 - BLK_L_X0, "h": h,
        "label": f"\\S{num} {tex_escape(title)}",
        "sub": f"{cov_by_sec.get(s, 0)}/{len(sec_clauses[s])} clauses",
        "extra": out_w[s],

        "lx": LBL_L_X, "ly": COL_TOP - COL_H * (i + 0.5) / len(lefts),
    })
for s in rights:
    num, title, _ = gsec_meta[s]
    units = [g for g in goal_sec if goal_sec[g] == s]
    n_cov = sum(1 for g in units if g not in uncovered_units)
    nodes.append({
        "key": f"R-{num}", "side": "R",
        "x": (BLK_R_X0 + BLK_R_X1) / 2, "y": ry0[s] + rh[s] / 2,
        "w": BLK_R_X1 - BLK_R_X0, "h": rh[s],
        "label": f"\\S{num} {tex_escape(title)}",
        "sub": f"{n_cov}/{len(units)} units",
        "extra": in_w[s],
        "lx": LBL_R_X, "ly": ry0[s] + rh[s] / 2,
    })


codes = sorted(g.rsplit(":", 1)[1] for g in uncovered_units)
nodes.append({
    "key": "D-R", "side": "D",
    "x": (BLK_R_X0 + BLK_R_X1) / 2, "y": -7.5,
    "w": BLK_R_X1 - BLK_R_X0 + 20, "h": 5.4,
    "label": "", "sub": "no IMPLEMENTS edge: " + " ".join(codes),
    "extra": 0, "lx": 0.0, "ly": 0.0,
})
n_pathless = 106 - len(covered_clauses)
nodes.append({
    "key": "D-L", "side": "D",
    "x": (BLK_L_X0 + BLK_L_X1) / 2 - 11, "y": -7.5,
    "w": LBL_L_X + 3, "h": 5.4,
    "label": "", "sub": f"{n_pathless}/106 clauses reach no goal unit",
    "extra": 0, "lx": 0.0, "ly": 0.0,
})

with open(HERE / "f09-nodes.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["key", "side", "x", "y", "w", "h", "label", "sub", "extra",
                "lx", "ly"])
    for n in nodes:
        w.writerow([n["key"], n["side"], f"{n['x']:.2f}", f"{n['y']:.2f}",
                    f"{n['w']:.2f}", f"{n['h']:.2f}", n["label"], n["sub"],
                    n["extra"], f"{n['lx']:.2f}", f"{n['ly']:.2f}"])

with open(HERE / "f09-bands.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["x0", "yt0", "yb0", "x1", "yt1", "yb1", "weight"])
    for b in bands:
        w.writerow([f"{BLK_L_X1:.2f}", f"{b['yt0']:.2f}", f"{b['yb0']:.2f}",
                    f"{BLK_R_X0:.2f}", f"{b['yt1']:.2f}", f"{b['yb1']:.2f}",
                    b["weight"]])

print(f"wrote f09-nodes.csv ({len(lefts)}+{len(rights)} blocks, "
      f"{len(uncovered_units)} unreached units) and f09-bands.csv "
      f"({len(bands)} bands from {len(implements)} IMPLEMENTS; "
      f"{n_pathless} clauses without a path)")
