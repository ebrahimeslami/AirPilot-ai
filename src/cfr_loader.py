from src.storage import upsert_doc, SessionLocal

# Basic regulatory text samples (to be replaced later with real CFR excerpts)
CFR_SNIPPETS = {
    "40 CFR 70.6": "Each permit shall include monitoring, recordkeeping, and reporting requirements...",
    "40 CFR 60 Subpart Db": "Standards of performance for industrial-commercial-institutional steam generating units...",
    "40 CFR 63 Subpart DDDDD": "NESHAP for major sources: Industrial, Commercial, and Institutional Boilers and Process Heaters..."
}

def load_cfr_into_db():
    """Insert CFR snippets into the database for use by the generator."""
    session = SessionLocal()
    for cite, text in CFR_SNIPPETS.items():
        upsert_doc(session, f"cfr:{cite}", "cfr", cite, text, {"citation": cite})
    session.close()
    print("✅ CFR snippets loaded into the database.")
