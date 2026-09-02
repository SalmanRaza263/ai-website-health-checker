import json
import re
from typing import Dict, List, Any, Optional

def parse_nmap_output(output: str) -> Dict[str, Any]:
    """
    Parse nmap command line output into structured data
    
    Args:
        output: Raw nmap output string
    
    Returns:
        Dict containing parsed results
    """
    results = {
        "hosts": [],
        "ports": [],
        "services": [],
        "summary": {},
        "errors": []
    }
    
    if not output:
        results["errors"].append("No output to parse")
        return results
    
    lines = output.split('\n')
    
    # Parse host information
    host_pattern = re.compile(r'Nmap scan report for (.+?)(?:\((.+?)\))?$')
    for line in lines:
        match = host_pattern.search(line)
        if match:
            hostname = match.group(1).strip()
            ip = match.group(2).strip() if match.group(2) else hostname
            results["hosts"].append({
                "hostname": hostname,
                "ip": ip
            })
    
    # Parse port information
    port_pattern = re.compile(r'^(\d+)/(tcp|udp)\s+(\w+)\s+(\w+)\s*(.*)$')
    for line in lines:
        match = port_pattern.search(line.strip())
        if match:
            port_num = int(match.group(1))
            protocol = match.group(2)
            state = match.group(3)
            service = match.group(4)
            extra = match.group(5).strip() if match.group(5) else ""
            
            port_info = {
                "port": port_num,
                "protocol": protocol,
                "state": state,
                "service": service,
                "extra": extra
            }
            results["ports"].append(port_info)
            
            # Also add to services list
            results["services"].append({
                "port": port_num,
                "protocol": protocol,
                "name": service,
                "state": state
            })
    
    # Parse summary
    summary_patterns = {
        "hosts_up": re.compile(r'(\d+)\s+hosts? up'),
        "hosts_down": re.compile(r'(\d+)\s+hosts? down'),
        "ports_scanned": re.compile(r'(\d+)\s+ports? scanned'),
        "scan_duration": re.compile(r'(\d+\.?\d*)\s+seconds')
    }
    
    for line in lines:
        for key, pattern in summary_patterns.items():
            match = pattern.search(line)
            if match:
                results["summary"][key] = match.group(1)
    
    # Parse errors
    error_pattern = re.compile(r'ERROR: (.+)$', re.IGNORECASE)
    for line in lines:
        match = error_pattern.search(line)
        if match:
            results["errors"].append(match.group(1).strip())
    
    return results


def parse_nmap_json(json_output: str) -> Dict[str, Any]:
    """
    Parse nmap JSON output
    
    Args:
        json_output: JSON string from nmap -oJ option
    
    Returns:
        Dict containing parsed JSON data
    """
    try:
        data = json.loads(json_output)
        return {
            "status": "success",
            "data": data,
            "scan_type": "json"
        }
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"Invalid JSON: {str(e)}",
            "scan_type": "json"
        }


def parse_nmap_xml(xml_output: str) -> Dict[str, Any]:
    """
    Parse nmap XML output (basic version without external libraries)
    
    Args:
        xml_output: XML string from nmap -oX option
    
    Returns:
        Dict containing parsed XML data
    """
    results = {
        "status": "partial",
        "hosts": [],
        "ports": [],
        "errors": []
    }
    
    if not xml_output:
        results["errors"].append("No XML output to parse")
        return results
    
    try:
        # Extract host information using regex (simple parsing)
        host_pattern = re.compile(r'<host[^>]*>.*?<address[^>]*addr="([^"]*)"[^>]*>.*?<hostname[^>]*name="([^"]*)"[^>]*>', re.DOTALL)
        for match in host_pattern.finditer(xml_output):
            ip = match.group(1)
            hostname = match.group(2) if match.group(2) else ip
            results["hosts"].append({
                "ip": ip,
                "hostname": hostname
            })
        
        # Extract port information
        port_pattern = re.compile(
            r'<port protocol="([^"]*)" portid="([^"]*)">.*?'
            r'<state state="([^"]*)"[^>]*>.*?'
            r'<service name="([^"]*)"[^>]*>',
            re.DOTALL
        )
        for match in port_pattern.finditer(xml_output):
            protocol = match.group(1)
            port = int(match.group(2))
            state = match.group(3)
            service = match.group(4)
            
            results["ports"].append({
                "port": port,
                "protocol": protocol,
                "state": state,
                "service": service
            })
        
        results["status"] = "success"
        
    except Exception as e:
        results["errors"].append(f"Parse error: {str(e)}")
        results["status"] = "error"
    
    return results


