from agents.base_agent import BaseAgent
from agents.utils.project_structure import analyse_structure_globale
from agents.utils.project_overview import detect_capabilities
from agents.utils.logger import get_logger

class InfrastructureBuilderAgent(BaseAgent):
    """
    Analyse la structure globale du projet et prépare l'infrastructure requise (dossiers, fichiers, etc).
    Utilise analyse_structure_globale et detect_capabilities des utils.
    """
    def __init__(self):
        super().__init__("InfrastructureBuilderAgent")
        self.logger = get_logger("InfrastructureBuilderAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        structure = analyse_structure_globale(project_path)
        capabilities = detect_capabilities(project_path)
        result = {
            "structure": structure,
            "capabilities": capabilities,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
