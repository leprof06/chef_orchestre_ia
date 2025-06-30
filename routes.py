# routes.py

from flask import render_template, redirect, url_for, session, flash, request, jsonify
from agents.utils.import_connectors import (
    import_zip_file, import_local_folder, import_from_github,
    import_from_gdrive, import_from_dropbox, import_from_icloud,
    import_from_s3, import_from_http, import_from_ftp,
    import_from_svn, import_from_bitbucket, import_from_gitlab
)

def register_routes(app, orchestrator):

    # --- ACCUEIL ---
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    # --- NOUVEAU PROJET (crée et va direct dans le chat) ---
    @app.route("/nouveau_projet", methods=["GET", "POST"])
    def nouveau_projet():
        if request.method == "POST":
            project_name = request.form.get("project_name", "Projet_sans_nom")
        else:
            # Si méthode GET, on génère un nom temporaire ou propose un formulaire
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

    # --- PROJET EXISTANT (liste des projets et choix) ---
    @app.route("/projet_existant", methods=["GET"])
    def projet_existant():
        projects = orchestrator.get_existing_projects() if hasattr(orchestrator, "get_existing_projects") else []
        return render_template("choose_project.html", projects=projects)

    # --- IMPORTS MULTI-SOURCE ---
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

    # ---- CHAT IA & ANALYSE (branché sur orchestrator) ----
    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        if request.method == "POST":
            message = request.form.get("message")
            result = orchestrator.chat(message) if hasattr(orchestrator, "chat") else "Réponse IA simulée : à implémenter"
            return jsonify({"reply": result})
        return render_template("chat.html")

    @app.route("/analyser", methods=["POST"])
    def analyser():
        project_path = request.form.get("project_path")
        result = orchestrator.analyse_manager.handle_task({"project_path": project_path}) if hasattr(orchestrator, "analyse_manager") else "Analyse simulée : à implémenter"
        return jsonify({"result": result})

    # --- LOGS, CODE, RESET, GESTION PROJETS ---
    @app.route("/logs")
    def logs():
        logs = orchestrator.get_logs() if hasattr(orchestrator, "get_logs") else []
        return render_template("logs.html", logs=logs)
    
    @app.route("/code")
    def code():
        code_state = orchestrator.get_code_state() if hasattr(orchestrator, "get_code_state") else ""
        return render_template("code.html", code=code_state)
    
    @app.route("/reset")
    def reset():
        session.pop('current_project', None)
        if hasattr(orchestrator, "init_new_project"):
            orchestrator.init_new_project()
        flash("Projet réinitialisé avec succès.")
        return redirect(url_for('index'))
    
    # --- CHOIX, CHARGEMENT, SAUVEGARDE, SUPPRESSION, EXPORT PROJET ---
    @app.route("/choose_project")
    def choose_project():
        projects = orchestrator.get_existing_projects() if hasattr(orchestrator, "get_existing_projects") else []
        return render_template("choose_project.html", projects=projects)
    
    @app.route("/load_project/<project_name>")
    def load_project(project_name):
        success = orchestrator.load_project(project_name) if hasattr(orchestrator, "load_project") else False
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
        success = orchestrator.save_project(project_name) if hasattr(orchestrator, "save_project") else False
        if success:
            flash(f"Projet '{project_name}' enregistré avec succès.")
            return redirect(url_for('choose_project'))
        else:
            flash(f"Échec de l'enregistrement du projet '{project_name}'.")
            return redirect(url_for('chat'))
    
    @app.route("/delete_project/<project_name>")
    def delete_project(project_name):
        success = orchestrator.delete_project(project_name) if hasattr(orchestrator, "delete_project") else False
        if success:
            flash(f"Projet '{project_name}' supprimé avec succès.")
            return redirect(url_for('choose_project'))
        else:
            flash(f"Échec de la suppression du projet '{project_name}'.")
            return redirect(url_for('choose_project'))
    
    @app.route("/export_project/<project_name>")
    def export_project(project_name):
        success, msg = orchestrator.export_project(project_name) if hasattr(orchestrator, "export_project") else (False, "Non implémenté")
        if success:
            flash(f"Projet '{project_name}' exporté avec succès.")
            return jsonify({"success": True, "msg": msg})
        else:
            flash(f"Échec de l'exportation du projet '{project_name}'.")
            return jsonify({"success": False, "msg": msg})

    # --- UPLOAD DIRECT ZIP (si besoin) ---
    ALLOWED_EXTENSIONS = {"zip"}
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
            from werkzeug.utils import secure_filename
            import os
            save_path = os.path.join(app.config.get('UPLOAD_FOLDER', "workspace/uploads"), secure_filename(file.filename))
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            file.save(save_path)
            flash("Fichier téléchargé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash("Fichier non valide (format attendu : .zip)")
            return redirect(request.url)

    @app.route("/chat_projet")
    def chat_projet():
        show_analyse = bool(session.get('current_project'))
        logs = orchestrator.get_logs() if hasattr(orchestrator, "get_logs") else []
        code = orchestrator.get_code_state() if hasattr(orchestrator, "get_code_state") else ""
        return render_template("chat.html", show_analyse_btn=show_analyse, logs=logs, code=code)

