##Defines all data structures for facilities, units, emissions, etc.
##These classes are used throughout the pipeline.
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import date

class ControlDevice(BaseModel):
    type: str
    efficiency_pct: Optional[float] = None

class EmissionLimit(BaseModel):
    pollutant: str
    form: str
    value: float
    basis: Optional[str] = None
    source_span: Optional[str] = None  # link to document text or citation

class MonitoringReq(BaseModel):
    method: str
    pollutant: Optional[str] = None
    spec: Optional[str] = None

class TestingReq(BaseModel):
    method: str
    frequency: Optional[str] = None

class ARItem(BaseModel):
    citation: str
    basis: str  # e.g., NSPS, MACT, SIP
    text_span_id: Optional[str] = None

class Unit(BaseModel):
    unit_id: str
    process: Optional[str] = None
    fuel: Optional[str] = None
    startup_date: Optional[date] = None
    controls: List[ControlDevice] = []
    emission_limits: List[EmissionLimit] = []
    applicable_requirements: List[ARItem] = []
    monitoring: List[MonitoringReq] = []
    testing: List[TestingReq] = []
    rr: List[str] = []  # recordkeeping/reporting items

class PTESummary(BaseModel):
    NOx_tpy: float = 0
    SO2_tpy: float = 0
    CO_tpy: float = 0
    VOC_tpy: float = 0
    PM_tpy: float = 0

class TitleV(BaseModel):
    permit_no: Optional[str] = None
    status: Optional[str] = None
    expiration: Optional[date] = None
    insignificant_activities: List[str] = []
    general_conditions: List[str] = []
    compliance_certification: Dict[str, str] = {"frequency": "annual"}

class NSR(BaseModel):
    permitting_path: Optional[str] = None  # PSD / NNSR / Minor
    bact_laer_refs: List[Dict[str, str]] = []

class Site(BaseModel):
    address: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    naics: Optional[str] = None
    attainment_status: Dict[str, str] = {}

class Facility(BaseModel):
    name: str
    epa_id: Optional[str] = None
    program_ids: Dict[str, str] = {}

class PermitBundle(BaseModel):
    facility: Facility
    site: Site
    units: List[Unit]
    pte_summary: PTESummary = PTESummary()
    title_v: TitleV = TitleV()
    nsr: NSR = NSR()
    sources: List[Dict[str, str]] = []  # document IDs or citations
