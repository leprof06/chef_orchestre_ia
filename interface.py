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

# Enregistre toutes les routes supplémentaires
register_all_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
