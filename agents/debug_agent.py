from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import check_python_syntax
from agents.utils.scan_vulnerabilities import scan_python_vuln
from agents.utils.logger import get_logger

class DebugAgent(BaseAgent):
    """
    Détecte les erreurs syntaxiques et potentielles failles dans le projet Python.
    Utilise check_python_syntax et scan_python_vuln des utils.
    """
    def __init__(self):
        super().__init__("DebugAgent")
        self.logger = get_logger("DebugAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        syntax = check_python_syntax(project_path)
        vuln = scan_python_vuln(project_path)
        result = {
            "syntax": syntax,
            "vulnerabilities": vuln,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
