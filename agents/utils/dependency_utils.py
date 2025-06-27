import os
import subprocess
from pathlib import Path

def detect_missing_python_dependencies(project_path):
    req_path = Path(project_path) / "requirements.txt"
    missing = []
    if req_path.exists():
        with open(req_path, encoding="utf-8") as f:
            for line in f:
                package = line.strip().split("==")[0]
                if not is_package_installed(package):
                    missing.append(package)
    return missing

def is_package_installed(package):
    try:
        subprocess.check_output(["python", "-c", f"import {package}"], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except ModuleNotFoundError:
        return False

def install_python_packages(packages):
    for package in packages:
        print(f"📦 Installation de {package}...")
        subprocess.call(["pip", "install", package])

def detect_and_install_dependencies(project_path):
    missing = detect_missing_python_dependencies(project_path)
    if missing:
        print("🚨 Dépendances manquantes détectées :", ", ".join(missing))
        install_python_packages(missing)
    else:
        print("✅ Toutes les dépendances Python sont présentes.")
