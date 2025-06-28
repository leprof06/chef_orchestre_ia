from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
from werkzeug.utils import secure_filename

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

# --- MAIN ---
if __name__ == "__main__":
    app.run(debug=True)
