import os
import subprocess
import sys
from analysis.utils import log_errors  # si tu as déjà une fonction de log

def install_package(package):
    """
    Cette fonction installe le paquet Python donné.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except subprocess.CalledProcessError as e:
        log_errors("Error", f"An error occurred while installing {package}: {e}", package)
        
def log_errors(err_type, err_msg=None, package=None):
    """
    Function to log errors
    """
    if err_type == "ImportError":
        print(f"📦 Installation de {package}...")
    elif err_type == "CalledProcessError":
        print(f"❌ Echec de l'installation du package : {package}. Vérifiez votre connexion Internet et réessayez.")

def check_and_install_packages(*packages):
    """
    Installe les packages manquants et les ajoute à requirements.txt si nécessaire.
    """
    requirements_path = os.path.join(os.getcwd(), "requirements.txt")

    # Charger les packages déjà enregistrés (s'il existe)
    existing = set()
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            existing = set(line.strip().split("==")[0] for line in f if line.strip())

    for package in packages:
        try:
            __import__(package)
        except ImportError:
            log_errors("ImportError", None, package)
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
            except subprocess.CalledProcessError:
                log_errors("CalledProcessError", None, package)

            # Ajouter à requirements.txt si absent
            if package not in existing:
                with open(requirements_path, "a", encoding="utf-8") as f:
                    f.write(f"{package}\n")
                    