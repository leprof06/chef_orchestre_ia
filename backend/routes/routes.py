import os
import logging
import subprocess
import threading
import json
from flask import request, redirect, Blueprint, url_for, render_template, render_template_string, jsonify, session, flash
from config import PROJECT_FOLDER
from agents.chef_agent import ChefOrchestreAgent

app = Flask(__name__, template_folder="../frontend")
chef = ChefOrchestreAgent(agents={})

routes_test = Blueprint("test_runner", __name__)
file_lock = threading.Lock()
application_data = {
    "latest_proposal": "",
    "selected_file": "",
    "custom_objectives": ""
}

load_readme()

def get_active_project_folder():
    return session.get("active_project", PROJECT_FOLDER)

@routes_test.route("/")
def home():
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    result = chef.handle_task(task)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)

@routes_test.route("/choose_project", methods=["GET", "POST"])
def choose_project():
    if request.method == "POST":
        selected = request.form.get("project")
        if selected:
            session["active_project"] = os.path.join(PROJECT_FOLDER, selected)
            return redirect(url_for("test_runner.home"))

    try:
        subfolders = [d for d in os.listdir(PROJECT_FOLDER) if os.path.isdir(os.path.join(PROJECT_FOLDER, d))]
    except Exception as e:
        subfolders = []
        logging.error(f"Erreur de lecture des projets disponibles : {e}")

    return render_template("choose_project.html", projects=subfolders)

@routes_test.route("/choose_file", methods=["GET", "POST"])
def choose_file():
    project_folder = get_active_project_folder()
    if request.method == "POST":
        application_data["selected_file"] = request.form.get("filename")
        return redirect(url_for("test_runner.auto_process"))

    files = [f for f in os.listdir(project_folder) if f.endswith(".py") or f.lower().startswith("readme")]
    return render_template("choose_file.html", files=files)

@routes_test.route("/optimize", methods=["POST"])
def auto_process():
    project_folder = get_active_project_folder()
    try:
        with file_lock:
            application_data["selected_file"] = request.form.get("filename")
            file_path = os.path.join(project_folder, application_data["selected_file"])
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            if not session.get("code_proposal_already_generated"):
                session["code_proposal_already_generated"] = True
                proposal = generate_code_proposal(code, application_data["selected_file"])
            else:
                logging.info("⛔ Proposition déjà générée, on ne relance pas.")
                proposal = "✅ Proposition déjà générée."

            application_data["latest_proposal"] = proposal

            return render_template("review.html",
                                   proposal=application_data["latest_proposal"],
                                   filename=application_data["selected_file"])
    except Exception as e:
        logging.error(f"Erreur d'optimisation : {e}")
        return jsonify({"erreur": str(e)})

@routes_test.route("/review")
def review():
    return render_template("review.html", proposal=application_data["latest_proposal"], filename=application_data["selected_file"])

@routes_test.route("/apply", methods=["POST"])
def apply_changes():
    project_folder = get_active_project_folder()
    try:
        with file_lock:
            file_path = os.path.join(project_folder, application_data["selected_file"])
            backup_file(file_path)
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"\n\n# 🔧 Améliorations intégrées par l'IA :\n{application_data['latest_proposal']}")
        return redirect(url_for("test_runner.review"))
    except Exception as e:
        logging.error(f"Erreur application : {e}")
        return f"❌ Erreur application : {e}"

@routes_test.route("/run_tests")
def run_tests():
    from dependency_checker import detect_and_install_dependencies

    project_folder = get_active_project_folder()

    try:
        # 🔁 Vérifie et installe les dépendances avant de lancer les tests
        log_install = detect_and_install_dependencies(project_folder)

        # 🧪 Lance les tests PyTest
        result = subprocess.run(["pytest", project_folder], capture_output=True, text=True)

        return render_template_string("""
            <h2>🧪 Résultat des tests :</h2>
            <pre>{{ install_log }}</pre>
            <hr>
            <pre>{{ test_result }}</pre>
            <a href='/'>⬅️ Retour à l'accueil</a>
        """, install_log=log_install, test_result=result.stdout)

    except Exception as e:
        logging.error(f"Erreur pendant les tests : {e}")
        return f"❌ Erreur pendant les tests : {e}"

