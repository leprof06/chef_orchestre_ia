# agents/routes/routes_project.py
from flask import render_template, redirect, url_for, session, flash, request, jsonify
from werkzeug.utils import secure_filename
import os
from agents.utils.project_tools import (
    create_project,
    list_projects,
    save_project_state,
    load_project_state,
    delete_project,
    export_project,
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
        projects = list_projects() if callable(list_projects) else []
        return render_template("choose_project.html", projects=projects)

    @app.route("/load_project/<project_name>")
    def load_project_route(project_name):
        success = load_project_state(project_name)
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
        success = save_project_state(project_name)
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
                flash("Projet importé avec succès.")
            else:
                flash("Erreur lors de l'import du projet.")
            return redirect(url_for('projet_existant'))
        else:
            flash("Format de fichier non autorisé.")
            return redirect(url_for('projet_existant'))

    # ------------------ AJOUT DES ROUTES POUR L’EXPLORER/CODE EDITOR ------------------

    def get_file_tree(root_path):
        tree = []
        try:
            for entry in sorted(os.listdir(root_path)):
                full_path = os.path.join(root_path, entry)
                if os.path.isdir(full_path):
                    tree.append({
                        'type': 'folder',
                        'name': entry,
                        'open': False,
                        'children': get_file_tree(full_path)
                    })
                else:
                    tree.append({
                        'type': 'file',
                        'name': entry
                    })
        except Exception as e:
            pass  # (log l’erreur en prod)
        return tree

    @app.route('/project_files')
    def project_files():
        project = request.args.get('project')
        if not project or '/' in project or '..' in project:
            return jsonify(success=False, message="Projet invalide.")

        root_path = os.path.join('projets', project)
        if not os.path.isdir(root_path):
            return jsonify(success=False, message="Projet introuvable.")

        tree = get_file_tree(root_path)
        return jsonify(success=True, tree=tree)

    @app.route('/load_file')
    def load_file():
        project = request.args.get('project')
        filename = request.args.get('filename')
        if not project or not filename or '/' in project or '..' in project or '..' in filename:
            return jsonify(success=False, message="Paramètres invalides.")

        file_path = os.path.join('projets', project, filename.lstrip('/'))
        if not os.path.isfile(file_path):
            return jsonify(success=False, message="Fichier introuvable.")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            return jsonify(success=True, code=code)
        except Exception as e:
            return jsonify(success=False, message=f"Erreur lecture: {str(e)}")

    @app.route('/save_code', methods=['POST'])
    def save_code():
        data = request.get_json()
        code = data.get('code')
        project = data.get('project')
        filename = data.get('filename')

        # Sécurité de base
        if not project or not filename or '/' in project or '..' in project or '..' in filename:
            return jsonify(success=False, message="Projet ou fichier non valide."), 400

        project_dir = os.path.join('projets', project)
        file_path = os.path.join(project_dir, filename)

        try:
            os.makedirs(project_dir, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(code)
            return jsonify(success=True, message="Code enregistré avec succès.")
        except Exception as e:
            return jsonify(success=False, message=f"Erreur lors de la sauvegarde : {str(e)}"), 500

    # ------------------------------------------------------------------------

