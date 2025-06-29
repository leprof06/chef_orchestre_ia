# agents/utils/requirements_parser.py

import os
import json

def parse_requirements(folder):
    reqs = set()
    for root, _, files in os.walk(folder):
        for f in files:
            if f == "requirements.txt":
                with open(os.path.join(root, f), encoding="utf-8") as file:
                    for l in file:
                        l = l.strip()
                        if l and not l.startswith("#"):
                            reqs.add(l)
    return sorted(reqs)

def parse_package_json(folder):
    pkgs = set()
    for root, _, files in os.walk(folder):
        for f in files:
            if f == "package.json":
                try:
                    with open(os.path.join(root, f), encoding="utf-8") as file:
                        data = json.load(file)
                        pkgs |= set(data.get("dependencies", {}).keys())
                        pkgs |= set(data.get("devDependencies", {}).keys())
                except Exception:
                    pass
    return sorted(pkgs)
