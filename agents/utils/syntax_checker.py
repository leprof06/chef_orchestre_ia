# agents/utils/syntax_checker.py

import ast
import json
import os

def check_python_syntax(code):
    try:
        ast.parse(code)
        return None
    except Exception as e:
        return str(e)

def check_json_syntax(code):
    try:
        json.loads(code)
        return None
    except Exception as e:
        return str(e)

def check_js_syntax(code):
    # Très basique, tu peux intégrer esprima si tu veux aller plus loin
    if "function" not in code and "=>" not in code:
        return "Aucune fonction JS détectée (test basique)."
    return None

def check_html_syntax(code):
    # Basique : vérifie balises de base
    if "<html" not in code.lower():
        return "Pas de balise <html> détectée."
    if "<body" not in code.lower():
        return "Pas de balise <body> détectée."
    return None

def analyze_folder_for_syntax(folder):
    errors = {}
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    code = file.read()
                if f.endswith(".py"):
                    err = check_python_syntax(code)
                elif f.endswith(".json"):
                    err = check_json_syntax(code)
                elif f.endswith(".js"):
                    err = check_js_syntax(code)
                elif f.endswith(".html"):
                    err = check_html_syntax(code)
                else:
                    err = None
                if err:
                    errors[path] = err
            except Exception as e:
                errors[path] = f"Erreur de lecture : {e}"
    return errors
