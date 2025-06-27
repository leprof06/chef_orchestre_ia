import os
import json
import logging
from flask import Blueprint, render_template, session
from config import PROJECT_FOLDER

scan_all_projects_routes = Blueprint("scan_all_projects", __name__)

@scan_all_projects_routes.route("/scan_all_projects")
def scan_all_projects():
    all_files = {}
    updates = []
    suggestions = []
    project_reports = {}

    try:
        # 🔁 Analyse chaque projet séparément
        for folder_name in os.listdir(PROJECT_FOLDER):
            project_path = os.path.join(PROJECT_FOLDER, folder_name)
            if not os.path.isdir(project_path):
                continue

            project_code = ""
            dependencies = set()

            for root, _, files in os.walk(project_path):
                for file in files:
                    if file.endswith(('.py', '.html', '.json', '.env', 'README.md', 'README_PROJECT.md')):
                        full_path = os.path.join(root, file)
                        try:
                            with open(full_path, encoding="utf-8") as f:
                                content = f.read()
                                all_files[full_path] = content
                                project_code += f"\n\n# Fichier : {file}\n" + content

                                if file.endswith(".py"):
                                    for line in content.splitlines():
                                        if line.strip().startswith("import") or line.strip().startswith("from"):
                                            parts = line.strip().split()
                                            if parts[0] == "import":
                                                dependencies.add(parts[1].split('.')[0])
                                            elif parts[0] == "from":
                                                dependencies.add(parts[1].split('.')[0])

                        except Exception as e:
                            all_files[full_path] = f"❌ Erreur de lecture : {e}"

            capabilities = detect_capabilities()
            missing = detect_capabilities_missing()

            project_reports[folder_name] = {
                "dependencies": sorted(list(dependencies)),
                "missing_capabilities": missing
            }

        # 📁 Sauvegarder dans rapport/rapport_global.json
        os.makedirs("rapport", exist_ok=True)
        with open("rapport/rapport_global.json", "w", encoding="utf-8") as f:
            json.dump(project_reports, f, indent=2, ensure_ascii=False)
            logging.info("✅ rapport_global.json généré dans /rapport")

        return render_template("scan_result.html", files=all_files, updates=[(k, "📄 Scanné") for k in all_files], suggestions=suggestions)

    except Exception as e:
        logging.error(f"❌ Erreur pendant le scan global : {e}")
        return f"❌ Erreur pendant le scan global : {e}"
