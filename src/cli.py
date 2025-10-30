## CLI runner (for quick end-to-end execution)
import argparse
from pathlib import Path
from src.config import settings
from src.cfr_loader import load_cfr_into_db
from src.data_models import PermitBundle, Facility, Site, Unit, ControlDevice
from src.generator import apply_rules, render_title_v, save_draft

def cmd_index(args):
    load_cfr_into_db()

def cmd_draft(args):
    # Minimal demo bundle (replace with real facility data later)
    bundle = PermitBundle(
        facility=Facility(name="Demo Plant", program_ids={"ICIS_AIR": "123456"}),
        site=Site(address="Houston, TX",
                  attainment_status={"Ozone": "Nonattainment (Serious)"}),
        units=[
            Unit(
                unit_id="U-1",
                process="Boiler",
                fuel="Natural Gas",
                controls=[ControlDevice(type="SCR", efficiency_pct=90.0)]
            ),
            Unit(
                unit_id="U-2",
                process="Combustion Turbine",
                fuel="Natural Gas",
                controls=[]
            )
        ]
    )

    # Apply applicability rules
    bundle = apply_rules(bundle, is_title_v_major=True, facility_major_hap=True)

    # Render permit
    text = render_title_v(bundle)

    # Save draft
    from src.config import settings
    out = Path(args.output or settings.data_dir / "processed" / "draft_title_v_demo.md").resolve()
    print(f"Resolved output path: {out}")  # debug line
    save_draft(text, out)
    print(f"✅ Draft written to: {out}")

def main():
    ap = argparse.ArgumentParser("AirPermit Draft CLI")
    sp = ap.add_subparsers(dest="cmd")

    p_idx = sp.add_parser("index", help="Load CFR text into local DB")
    p_idx.set_defaults(func=cmd_index)

    p_draft = sp.add_parser("draft", help="Generate a Title V/NSR draft")
    p_draft.add_argument("--output", default=None, help="Output path (*.md)")
    p_draft.set_defaults(func=cmd_draft)

    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help(); return
    args.func(args)

if __name__ == "__main__":
    main()
