from flask import Blueprint, request, jsonify
from orchestrator import Orchestrator

chat_bp = Blueprint("chat", __name__)
orchestrator = Orchestrator()

def parse_user_input(user_input, project_path=None):
    user_input = user_input.lower()
    if "analyse" in user_input or "scanner" in user_input:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path}
    elif "clé api" in user_input or "api key" in user_input:
        return {"manager": "analyse", "type": "detect_api_keys", "project_path": project_path}
    elif "dépendance" in user_input or "requirement" in user_input:
        return {"manager": "devops", "type": "manage_dependencies", "project_path": project_path}
    elif "génère" in user_input or "écris" in user_input:
        return {"manager": "code", "type": "generate_code", "project_path": project_path}
    elif "optimise" in user_input:
        return {"manager": "code", "type": "optimize_code", "project_path": project_path}
    elif "debug" in user_input or "corrige" in user_input:
        return {"manager": "code", "type": "debug_code", "project_path": project_path}
    elif "agent" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_agent"}
    elif "manager" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_manager"}
    elif "interface" in user_input or "ui" in user_input:
        return {"manager": "ux", "type": "analyze_ui", "project_path": project_path}
    else:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path, "note": "🔍 Interprétation approximative"}

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    project_path = data.get("project_path")  # Peut venir d’un champ global côté frontend

    if not user_input:
        return jsonify({"error": "Message vide"}), 400

    task = parse_user_input(user_input, project_path)
    response = orchestrator.dispatch_task(task)
    return jsonify(response)
