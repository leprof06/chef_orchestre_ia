import json
import os

def load_json_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"❌ Erreur de lecture JSON : {e}")
        return []

def save_json_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError as e:
        print(f"❌ Erreur d'écriture JSON : {e}")

def log_errors(err_type, err_msg=None, package=None):
    """
    Function to log errors
    """
    if err_type == "ImportError":
        print(f"📦 Installation de {package}...")
    elif err_type == "CalledProcessError":
        print(f"❌ Échec de l'installation du package : {package}. Vérifiez votre connexion Internet et réessayez.")
    elif err_type == "Other":
        print(f"⚠️ Erreur : {err_msg}")

def is_code_file(file_path):
    """Détermine si un fichier est un fichier de code source."""
    code_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.cs', '.go', '.rb']
    _, ext = os.path.splitext(file_path)
    return ext in code_extensions

def extract_code_structure(file_path):
    """Extrait une structure simple d’un fichier de code sous forme de texte brut."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return {
            "file": file_path,
            "lines": lines[:20]  # Renvoie les 20 premières lignes à titre d'exemple
        }
    except Exception as e:
        return {
            "file": file_path,
            "error": str(e)
        }