from celery import Task
from app.core.celery_app import celery_app
import httpx
import nmap
from datetime import datetime
import json

class ScanTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(f"Task {task_id} failed: {exc}")

@celery_app.task(base=ScanTask, bind=True)
def run_website_scan(self, url: str, scan_type: str = "full"):
    """Celery task to run website scan"""
    results = {
        "url": url,
        "scan_type": scan_type,
        "started_at": datetime.now().isoformat(),
        "status": "running"
    }
    
    try:
        # Health check
        with httpx.Client(timeout=10.0) as client:
            response = client.get(url)
            results["health"] = {
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "server": response.headers.get("server", "Unknown"),
            }
        
        # Port scan (if nmap is available)
        try:
            scanner = nmap.PortScanner()
            domain = url.split("//")[1].split("/")[0]
            scanner.scan(domain, arguments='-sS --top-ports 50')
            
            open_ports = []
            if domain in scanner.all_hosts():
                for proto in scanner[domain].all_protocols():
                    for port in scanner[domain][proto].keys():
                        if scanner[domain][proto][port]['state'] == 'open':
                            open_ports.append({
                                "port": port,
                                "protocol": proto,
                                "service": scanner[domain][proto][port].get('name', 'unknown')
                            })
            results["ports"] = open_ports
        except Exception as e:
            results["nmap_error"] = str(e)
        
        results["status"] = "completed"
        results["completed_at"] = datetime.now().isoformat()
        
        return results
        
    except Exception as e:
        results["status"] = "failed"
        results["error"] = str(e)
        return results