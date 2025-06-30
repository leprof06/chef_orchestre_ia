import os
import ast

def analyser_fichier(filepath):
    """
    Analyse un fichier Python pour en extraire la structure : classes, fonctions, imports.
    Retourne un dict ou False si non Python.
    """
    if not filepath.endswith('.py'):
        return False
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        structure = {
            "classes": [node.name for node in tree.body if isinstance(node, ast.ClassDef)],
            "functions": [node.name for node in tree.body if isinstance(node, ast.FunctionDef)],
            "imports": [node.names[0].name for node in tree.body if isinstance(node, ast.Import)],
        }
        return structure
    except Exception as e:
        return {"error": str(e)}

def analyse_structure_globale(folder):
    """
    Analyse récursivement la structure d’un dossier projet (Python).
    Retourne {fichier : structure} pour chaque .py trouvé.
    """
    resultat = {}
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                resultat[path] = analyser_fichier(path)
    return resultat
