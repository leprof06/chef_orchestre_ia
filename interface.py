from flask import Flask, render_template, request, jsonify, send_from_directory
from agents.chef_agent import ChefOrchestreAgent
from backend.routes.routes import register_all_routes
import os

app = Flask(__name__, template_folder="frontend/templates")
chef = ChefOrchestreAgent(agents={})

is_paused = False

@app.route("/")
def index():
    return render_template("interface.html")

@app.route("/run", methods=["POST"])
def run():
    global is_paused
    if is_paused:
        return jsonify({"result": "Execution paused."})
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    result = chef.handle_task(task)
    return jsonify({"result": result})

@app.route("/toggle_pause", methods=["POST"])
def toggle_pause():
    global is_paused
    is_paused = not is_paused
    return jsonify({"paused": is_paused})

@app.route("/files")
def list_files():
    files = []
    for root, _, filenames in os.walk("."):
        for f in filenames:
            if f.endswith(".py") and "__pycache__" not in root:
                path = os.path.join(root, f).replace("\\", "/")
                files.append(path[2:] if path.startswith("./") else path)
    return jsonify({"files": files})

@app.route("/file", methods=["GET"])
def read_file():
    path = request.args.get("path")
    if not path or not os.path.isfile(path):
        return jsonify({"error": "Invalid file path."}), 400
    with open(path, "r", encoding="utf-8") as f:
        return jsonify({"content": f.read()})

@app.route("/file", methods=["POST"])
def write_file():
    data = request.json
    path = data.get("path")
    content = data.get("content")
    if not path or not os.path.isfile(path):
        return jsonify({"error": "Invalid file path."}), 400
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return jsonify({"success": True})

# Enregistre toutes les routes supplémentaires
register_all_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
