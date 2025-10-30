from pathlib import Path
from src.export_docx import convert_draft_md_to_docx

def main():
    # locate latest processed markdown file
    proc = Path("data/processed")
    md_files = sorted(proc.glob("draft_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not md_files:
        print("⚠️ No draft markdown found in data/processed/")
        return
    latest = md_files[0]
    print(f"Converting: {latest.name}")
    convert_draft_md_to_docx(latest)

if __name__ == "__main__":
    main()