@routes_test.route("/apply_and_test", methods=["POST"])
def apply_and_test():
    project_folder = get_active_project_folder()
    try:
        with file_lock:
            file_path = os.path.join(project_folder, application_data["selected_file"])
            new_code = application_data["latest_proposal"]
            success, output = safe_apply_modification(file_path, new_code, test_command=["pytest", project_folder])
            if success:
                return f"<h2>✅ Tests passés avec succès :</h2><pre>{output}</pre><a href='/'>Retour</a>"
            else:
                return f"<h2>❌ Échec des tests — fichier restauré :</h2><pre>{output}</pre><a href='/'>Retour</a>"
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'application ou des tests : {e}")
        return f"<h2>Erreur :</h2><pre>{e}</pre><a href='/'>Retour</a>"

@routes_test.route("/run_auto_fixer", methods=["POST"])
def run_auto_fixer():
    try:
        script_path = os.path.join(PROJECT_FOLDER, "auto_fixer.py")
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        output = result.stdout + "\n" + result.stderr
        return render_template("install_result.html", output=output)
    except Exception as e:
        return f"❌ Erreur lors de l'exécution du correcteur automatique : {e}"

@routes_test.route("/auto_ai_fixer_project")
def auto_ai_fixer_project():
    try:
        from services import generate_code_proposal
        project_path = session.get("active_project", PROJECT_FOLDER)
        all_feedback = []

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
        logging.error(f"❌ Problème dans auto_ai_fixer_project : {e}")
        return f"Erreur auto_ai_fixer_project : {e}"

@routes_test.route("/generate_todo_from_readmes", methods=["POST"])
def generate_todo_from_readmes():
    try:
        projet = session.get("selected_project")
        if not projet:
            return "❌ Aucun projet sélectionné."
        chemin = os.path.join(PROJECT_FOLDER, projet)
        generer_todo(chemin)
        flash("📝 todo.md généré avec succès depuis les README.", "success")
        return redirect(url_for("test_runner.home"))
    except Exception as e:
        logging.error(f"Erreur génération todo.md : {e}")
        return f"❌ Erreur génération du todo.md : {e}"

@routes_test.route("/edit_readme", methods=["GET", "POST"])
def edit_readme():
    if request.method == "POST":
        content = request.form.get("readme_content", "")
        try:
            with open(README_PATH, "w", encoding="utf-8") as f:
                f.write(content)
                application_data["custom_objectives"] = content
            logging.info("✅ README.md mis à jour via interface web")
            return redirect(url_for("test_runner.home"))
        except IOError as e:
            logging.error(f"Erreur d'écriture du fichier : {e}")
            return f"Erreur d'écriture du fichier : {e}"
    else:
        try:
            with open(README_PATH, "r", encoding="utf-8") as f:
                content = f.read()
            return render_template("edit_readme.html", content=content)
        except IOError as e:
            logging.error(f"Erreur de lecture du fichier : {e}")
            return f"Erreur de lecture du fichier : {e}"

@routes_test.route("/generate_ai_report")
def generate_ai_report():
    try:
        scan_and_generate_report()
        return "✅ Rapport généré avec succès. Consultez le fichier dans /rapports."
    except Exception as e:
        logging.error(f"Erreur génération du rapport : {e}")
        return f"❌ Erreur lors de la génération du rapport : {e}"

@routes_test.route("/run_test_routes", methods=["POST"])
def run_test_routes():
    try:
        result = subprocess.run(["pytest", "test_routes.py"], capture_output=True, text=True)
        return render_template_string("""
            <h1>🧪 Résultat des tests API</h1>
            <pre>{{ result }}</pre>
            <a href='/'>⬅️ Retour à l'accueil</a>
        """, result=result.stdout)
    except Exception as e:
        return f"❌ Erreur lors de l'exécution des tests : {e}"

