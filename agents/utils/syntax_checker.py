import ast
import json
import os

# --- PYTHON ---
def check_python_syntax(filepath):
    """
    Vérifie la syntaxe d'un fichier Python.
    Retourne True si syntaxe OK, sinon message d'erreur.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        ast.parse(source)
        return True
    except Exception as e:
        return f"Erreur syntaxe Python: {e}"

# --- JSON ---
def check_json_syntax(filepath):
    """
    Vérifie la syntaxe d'un fichier JSON.
    Retourne True si syntaxe OK, sinon message d'erreur.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except Exception as e:
        return f"Erreur syntaxe JSON: {e}"

# --- JS (binaire simple, pas d'analyse AST) ---
def check_js_syntax(filepath):
    """
    Vérifie rapidement la syntaxe d'un fichier JS (brut, via try/except exec si dispo, sinon basique).
    Retourne True si syntaxe OK, sinon message d'erreur.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        compile(source, filepath, "exec")  # ATTENTION : ça ne gère pas JS réel, mais détecte fichier non-Python !
        return True
    except Exception as e:
        return f"Erreur syntaxe JS (test basique, à améliorer) : {e}"

# --- HTML ---
def check_html_syntax(filepath):
    """
    Vérifie la structure d'un fichier HTML (recherche basique de balises fermées, peut être amélioré).
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            html = f.read()
        # Simple test : balise <html> et </html>
        if '<html' in html.lower() and '</html>' in html.lower():
            return True
        return "Fichier HTML incomplet"
    except Exception as e:
        return f"Erreur lecture HTML: {e}"

# --- SCAN DOSSIER (multi-langage) ---
def analyze_folder_for_syntax(folder, extensions=(".py", ".json", ".js", ".html")):
    """
    Analyse récursivement un dossier, vérifie la syntaxe de tous les fichiers supportés.
    Retourne un dict {fichier: result}.
    """
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
