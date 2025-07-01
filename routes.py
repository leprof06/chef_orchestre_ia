from flask import render_template, redirect, url_for, session, flash, request, jsonify
import os
from werkzeug.utils import secure_filename

# ——— IMPORT UTILITAIRES (pour gestion projets, upload, import, etc) ———
from agents.utils.projet_tools import (
    get_existing_projects,
    save_project,
    load_project,
    delete_project,
    export_project,
    import_zip_file,
    import_local_folder,
    import_from_github,
    import_from_gdrive,
    import_from_dropbox,
    import_from_icloud,
    import_from_s3,
    import_from_http,
    import_from_ftp,
    import_from_svn,
    import_from_bitbucket,
    import_from_gitlab,
)
# ———————————————————————————————————————————————————————————————

def register_routes(app, orchestrator):

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

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
        # Utilise utilitaire :
        projects = get_existing_projects() if callable(get_existing_projects) else []
        return render_template("choose_project.html", projects=projects)

    # --- IMPORTS MULTI-SOURCE (utilitaires gérés) ---
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
            result = orchestrator.chat(message) if hasattr(orchestrator, "chat") else "Aucune IA disponible : fonction non implémentée"
            return jsonify({"reply": result})
        return render_template("chat.html")

    @app.route("/analyser", methods=["POST"])
    def analyser():
        project_path = request.form.get("project_path")
        # Appelle le manager réel, pas de simulation
        result = orchestrator.analyse_manager.handle("analyse_code", project_path) \
            if hasattr(orchestrator, "analyse_manager") else "Analyse non implémentée"
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

    @app.route("/choose_project")
    def choose_project():
        projects = get_existing_projects() if callable(get_existing_projects) else []
        return render_template("choose_project.html", projects=projects)

    @app.route("/load_project/<project_name>")
    def load_project_route(project_name):
        # Utilise le utilitaire (à adapter si tu veux garder la méthode d’orchestrator)
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
            # Tu peux utiliser le bon chemin d'upload ici (UPLOAD_FOLDER doit être configuré dans app.config !)
            save_path = os.path.join(app.config.get('UPLOAD_FOLDER', 'uploads'), filename)
            file.save(save_path)
            flash("Projet importé avec succès.")
            return redirect(url_for('chat_projet'))
        else:
            flash("Fichier non valide (format attendu : .zip)")
            return redirect(url_for('projet_existant'))

    @app.route("/chat_projet")
    def chat_projet():
        show_analyse = bool(session.get('current_project'))
        logs = orchestrator.get_logs() if hasattr(orchestrator, "get_logs") else []
        code = orchestrator.get_code_state() if hasattr(orchestrator, "get_code_state") else ""
        return render_template("chat.html", show_analyse_btn=show_analyse, logs=logs, code=code)

