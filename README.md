# AirPermit-AI
**Generative Drafting Tool for EPA Air Permits (Title V / NSR)**  
Created by **Ebrahim Eslami, PhD** — 2025

---

### 🌎 Overview
AirPermit-AI is a Python-based system that reads and interprets public EPA datasets (ECHO/ICIS-Air, RBLC, CEDRI, and Title 40 CFR text) to generate **draft air permits** (Title V and NSR).  
It uses rule-based preselection + retrieval-augmented generation (RAG) to automatically fill applicable regulatory requirements and create compliance roadmaps.

---

### 📁 Project layout

airpermit-ai/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ requirements.txt
├─ .env.example
├─ setup.py
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ data_models.py
│  ├─ storage.py
│  ├─ echo_client.py
│  ├─ rblc_client.py
│  ├─ cedri_client.py
│  ├─ cfr_loader.py
│  ├─ pdf_parser.py
│  ├─ chunking.py
│  ├─ embeddings.py
│  ├─ vectorstore.py
│  ├─ rules_engine.py
│  ├─ generator.py
│  ├─ cli.py
│  └─ templates/
│     └─ title_v_template.jinja
├─ tests/
│  ├─ test_rules_engine.py
│  └─ test_generator_smoke.py
└─ data/ (ignored by Git)



---

### 🧠 Features (MVP)
- Structured data schema for facilities, units, and permits  
- Rule engine for NSPS/MACT/SIP applicability  
- Jinja2 generator for Title V permit drafts  
- Extensible ingestion clients for ECHO, RBLC, CEDRI  
- Local embeddings & FAISS vector search (planned)  

---

### ⚙️ Installation
```bash
git clone https://github.com/<your-username>/AirPilot-ai.git
cd airpermit-ai
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

🚀 Quick start
python -m src.cli index    # load CFR snippets
python -m src.cli draft --output ./src/data/processed/draft_title_v_demo.md

🧰 Next steps

Connect real ECHO/RBLC/CEDRI data sources
Expand rules for actual NSPS/MACT/PSD thresholds
Add vector retrieval and QA traceability
Integrate DOCX/PDF export for client-ready drafts
