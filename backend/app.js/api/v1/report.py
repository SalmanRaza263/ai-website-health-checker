from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from datetime import datetime

router = APIRouter()

class ReportResponse(BaseModel):
    scan_id: str
    report: Dict[str, Any]
    format: str

@router.get("/report/{scan_id}")
async def get_report(scan_id: str, format: Optional[str] = "json"):
    """Get scan report"""
    from app.api.v1.scan import scan_results
    
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    scan_data = scan_results[scan_id]
    
    if scan_data["status"] != "completed":
        raise HTTPException(status_code=400, detail="Scan not completed yet")
    
    if format == "pdf":
        # Generate PDF report
        return {"message": "PDF report generation coming soon"}
    
    return ReportResponse(
        scan_id=scan_id,
        report=scan_data["results"],
        format="json"
    )

@router.get("/report/{scan_id}/download")
async def download_report(scan_id: str, format: Optional[str] = "json"):
    """Download report in specified format"""
    from app.api.v1.scan import scan_results
    
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    # For now, return JSON
    return scan_results[scan_id]