@routes_test.route("/generate_ai_suggestions", methods=["GET"])
def generate_ai_suggestions():
    from services import generate_code_proposal
    project_folder = session.get("active_project", PROJECT_FOLDER)
    try:
        all_code = ""
        for filename in os.listdir(project_folder):
            if filename.endswith(".py"):
                with open(os.path.join(project_folder, filename), "r", encoding="utf-8") as f:
                    all_code += f"# File: {filename}\n" + f.read() + "\n\n"

        if not all_code.strip():
            return "❌ Aucun fichier .py trouvé pour générer des suggestions."

        application_data["latest_proposal"] = generate_code_proposal(all_code, "Projet complet")
        return render_template("review.html", proposal=application_data["latest_proposal"], filename="Projet complet")

    except Exception as e:
        logging.error(f"Erreur lors de la génération des suggestions IA : {e}")
        return f"❌ Erreur : {e}"

@routes_test.route("/generate_ai_project_report")
def generate_ai_project_report():
    from global_ai_report_generator import generate_project_report, save_project_report
    project_path = session.get("active_project", PROJECT_FOLDER)

    if not os.path.isdir(project_path):
        return f"❌ Aucun projet sélectionné ou chemin invalide : {project_path}"

    try:
        project_name = os.path.basename(project_path.rstrip("/\\"))
        report = generate_project_report(project_path)
        save_project_report(project_name, report)
        return f"✅ Rapport généré pour le projet : {project_name}. Consultez /rapports/rapport_{project_name}.json"
    except Exception as e:
        logging.error(f"❌ Erreur génération rapport projet : {e}")
        return f"❌ Erreur : {e}"
    
@routes_test.route("/generate_readmes_from_structure", methods=["POST"])
def generate_readmes_from_structure():
    try:
        analyser_tous_les_projets()
        flash("✅ README_BACKEND.md et README_FRONTEND.md générés avec succès.", "success")
        return redirect(url_for("test_runner.home"))
    except Exception as e:
        logging.error(f"Erreur génération des README par structure : {e}")
        return f"❌ Erreur génération des README : {e}"

@routes_test.route("/scan_all_projects")
def scan_all_projects():
    all_files = {}
    all_requirements = set()
    suggestions = []
    env_capabilities = detect_capabilities()

    ALT_API = {
        "IFLYTEK_API_KEY": ["AWS_API_KEY", "GOOGLE_API_KEY"],
        "DEEPL_API_KEY": ["GOOGLE_API_KEY"],
        "ANTHROPIC_API_KEY": ["OPENAI_API_KEY"],
    }

    try:
        for project_name in os.listdir(PROJECT_FOLDER):
            project_path = os.path.join(PROJECT_FOLDER, project_name)
            if not os.path.isdir(project_path):
                continue
            for root, _, files in os.walk(project_path):
                for f in files:
                    if f.endswith((".py", ".html", ".json", ".env")):
                        path = os.path.join(root, f)
                        try:
                            with open(path, "r", encoding="utf-8") as file:
                                content = file.read()
                                all_files[path] = content

                                for line in content.splitlines():
                                    if line.strip().startswith("import") or line.strip().startswith("from"):
                                        words = line.strip().split()
                                        if words[0] == "import":
                                            all_requirements.add(words[1].split('.')[0])
                                        elif words[0] == "from":
                                            all_requirements.add(words[1].split('.')[0])

                        except Exception as e:
                            all_files[path] = f"❌ Erreur de lecture : {e}"

        for cap, info in env_capabilities.items():
            if not info["active"] and info["via"] in ALT_API:
                alternatives = ALT_API[info["via"]]
                for alt in alternatives:
                    if not env_capabilities.get(alt, {}).get("active"):
                        suggestions.append(f"🔁 Pour remplacer {info['via']}, essayez d'utiliser {alt} si disponible.")

        return render_template("scan_result.html", files=all_files, updates=[(k, "📄 Scanné") for k in all_files], suggestions=suggestions, requirements=sorted(all_requirements))
    except Exception as e:
        logging.error(f"Erreur lors du scan complet des projets : {e}")
        return f"❌ Erreur pendant le scan global : {e}"

__all__ = ["routes_test"]
