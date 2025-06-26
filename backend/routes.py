# backend/routes.py

from flask import Flask, request, jsonify
from agents.chef_agent import ChefOrchestreAgent

# Exemple minimal sans instanciation dynamique
app = Flask(__name__)
chef = ChefOrchestreAgent(agents={})

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
