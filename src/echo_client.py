from pathlib import Path
import requests
from src.config import settings

class ECHOClient:
    """Handles fetching facility and permit data from EPA's ECHO system."""

    def __init__(self):
        self.data_dir = Path(settings.data_dir) / "raw" / "echo"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def download_facility_snapshot(self):
        """
        Download a public ECHO Air Facilities CSV snapshot.
        (For MVP, this downloads a small sample.)
        """
        out = self.data_dir / "echo_air_facilities.csv"
        if out.exists():
            print(f"File already exists: {out}")
            return out

        # ECHO offers bulk downloads (large). For demo, use a small mock file.
        print("Creating demo ECHO dataset...")
        text = (
            "facility_id,name,state,permit_type\n"
            "TX0001,Demo Refinery,TX,Title V\n"
            "LA0002,Example Chemical Plant,LA,NSR\n"
        )
        out.write_text(text)
        print(f"Sample dataset created: {out}")
        return out

    def fetch_permit_pdf(self, url: str, filename: str):
        """
        Download a permit or report PDF by URL (if you have one).
        Saves to /data/raw/echo.
        """
        p = self.data_dir / filename
        if p.exists():
            print(f"Already downloaded: {p}")
            return p
        print(f"Downloading {url} ...")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        p.write_bytes(r.content)
        print(f"Saved PDF: {p}")
        return p
