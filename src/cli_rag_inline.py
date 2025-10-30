from pathlib import Path
from src.config import settings
from src.data_models import PermitBundle, Facility, Site, Unit, ControlDevice
from src.generator import apply_rules, render_title_v_with_evidence, save_draft

def main():
    bundle = PermitBundle(
        facility=Facility(name="Demo Plant", program_ids={"ICIS_AIR": "123456"}),
        site=Site(address="Houston, TX",
                  attainment_status={"Ozone": "Nonattainment (Serious)"}),
        units=[
            Unit(unit_id="U-1", process="Boiler", fuel="Natural Gas",
                 controls=[ControlDevice(type="SCR", efficiency_pct=90.0)]),
            Unit(unit_id="U-2", process="Combustion Turbine", fuel="Natural Gas")
        ]
    )
    bundle = apply_rules(bundle)
    text = render_title_v_with_evidence(bundle)
    out = Path(settings.data_dir) / "processed" / "draft_title_v_with_evidence.md"
    out = out.resolve()
    save_draft(text, out)
    print(f"✅ Draft with evidence written to: {out}")

if __name__ == "__main__":
    main()
