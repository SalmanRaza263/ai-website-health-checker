import json
import re
from typing import Dict, List, Any

def parse_nmap_output(output: str) -> Dict[str, Any]:
    """Parse nmap output"""
    results = {
        "hosts": [],
        "ports": [],
        "services": []
    }
    
    # Parse host
    host_match = re.search(r'Nmap scan report for (.*?)\n', output)
    if host_match:
        results["hosts"].append(host_match.group(1))
    
    # Parse ports
    port_pattern = r'(\d+)/(tcp|udp)\s+(\w+)\s+(\w+)\s*(.*)'
    for match in re.finditer(port_pattern, output):
        port, protocol, state, service, extra = match.groups()
        results["ports"].append({
            "port": int(port),
            "protocol": protocol,
            "state": state,
            "service": service,
            "extra": extra.strip()
        })
    
    return results

def parse_nmap_json(json_output: str) -> Dict[str, Any]:
    """Parse nmap JSON output"""
    try:
        data = json.loads(json_output)
        return data
    except:
        return {"error": "Invalid JSON output"}