import httpx
import re
from typing import Dict, Any

async def check_accessibility(url: str) -> Dict[str, Any]:
    """Check accessibility (WCAG)"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            html = response.text
            
            accessibility = {
                "aria_labels": 0,
                "alt_text_images": 0,
                "total_images": 0,
                "semantic_elements": 0,
                "header_structure": False,
                "landmarks": [],
                "issues": [],
                "score": 0
            }
            
            # Count ARIA labels
            accessibility["aria_labels"] = len(re.findall(r'aria-label=["\'][^"\']*["\']', html, re.IGNORECASE))
            accessibility["aria_labels"] += len(re.findall(r'aria-labelledby=["\'][^"\']*["\']', html, re.IGNORECASE))
            
            # Count alt text
            images = re.findall(r'<img[^>]*>', html, re.IGNORECASE)
            accessibility["total_images"] = len(images)
            accessibility["alt_text_images"] = len(re.findall(r'<img[^>]*alt=["\'][^"\']+["\'][^>]*>', html, re.IGNORECASE))
            
            # Check for semantic elements
            semantic = re.findall(r'<(article|aside|details|figcaption|figure|footer|header|main|mark|nav|section|summary|time)[^>]*>', html, re.IGNORECASE)
            accessibility["semantic_elements"] = len(semantic)
            
            # Check header structure
            if len(re.findall(r'<h1[^>]*>', html, re.IGNORECASE)) > 0:
                accessibility["header_structure"] = True
            
            # Find landmarks
            landmarks = re.findall(r'<main[^>]*>', html, re.IGNORECASE)
            if landmarks:
                accessibility["landmarks"].append("main")
            if re.findall(r'<nav[^>]*>', html, re.IGNORECASE):
                accessibility["landmarks"].append("navigation")
            if re.findall(r'<header[^>]*>', html, re.IGNORECASE):
                accessibility["landmarks"].append("header")
            if re.findall(r'<footer[^>]*>', html, re.IGNORECASE):
                accessibility["landmarks"].append("footer")
            
            # Accessibility score
            score = 0
            if accessibility["alt_text_images"] > 0:
                score += 25
            if accessibility["semantic_elements"] > 0:
                score += 25
            if accessibility["header_structure"]:
                score += 20
            if accessibility["aria_labels"] > 0:
                score += 15
            if len(accessibility["landmarks"]) >= 3:
                score += 15
            
            accessibility["score"] = score
            
            return accessibility
            
    except Exception as e:
        return {"error": str(e)}