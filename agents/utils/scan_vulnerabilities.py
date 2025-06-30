import os
import ast
import json

def scan_python_vuln(project_path):
    """
    Scan basique : cherche des patterns risqués dans du code Python (ex : eval, exec, os.system, etc.)
    Retourne {fichier: [pattern]} pour chaque occurence.
    """
    RISKY = ("eval(", "exec(", "os.system", "subprocess.", "input(")
    found = {}
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                    matches = [r for r in RISKY if r in content]
                    if matches:
                        found[path] = matches
                except Exception:
                    continue
    return found

def scan_node_vuln(project_path):
    """
    Scan ultra simple : cherche 'child_process', 'eval', 'require(' dans les .js
    """
    RISKY = ("child_process", "eval(", "require(")
    found = {}
    for root, _, files in os.walk(project_path):
        for f in files:
            if f.endswith('.js'):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                    matches = [r for r in RISKY if r in content]
                    if matches:
                        found[path] = matches
                except Exception:
                    continue
    return found
