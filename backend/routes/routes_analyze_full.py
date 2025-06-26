from flask import Blueprint, redirect, url_for, render_template, flash, session, request
import logging
import os
from generation.generate_global_report import scan_and_generate_report
from core.history_manager import load_history, save_proposal
from core.safe_update import safe_apply_modification
from config.config import PROJECT_FOLDER
from core.services import generate_code_proposal

analyze_full = Blueprint("analyze_full", __name__)

@analyze_full.route("/analyze_full_project")
def analyze_full_project():
    try:
        scan_and_generate_report()
        flash("✅ Analyse complète terminée avec succès.", "success")

        project_path = session.get("active_project", PROJECT_FOLDER)
        last_proposals = []

        for root, _, files in os.walk(project_path):
            for f in files:
                if f.endswith(('.py', '.html', '.js', '.ts', '.json')):
                    filepath = os.path.join(root, f)
                    try:
                        try:
                            with open(filepath, "r", encoding="utf-8") as file:
                                content = file.read()
                        except UnicodeDecodeError:
                            with open(filepath, "r", encoding="latin-1") as file:
                                content = file.read()

                        if not session.get("code_proposal_already_generated"):
                            session["code_proposal_already_generated"] = True
                            proposal = generate_code_proposal(content, f)
                        else:
                            logging.info("⛔ Proposition déjà générée, on ne relance pas.")
                            proposal = "✅ Proposition déjà générée."

                        if proposal and len(proposal.strip()) > 0:
                            save_proposal(f, content, proposal, accepted=False)
                            last_proposals.append({
                                "filename": f,
                                "proposal": proposal,
                                "timestamp": "nouvelle analyse"
                            })
                    except Exception as e:
                        logging.error(f"❌ Erreur lecture ou génération pour {f} : {e}")

        return render_template("full_analysis_result.html", proposals=last_proposals)

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'analyse complète : {e}")
        flash(f"❌ Erreur lors de l'analyse : {e}", "danger")
        return redirect(url_for("test_runner.home"))

@analyze_full.route("/apply_proposal", methods=["POST"])
def apply_proposal():
    try:
        filename = request.form.get("filename")
        proposal = request.form.get("proposal")

        project_path = session.get("active_project", PROJECT_FOLDER)
        filepath = os.path.join(project_path, filename)

        success, output = safe_apply_modification(filepath, proposal, test_command=["pytest", project_path])
        if success:
            flash(f"✅ Proposition appliquée avec succès sur {filename}", "success")
        else:
            flash(f"❌ Échec de l'application sur {filename}. Fichier restauré. Détails : {output}", "danger")

    except Exception as e:
        logging.error(f"❌ Erreur lors de l'application de la proposition : {e}")
        flash(f"❌ Erreur : {e}", "danger")

    return redirect(url_for("analyze_full_project"))
