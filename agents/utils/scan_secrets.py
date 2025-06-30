import re
import os

def get_default_key_patterns():
    """
    Retourne la liste complète de patterns de clés API à détecter (OpenAI, GitHub, HF, Google, générique...)
    """
    return [
        r"(sk-\w{20,})",                # OpenAI
        r"(hf_\w{16,})",                # HuggingFace
        r"(ghp_[A-Za-z0-9]{36})",       # GitHub PAT
        r"(AIza[0-9A-Za-z-_]{35})",     # Google API
        r"(?i)api[_-]?key\s*[:=]\s*['\"]?([A-Za-z0-9\-_=]{16,})" # Générique
    ]

def scan_for_secrets(content, key_patterns=None):
    """
    Cherche la présence de clés/secret/API dans le texte fourni.
    Retourne une liste de tuples (pattern, match).
    """
    if key_patterns is None:
        key_patterns = get_default_key_patterns()
    found = []
    for pattern in key_patterns:
        for match in re.findall(pattern, content):
            found.append((pattern, match))
    return found

def scan_file_for_secrets(filepath, key_patterns=None):
    """
    Ouvre un fichier texte et applique scan_for_secrets sur son contenu.
    """
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return scan_for_secrets(content, key_patterns=key_patterns)
    except Exception as e:
        return [("error", f"Impossible de scanner {filepath}: {e}")]

def scan_folder_for_secrets(folder, exts=(".py", ".js", ".env", ".json", ".yml", ".yaml"), key_patterns=None):
    """
    Scanne récursivement un dossier à la recherche de secrets dans tous les fichiers d'extension concernée.
    Retourne un dict {fichier: [(pattern, match)]}
    """
    all_found = {}
    if not folder or not os.path.isdir(folder):
        return {"error": "Chemin dossier invalide."}
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(exts):
                path = os.path.join(root, f)
                found = scan_file_for_secrets(path, key_patterns)
                if found:
                    all_found[path] = found
    return all_found
