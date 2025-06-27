from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from agents.chef_agent import ChefOrchestreAgent
from backend.routes.routes import register_all_routes
import os

app = Flask(__name__, template_folder="frontend/templates")
chef = ChefOrchestreAgent(agents={})

@app.route("/")
def index():
    return render_template("interface.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    result = chef.handle_task(task)
    return jsonify({"result": result})

# Enregistre les autres routes
register_all_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
