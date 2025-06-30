import ast
import os

def extract_docstrings(filepath):
    """
    Extrait tous les docstrings d’un fichier Python (module, classes, fonctions).
    Retourne un dict par type.
    """
    if not filepath.endswith('.py'):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source)
        docstrings = {
            "module": ast.get_docstring(tree),
            "classes": {},
            "functions": {}
        }
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                docstrings["classes"][node.name] = ast.get_docstring(node)
                for sub in node.body:
                    if isinstance(sub, ast.FunctionDef):
                        key = f"{node.name}.{sub.name}"
                        docstrings["functions"][key] = ast.get_docstring(sub)
            elif isinstance(node, ast.FunctionDef):
                docstrings["functions"][node.name] = ast.get_docstring(node)
        return docstrings
    except Exception as e:
        return {"error": str(e)}
