from agents.base_agent import BaseAgent
from agents.utils.project_overview import detect_capabilities
from agents.utils.code_inspector import extract_code_structure
from agents.utils.logger import get_logger

class OptimizeAgent(BaseAgent):
    """
    Analyse les capacités du projet et propose des pistes d’optimisation.
    Utilise detect_capabilities et extract_code_structure des utils.
    """
    def __init__(self):
        super().__init__("OptimizeAgent")
        self.logger = get_logger("OptimizeAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        capabilities = detect_capabilities(project_path)
        structure = extract_code_structure(project_path)
        result = {
            "capabilities": capabilities,
            "structure": structure,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
