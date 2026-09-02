from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class ScanBase(BaseModel):
    url: str
    user_id: Optional[str] = None

class ScanCreate(ScanBase):
    status: str = "pending"
    scan_type: str = "full"

class Scan(ScanBase):
    id: str
    status: str
    scan_type: str
    results: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    overall_score: Optional[int] = None

class ScanResult(BaseModel):
    scan_id: str
    category: str
    score: int
    data: Dict[str, Any]
    summary: Optional[Dict[str, Any]] = None
    created_at: datetime