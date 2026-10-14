import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "reports" / "evidence-audit" / "literature-map.csv"
HERE = Path(__file__).resolve().parent


FAMILIES = [
    (1, 6, "Durable work record"),
    (7, 16, "Decomposition"),
    (17, 30, "Contract and obligation"),
    (31, 49, "Verification and acceptance"),
    (50, 54, "Configuration control"),
    (55, 59, "Traceability and lineage"),
    (60, 60, "Decision record"),
    (61, 62, "Risk and failure"),
    (63, 67, "Executor boundary"),
    (68, 73, "Governance document"),
    (74, 76, "Role and authority"),
    (77, 79, "Reusable procedure"),
]
DOMAIN_LABELS = {
    "software & computing": "Software and computing",
    "org. science & mgmt": "Organization science and management",
    "medicine & patient safety": "Medicine and patient safety",
    "aviation & aerospace": "Aviation and aerospace",
    "manufacturing & quality": "Manufacturing and quality",
    "standards & specs": "Standards and specifications",
    "construction & civil eng.": "Construction and civil engineering",
    "law & regulation": "Law and regulation",
    "economics & policy": "Economics and policy",
    "library & info science": "Library and information science",
    "hci & human factors": "Human factors",
}
STATES = {"Read-verified": "verified", "Abstract-only": "abstract", "Lead": "lead", "Rejected": "rejected"}


def family_of(item):
    n = int(item[3:])
    return next(i for i, (a, b, _) in enumerate(FAMILIES, 1) if a <= n <= b)


rows = [r for r in csv.DictReader(SRC.open(newline="")) if r["is_control"] == "no"]
members = defaultdict(list)
for r in rows:
    items = {i.strip() for i in r["found_for_items"].split(";")}
    fams = {family_of(i) for i in items if i.startswith("GP-") and i[3:].isdigit()}
    for f in fams:
        members[f].append(r)

cells = defaultdict(Counter)
domain_total = Counter()
fam_rows = []
for f, (a, b, label) in enumerate(FAMILIES, 1):
    src = members[f]
    dom = Counter(r["domain"] for r in src)
    unclassified = dom.pop("unclassified", 0)
    unknown = set(dom) - set(DOMAIN_LABELS)
    if unknown:
        raise SystemExit(f"unmapped domain(s): {sorted(unknown)}")
    cells[f] = dom
    domain_total.update(dom)
    st = Counter(STATES[r["best_citation_state"]] for r in src)
    rng = f"GP-{a:02d}" if a == b else f"GP-{a:02d} to GP-{b:02d}"
    fam_rows.append({
        "family": f, "label": label, "range": rng, "sources": len(src),
        "classified": sum(dom.values()), "unclassified": unclassified,
        **{k: st.get(k, 0) for k in STATES.values()},
    })

order = [d for d, _ in sorted(domain_total.items(), key=lambda kv: (-kv[1], kv[0]))]

with (HERE / "f11-domains.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["domain", "label", "sources"])
    for i, d in enumerate(order, 1):
        w.writerow([i, DOMAIN_LABELS[d], domain_total[d]])

with (HERE / "f11-cells.csv").open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["family", "domain", "count", "share"])
    for fr in fam_rows:
        f = fr["family"]
        for i, d in enumerate(order, 1):
            c = cells[f].get(d, 0)
            w.writerow([f, i, c, round(100 * c / fr["classified"], 1) if fr["classified"] else 0])

with (HERE / "f11-families.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(fam_rows[0]))
    w.writeheader()
    w.writerows(fam_rows)

print(f"{len(rows)} sources; per-family rows written for {len(fam_rows)} families")
