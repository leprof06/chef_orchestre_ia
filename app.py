from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename

# -- Orchestrator IA --
from orchestrator import Orchestrator
orchestrator = Orchestrator()

UPLOAD_FOLDER = os.path.join('workspace', 'uploads')
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = 'dev-secret-1234'  # à personnaliser
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === PAGES HTML ===

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nouveau-projet")
def nouveau_projet():
    # Projet vierge : pas d'upload, pas de bouton analyse
    return render_template("chat.html", show_analyse_btn=False)

@app.route("/projet-existant", methods=["GET"])
def projet_existant():
    return render_template("choose_project.html")

@app.route("/projet-existant/upload", methods=["POST"])
def upload_projet_existant():
    if "project_zip" not in request.files:
        flash("Aucun fichier fourni.")
        return redirect(url_for('projet_existant'))
    file = request.files["project_zip"]
    if file.filename == '':
        flash("Aucun fichier sélectionné.")
        return redirect(url_for('projet_existant'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(save_path)
        session['current_project'] = save_path
        return redirect(url_for('chat_projet'))
    else:
        flash("Fichier non valide (format attendu : .zip)")
        return redirect(url_for('projet_existant'))

@app.route("/chat")
def chat_projet():
    show_analyse = bool(session.get('current_project'))
    return render_template("chat.html", show_analyse_btn=show_analyse)

@app.route("/analyser", methods=["POST"])
def analyser_projet():
    # Appel IA pour analyse (à compléter)
    flash("Fonction d'analyse en cours de développement.")
    return redirect(url_for('chat_projet'))

# === API CHAT AJAX ===

def parse_user_input(user_input, project_path=None):
    user_input = user_input.lower()
    if "analyse" in user_input or "scanner" in user_input:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path}
    elif "clé api" in user_input or "api key" in user_input:
        return {"manager": "analyse", "type": "detect_api_keys", "project_path": project_path}
    elif "dépendance" in user_input or "requirement" in user_input:
        return {"manager": "devops", "type": "manage_dependencies", "project_path": project_path}
    elif "génère" in user_input or "écris" in user_input:
        return {"manager": "code", "type": "generate_code", "project_path": project_path}
    elif "optimise" in user_input:
        return {"manager": "code", "type": "optimize_code", "project_path": project_path}
    elif "debug" in user_input or "corrige" in user_input:
        return {"manager": "code", "type": "debug_code", "project_path": project_path}
    elif "agent" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_agent"}
    elif "manager" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_manager"}
    elif "interface" in user_input or "ui" in user_input:
        return {"manager": "ux", "type": "analyze_ui", "project_path": project_path}
    else:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path, "note": "🔍 Interprétation approximative"}

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_input = data.get("message")
    project_path = session.get('current_project', None)
    if not user_input:
        return jsonify({"error": "Message vide"}), 400

    task = parse_user_input(user_input, project_path)
    result = orchestrator.dispatch_task(task)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
