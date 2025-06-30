import os

def is_code_file(filepath, extensions=(".py", ".js", ".ts", ".java", ".cpp", ".c", ".go")):
    """
    Détecte si un fichier est un fichier code source connu.
    """
    return filepath.endswith(extensions)

def extract_code_structure(filepath):
    """
    Extrait rapidement la structure d’un fichier code (Python ou autre : nom, taille, extension)
    """
    try:
        size = os.path.getsize(filepath)
        name = os.path.basename(filepath)
        ext = os.path.splitext(filepath)[-1]
        return {"filename": name, "extension": ext, "size": size}
    except Exception as e:
        return {"error": str(e)}
