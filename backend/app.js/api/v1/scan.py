from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

router = APIRouter()

class ScanRequest(BaseModel):
    url: str
    scan_type: Optional[str] = "full"

class ScanResponse(BaseModel):
    scan_id: str
    url: str
    status: str
    message: str

# In-memory storage (replace with database)
scan_results = {}

@router.post("/scan")
async def start_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    """Start a website scan"""
    try:
        scan_id = str(uuid.uuid4())
        url = request.url
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        
        scan_results[scan_id] = {
            "id": scan_id,
            "url": url,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "results": None
        }
        
        # Run scan in background
        background_tasks.add_task(run_scan, scan_id, url)
        
        return ScanResponse(
            scan_id=scan_id,
            url=url,
            status="pending",
            message="Scan started successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan/{scan_id}")
async def get_scan_status(scan_id: str):
    """Get scan status and results"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan_results[scan_id]

@router.get("/history")
async def get_scan_history():
    """Get scan history"""
    return {
        "scans": list(scan_results.values()),
        "total": len(scan_results)
    }

async def run_scan(scan_id: str, url: str):
    """Background task to run scan"""
    try:
        scan_results[scan_id]["status"] = "running"
        
        # Import services
        from app.services.wappalyzer_service import detect_technologies
        from app.services.performance_service import check_performance
        from app.services.seo_service import check_seo
        from app.services.accessibility_service import check_accessibility
        
        # Run all scans
        results = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "technologies": await detect_technologies(url),
            "performance": await check_performance(url),
            "seo": await check_seo(url),
            "accessibility": await check_accessibility(url),
        }
        
        scan_results[scan_id]["results"] = results
        scan_results[scan_id]["status"] = "completed"
        scan_results[scan_id]["completed_at"] = datetime.now().isoformat()
        
    except Exception as e:
        scan_results[scan_id]["status"] = "failed"
        scan_results[scan_id]["error"] = str(e)