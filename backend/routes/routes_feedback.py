import logging
import os
from flask import Blueprint, request, render_template, redirect, url_for, session
from core.services import generate_code_proposal
from core.history_manager import save_proposal
from routes.routes import application_data, get_active_project_folder

routes_feedback = Blueprint("feedback", __name__)

@routes_feedback.route("/custom_feedback", methods=["POST"])
def custom_feedback():
    try:
        custom_prompt = request.form.get("custom_prompt", "").strip()
        if not custom_prompt:
            logging.warning("Aucune consigne personnalisée fournie.")
            return redirect(url_for("review"))

        project_folder = get_active_project_folder()
        filename = application_data.get("selected_file")
        file_path = os.path.join(project_folder, filename) if filename else None

        if not file_path or not os.path.exists(file_path):
            logging.error("Fichier introuvable pour re-génération : %s", file_path)
            return f"❌ Erreur : fichier introuvable."

        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        prompt_context = (
            f"Tu dois adapter ta proposition à cette consigne spéciale :\n{custom_prompt}\n\n"
            f"Voici le code actuel :\n{code}"
        )

        if not session.get("code_proposal_already_generated"):
            session["code_proposal_already_generated"] = True
            proposal = generate_code_proposal(prompt_context, filename)
        else:
            logging.info("⛔ Proposition déjà générée, on ne relance pas.")
            proposal = "✅ Proposition déjà générée."

        application_data["latest_proposal"] = proposal
        save_proposal(filename, code, proposal, accepted=False)

        return render_template("review.html", proposal=proposal, filename=filename)

    except Exception as e:
        logging.error(f"Erreur lors du traitement de la consigne personnalisée : {e}")
        return f"❌ Erreur interne : {e}"
