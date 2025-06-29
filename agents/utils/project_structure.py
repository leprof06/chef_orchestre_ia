# agents/utils/project_structure.py

import os
import ast
import json
from pathlib import Path

EXTENSIONS_CIBLES = (".py", ".html", ".js", ".jsx")

def analyser_fichier(path):
    resultat = {
        "filename": os.path.basename(path),
        "filepath": str(path),
        "functions": [],
        "classes": [],
        "routes": [],
        "type": "",
        "description": ""
    }

    if path.endswith(".py"):
        try:
            with open(path, encoding="utf-8") as f:
                contenu = f.read()
                arbre = ast.parse(contenu)

            for noeud in arbre.body:
                if isinstance(noeud, ast.FunctionDef):
                    resultat["functions"].append(noeud.name)
                    for deco in noeud.decorator_list:
                        if isinstance(deco, ast.Call) and hasattr(deco.func, 'attr'):
                            if deco.func.attr == "route":
                                for arg in deco.args:
                                    if isinstance(arg, ast.Str):
                                        resultat["routes"].append(arg.s)
                elif isinstance(noeud, ast.ClassDef):
                    resultat["classes"].append(noeud.name)

            if "Blueprint" in contenu or "@app.route" in contenu:
                resultat["type"] = "flask_blueprint"
                resultat["description"] = "Fichier Flask : contient des routes backend."
            elif "def" in contenu:
                resultat["type"] = "python_module"
                resultat["description"] = "Module Python standard."
        except Exception as e:
            resultat["description"] = f"❌ Erreur analyse Python : {e}"

    elif path.endswith(".html"):
        resultat["type"] = "html_template"
        resultat["description"] = "Template HTML utilisé côté frontend."

    elif path.endswith(".js") or path.endswith(".jsx"):
        resultat["type"] = "frontend_component"
        resultat["description"] = "Composant JS ou React."

    return resultat

def analyse_structure_globale(folder):
    structure = {
        "root_files": [],
        "main_scripts": [],
        "test_dirs": [],
        "data_dirs": [],
        "suspicious_files": []
    }
    for root, dirs, files in os.walk(folder):
        for f in files:
            path = os.path.relpath(os.path.join(root, f), folder)
            if root == folder:
                structure["root_files"].append(f)
            if f.startswith("test_") or "test" in root.lower():
                structure["test_dirs"].append(path)
            if f.endswith((".csv", ".db", ".xlsx", ".json")):
                structure["data_dirs"].append(path)
            if f.lower() in ["secrets.py", ".env", "config.old"]:
                structure["suspicious_files"].append(path)
            if f == "main.py" or f == "app.py":
                structure["main_scripts"].append(path)
    return structure

def analyser_structure_projet(racine_projet, rapport_dir=None):
    """
    Retourne à la fois le résumé global et les analyses détaillées fichier par fichier.
    """
    resume_projet = []
    for root, _, files in os.walk(racine_projet):
        if any(x in root for x in ["venv", "node_modules", "__pycache__", ".git"]):
            continue
        for file in files:
            if file.endswith(EXTENSIONS_CIBLES):
                chemin = os.path.join(root, file)
                analyse = analyser_fichier(chemin)
                resume_projet.append(analyse)
                if rapport_dir:
                    rapport_dir = Path(rapport_dir)
                    rapport_dir.mkdir(parents=True, exist_ok=True)
                    nom_base = os.path.basename(file).split('.')[0]
                    sortie = rapport_dir / f"{nom_base}.json"
                    with open(sortie, "w", encoding="utf-8") as f:
                        json.dump(analyse, f, indent=2, ensure_ascii=False)

    structure = analyse_structure_globale(racine_projet)
    return {
        "structure_summary": structure,
        "detailed_files": resume_projet
    }
