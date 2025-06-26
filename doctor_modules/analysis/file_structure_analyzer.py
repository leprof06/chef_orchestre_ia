import os
import ast
import json
from pathlib import Path

ANALYSIS_OUTPUT = Path("rapports/filemap")
ANALYSIS_OUTPUT.mkdir(parents=True, exist_ok=True)

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


def analyser_dossier_projet(racine_projet):
    resume_projet = []

    for root, _, files in os.walk(racine_projet):
        if any(x in root for x in ["venv", "node_modules", "__pycache__", ".git"]):
            continue

        for file in files:
            if file.endswith(EXTENSIONS_CIBLES):
                chemin = os.path.join(root, file)
                analyse = analyser_fichier(chemin)
                resume_projet.append(analyse)

                nom_base = os.path.basename(file).replace(".py", "").replace(".html", "").replace(".js", "").replace(".jsx", "")
                sortie = ANALYSIS_OUTPUT / f"{nom_base}.json"
                with open(sortie, "w", encoding="utf-8") as f:
                    json.dump(analyse, f, indent=2, ensure_ascii=False)

                print(f"✅ Analyse sauvegardée : {sortie}")

    # 🔄 Génération d'un fichier résumé global pour le projet entier
    nom_projet = Path(racine_projet).name.lower().replace(" ", "_")
    global_json_path = ANALYSIS_OUTPUT / f"structure_{nom_projet}.json"
    with open(global_json_path, "w", encoding="utf-8") as f:
        json.dump(resume_projet, f, indent=2, ensure_ascii=False)
    print(f"📦 Résumé global du projet enregistré : {global_json_path}")


if __name__ == "__main__":
    projet = input("Dossier du projet à analyser : ")
    if os.path.isdir(projet):
        analyser_dossier_projet(projet)
    else:
        print("❌ Dossier introuvable.")
