import os
import logging
from flask import Blueprint, render_template, request, redirect, url_for, session
from orchestrator import PROJECT_FOLDER
from routes.routes import application_data
from core.history_manager import save_proposal
from core.services import generate_code_proposal

routes_auto_fix = Blueprint("auto_fix", __name__)

@routes_auto_fix.route("/auto_fix", methods=["GET", "POST"])
def auto_fix():
    proposals = {}
    selected_project = session.get("selected_auto_fix_project")

    if request.method == "POST":
        selected_project = request.form.get("project")
        session["selected_auto_fix_project"] = selected_project

    if selected_project:
        project_path = os.path.join(PROJECT_FOLDER, selected_project)
        selected_file = session.get("selected_file")

        if selected_file:
            full_path = os.path.join(project_path, selected_file)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()

                prompt = (
                    f"Voici le fichier {selected_file} extrait du projet :\n\n"
                    f"{code}\n\n➡️ Propose les améliorations nécessaires : structure, bugs, style, performance."
                )

                filename = f"{selected_project.replace('/', '_')}_autofix_{selected_file}"
                if not session.get("code_proposal_already_generated"):
                    session["code_proposal_already_generated"] = True
                    proposal = generate_code_proposal(prompt, selected_file)
                else:
                    logging.info("⛔ Proposition déjà générée, on ne relance pas.")
                    proposal = "✅ Proposition déjà générée."

                application_data["latest_proposal"] = proposal
                application_data["selected_file"] = selected_file
                save_proposal(filename, prompt, proposal, accepted=False)
                proposals[filename] = proposal

            except Exception as e:
                proposals["Erreur"] = f"❌ Erreur lecture fichier : {e}"

    try:
        project_list = [d for d in os.listdir(PROJECT_FOLDER) if os.path.isdir(os.path.join(PROJECT_FOLDER, d))]
    except Exception as e:
        project_list = []
        logging.error(f"Erreur de lecture des projets : {e}")

    return render_template("auto_fix.html",
                           proposals=proposals,
                           selected_project=selected_project,
                           project_list=project_list)

@routes_auto_fix.route("/auto_fix_from_readme", methods=["GET", "POST"])
def auto_fix_from_readme():
    selected_project = session.get("selected_auto_fix_project")
    proposals = {}

    if request.method == "POST":
        selected_project = request.form.get("project")
        if selected_project:
            session["selected_auto_fix_project"] = selected_project

    if selected_project:
        project_path = os.path.join(PROJECT_FOLDER, selected_project)
        readme_paths = [
            os.path.join(project_path, "todo.md"),
            os.path.join(project_path, "README_PROJECT.md"),
            os.path.join(project_path, "README.md"),
            os.path.join(project_path, "README_AUTEUR.md")
        ]

        try:
            readme_content = ""
            used_file = None
            for path in readme_paths:
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f:
                        readme_content = f.read()
                        used_file = os.path.basename(path)
                        break

            if readme_content.strip():
                logging.info("📖 Fichier de TODO détecté. Génération de proposition IA...")

                prompt = (
                    "Ce fichier liste des bugs connus et des améliorations souhaitées.\n"
                    "Pour chaque ligne, propose une correction technique claire :\n"
                    "- Quels fichiers ou fonctions sont concernés\n"
                    "- Quel code ou stratégie utiliser\n"
                    "- Ne reformule pas. Corrige.\n\n"
                    + readme_content
                )

                proposal = generate_code_proposal(prompt, used_file or "todo.md")
                application_data["latest_proposal"] = proposal
                application_data["selected_file"] = used_file or "todo.md"
                save_proposal(used_file or "todo.md", readme_content, proposal, accepted=False)
                proposals[used_file or "todo.md"] = proposal
            else:
                proposals["README"] = "❌ Aucun contenu détecté dans les fichiers TODO ou README."

        except Exception as e:
            proposals["README"] = f"❌ Erreur lors de la lecture : {e}"

    try:
        project_list = [d for d in os.listdir(PROJECT_FOLDER) if os.path.isdir(os.path.join(PROJECT_FOLDER, d))]
    except Exception as e:
        project_list = []
        logging.error(f"Erreur de lecture des projets : {e}")

    return render_template("auto_fix_summary.html",
                           proposals=proposals,
                           selected_project=selected_project,
                           project_list=project_list)

@routes_auto_fix.route("/apply_auto_fix", methods=["POST"])
def apply_auto_fix():
    selected_project = session.get("selected_auto_fix_project")
    if not selected_project:
        return "❌ Aucun projet sélectionné."

    project_path = os.path.join(PROJECT_FOLDER, selected_project)
    todo_path = os.path.join(project_path, "todo.md")
    if not os.path.exists(todo_path):
        todo_path = os.path.join(project_path, "README_PROJECT.md")

    try:
        with open(todo_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n# 🔧 Suggestion IA appliquée :\n{application_data['latest_proposal']}\n")
        return redirect(url_for("auto_fix.auto_fix_from_readme"))
    except Exception as e:
        return f"❌ Erreur d'application : {e}"
