import json

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
