from flask import Flask, render_template, request, jsonify
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
    file_list = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                file_list.append(os.path.relpath(full_path))
    return jsonify(file_list)

@app.route("/file")
def get_file():
    path = request.args.get("path")
    if not path or not os.path.exists(path):
        return jsonify({"error": "Invalid file path"}), 400
    with open(path, "r", encoding="utf-8") as f:
        return jsonify({"content": f.read()})

@app.route("/file", methods=["POST"])
def save_file():
    data = request.json
    path = data.get("path")
    content = data.get("content")
    if not path:
        return jsonify({"error": "Path required"}), 400
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return jsonify({"result": "Fichier sauvegardé avec succès"})

# Enregistre toutes les routes supplémentaires
register_all_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
