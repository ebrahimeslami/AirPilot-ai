from datetime import date
from typing import Dict, List

# --- Helper logic (expand with real thresholds as you iterate) ---

def _is_boiler(unit: Dict) -> bool:
    proc = (unit.get("process") or "").lower()
    return "boiler" in proc or "steam" in proc

def _is_turbine(unit: Dict) -> bool:
    proc = (unit.get("process") or "").lower()
    return "turbine" in proc

def _is_engine(unit: Dict) -> bool:
    proc = (unit.get("process") or "").lower()
    return ("engine" in proc) or ("ice" in proc) or ("r.i.c.e" in proc)

def _fuel(unit: Dict) -> str:
    return (unit.get("fuel") or "").lower()

def _startup_year(unit: Dict) -> int:
    sd = unit.get("startup_date")
    if not sd:
        return 0
    if isinstance(sd, date):
        return sd.year
    try:
        return int(str(sd)[:4])
    except Exception:
        return 0

# --- Applicability determinations (MVP heuristics; refine later) ---

def nsps_applicability(unit: Dict) -> List[Dict]:
    """
    Very simplified NSPS triggers for MVP:
      - Boilers/steam generators -> Subpart Db/ Dc (capacity/date unknown in MVP)
      - Combustion turbines -> Subpart KKKK
      - RICE engines -> Subpart JJJJ (SI) or Subpart IIII (CI) [not differentiated here]
    """
    out = []
    fuel = _fuel(unit)
    year = _startup_year(unit)

    if _is_boiler(unit):
        # Capacity & date thresholds omitted for MVP
        out.append({"citation": "40 CFR 60 Subpart Db", "basis": "NSPS"})
    if _is_turbine(unit):
        out.append({"citation": "40 CFR 60 Subpart KKKK", "basis": "NSPS"})
    if _is_engine(unit):
        out.append({"citation": "40 CFR 60 Subpart JJJJ/IIII", "basis": "NSPS"})

    return out

def mact_applicability(unit: Dict, facility_major_hap: bool = True) -> List[Dict]:
    """
    Simplified MACT logic (MVP):
      - Industrial/Commercial/Institutional Boilers (major HAP) -> Subpart DDDDD
      - RICE at major HAP -> Subpart ZZZZ
    """
    out = []
    if not facility_major_hap:
        return out

    if _is_boiler(unit):
        out.append({"citation": "40 CFR 63 Subpart DDDDD", "basis": "MACT"})
    if _is_engine(unit):
        out.append({"citation": "40 CFR 63 Subpart ZZZZ", "basis": "MACT"})
    return out

def cam_applicability(unit: Dict, is_title_v_major: bool = True) -> List[Dict]:
    """
    Very simplified Compliance Assurance Monitoring (CAM) flagging:
      - If the unit has a control device AND the facility is major (Title V), flag Part 64.
    """
    out = []
    controls = unit.get("controls") or []
    if is_title_v_major and len(controls) > 0:
        out.append({"citation": "40 CFR Part 64 (CAM)", "basis": "CAM"})
    return out

def sip_placeholder(unit: Dict) -> List[Dict]:
    """Placeholder for state-specific SIP rules to be populated later."""
    return [{"citation": "[State SIP rule – insert citation]", "basis": "SIP"}]

def select_applicable_requirements(unit: Dict,
                                   is_title_v_major: bool = True,
                                   facility_major_hap: bool = True) -> List[Dict]:
    ars = []
    ars += nsps_applicability(unit)
    ars += mact_applicability(unit, facility_major_hap=facility_major_hap)
    ars += cam_applicability(unit, is_title_v_major=is_title_v_major)
    ars += sip_placeholder(unit)
    # Deduplicate by citation
    seen = set()
    dedup = []
    for a in ars:
        if a["citation"] not in seen:
            dedup.append(a)
            seen.add(a["citation"])
    return dedup
