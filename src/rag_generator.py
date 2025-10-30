## Wraps your existing generator to attach supporting context per unit/section.
from pathlib import Path
from typing import Dict, List
from src.data_models import PermitBundle
from src.generator import apply_rules, render_title_v, save_draft
from src.retriever import search_index

IDX = Path("src/indexes")

def _collect_context(queries: List[str], corpus: str, k=3) -> List[Dict]:
    idx = IDX / f"{corpus}.faiss"
    if not idx.exists():
        return []
    ctx = []
    for q in queries:
        ctx.extend(search_index(idx, q, k=k))
    return ctx[:k]

def add_context(bundle: PermitBundle) -> Dict[str, List[Dict]]:
    """Build retrieval queries and collect top-K snippets per major section."""
    q = {
        "applicable_reqs": [],
        "mrr": [],
        "limits": [],
    }
    # Build queries from bundle content (very simple MVP)
    for u in bundle.units:
        if u.process:
            q["applicable_reqs"].append(f"NSPS MACT SIP requirements for {u.process}")
            q["mrr"].append(f"Monitoring testing recordkeeping reporting for {u.process}")
            q["limits"].append(f"BACT/LAER limits for {u.process} {u.fuel or ''}")

    ctx = {
        "applicable_reqs": _collect_context(q["applicable_reqs"], "cfr_docs") +
                           _collect_context(q["applicable_reqs"], "echo_docs"),
        "mrr": _collect_context(q["mrr"], "cedri_docs") +
               _collect_context(q["mrr"], "cfr_docs"),
        "limits": _collect_context(q["limits"], "rblc_docs") +
                  _collect_context(q["limits"], "webfire_docs"),
    }
    return ctx

def render_with_context(bundle: PermitBundle, out: Path) -> Path:
    bundle = apply_rules(bundle)
    context = add_context(bundle)
    text = render_title_v(bundle)

    # Append a Sources/Context section
    if any(context.values()):
        text += "\n\n---\n\n# Retrieved Context (Top-K)\n"
        for sec, items in context.items():
            if not items:
                continue
            text += f"\n## {sec}\n"
            for it in items:
                path = it.get("path","")
                score = it.get("score",0)
                text += f"- ({score:.2f}) {path}\n"
    return save_draft(text, out)
