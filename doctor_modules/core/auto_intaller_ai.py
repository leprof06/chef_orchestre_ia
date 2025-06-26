import os
import subprocess
import logging
from flask import Blueprint, render_template, request
from config.config import PROJECT_FOLDER

install_routes = Blueprint("install_dependencies", __name__)

@install_routes.route("/install_dependencies", methods=["GET"])
def install_dependencies():
    logs = []
    try:
        for project_name in os.listdir(PROJECT_FOLDER):
            project_path = os.path.join(PROJECT_FOLDER, project_name)
            if not os.path.isdir(project_path):
                continue

            package_json = os.path.join(project_path, "package.json")
            requirements_txt = os.path.join(project_path, "requirements.txt")

            if os.path.exists(package_json):
                # Choix intelligent entre yarn et npm
                if os.path.exists(os.path.join(project_path, "yarn.lock")):
                    cmd = ["yarn", "install"]
                    outil = "Yarn"
                else:
                    cmd = ["npm", "install"]
                    outil = "NPM"

                result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)
                logs.append(f"📦 {outil} installé dans {project_name}\n{result.stdout}")

            if os.path.exists(requirements_txt):
                cmd = ["pip", "install", "-r", requirements_txt]
                result = subprocess.run(cmd, cwd=project_path, capture_output=True, text=True)
                logs.append(f"🐍 pip installé dans {project_name}\n{result.stdout}")

    except Exception as e:
        logs.append(f"❌ Erreur pendant l'installation : {e}")

    return render_template("install_result.html", logs=logs)
