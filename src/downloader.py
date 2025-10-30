## ✔ Sources for these endpoints:

##   ECHO bulk downloads & ICIS-Air summaries.
##    RBLC info / catalog listing.
##   CEDRI overview.
##    eCFR API for Title 40.
##    WebFIRE documentation PDF (optional).
## Downloads bulk datasets to data\raw\…

from pathlib import Path
import requests, time
from src.config import settings

RAW = Path(settings.data_dir) / "raw"
RAW.mkdir(parents=True, exist_ok=True)

def _fetch(url: str, out: Path, chunk=1<<15):
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        print(f"✓ Exists: {out}")
        return out
    print(f"↓ Downloading {url}\n→ {out}")
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(out, "wb") as f:
            for part in r.iter_content(chunk_size=chunk):
                if part: f.write(part)
    print(f"✓ Saved: {out}")
    return out

def download_echo_icis_air():
    # New fallback URL (smaller ECHO dataset) – verified 2025
    url = "https://echo.epa.gov/files/echodownloads/ICIS-AIR_downloads.zip"
    return _fetch(url, RAW / "echo" / "ICIS-AIR-CAFO.csv.zip")


def download_echo_air_emissions():
    # Combined Air Emissions dataset (facility aggregates)
    url = "https://echo.epa.gov/files/echodownloads/POLL_RPT_COMBINED_EMISSIONS.zip"
    return _fetch(url, RAW / "echo" / "AIR_EMISSIONS.zip")

def download_rblc_catalog():
    """
    The RBLC metadata indicates that the public access endpoint is
    the EPA RBLC Search portal. There is no direct JSON feed.
    For now we will store metadata locally and create a placeholder CSV
    that can be updated manually or via web scraping later.
    """
    out_json = RAW / "rblc" / "rblc_metadata.json"
    out_csv = RAW / "rblc" / "rblc_demo.csv"
    out_json.parent.mkdir(parents=True, exist_ok=True)

    # Save the known metadata JSON locally
    metadata = {
        "title": "RACT/BACT/LAER Clearinghouse (RBLC)",
        "accessURL": "https://cfpub.epa.gov/rblc/index.cfm?action=Search.BasicSearch&lang=en",
        "description": (
            "Summary information on air permitting actions from EPA, state, and local "
            "permitting agencies. Contains control technology data for RACT, BACT, and LAER determinations."
        ),
        "contact": "Joe Steigerwald <Steigerwald.joe@epa.gov>",
        "license": "https://edg.epa.gov/EPA_Data_License.html"
    }
    import json
    out_json.write_text(json.dumps(metadata, indent=2))
    print(f"✓ Saved RBLC metadata to: {out_json}")

    # Create a small demo CSV for indexing (simulating BACT/LAER data)
    import pandas as pd
    data = [
        ["TX-1001", "NOx", "Selective Catalytic Reduction", 9.0, "ppmvd @ 15% O2", "Boiler"],
        ["CA-2002", "SO2", "Wet Scrubber", 0.02, "lb/MMBtu", "Boiler"],
        ["OH-3003", "VOC", "Thermal Oxidizer", 0.005, "lb/MMBtu", "Combustion Turbine"]
    ]
    df = pd.DataFrame(data, columns=["rblc_id", "pollutant", "tech", "limit", "form", "process"])
    df.to_csv(out_csv, index=False)
    print(f"✓ Created demo RBLC dataset: {out_csv}")
    return out_csv

def download_webfire_procedures_pdf():
    url = "https://www.epa.gov/system/files/documents/2024-09/final-webfire-procedures-document_aug-2024.pdf"
    return _fetch(url, RAW / "webfire" / "webfire_procedures_2024.pdf")

import datetime, json, requests

def download_ecfr_title40_toc():
    """
    Download the most recent eCFR Title 40 structure JSON using the Versioner API.
    Falls back to placeholder if all attempts fail.
    """
    base = "https://www.ecfr.gov/api/versioner/v1"
    out_json = RAW / "cfr" / "title40_structure_latest.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)

    try:
        # 1️⃣ Get list of available versions for Title 40
        ver_url = f"{base}/versions/title-40.json"
        print(f"↓ Getting version list: {ver_url}")
        resp = requests.get(ver_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
        resp.raise_for_status()
        versions = resp.json().get("versions", [])
        if not versions:
            raise ValueError("No versions found")
        latest = versions[-1]["date"]
        print(f"→ Latest version date: {latest}")

        # 2️⃣ Download that version’s structure
        struct_url = f"{base}/structure/{latest}/title-40.json"
        print(f"↓ Downloading {struct_url}")
        r2 = requests.get(struct_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=90)
        r2.raise_for_status()
        out_json.write_text(json.dumps(r2.json(), indent=2))
        print(f"✓ Saved Title 40 structure: {out_json}")
        return out_json

    except Exception as e:
        print(f"⚠️ Could not fetch Title 40 structure: {e}")
        # 3️⃣ Fallback placeholder
        data = {
            "title": 40,
            "description": "Placeholder structure for eCFR Title 40.",
            "sections": [
                {"part": "50", "title": "National Ambient Air Quality Standards"},
                {"part": "60", "title": "New Source Performance Standards"},
                {"part": "63", "title": "NESHAP for Hazardous Air Pollutants"},
                {"part": "70", "title": "State Operating Permit Programs"},
                {"part": "71", "title": "Federal Operating Permit Programs"},
            ],
        }
        out_json.write_text(json.dumps(data, indent=2))
        print(f"Created placeholder: {out_json}")
        return out_json


def download_ecfr_part(title=40, part="60"):
    """
    Download specific eCFR part (e.g., 40 CFR Part 60) as XML.
    """
    today = datetime.date.today().isoformat()
    out_xml = RAW / "cfr" / f"title{title}_part{part}_{today}.xml"
    base = "https://www.ecfr.gov/api/versioner/v1"
    url = f"{base}/full/{today}/title-{title}-part-{part}.xml"
    try:
        print(f"↓ Downloading {url}")
        return _fetch(url, out_xml)
    except Exception as e:
        print(f"⚠️ Could not fetch part {part}: {e}")
        out_xml.write_text(f"<placeholder>Title {title} Part {part}</placeholder>")
        return out_xml

def download_cedri_info_page():
    # CEDRI landing HTML (reference). Actual reports are pulled by search; many are PDFs/ZIPs.
    url = "https://www.epa.gov/electronic-reporting-air-emissions/cedri"
    return _fetch(url, RAW / "cedri" / "cedri.html")
