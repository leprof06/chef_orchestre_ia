
from flask import Blueprint, jsonify, request
from proxy_client import list_github_repo_files, read_github_file, read_google_drive_file

routes_proxy = Blueprint("routes_proxy", __name__)

# 📦 Données projets complètes issues du README
projects = {
    "IA publications": {
        "repo": "IA-publication",
        "drive": "https://drive.google.com/drive/folders/1__BrItdYl2pg74dDT27ULQAFgpdOPx1i?usp=drive_link"
    },
    "Création site internet": {
        "repo": "cr-ation-de-site-internet",
        "drive": "https://drive.google.com/drive/folders/18y3WsWR9rYepBX1BezM_pz7rvbUkYKx0?usp=drive_link"
    },
    "IA programeuse": {
        "repo": "I.A.-Programeuse",
        "drive": "https://drive.google.com/drive/folders/1_4Guzx8dCOYprY2iHRhjjggJwPm0tXyk?usp=drive_link"
    },
    "Chatbot - ai": {
        "repo": "chatbot-ai",
        "drive": "https://drive.google.com/drive/folders/1hFbRXXGoMhq3nePbBsbPHQwAYqePUU2M?usp=drive_link"
    },
    "AssistantProfesseurIA": {
        "repo": "AssistantProfesseurIA",
        "drive": None
    },
    "I.A Sosie": {
        "repo": "I.A.-Sosie",
        "drive": None
    },
    "Serveur proxy": {
        "repo": "github-proxy",
        "drive": "https://drive.google.com/drive/folders/11MGCKc705ujEaSHxOWojA0lf9I-MXRIN?usp=drive_link"
    }
}

@routes_proxy.route("/proxy/github/<project_name>")
def list_repo_files(project_name):
    project = projects.get(project_name)
    if not project:
        return jsonify({"error": "Projet inconnu"}), 404
    repo = project["repo"]
    files = list_github_repo_files("Yann", repo)
    return jsonify(files)

@routes_proxy.route("/proxy/github/<project_name>/read")
def read_file_from_repo(project_name):
    path = request.args.get("path", "")
    project = projects.get(project_name)
    if not project:
        return jsonify({"error": "Projet inconnu"}), 404
    repo = project["repo"]
    content = read_github_file("Yann", repo, path)
    return jsonify(content)

@routes_proxy.route("/proxy/gdrive/<project_name>")
def read_drive_file(project_name):
    file_id = request.args.get("file_id", "")
    if not file_id:
        return jsonify({"error": "file_id requis"}), 400
    content = read_google_drive_file(file_id)
    return jsonify(content)
