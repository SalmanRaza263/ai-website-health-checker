from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class IssueBase(BaseModel):
    scan_id: str
    category: str
    severity: str  # critical, high, medium, low, info
    title: str
    description: str
    recommendation: str

class IssueCreate(IssueBase):
    cve_id: Optional[str] = None
    location: Optional[str] = None

class Issue(IssueBase):
    id: str
    cve_id: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime