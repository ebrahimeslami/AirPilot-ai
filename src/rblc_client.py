from pathlib import Path
import pandas as pd
from src.config import settings

class RBLCClient:
    """Loads BACT/LAER determinations from EPA's RBLC Clearinghouse."""

    def __init__(self):
        self.data_dir = Path(settings.data_dir) / "raw" / "rblc"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def create_demo_rblc(self):
        """Create a demo RBLC dataset for testing."""
        out = self.data_dir / "rblc_demo.csv"
        data = [
            ["TX-12345", "NOx", "Selective Catalytic Reduction", 9, "ppmvd @ 15% O2"],
            ["CA-56789", "SO2", "Wet Scrubber", 0.02, "lb/MMBtu"]
        ]
        df = pd.DataFrame(data, columns=["rblc_id", "pollutant", "tech", "limit", "form"])
        df.to_csv(out, index=False)
        print(f"Demo RBLC data saved: {out}")
        return out
