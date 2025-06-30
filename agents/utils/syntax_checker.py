# agents/utils/syntax_checker.py

import ast
import json
import os

def check_python_syntax(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        return True
    except Exception as e:
        return f"Erreur syntaxe Python: {e}"

def check_json_syntax(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except Exception as e:
        return f"Erreur syntaxe JSON: {e}"

def check_js_syntax(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        compile(source, filepath, "exec")  # ATTENTION : pas de JS réel !
        return True
    except Exception as e:
        return f"Erreur syntaxe JS (test basique): {e}"

def check_html_syntax(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        if '<html' in html.lower() and '</html>' in html.lower():
            return True
        return "Fichier HTML incomplet"
    except Exception as e:
        return f"Erreur lecture HTML: {e}"

def analyze_folder_for_syntax(folder, extensions=(".py", ".json", ".js", ".html")):
    results = {}
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            if f.endswith(extensions):
                if f.endswith(".py"):
                    results[path] = check_python_syntax(path)
                elif f.endswith(".json"):
                    results[path] = check_json_syntax(path)
                elif f.endswith(".js"):
                    results[path] = check_js_syntax(path)
                elif f.endswith(".html"):
                    results[path] = check_html_syntax(path)
    return results
