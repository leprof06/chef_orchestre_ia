# agents/routes/routes_project.py
from flask import render_template, redirect, url_for, session, flash, request, jsonify
from werkzeug.utils import secure_filename
import os

from agents.utils.projet_tools import (
    get_existing_projects, save_project, load_project,
    delete_project, export_project
)

def register_routes(app, orchestrator):

    @app.route("/nouveau_projet", methods=["GET", "POST"])
    def nouveau_projet():
        if request.method == "POST":
            project_name = request.form.get("project_name", "Projet_sans_nom")
        else:
            import time
            project_name = f"Projet_{int(time.time())}"
        success = orchestrator.create_new_project(project_name)
        if success:
            session['current_project'] = project_name
            flash(f"Nouveau projet '{project_name}' créé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash(f"Erreur lors de la création du projet.")
            return redirect(url_for('index'))

    @app.route("/projet_existant", methods=["GET"])
    def projet_existant():
        projects = get_existing_projects() if callable(get_existing_projects) else []
        return render_template("choose_project.html", projects=projects)

    @app.route("/load_project/<project_name>")
    def load_project_route(project_name):
        success = load_project(project_name)
        if success:
            session['current_project'] = project_name
            flash(f"Projet '{project_name}' chargé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash(f"Échec du chargement du projet '{project_name}'.")
            return redirect(url_for('choose_project'))

    @app.route("/save_project", methods=["POST"])
    def save_project_route():
        project_name = request.form.get("project_name")
        success = save_project(project_name)
        if success:
            flash(f"Projet '{project_name}' enregistré avec succès.")
            return redirect(url_for('choose_project'))
        else:
            flash(f"Échec de l'enregistrement du projet '{project_name}'.")
            return redirect(url_for('chat'))

    @app.route("/delete_project/<project_name>")
    def delete_project_route(project_name):
        success = delete_project(project_name)
        if success:
            flash(f"Projet '{project_name}' supprimé avec succès.")
            return redirect(url_for('choose_project'))
        else:
            flash(f"Échec de la suppression du projet '{project_name}'.")
            return redirect(url_for('choose_project'))

    @app.route("/export_project/<project_name>")
    def export_project_route(project_name):
        success, msg = export_project(project_name)
        if success:
            flash(f"Projet '{project_name}' exporté avec succès.")
            return jsonify({"success": True, "msg": msg})
        else:
            flash(f"Échec de l'exportation du projet '{project_name}'.")
            return jsonify({"success": False, "msg": msg})

    # Gestion upload zip
    ALLOWED_EXTENSIONS = {"zip"}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route("/upload_projet_existant", methods=["POST"])
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
            save_path = os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), filename)
            file.save(save_path)
            ok = orchestrator.init_from_zip(save_path)
            if ok:
                flash("Projet importé et chargé avec succès.")
            else:
                flash("Erreur lors de l'import du ZIP.")
            return redirect(url_for('chat_projet'))
        else:
            flash("Fichier non valide (format attendu : .zip)")
            return redirect(url_for('projet_existant'))
