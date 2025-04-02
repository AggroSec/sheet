import xml.etree.ElementTree as ET
import json
import argparse
import re
import os

def print_logo():
    """Print the ASCII art logo."""
    logo = """
 _________ ___ ____________________________________
 /   _____//   |   \_   _____/\_   _____/\__    ___/
 \_____  \/    ~    \    __)_  |    __)_   |    |   
 /        \    Y    /        \ |        \  |    |   
/_______  /\___|_  /_______  //_______  /  |____|   
        \/       \/        \/         \/            
        Cheatsheet for the Offensive Edge
    """
    print(logo)

def sanitize_text(text):
    """Sanitize IPs and hostnames, but preserve URLs."""
    url_pattern = r'(https?://[^\s]+)'
    urls = re.findall(url_pattern, text)
    for i, url in enumerate(urls):
        text = text.replace(url, f"{{URL{i}}}")
    
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[SANITIZED_IP]', text)
    text = re.sub(r'\b([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b(?![^\s]*\])', '[SANITIZED_HOST]', text)
    
    for i, url in enumerate(urls):
        text = text.replace(f"{{URL{i}}}", url)
    return text

def load_config(file_path):
    """Load a JSON config file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Config file {file_path} not found!")
    with open(file_path, 'r') as f:
        return json.load(f)

def parse_nmap(xml_file):
    """Parse Nmap XML output and return target IP and list of open ports."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ports = []
    target = None
    
    host = root.find(".//host")
    if host:
        address = host.find("address")
        if address is not None:
            target = address.get("addr")
    
    for port in root.findall(".//port"):
        port_id = port.get("portid")
        state = port.find("state").get("state")
        if state != "open":
            continue
        service = port.find("service").get("name") if port.find("service") else "unknown"
        version = port.find("service").get("version") if port.find("service") else "unknown"
        ports.append({"port": port_id, "service": service, "version": version})
    return target, ports

def generate_cheat_sheet(ports, target, port_rules, service_rules, sanitize=False):
    """Generate a cheat sheet for each open port based on config rules."""
    cheat_sheets = {}
    
    for port in ports:
        port_id = port["port"]
        service = port["service"]
        version = port["version"]
        
        cheat_sheets[port_id] = {
            "service": service,
            "version": version,
            "tools": [],
            "commands": [],
            "resources": []
        }
        
        if port_id in port_rules:
            rules = port_rules[port_id]
            cheat_sheets[port_id]["tools"] = rules["tools"]
            cheat_sheets[port_id]["commands"] = [
                cmd.format(target=target) for cmd in rules["commands"]
            ]
            cheat_sheets[port_id]["resources"] = [
                r.format(service=service, version=version) for r in rules["resources"]
            ]
        elif service in service_rules:
            rules = service_rules[service]
            cheat_sheets[port_id]["tools"] = rules["tools"]
            cheat_sheets[port_id]["commands"] = [
                cmd.format(target=target, port=port_id) for cmd in rules["commands"]
            ]
            cheat_sheets[port_id]["resources"] = [
                r.format(service=service, version=version, port=port_id) for r in rules["resources"]
            ]
        elif service == "unknown" and "unknown" in service_rules:
            rules = service_rules["unknown"]
            cheat_sheets[port_id]["tools"] = rules["tools"]
            cheat_sheets[port_id]["commands"] = [
                cmd.format(target=target, port=port_id) for cmd in rules["commands"]
            ]
            cheat_sheets[port_id]["resources"] = [
                r.format(service=service, version=version, port=port_id) for r in rules["resources"]
            ]
        
        if sanitize:
            cheat_sheets[port_id]["commands"] = [sanitize_text(cmd) for cmd in cheat_sheets[port_id]["commands"]]
            cheat_sheets[port_id]["resources"] = [sanitize_text(r) for r in cheat_sheets[port_id]["resources"]]
    
    return cheat_sheets

def save_cheat_sheet(cheat_sheets, target, output_format="markdown", filename="cheat_sheet.md", sanitize=False, name=None):
    """Save cheat sheets in the specified format with a dynamic title."""
    if output_format == "json":
        with open(filename.replace(".md", ".json"), "w") as f:
            json.dump(cheat_sheets, f, indent=4)
        return
    
    title = "# Recon Cheat Sheet"
    if sanitize:
        if not name:
            raise ValueError("A --name parameter is required when --sanitize is used.")
        title += f" - {name}"
    else:
        title += f" - {target}"
    
    with open(filename, "w") as f:
        f.write(f"{title}\n\n")
        for port, sheet in cheat_sheets.items():
            f.write(f"## Port {port} ({sheet['service']} {sheet['version']})\n")
            f.write("### Tools\n")
            for tool in sheet["tools"]:
                f.write(f"- {tool}\n")
            f.write("\n### Commands\n")
            for cmd in sheet["commands"]:
                f.write(f"- `{cmd}`\n")
            f.write("\n### Resources\n")
            for resource in sheet["resources"]:
                f.write(f"- {resource}\n")
            f.write("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate port-specific recon cheat sheets from Nmap XML.")
    parser.add_argument("nmap_file", help="Path to Nmap XML output file")
    parser.add_argument("--target", help="Target IP or hostname (optional, defaults to IP from scan)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--sanitize", action="store_true", help="Sanitize IPs and hostnames in output")
    parser.add_argument("--output", default="cheat_sheet", help="Base name for output file (e.g., 'lab1' → 'lab1.md')")
    parser.add_argument("--name", help="Name for sanitized output title (required if --sanitize is used)")
    args = parser.parse_args()
    
    port_rules = load_config("port_rules.json")
    service_rules = load_config("service_rules.json")
    
    print_logo()
    parsed_target, ports = parse_nmap(args.nmap_file)
    target = args.target if args.target else parsed_target
    if not target:
        raise ValueError("No target specified and none found in Nmap XML!")
    
    cheat_sheets = generate_cheat_sheet(ports, target, port_rules, service_rules, sanitize=args.sanitize)
    filename = f"{args.output}.md" if args.format == "markdown" else f"{args.output}.json"
    save_cheat_sheet(cheat_sheets, target, output_format=args.format, filename=filename, sanitize=args.sanitize, name=args.name)
