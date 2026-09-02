from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ResultBase(BaseModel):
    scan_id: str
    category: str
    score: int
    data: Dict[str, Any]

class ResultCreate(ResultBase):
    summary: Optional[Dict[str, Any]] = None

class Result(ResultBase):
    id: str
    summary: Optional[Dict[str, Any]] = None
    created_at: datetime

class Issue(BaseModel):
    id: str
    scan_id: str
    category: str
    severity: str  # critical, high, medium, low, info
    title: str
    description: str
    recommendation: str
    cve_id: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime