import csv
import re
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DB = ROOT / "subspec" / "e1-dependencies-graph.db"
HERE = Path(__file__).resolve().parent

SECTIONS = list(range(1, 17))
TITLES = {
	1: "Purpose and Scope", 2: "Terminology", 3: "Purpose",
	4: "The Project Record", 5: "Decomposition and Work Units",
	6: "Component Specifications", 7: "Verification and Acceptance",
	8: "Phases and Gates", 9: "Baselines and Change Control",
	10: "Traceability and Lineage", 11: "Decision Records", 12: "Risk and Failure",
	13: "Executor Boundaries", 14: "Governance Documents",
	15: "Roles and Human Authority", 16: "Normative Checks",
}

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
meta = dict(con.execute("SELECT key, value FROM meta"))
assert meta["depends_pass_policy"] == "RELATION_PASS_DEPENDS_ON_TILED_V2", meta["depends_pass_policy"]
assert meta["depends_evidence_policy"] == "REVIEWED_TILED_RELATION_AI_ADJUDICATED_V1", meta["depends_evidence_policy"]
assert meta["depends_human_verified"] == "0", meta["depends_human_verified"]

ntype = dict(con.execute("SELECT id, type FROM nodes"))
cparent = {d: s for s, d in con.execute("SELECT src, dst FROM edges WHERE type='CONTAINS'")}
depends = list(con.execute("SELECT src, dst FROM edges WHERE type='DEPENDS_ON'"))
assert len(depends) == int(meta["depends_edge_count"]), len(depends)


def top_section(node):
	while True:
		p = cparent.get(node)
		if p is None or ntype[p] == "DocumentNode":
			return node
		node = p


def section_number(clause):
	top = top_section(clause)
	m = re.fullmatch(r"PSS:section:(\d+)", top)
	assert m, f"{clause} sits under {top}"
	n = int(m.group(1))
	assert n == int(clause.split(":")[2].split(".")[0]), (clause, top)
	return n



clause_pairs = [(s, d) for s, d in depends
                if ntype.get(s) == "ClauseNode" and ntype.get(d) == "ClauseNode"]
weight = Counter((section_number(s), section_number(d)) for s, d in clause_pairs)
drawn = sum(weight.values())
assert drawn == len(clause_pairs)


excluded = Counter((ntype.get(s), ntype.get(d)) for s, d in depends
                   if (ntype.get(s), ntype.get(d)) != ("ClauseNode", "ClauseNode"))

inter = {(a, b): w for (a, b), w in weight.items() if a != b}


present = sorted({a for a, _ in inter} | {b for _, b in inter})
index = {s: i for i, s in enumerate(present)}
n = len(present)
full = (1 << n) - 1

after = [[0] * n for _ in range(n)]
for (a, b), w in inter.items():
	after[index[a]][index[b]] = w
best = [None] * (1 << n)
best[0] = (0, ())
for mask in range(1 << n):
	if best[mask] is None:
		continue
	cost, order = best[mask]
	for v in range(n):
		if mask >> v & 1:
			continue
		add = sum(after[v][u] for u in range(n) if mask >> u & 1)
		nxt = mask | 1 << v
		cand = (cost + add, order + (v,))
		if best[nxt] is None or cand[0] < best[nxt][0]:
			best[nxt] = cand
backward_weight, best_order = best[full]
order = [present[i] for i in best_order]
order += [s for s in SECTIONS if s not in order]
assert sorted(order) == SECTIONS
pos = {s: i + 1 for i, s in enumerate(order)}


adj = defaultdict(set)
for (a, b) in inter:
	adj[a].add(b)
idx, low, stack, onstack, comps, counter = {}, {}, [], set(), [], [0]


def strongconnect(v):
	work = [(v, iter(sorted(adj[v])))]
	idx[v] = low[v] = counter[0]
	counter[0] += 1
	stack.append(v)
	onstack.add(v)
	while work:
		u, it = work[-1]
		for w in it:
			if w not in idx:
				idx[w] = low[w] = counter[0]
				counter[0] += 1
				stack.append(w)
				onstack.add(w)
				work.append((w, iter(sorted(adj[w]))))
				break
			if w in onstack:
				low[u] = min(low[u], idx[w])
		else:
			work.pop()
			if work:
				low[work[-1][0]] = min(low[work[-1][0]], low[u])
			if low[u] == idx[u]:
				comp = []
				while True:
					w = stack.pop()
					onstack.discard(w)
					comp.append(w)
					if w == u:
						break
				comps.append(sorted(comp))


for s in SECTIONS:
	if s not in idx:
		strongconnect(s)
core = max(comps, key=len)
core = set(core) if len(core) > 1 else set()

out_deg = Counter()
in_deg = Counter()
for (a, b), w in inter.items():
	out_deg[a] += w
	in_deg[b] += w


with open(HERE / "f10-matrix.csv", "w", newline="") as fh:
	w = csv.writer(fh)
	w.writerow(["row", "col", "src", "dst", "count", "kind", "k"])
	for (a, b), n_edges in sorted(weight.items(), key=lambda kv: (pos[kv[0][0]], pos[kv[0][1]])):
		kind = "self" if a == b else ("forward" if pos[a] < pos[b] else "backward")
		w.writerow([pos[a], pos[b], a, b, n_edges, kind, {"self": 0, "forward": 1, "backward": 2}[kind]])

with open(HERE / "f10-sections.csv", "w", newline="") as fh:
	w = csv.writer(fh)
	w.writerow(["pos", "section", "label", "out", "in", "scc"])
	assert not any("," in t for t in TITLES.values()), "labels must not need CSV quoting"
	for s in SECTIONS:
		w.writerow([pos[s], s, TITLES[s], out_deg[s], in_deg[s], 1 if s in core else 0])

self_weight = sum(w for (a, b), w in weight.items() if a == b)
forward_weight = sum(w for (a, b), w in inter.items() if pos[a] < pos[b])
print(f"DEPENDS_ON edges in the database: {len(depends)}")
print(f"clause-to-clause, drawn:          {drawn}")
print(f"  intra-section (diagonal):       {self_weight}")
print(f"  forward after reordering:       {forward_weight}")
print(f"  backward after reordering:      {backward_weight} (proved minimal)")
print(f"sections carrying an edge:        {len(present)} of 16")
print(f"cyclic core:                      {sorted(core)}")
print(f"order:                            {order}")
for k, v in sorted(excluded.items(), key=lambda kv: -kv[1]):
	print(f"excluded by the reduction: {k[0]} -> {k[1]}: {v}")
