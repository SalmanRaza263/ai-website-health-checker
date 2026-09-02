import httpx
import re
from typing import Dict, Any

async def check_seo(url: str) -> Dict[str, Any]:
    """Check SEO elements"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            html = response.text
            
            seo = {
                "title": "Missing",
                "title_length": 0,
                "description": "Missing",
                "description_length": 0,
                "keywords": "Missing",
                "h1": 0,
                "h2": 0,
                "h3": 0,
                "h4": 0,
                "images": 0,
                "alt_text": 0,
                "links": 0,
                "internal_links": 0,
                "external_links": 0,
                "canonical": "Missing",
                "robots": "Missing",
                "sitemap": "Missing"
            }
            
            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
            if title_match:
                seo["title"] = title_match.group(1)
                seo["title_length"] = len(title_match.group(1))
            
            # Extract meta tags
            meta_desc = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if meta_desc:
                seo["description"] = meta_desc.group(1)
                seo["description_length"] = len(meta_desc.group(1))
            
            meta_keywords = re.search(r'<meta\s+name=["\']keywords["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if meta_keywords:
                seo["keywords"] = meta_keywords.group(1)
            
            # Canonical
            canonical = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE)
            if canonical:
                seo["canonical"] = canonical.group(1)
            
            # Robots
            robots = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
            if robots:
                seo["robots"] = robots.group(1)
            
            # Count headings
            seo["h1"] = len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE))
            seo["h2"] = len(re.findall(r'<h2[^>]*>', html, re.IGNORECASE))
            seo["h3"] = len(re.findall(r'<h3[^>]*>', html, re.IGNORECASE))
            seo["h4"] = len(re.findall(r'<h4[^>]*>', html, re.IGNORECASE))
            
            # Count images with alt
            images = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
            seo["images"] = len(images)
            seo["alt_text"] = len(re.findall(r'<img[^>]*alt=["\'][^"\']*["\'][^>]*>', html, re.IGNORECASE))
            
            # Count links
            links = re.findall(r'<a[^>]*href=["\'](.*?)["\'][^>]*>', html, re.IGNORECASE)
            seo["links"] = len(links)
            
            domain = url.split("//")[1].split("/")[0]
            for link in links:
                if domain in link or link.startswith("/"):
                    seo["internal_links"] += 1
                elif link.startswith("http"):
                    seo["external_links"] += 1
            
            # SEO Score
            score = 0
            if seo["title"] != "Missing" and 30 <= seo["title_length"] <= 60:
                score += 20
            if seo["description"] != "Missing" and 120 <= seo["description_length"] <= 160:
                score += 20
            if seo["h1"] > 0:
                score += 15
            if seo["canonical"] != "Missing":
                score += 10
            if seo["robots"] != "Missing":
                score += 10
            if seo["alt_text"] > 0:
                score += 10
            if seo["internal_links"] > 5:
                score += 10
            
            seo["seo_score"] = score
            
            return seo
            
    except Exception as e:
        return {"error": str(e)}