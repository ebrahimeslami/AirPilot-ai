from pathlib import Path
import json
from src.config import settings

class CEDRIClient:
    """Loads or creates demo stack test and compliance data (CEDRI)."""

    def __init__(self):
        self.data_dir = Path(settings.data_dir) / "raw" / "cedri"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def create_demo_cedri(self):
        """Create a simple test report JSON for demo."""
        report = {
            "facility": "Demo Refinery",
            "unit": "U-1",
            "test_method": "Method 7E",
            "pollutant": "NOx",
            "result": "PASS",
            "next_test_due": "2030-01-01"
        }
        out = self.data_dir / "cedri_demo.json"
        out.write_text(json.dumps(report, indent=2))
        print(f"Demo CEDRI data saved: {out}")
        return out
