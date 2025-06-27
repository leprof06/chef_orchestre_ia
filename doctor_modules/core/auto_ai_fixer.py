
from flask import Blueprint, redirect, url_for, render_template, flash
import logging
import os
from orchestrator import PROJECT_FOLDER
from core.install_utils import check_and_install_packages
from core.safe_update import safe_apply_modification
from core.services import generate_code_proposal

ai_fixer = Blueprint("auto_ai_fixer", __name__)

@ai_fixer.route("/auto_ai_fixer")
def auto_ai_fixer():
    try:
        logging.info("🚀 Début de la correction automatique par l'IA...")
        all_feedback = []

        # Parcours des projets
        for project_name in os.listdir(PROJECT_FOLDER):
            project_path = os.path.join(PROJECT_FOLDER, project_name)
            if not os.path.isdir(project_path):
                continue

            for root, _, files in os.walk(project_path):
                for filename in files:
                    if filename.endswith(".py"):
                        path = os.path.join(root, filename)

                        with open(path, encoding="utf-8") as f:
                            content = f.read()

                        fix = generate_code_proposal(content, filename)

                        if "Erreur" not in fix and len(fix.strip()) > 10:
                            success, result = safe_apply_modification(path, fix, test_command=["pytest", project_path])
                            all_feedback.append((filename, success, result))

        return render_template("install_result.html", fixes=all_feedback)

    except Exception as e:
        logging.error(f"❌ Problème dans auto_ai_fixer : {e}")
        return f"Erreur auto_ai_fixer : {e}"

__all__ = ["ai_fixer"]
