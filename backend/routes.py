# backend/routes.py

from flask import Flask, request, jsonify, render_template
from agents.chef_agent import ChefOrchestreAgent
import os

# Configuration du chemin de template personnalisé
TEMPLATE_DIR = os.path.abspath("doctor_modules/templates")
app = Flask(__name__, template_folder=TEMPLATE_DIR)

chef = ChefOrchestreAgent(agents={})

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run():
    data = request.json
    task = data.get("task")
    if not task:
        return jsonify({"error": "No task provided"}), 400
    result = chef.handle_task(task)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
