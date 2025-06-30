import os
import json

def parse_requirements(project_path):
    """
    Parse requirements.txt et retourne la liste des packages.
    """
    req_path = os.path.join(project_path, "requirements.txt")
    if not os.path.isfile(req_path):
        return []
    with open(req_path) as f:
        return [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]

def parse_package_json(project_path):
    """
    Parse package.json et retourne les dépendances (npm/yarn).
    """
    pkg_path = os.path.join(project_path, "package.json")
    if not os.path.isfile(pkg_path):
        return {}
    with open(pkg_path) as f:
        data = json.load(f)
    return data.get("dependencies", {})
