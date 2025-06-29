# agents/utils/scan_vulnerabilities.py

import subprocess

def scan_python_vuln(requirements_path="requirements.txt"):
    try:
        res = subprocess.run(
            ["safety", "check", "-r", requirements_path, "--full-report"],
            capture_output=True, text=True, timeout=30
        )
        return res.stdout
    except Exception as e:
        return f"Erreur Safety : {e}"

def scan_node_vuln(folder):
    try:
        res = subprocess.run(
            ["npm", "audit", "--json"], cwd=folder,
            capture_output=True, text=True, timeout=30
        )
        return res.stdout
    except Exception as e:
        return f"Erreur npm audit : {e}"
