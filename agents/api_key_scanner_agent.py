import os
from agents.base_agent import BaseAgent

class APIKeyScannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("APIKeyScannerAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path or not os.path.exists(project_path):
            return {"error": "Chemin de projet invalide ou manquant."}

        keys_found = {}
        api_keywords = ["OPENAI_API_KEY", "HUGGINGFACE_TOKEN", "STRIPE_SECRET_KEY", "API_KEY", "TOKEN"]

        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith((".env", ".json", ".py", ".txt")):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            content = f.read()
                            for keyword in api_keywords:
                                if keyword in content:
                                    if file not in keys_found:
                                        keys_found[file] = []
                                    keys_found[file].append(keyword)
                    except Exception:
                        continue

        if not keys_found:
            return {"result": "Aucune clé API détectée dans le projet."}

        return {
            "result": "Clés API détectées dans certains fichiers.",
            "details": keys_found
        }
