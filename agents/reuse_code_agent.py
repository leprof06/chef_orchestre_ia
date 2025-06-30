from agents.base_agent import BaseAgent
from agents.utils.code_inspector import is_code_file
from agents.utils.logger import get_logger
from agents.utils.project_scanner import extract_imports

class ReuseCodeAgent(BaseAgent):
    """
    Détecte les modules et fonctions réutilisables dans le code du projet.
    Utilise extract_imports et is_code_file des utils.
    """
    def __init__(self):
        super().__init__("ReuseCodeAgent")
        self.logger = get_logger("ReuseCodeAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        imports = extract_imports(project_path)
        reusable = is_code_file(project_path)
        result = {
            "imports": imports,
            "is_code_file": reusable,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
