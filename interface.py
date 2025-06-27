from flask import Blueprint, request, jsonify, send_from_directory
import os
from agents.chef_agent import ChefOrchestreAgent
from doctor_modules.analysis.project_analyser import analyse_project

routes = Blueprint("routes", __name__)

chef = ChefOrchestreAgent(agents={})
paused = False
UPLOAD_FOLDER = "uploaded_projects"

@routes.route("/run", methods=["POST"])
def run():
    if paused:
        return jsonify({"result": "⏸ En pause. Reprenez pour continuer."})
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    result = chef.handle_task(task)
    return jsonify({"result": result})

@routes.route("/upload", methods=["POST"])
def upload():
    if "project" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["project"]
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    result = analyse_project(filepath)
    return jsonify({"result": result})

@routes.route("/toggle_pause", methods=["POST"])
def toggle_pause():
    global paused
    paused = not paused
    return jsonify({"paused": paused})

@routes.route("/files", methods=["GET"])
def list_files():
    files = []
    for root, dirs, filenames in os.walk(UPLOAD_FOLDER):
        for f in filenames:
            rel_path = os.path.relpath(os.path.join(root, f), UPLOAD_FOLDER)
            files.append(rel_path)
    return jsonify({"files": files})

@routes.route("/file", methods=["GET"])
def get_file():
    path = request.args.get("path")
    full_path = os.path.join(UPLOAD_FOLDER, path)
    if not os.path.isfile(full_path):
        return jsonify({"error": "File not found"}), 404
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    return jsonify({"content": content})

@routes.route("/file", methods=["POST"])
def save_file():
    data = request.json
    path = data.get("path")
    content = data.get("content")
    full_path = os.path.join(UPLOAD_FOLDER, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return jsonify({"result": "Fichier sauvegardé avec succès."})
