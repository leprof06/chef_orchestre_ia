import os

def is_code_file(filename):
    """Retourne True si le fichier est un fichier code reconnu (par extension)."""
    extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs']
    return any(filename.endswith(ext) for ext in extensions)

def extract_code_structure(file_path):
    """
    Extrait la structure d’un fichier code.
    Pour simplifier, cette version retourne juste les noms de fonctions et de classes Python.
    """
    structure = {"functions": [], "classes": []}
    if not file_path.endswith(".py") or not os.path.isfile(file_path):
        return structure

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("def "):
                structure["functions"].append(line.split("(")[0][4:])
            elif line.startswith("class "):
                structure["classes"].append(line.split("(")[0][6:].strip(":"))

    return structure
