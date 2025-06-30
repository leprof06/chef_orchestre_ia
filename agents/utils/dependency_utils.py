import os
import subprocess

def detect_missing_python_dependencies(project_path):
    """
    Scan requirements.txt et retourne la liste des packages manquants.
    """
    req_path = os.path.join(project_path, "requirements.txt")
    if not os.path.isfile(req_path):
        return []
    with open(req_path) as f:
        requirements = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
    import pkg_resources
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [r for r in requirements if r.split("==")[0].lower() not in installed]
    return missing

def is_package_installed(package_name):
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def detect_and_install_dependencies(project_path):
    """
    Détecte les dépendances manquantes et tente de les installer automatiquement.
    """
    missing = detect_missing_python_dependencies(project_path)
    if not missing:
        return {"installed": True, "missing": []}
    try:
        subprocess.check_call(["pip", "install"] + missing)
        return {"installed": True, "missing": []}
    except Exception as e:
        return {"installed": False, "missing": missing, "error": str(e)}
