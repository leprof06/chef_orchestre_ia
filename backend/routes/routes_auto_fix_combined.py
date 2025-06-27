import os
import logging
from flask import Blueprint, render_template, request, session, redirect, url_for
from orchestrator import PROJECT_FOLDER
from routes.routes import application_data
from core.history_manager import save_proposal
from core.services import generate_code_proposal

routes_auto_fix_combined = Blueprint("auto_fix_combined", __name__)

@routes_auto_fix_combined.route("/auto_fix_combined", methods=["GET", "POST"])
def auto_fix_combined():
    selected_project = session.get("selected_auto_fix_project")
    proposals = {}

    if request.method == "POST":
        selected_project = request.form.get("project")
        if selected_project:
            session["selected_auto_fix_project"] = selected_project

    if selected_project:
        project_path = os.path.join(PROJECT_FOLDER, selected_project)
        todo_path = os.path.join(project_path, "todo.md")
        code_blobs = []
        todo_content = ""

        # 📝 Lecture du todo.md
        if os.path.exists(todo_path):
            with open(todo_path, "r", encoding="utf-8") as f:
                todo_content = f.read()

        # 📂 Analyse des fichiers du projet
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith((".py", ".js", ".jsx", ".html")):
                    full_path = os.path.join(root, file)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            code_blobs.append(f"# 📁 {file}\n{content}")
                    except Exception as e:
                        logging.warning(f"❌ Erreur lecture {file} : {e}")

        # 🧠 Création du super prompt combiné
        prompt = (
            "Voici les problèmes listés dans le fichier todo.md :\n"
            f"{todo_content}\n\n"
            "Voici l'intégralité du code du projet analysé :\n"
            f"{chr(10).join(code_blobs)}\n\n"
            "➡️ Génére un plan d’action clair :\n"
            "- Associe chaque bug à un fichier ou fonction\n"
            "- Propose les corrections concrètes\n"
            "- Donne les extraits de code à modifier si possible\n"
            "- Ne reformule pas, corrige."
        )

        try:
            filename = "todo+code.md"
            if len(prompt) < 5000:
                proposal = generate_code_proposal(prompt, filename)
            else:
                proposal = get_best_model_response(prompt)

            application_data["latest_proposal"] = proposal
            application_data["selected_file"] = filename
            save_proposal(filename, prompt, proposal, accepted=False)
            proposals[filename] = proposal
        except Exception as e:
            proposals["Erreur"] = f"❌ Erreur lors de la génération : {e}"

    try:
        project_list = [d for d in os.listdir(PROJECT_FOLDER) if os.path.isdir(os.path.join(PROJECT_FOLDER, d))]
    except Exception as e:
        project_list = []
        logging.error(f"Erreur de lecture des projets : {e}")

    return render_template("auto_fix_combined_summary.html",
                           proposals=proposals,
                           selected_project=selected_project,
                           project_list=project_list)

@routes_auto_fix_combined.route("/apply_combined_fix", methods=["POST"])
def apply_combined_fix():
    selected_project = session.get("selected_auto_fix_project")
    if not selected_project:
        return "❌ Aucun projet sélectionné."

    project_path = os.path.join(PROJECT_FOLDER, selected_project)
    log_path = os.path.join(project_path, "todo_combined_log.md")

    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n# 🔧 Correction IA combinée appliquée :\n{application_data['latest_proposal']}\n")
        return redirect(url_for("auto_fix_combined.auto_fix_combined"))
    except Exception as e:
        return f"❌ Erreur d'application : {e}"
