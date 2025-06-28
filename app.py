from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename
from orchestrator import Orchestrator

orchestrator = Orchestrator()

# Configuration
UPLOAD_FOLDER = os.path.join('workspace', 'uploads')
ALLOWED_EXTENSIONS = {'zip'}

app = Flask(__name__)
app.secret_key = 'dev-secret-1234'  # à personnaliser/masquer
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- ROUTES FRONTEND ---

# 1. Accueil
@app.route("/")
def index():
    return render_template("index.html")

# 2. Page "nouveau projet" : chat vierge
@app.route("/nouveau-projet")
def nouveau_projet():
    # Ici on pourrait initialiser une session de projet vierge si besoin
    return render_template("chat.html", show_analyse_btn=False)

# 3. Page "projet existant" : upload
@app.route("/projet-existant", methods=["GET"])
def projet_existant():
    return render_template("choose_project.html")

# 4. Traitement de l'upload ZIP
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
        # Ici tu peux ajouter l'extraction, l'analyse, etc.
        # Par exemple, stocker le chemin du projet dans la session :
        session['current_project'] = save_path
        return redirect(url_for('chat_projet'))
    else:
        flash("Fichier non valide (format attendu : .zip)")
        return redirect(url_for('projet_existant'))

# 5. Page chat pour un projet (après upload ou création vierge)
@app.route("/chat")
def chat_projet():
    # On affiche le bouton analyse SI un projet a été uploadé (sinon, projet vierge)
    show_analyse = bool(session.get('current_project'))
    return render_template("chat.html", show_analyse_btn=show_analyse)

# -- ROUTE OPTIONNELLE pour le bouton "Analyser le projet"
@app.route("/analyser", methods=["POST"])
def analyser_projet():
    # Ici on branchera l'appel à l'agent d'analyse IA
    flash("Fonction d'analyse en cours de développement.")
    return redirect(url_for('chat_projet'))

# Pour le parsing, tu peux reprendre ta fonction existante
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

# === API chat AJAX ===
@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    user_input = data.get("message")
    project_path = data.get("project_path", None)
    if not user_input:
        return jsonify({"error": "Message vide"}), 400

    task = parse_user_input(user_input, project_path)
    result = orchestrator.dispatch_task(task)
    return jsonify(result)

# --- MAIN ---
if __name__ == "__main__":
    app.run(debug=True)
