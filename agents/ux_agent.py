from agents.base_agent import BaseAgent
from agents.utils.project_overview import detect_capabilities
from agents.utils.logger import get_logger

class UXAgent(BaseAgent):
    """
    UXAgent : analyse les capacités techniques pour améliorer l’UX.
    Utilise detect_capabilities des utils.
    """
    def __init__(self):
        super().__init__("UXAgent")
        self.logger = get_logger("UXAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        capabilities = detect_capabilities(project_path)
        result = {
            "capabilities": capabilities
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
