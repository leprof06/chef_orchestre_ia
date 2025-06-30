import os

def should_analyze_file(filepath):
    """
    Détermine si un fichier doit être analysé (évite binaires, images, etc).
    """
    IGNORE_EXT = ('.png', '.jpg', '.jpeg', '.exe', '.dll', '.so', '.bin')
    return not filepath.endswith(IGNORE_EXT)

def detect_capabilities(folder):
    """
    Essaie de deviner quelques capacités du projet en lisant les fichiers clés.
    Ex : présence de requirements.txt, tests, docs, notebook, etc.
    """
    caps = {}
    for root, _, files in os.walk(folder):
        for f in files:
            if f == "requirements.txt":
                caps["python_dependencies"] = True
            if f == "package.json":
                caps["node_project"] = True
            if f.endswith(".ipynb"):
                caps["jupyter"] = True
            if f.startswith("test_") or f.endswith("_test.py"):
                caps["tests"] = True
            if f in ("README.md", "README.rst"):
                caps["docs"] = True
    return caps
