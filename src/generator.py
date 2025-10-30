from pathlib import Path
from typing import List
from jinja2 import Environment, FileSystemLoader, select_autoescape
from src.data_models import PermitBundle, Unit, ARItem
from src.rules_engine import select_applicable_requirements

TEMPLATE_DIR = Path(__file__).parent / "templates"

def apply_rules(bundle: PermitBundle,
                is_title_v_major: bool = True,
                facility_major_hap: bool = True) -> PermitBundle:
    # Apply applicability determinations per unit
    updated_units: List[Unit] = []
    for u in bundle.units:
        # Convert to dict for the rules function
        u_dict = u.model_dump()
        ars = select_applicable_requirements(
            u_dict,
            is_title_v_major=is_title_v_major,
            facility_major_hap=facility_major_hap
        )
        u.applicable_requirements = [ARItem(**a) for a in ars]
        updated_units.append(u)
    bundle.units = updated_units
    return bundle

def render_title_v(bundle: PermitBundle) -> str:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=select_autoescape(enabled_extensions=("jinja",))
    )
    tpl = env.get_template("title_v_template.jinja")
    text = tpl.render(**bundle.model_dump())
    return text

def save_draft(text: str, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(text, encoding="utf-8")
    return out_path
