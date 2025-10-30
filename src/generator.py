from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.data_models import PermitBundle, Unit, ARItem
from src.rules_engine import select_applicable_requirements
from src.rag_sections import retrieve_for_unit

TEMPLATE_DIR = Path(__file__).parent / "templates"

def apply_rules(bundle: PermitBundle,
                is_title_v_major: bool = True,
                facility_major_hap: bool = True) -> PermitBundle:
    updated_units: List[Unit] = []
    for u in bundle.units:
        ars = select_applicable_requirements(
            u.model_dump(),
            is_title_v_major=is_title_v_major,
            facility_major_hap=facility_major_hap
        )
        u.applicable_requirements = [ARItem(**a) for a in ars]
        updated_units.append(u)
    bundle.units = updated_units
    return bundle

def render_title_v(bundle: PermitBundle) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)),
                      autoescape=select_autoescape(enabled_extensions=("jinja",)))
    tpl = env.get_template("title_v_template.jinja")
    return tpl.render(**bundle.model_dump())

def render_title_v_with_evidence(bundle: PermitBundle) -> str:
    # base draft
    text = render_title_v(bundle)

    # embed evidence per unit/discipline
    text += "\n\n---\n# Evidence (Top-K excerpts)\n"
    for u in bundle.units:
        text += f"\n## Unit {u.unit_id}\n"
        for topic in ["applicability", "limits", "monitoring", "testing", "recordkeeping"]:
            ctx = retrieve_for_unit(u, topic, k=3)
            if not ctx:
                continue
            text += f"\n**{topic.title()}**\n"
            for c in ctx:
                citation_str = (f" — {c['citation']}" if c['citation'] else "")
                text += (
                    f"- ({c['score']:.2f}) {c['excerpt']}  \n"
                    f"  _source: {c['path']}{citation_str}_\n"
                )
    return text

def save_draft(text: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return out_path
