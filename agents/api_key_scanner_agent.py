from agents.base_agent import BaseAgent
import os
from agents.utils.scan_secrets import scan_for_secrets
from agents.utils.logger import get_logger

class APIKeyScannerAgent(BaseAgent):
    """
    Scanne un dossier à la recherche de fuites de clés API ou secrets en dur.
    Utilise agents.utils.scan_secrets.scan_for_secrets pour la détection.
    """

    def __init__(self):
        super().__init__("APIKeyScannerAgent")
        self.logger = get_logger("APIKeyScannerAgent")

    def execute(self, task):
        folder = task.get("project_path")
        all_found = {}
        if not folder or not os.path.isdir(folder):
            return {"error": "Chemin projet invalide."}
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith((".py", ".js", ".env", ".json", ".yml", ".yaml")):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()
                        secrets = scan_for_secrets(content)
                        if secrets:
                            all_found[path] = secrets
                    except Exception as e:
                        self.logger.error(f"Erreur scan {path} : {e}")
        return {"api_key_leaks": all_found or "Aucune clé API trouvée."}
