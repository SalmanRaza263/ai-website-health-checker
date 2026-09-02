import httpx
import time
from typing import Dict, Any

async def check_performance(url: str) -> Dict[str, Any]:
    """Check website performance"""
    try:
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            load_time = time.time() - start_time
            
            # Get page size
            content_length = len(response.content)
            
            # Count requests (approximate)
            html = response.text
            import re
            scripts = len(re.findall(r'<script[^>]*>', html))
            styles = len(re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', html))
            images = len(re.findall(r'<img[^>]*>', html))
            
            return {
                "load_time": round(load_time, 2),
                "page_size": round(content_length / 1024, 2),
                "requests": scripts + styles + images,
                "scripts": scripts,
                "styles": styles,
                "images": images,
                "status_code": response.status_code
            }
            
    except Exception as e:
        return {"error": str(e)}