##Handles all paths and environment settings.
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """Stores global project settings and paths."""
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    db_url: str = os.getenv("DB_URL", "sqlite:///./data/airpermit.db")
    indexes_dir: Path = Path("./src/indexes")

# Instantiate and create directories if missing
settings = Settings()
settings.data_dir.mkdir(parents=True, exist_ok=True)
(settings.data_dir / "raw").mkdir(parents=True, exist_ok=True)
(settings.data_dir / "processed").mkdir(parents=True, exist_ok=True)
settings.indexes_dir.mkdir(parents=True, exist_ok=True)
