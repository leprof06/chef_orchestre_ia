# routes.py

import os
from flask import request, render_template, redirect, url_for, session, flash, jsonify
from werkzeug.utils import secure_filename

from agents.utils.import_connectors import (
    import_zip_file, import_local_folder, import_from_github,
    import_from_gdrive, import_from_dropbox, import_from_icloud,
    import_from_s3, import_from_http, import_from_ftp,
    import_from_svn, import_from_bitbucket, import_from_gitlab
)

ALLOWED_EXTENSIONS = {'zip'}
UPLOAD_FOLDER = os.path.join('workspace', 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def register_routes(app, orchestrator):
    # --- PAGE ACCUEIL ---
    @app.route("/")
    def index():
        return render_template("index.html")

    # --- CHAT PRINCIPAL ---
    @app.route("/chat_projet", methods=["GET", "POST"])
    def chat_projet():
        if request.method == "POST":
            user_input = request.form.get("message") or request.json.get("message")
            project_path = session.get("current_project")
            if not user_input:
                return jsonify({"error": "Message vide"}), 400
            task = orchestrator.parse_user_input(user_input, project_path)
            result = orchestrator.dispatch_task(task)
            return jsonify(result)
        # GET : affiche l’UI principale (logs/code)
        logs = orchestrator.get_logs()
        code = orchestrator.get_code_state()
        show_analyse = bool(session.get('current_project'))
        return render_template("chat.html", show_analyse_btn=show_analyse, logs=logs, code=code)

    # --- ANALYSE ---
    @app.route("/analyser", methods=["POST"])
    def analyser():
        project_path = session.get('current_project')
        result = orchestrator.analyse_project(project_path)
        logs = orchestrator.get_logs()
        return jsonify({"logs": "\n".join(logs) if logs else "Aucun log généré", "result": result})

    # --- LOGS & CODE ---
    @app.route("/logs")
    def logs():
        logs = orchestrator.get_logs()
        return render_template("logs.html", logs=logs)

    @app.route("/code")
    def code():
        code_state = orchestrator.get_code_state()
        return render_template("code.html", code=code_state)

    # --- RESET ---
    @app.route("/reset")
    def reset():
        session.pop('current_project', None)
        orchestrator.init_new_project()
        flash("Projet réinitialisé avec succès.")
        return redirect(url_for('index'))

    # --- PROJETS (choix, chargement, sauvegarde, suppression, export) ---
    @app.route("/nouveau_projet", methods=["GET"])
    def nouveau_projet():
        # Génère un nom temporaire unique (timestamp)
        default_name = f"projet_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        success = orchestrator.create_new_project(default_name)  # à implémenter côté orchestrator
        if success:
            session['current_project'] = default_name
            flash(f"Nouveau projet '{default_name}' créé !")
            return redirect(url_for('chat_projet'))
        else:
            flash("Erreur lors de la création du projet.")
            return redirect(url_for('index'))
    
    @app.route("/choose_project")
    def choose_project():
        projects = orchestrator.get_existing_projects()
        return render_template("choose_project.html", projects=projects)

    @app.route("/load_project/<project_name>")
    def load_project(project_name):
        success = orchestrator.load_project(project_name)
        if success:
            session['current_project'] = project_name
            flash(f"Projet '{project_name}' chargé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash(f"Échec du chargement du projet '{project_name}'.")
            return redirect(url_for('choose_project'))

    @app.route("/save_project", methods=["POST"])
    def save_project():
        project_name = request.form.get("project_name")
        success = orchestrator.save_project(project_name)
        if success:
            flash(f"Projet '{project_name}' enregistré avec succès.")
            return redirect(url_for('choose_project'))
        else:
            flash(f"Échec de l'enregistrement du projet '{project_name}'.")
            return redirect(url_for('chat_projet'))

    @app.route("/delete_project/<project_name>")
    def delete_project(project_name):
        success = orchestrator.delete_project(project_name)
        if success:
            flash(f"Projet '{project_name}' supprimé avec succès.")
        else:
            flash(f"Échec de la suppression du projet '{project_name}'.")
        return redirect(url_for('choose_project'))

    @app.route("/export_project/<project_name>")
    def export_project(project_name):
        success, msg = orchestrator.export_project(project_name)
        return jsonify({"success": success, "msg": msg})

    # --- IMPORT MULTI-SOURCES ---
    @app.route("/import/zip", methods=["POST"])
    def import_zip():
        zip_path = request.form.get("zip_path")
        ok, msg = import_zip_file(zip_path)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/local", methods=["POST"])
    def import_local():
        folder_path = request.form.get("folder_path")
        ok, msg = import_local_folder(folder_path)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/github", methods=["POST"])
    def import_github():
        github_url = request.form.get("github_url")
        token = request.form.get("token")
        ok, msg = import_from_github(github_url, token=token)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/gdrive", methods=["POST"])
    def import_gdrive():
        gdrive_id = request.form.get("gdrive_id")
        token = request.form.get("token")
        ok, msg = import_from_gdrive(gdrive_id, gdrive_token=token)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/dropbox", methods=["POST"])
    def import_dropbox():
        dropbox_link = request.form.get("dropbox_link")
        token = request.form.get("token")
        ok, msg = import_from_dropbox(dropbox_link, dropbox_token=token)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/icloud", methods=["POST"])
    def import_icloud():
        icloud_url = request.form.get("icloud_url")
        token = request.form.get("token")
        ok, msg = import_from_icloud(icloud_url, icloud_token=token)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/s3", methods=["POST"])
    def import_s3():
        s3_url = request.form.get("s3_url")
        key = request.form.get("aws_access_key")
        secret = request.form.get("aws_secret_key")
        ok, msg = import_from_s3(s3_url, aws_access_key=key, aws_secret_key=secret)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/http", methods=["POST"])
    def import_http():
        http_url = request.form.get("http_url")
        ok, msg = import_from_http(http_url)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/ftp", methods=["POST"])
    def import_ftp():
        ftp_url = request.form.get("ftp_url")
        ftp_user = request.form.get("ftp_user")
        ftp_pass = request.form.get("ftp_pass")
        ok, msg = import_from_ftp(ftp_url, ftp_user=ftp_user, ftp_pass=ftp_pass)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/svn", methods=["POST"])
    def import_svn():
        svn_url = request.form.get("svn_url")
        ok, msg = import_from_svn(svn_url)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/bitbucket", methods=["POST"])
    def import_bitbucket():
        bitbucket_url = request.form.get("bitbucket_url")
        token = request.form.get("token")
        ok, msg = import_from_bitbucket(bitbucket_url, token=token)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/gitlab", methods=["POST"])
    def import_gitlab():
        gitlab_url = request.form.get("gitlab_url")
        token = request.form.get("token")
        ok, msg = import_from_gitlab(gitlab_url, token=token)
        return jsonify({"success": ok, "msg": msg})

    # --- UPLOAD FICHIERS ---
    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            flash("Aucun fichier fourni.")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == '':
            flash("Aucun fichier sélectionné.")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(save_path)
            flash("Fichier téléchargé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash("Fichier non valide (format attendu : .zip)")
            return redirect(request.url)
