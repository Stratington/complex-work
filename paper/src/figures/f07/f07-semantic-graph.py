import math
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "e1-dependencies-graph.db"
HERE = Path(__file__).resolve().parent
OUT = HERE / "f07-semantic-graph-data.tex"
ANCHORS = HERE / "f07-semantic-graph-anchors.tex"


MM_PER_NODE_AREA = 34.0 / math.sqrt(2005)
ROOT_FRAC = 0.10
CENTRES = {
    "GP":   (35.0, 56.0),
    "PSS":  (125.0, 56.0),
    "GOAL": (166.5, 80.0),
    "TBF":  (166.5, 31.0),
}
SYM_COL = (82.0, 20.0, 88.0)
GRID_CENTRE = (82.0, 8.5)
GRID_COLS, GRID_PITCH = 34, 0.85
DOT_R = {"src": 0.11, "sym": 0.14, "root": 0.45}



EDGE_CLASS = [
    ("structure", ("PRECEDES", "CONTAINS"),                  0.10, 0.80),
    ("term",      ("USES_TERM", "DEFINED_BY",
                   "TARGETS_ENTITY", "BINDS_ACTOR"),         0.12, 0.45),
    ("other",     ("REFERENCES", "REQUIRES_PRECONDITION",
                   "GROUNDED_IN"),                           0.15, 0.55),
    ("implements", ("IMPLEMENTS",),                          0.20, 0.60),
    ("depends",   ("DEPENDS_ON",),                           0.40, 1.00),
]

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
ntype = dict(con.execute("SELECT id, type FROM nodes"))
ordinal = dict(con.execute("SELECT id, ordinal FROM nodes"))
edges = list(con.execute("SELECT src, dst, type FROM edges"))
policy = con.execute(
    "SELECT value FROM meta WHERE key='depends_evidence_policy'").fetchone()[0]
assert policy == "REVIEWED_TILED_RELATION_AI_ADJUDICATED_V1", policy
con.close()

children, parent = {}, {}
for s, d, t in edges:
    if t == "CONTAINS":
        children.setdefault(s, []).append(d)
        parent[d] = s



by_class = {c: [] for c, _, _, _ in EDGE_CLASS}
class_of = {t: c for c, ts, _, _ in EDGE_CLASS for t in ts}
assert set(class_of) == {t for _, _, t in edges}, "edge types differ"
seen, collapsed = set(), 0
for s, d, t in edges:
    key = (t, (s, d) if s < d else (d, s))
    if key in seen:
        collapsed += 1
        continue
    seen.add(key)
    by_class[class_of[t]].append((s, d))

roots = sorted(n for n, t in ntype.items()
               if t == "DocumentNode" and n not in parent)
assert [r.split(":")[0] for r in roots] == sorted(CENTRES)

xy, kind = {}, {}
radius_of = {}
for r in roots:
    doc = r.split(":")[0]

    order, depth, stack = [], {r: 0}, [r]
    while stack:
        n = stack.pop()
        order.append(n)
        kids = sorted(children.get(n, []), key=lambda k: (ordinal[k], k))
        for k in kids:
            depth[k] = depth[n] + 1
        stack.extend(reversed(kids))
    leaves = [n for n in order if not children.get(n)]
    angle = {leaf: math.pi / 2 - 2 * math.pi * i / len(leaves)
             for i, leaf in enumerate(leaves)}
    for n in reversed(order):
        kids = children.get(n, [])
        if kids:
            angle[n] = math.atan2(sum(math.sin(angle[k]) for k in kids),
                                  sum(math.cos(angle[k]) for k in kids))
    radius = MM_PER_NODE_AREA * math.sqrt(len(order))
    radius_of[doc] = radius
    d_max = max(depth.values())
    cx, cy = CENTRES[doc]
    for n in order:
        if not children.get(n):
            rr = radius
        else:
            rr = radius * (ROOT_FRAC + (1 - ROOT_FRAC) * depth[n] / d_max)
        if n == r:
            rr = 0.0
        xy[n] = (cx + rr * math.cos(angle[n]), cy + rr * math.sin(angle[n]))
        kind[n] = "root" if n == r else "src"

has_edge = {n for pairs in by_class.values() for p in pairs for n in p}
symbols = sorted(n for n, t in ntype.items() if t == "SemanticSymbolNode")
sym_conn = [s for s in symbols if s in has_edge]
sym_iso = [s for s in symbols if s not in has_edge]
nbr_y = {s: [] for s in sym_conn}
for pairs in by_class.values():
    for a, b in pairs:
        if a in nbr_y and b in xy:
            nbr_y[a].append(xy[b][1])
        if b in nbr_y and a in xy:
            nbr_y[b].append(xy[a][1])
assert all(nbr_y.values()), "a symbol links only to symbols"
sym_conn.sort(key=lambda s: (sum(nbr_y[s]) / len(nbr_y[s]), s))
col_x, y0, y1 = SYM_COL
for i, s in enumerate(sym_conn):
    xy[s] = (col_x, y0 + (y1 - y0) * i / (len(sym_conn) - 1))
    kind[s] = "sym"
rows = math.ceil(len(sym_iso) / GRID_COLS)
gx0 = GRID_CENTRE[0] - (GRID_COLS - 1) * GRID_PITCH / 2
gy0 = GRID_CENTRE[1] + (rows - 1) * GRID_PITCH / 2
for k, s in enumerate(sym_iso):
    r_, c_ = divmod(k, GRID_COLS)
    xy[s] = (gx0 + c_ * GRID_PITCH, gy0 - r_ * GRID_PITCH)
    kind[s] = "sym"
assert len(xy) == len(ntype), "a node has no position"


def p(pt):
    return f"({pt[0]:.2f},{pt[1]:.2f})"


with open(ANCHORS, "w") as f:
    for doc, (x, y) in CENTRES.items():
        f.write(f"\\coordinate (c{doc}) at ({x:.2f},{y:.2f});\n")
        f.write(f"\\def\\r{doc}{{{radius_of[doc]:.2f}}}\n")
    f.write(f"\\coordinate (colS) at ({col_x:.2f},{y0:.2f});\n")
    f.write(f"\\coordinate (colN) at ({col_x:.2f},{y1:.2f});\n")
    gw = (GRID_COLS - 1) * GRID_PITCH
    f.write(f"\\coordinate (gridNW) at ({gx0:.2f},{gy0:.2f});\n")
    f.write(f"\\coordinate (gridSE) at ({gx0 + gw:.2f},"
            f"{gy0 - (rows - 1) * GRID_PITCH:.2f});\n")

with open(OUT, "w") as f:
    for c, _, width, opac in EDGE_CLASS:
        f.write(f"\\begin{{scope}}[e{c},line width={width}pt,"
                f"draw opacity={opac}]\n")
        for s, d in by_class[c]:
            f.write(f"\\draw{p(xy[s])}--{p(xy[d])};\n")
        f.write("\\end{scope}\n")
    for k in ("src", "sym", "root"):
        f.write(f"\\begin{{scope}}[n{k}]\n")
        for n in sorted(n for n in xy if kind[n] == k):
            f.write(f"\\fill{p(xy[n])}circle[radius={DOT_R[k]}];\n")
        f.write("\\end{scope}\n")

total = sum(len(v) for v in by_class.values())
print(f"wrote {OUT.name} and {ANCHORS.name}: {len(xy)} nodes ({len(sym_iso)} carry no edge), "
      f"{total} lines ({collapsed} parallel edges collapsed); radii "
      + ", ".join(f"{d}={r:.1f}" for d, r in radius_of.items()))
