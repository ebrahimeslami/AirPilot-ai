import argparse
from src.downloader import (
    download_echo_icis_air, download_echo_air_emissions,
    download_rblc_catalog, download_webfire_procedures_pdf,
    download_ecfr_title40_toc, download_cedri_info_page
)

def main():
    ap = argparse.ArgumentParser("Downloader CLI")
    ap.add_argument("--all", action="store_true", help="Download all datasets")
    ap.add_argument("--echo", action="store_true")
    ap.add_argument("--emissions", action="store_true")
    ap.add_argument("--rblc", action="store_true")
    ap.add_argument("--webfire", action="store_true")
    ap.add_argument("--ecfr40", action="store_true")
    ap.add_argument("--cedri", action="store_true")
    args = ap.parse_args()

    if args.all or args.echo: download_echo_icis_air()
    if args.all or args.emissions: download_echo_air_emissions()
    if args.all or args.rblc: download_rblc_catalog()
    if args.all or args.webfire: download_webfire_procedures_pdf()
    if args.all or args.ecfr40: download_ecfr_title40_toc()
    if args.all or args.cedri: download_cedri_info_page()

if __name__ == "__main__":
    main()
