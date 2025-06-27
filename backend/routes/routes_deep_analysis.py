import os
import logging
from flask import Blueprint, render_template, request, session
from orchestrator import PROJECT_FOLDER
from core.services import generate_code_proposal
from core.history_manager import save_proposal
from generation.init_readme_sync import get_readme_insight

routes_deep_analysis = Blueprint("deep_analysis", __name__)

def find_projects_recursively(root_folder):
    projects = []
    for root, dirs, _ in os.walk(root_folder):
        for d in dirs:
            full_path = os.path.join(root, d)
            try:
                if any(f.endswith((".py", ".js", ".html")) for f in os.listdir(full_path)):
                    rel_path = os.path.relpath(full_path, root_folder)
                    projects.append(rel_path)
            except Exception:
                continue
        break  # Ne pas descendre trop profondément
    return sorted(projects)

@routes_deep_analysis.route("/deep_analysis", methods=["GET", "POST"]) 
def deep_analysis():
    proposals = {}
    selected_project = session.get("selected_deep_project")

    if request.method == "POST":
        selected_project = request.form.get("project")
        session["selected_deep_project"] = selected_project

    if selected_project:
        project_path = os.path.join(PROJECT_FOLDER, selected_project)
        prompt_parts = []
        cache_fichier = []
        cache_resumés = []

        for root, dirs, files in os.walk(project_path):
            if any(x in root for x in ["node_modules", "venv", "__pycache__", ".git"]):
                continue

            for file in files:
                if file.endswith((".py", ".js", ".jsx", ".html")):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, PROJECT_FOLDER)

                    insight = get_readme_insight(rel_path)
                    if insight and "rien à optimiser" in insight.lower():
                        continue

                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()

                            # Si pas d'insight, créer un résumé rapide et stocker temporairement
                            if not insight or insight.strip() == "":
                                summary_prompt = f"Explique en une phrase ce que fait ce fichier nommé {file}. Voici son contenu :\n{content[:1500]}"
                                insight = generate_code_proposal(summary_prompt, "_temp_summary")
                                cache_resumés.append((rel_path, insight))

                            prompt_parts.append(f"# Fichier : {file}\n# Infos README : {insight}\n{content}\n")
                            cache_fichier.append(rel_path)
                    except Exception as e:
                        logging.warning(f"Erreur lecture {file} : {e}")

        prompt = (
            "Voici l'ensemble du code du projet suivant à analyser et optimiser :\n"
            + "\n".join(prompt_parts)
            + "\n\n➡️ Fais une analyse complète du projet :\n"
              "- Quels fichiers devraient être restructurés ?\n"
              "- Y a-t-il des bugs ou duplications ?\n"
              "- Quelles sont les optimisations possibles ?\n"
              "- Quels fichiers doivent être modifiés ?\n"
              "- Résume aussi les fonctions principales et leur rôle.\n"
        )

        try:
            filename = f"{selected_project.replace('/', '_')}_deep_summary.md"
            if not session.get("code_proposal_already_generated"):
                session["code_proposal_already_generated"] = True
                suggestion = generate_code_proposal(prompt, filename)
            else:
                logging.info("⛔ Proposition déjà générée, on ne relance pas.")
                suggestion = "✅ Proposition déjà générée."

            save_proposal(filename, prompt, suggestion, accepted=False)
            proposals[filename] = suggestion
        except Exception as e:
            proposals["Erreur"] = f"❌ Erreur lors de la génération : {e}"

    try:
        project_list = find_projects_recursively(PROJECT_FOLDER)
    except Exception as e:
        project_list = []
        logging.error(f"Erreur lecture des projets : {e}")

    return render_template(
        "deep_analysis.html",
        proposals=proposals,
        selected_project=selected_project,
        project_list=project_list
    )
