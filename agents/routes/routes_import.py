# agents/routes/routes_import.py
from flask import request, jsonify
from agents.utils.project_tools import (
    import_from_zip_file,
    import_from_local_folder,
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

def register_routes(app, orchestrator):
    @app.route("/import/zip", methods=["POST"])
    def import_from_zip():
        zip_path = request.form.get("zip_path")
        ok, msg = import_from_zip_file(zip_path)
        return jsonify({"success": ok, "msg": msg})

    @app.route("/import/local", methods=["POST"])
    def import_from_local():
        folder_path = request.form.get("folder_path")
        ok, msg = import_from_local_folder(folder_path)
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
