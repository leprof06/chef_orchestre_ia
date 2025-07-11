import os

def read_file_safe(path, max_bytes=10*1024*1024):
    """
    Lecture sécurisée : retourne le contenu d’un fichier texte jusqu'à max_bytes (ou message d’erreur).
    """
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = f.read(max_bytes)
        return data
    except Exception as e:
        return f"Erreur de lecture {path}: {e}"

def write_file_safe(path, content):
    """
    Écriture sécurisée : écrit du contenu dans un fichier (texte).
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        return f"Erreur d’écriture {path}: {e}"

def list_files_recursive(folder, extensions=None, max_files=5000):
    """
    Liste récursivement tous les fichiers du dossier, avec un filtre d’extensions et un max de fichiers.
    """
    all_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            if not extensions or f.endswith(tuple(extensions)):
                all_files.append(os.path.join(root, f))
                if len(all_files) > max_files:
                    return all_files
    return all_files
