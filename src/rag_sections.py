from pathlib import Path
from typing import List, Dict
from src.retriever import search_index

IDX = Path("src/indexes")

TOPIC_TO_CORPORA = {
    "applicability": ["cfr_sections", "cfr_docs", "echo_docs"],
    "limits":        ["rblc_docs", "cfr_sections", "webfire_docs"],
    "monitoring":    ["cfr_sections", "cedri_docs", "cfr_docs"],
    "testing":       ["cedri_docs", "cfr_sections", "cfr_docs"],
    "recordkeeping": ["cfr_sections", "cfr_docs"],
}

def _queries_for_unit(unit, topic: str) -> List[str]:
    proc = (unit.process or "").strip()
    fuel = (unit.fuel or "").strip()
    base = f"{proc} {fuel} {topic} requirements 40 CFR"
    # small variations to improve recall
    q = [base]
    if proc:
        q.append(f"{proc} {topic} 40 CFR")
    if fuel:
        q.append(f"{proc} {fuel} 40 CFR {topic}")
    return q

def retrieve_for_unit(unit, topic: str, k=3) -> List[Dict]:
    corpora = TOPIC_TO_CORPORA.get(topic, ["cfr_sections"])
    queries = _queries_for_unit(unit, topic)
    pool: List[Dict] = []
    for corpus in corpora:
        idx = IDX / f"{corpus}.faiss"
        if not idx.exists():
            continue
        # first query only (keeps runtime small); expand later if needed
        hits = search_index(idx, queries[0], k=k)
        for h in hits:
            pool.append({
                "excerpt": h.get("text", "")[:500],
                "citation": "; ".join(h.get("citations", [])),
                "path": h.get("path", str(idx)),
                "score": h.get("score", 0.0)
            })
    # rank + de-dup
    pool.sort(key=lambda x: x["score"], reverse=True)
    uniq, seen = [], set()
    for p in pool:
        key = (p["path"], p["citation"], p["excerpt"][:80])
        if key in seen:
            continue
        uniq.append(p)
        seen.add(key)
        if len(uniq) >= k:
            break
    return uniq
