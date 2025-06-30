from agents.base_agent import BaseAgent
from agents.utils.project_structure import analyse_structure_globale
from agents.utils.syntax_checker import analyze_folder_for_syntax
from agents.utils.scan_secrets import scan_for_secrets
from agents.utils.logger import get_logger

class RHAgent(BaseAgent):
    """
    RHAgent : évalue la structure projet, la syntaxe et la confidentialité (fuites de secrets) pour l’aspect "équipe/ressources humaines".
    Utilise les utils project_structure, syntax_checker, scan_secrets.
    """
    def __init__(self):
        super().__init__("RHAgent")
        self.logger = get_logger("RHAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        structure = analyse_structure_globale(project_path)
        syntax = analyze_folder_for_syntax(project_path)
        secrets = scan_for_secrets(project_path)
        result = {
            "structure": structure,
            "syntax": syntax,
            "secrets": secrets,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