def extract_open_ports(parsed_data: Dict[str, Any]) -> List[int]:
    """
    Extract list of open ports from parsed nmap data
    
    Args:
        parsed_data: Parsed nmap data from parse_nmap_output
    
    Returns:
        List of open port numbers
    """
    open_ports = []
    for port in parsed_data.get("ports", []):
        if port.get("state") == "open":
            open_ports.append(port.get("port"))
    return sorted(open_ports)


def extract_services(parsed_data: Dict[str, Any]) -> Dict[int, str]:
    """
    Extract service names by port from parsed nmap data
    
    Args:
        parsed_data: Parsed nmap data from parse_nmap_output
    
    Returns:
        Dict mapping port numbers to service names
    """
    services = {}
    for port in parsed_data.get("ports", []):
        if port.get("state") == "open":
            services[port.get("port")] = port.get("service", "unknown")
    return services


def get_nmap_summary(parsed_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of nmap scan results
    
    Args:
        parsed_data: Parsed nmap data from parse_nmap_output
    
    Returns:
        Summary dict with key metrics
    """
    ports = parsed_data.get("ports", [])
    open_ports = [p for p in ports if p.get("state") == "open"]
    closed_ports = [p for p in ports if p.get("state") == "closed"]
    
    return {
        "total_hosts": len(parsed_data.get("hosts", [])),
        "total_ports_found": len(ports),
        "open_ports": len(open_ports),
        "closed_ports": len(closed_ports),
        "filtered_ports": len([p for p in ports if p.get("state") == "filtered"]),
        "services_found": list(set([p.get("service") for p in open_ports if p.get("service")])),
        "has_errors": len(parsed_data.get("errors", [])) > 0,
        "error_count": len(parsed_data.get("errors", []))
    }


def format_nmap_results(parsed_data: Dict[str, Any]) -> str:
    """
    Format nmap results as readable text
    
    Args:
        parsed_data: Parsed nmap data from parse_nmap_output
    
    Returns:
        Formatted string
    """
    lines = []
    lines.append("=" * 50)
    lines.append("NMAP SCAN RESULTS")
    lines.append("=" * 50)
    
    # Hosts
    hosts = parsed_data.get("hosts", [])
    if hosts:
        lines.append("\n[*] Hosts Found:")
        for host in hosts:
            lines.append(f"    - {host.get('hostname', 'Unknown')} ({host.get('ip', 'Unknown')})")
    
    # Open Ports
    open_ports = extract_open_ports(parsed_data)
    services = extract_services(parsed_data)
    
    if open_ports:
        lines.append("\n[*] Open Ports:")
        for port in open_ports:
            service = services.get(port, "unknown")
            lines.append(f"    - Port {port}: {service}")
    else:
        lines.append("\n[*] No open ports found")
    
    # Summary
    summary = get_nmap_summary(parsed_data)
    lines.append("\n[*] Summary:")
    lines.append(f"    - Total Hosts: {summary['total_hosts']}")
    lines.append(f"    - Open Ports: {summary['open_ports']}")
    lines.append(f"    - Services: {', '.join(summary['services_found']) if summary['services_found'] else 'None'}")
    
    # Errors
    errors = parsed_data.get("errors", [])
    if errors:
        lines.append("\n[!] Errors:")
        for error in errors:
            lines.append(f"    - {error}")
    
    lines.append("\n" + "=" * 50)
    
    return "\n".join(lines)