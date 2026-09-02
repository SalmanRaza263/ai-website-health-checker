import httpx
from bs4 import BeautifulSoup
from typing import Dict, Any, List

async def detect_technologies(url: str) -> Dict[str, Any]:
    """Detect website technologies"""
    technologies = []
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            html = response.text
            headers = response.headers
            
            # Server detection
            server = headers.get("server", "").lower()
            if "nginx" in server:
                technologies.append({"name": "Nginx", "category": "Web Server", "version": server.split("/")[-1] if "/" in server else "Unknown"})
            elif "apache" in server:
                technologies.append({"name": "Apache", "category": "Web Server", "version": server.split("/")[-1] if "/" in server else "Unknown"})
            
            # CMS detection
            if "wp-content" in html or "wp-includes" in html:
                technologies.append({"name": "WordPress", "category": "CMS"})
            if "Joomla" in html or "joomla" in html.lower():
                technologies.append({"name": "Joomla", "category": "CMS"})
            if "Drupal" in html or "drupal" in html.lower():
                technologies.append({"name": "Drupal", "category": "CMS"})
            
            # JavaScript frameworks
            if "react" in html.lower():
                technologies.append({"name": "React", "category": "JavaScript Framework"})
            if "vue" in html.lower():
                technologies.append({"name": "Vue.js", "category": "JavaScript Framework"})
            if "angular" in html.lower():
                technologies.append({"name": "Angular", "category": "JavaScript Framework"})
            if "jquery" in html.lower():
                technologies.append({"name": "jQuery", "category": "JavaScript Library"})
            
            # CSS frameworks
            if "bootstrap" in html.lower():
                technologies.append({"name": "Bootstrap", "category": "CSS Framework"})
            if "tailwind" in html.lower():
                technologies.append({"name": "Tailwind CSS", "category": "CSS Framework"})
            
            # Analytics
            if "google-analytics" in html.lower():
                technologies.append({"name": "Google Analytics", "category": "Analytics"})
            if "gtag" in html.lower():
                technologies.append({"name": "Google Tag Manager", "category": "Analytics"})
            
            return {
                "technologies": technologies,
                "count": len(technologies)
            }
            
    except Exception as e:
        return {"error": str(e), "technologies": []}