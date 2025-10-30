## end-to-end demo
## Downloads sample corpora
## Builds indexes
##  Generates a draft with retrieved context list at the end

import argparse
from pathlib import Path
from src.config import settings
from src.downloader import (
    download_echo_icis_air, download_echo_air_emissions,
    download_rblc_catalog, download_webfire_procedures_pdf,
    download_ecfr_title40_toc, download_cedri_info_page
)
from src.rag_indexer import demo_build_all_indexes
from src.data_models import PermitBundle, Facility, Site, Unit, ControlDevice
from src.rag_generator import render_with_context

def cmd_demo(args):
    # 1) Download small set of resources
    download_echo_icis_air()
    download_echo_air_emissions()
    download_rblc_catalog()
    download_webfire_procedures_pdf()
    download_ecfr_title40_toc()
    download_cedri_info_page()

    # 2) Build indexes (walk raw folders)
    demo_build_all_indexes()

    # 3) Create a demo bundle
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

    # 4) Render draft with context (RAG)
    out = Path(settings.data_dir) / "processed" / "draft_title_v_rag_demo.md"
    out = out.resolve()
    render_with_context(bundle, out)
    print(f"✅ RAG draft written to: {out}")

def main():
    ap = argparse.ArgumentParser("RAG Demo CLI")
    ap.set_defaults(func=cmd_demo)
    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
