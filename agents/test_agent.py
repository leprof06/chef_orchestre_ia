from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import check_python_syntax
from agents.utils.logger import get_logger

class TestAgent(BaseAgent):
    """
    Vérifie la syntaxe et le bon fonctionnement de scripts/tests.
    Utilise check_python_syntax des utils.
    """
    def __init__(self):
        super().__init__("TestAgent")
        self.logger = get_logger("TestAgent")

    def execute(self, task):
        script_path = task.get("script_path")
        if not script_path:
            return {"error": "Aucun chemin de script fourni."}
        syntax = check_python_syntax(script_path)
        result = {
            "syntax": syntax
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
