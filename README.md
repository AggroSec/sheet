SHEET - Security Hacking Enumeration and Exploitation Tool

Cheatsheet for the Offensive Edge

SHEET (Security Hacking Enumeration and Exploitation Tool) is a pentesting cheatsheet generator built to accelerate reconnaissance and enumeration during CTFs, pentests, or security assessments. It maps ports and services to actionable commands and resources, powered by Hacktricks. Perfect for Nmap scans or quick reference when you need to strike fast.
Features

    Port Rules: 100 common ports with services, tools, commands, and Hacktricks links.
    Service Rules: 167 unique services with pentesting details.
    Config-Driven: Customize via port_rules.json and service_rules.json.
    Obsidian Bonus: Unofficial plugin to paste and collapse cheatsheets (see Extras).

Installation

    Clone the repo:
    git clone https://github.com/AggroSec/sheet.git
    cd sheet
    (Add a code block flair here for the commands if you want!)
    Ensure Python 3.x is installed.
    Use the included config files:
        port_rules.json
        service_rules.json

Usage

    Generate a cheatsheet from an Nmap scan:
    python sheet.py -i nmap_output.xml -o sheet.md
    (Add a code block flair here for the command!)
    Edit port_rules.json or service_rules.json to suit your needs.
    Open sheet.md in a Markdown viewer (Obsidian recommended!).

Config Files

    port_rules.json: Maps ports to services and tools.
    service_rules.json: Details 167 services with Hacktricks links.

Example port_rules.json entry:

"21": {

"service": "ftp",

"tools": ["ftp", "hydra"],

"commands": ["ftp {target}", "hydra -l anonymous -P passwords.txt ftp://{target}"],

"resources": ["https://book.hacktricks.wiki/en/network-services-pentesting/pentesting-ftp/index.html"]

}

(Add a code block flair around the JSON if you’d like!)
Extras

    Obsidian Plugin: The extras/sheet-collapse-plugin/ folder includes an unofficial plugin to paste your SHEET cheatsheet into Obsidian with all headings collapsed. See the README in that folder for installation and usage details.
    Disclaimer: This is an unofficial plugin, not endorsed by Obsidian. Review main.js before use—run at your own risk!

Contributing

    Add ports/services to the JSON files and submit a PR.
    Got ideas? Open an issue—let’s talk!

To-Do

    Integrate CVE lookups.
    Support more scan types.
    Maybe a GUI later?

Credits

    Built by AggroSec, with Grok (xAI) as co-pilot.
    Inspired by Hacktricks.

License

MIT License—hack, tweak, and share freely!
