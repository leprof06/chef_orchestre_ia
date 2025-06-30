from agents.base_agent import BaseAgent
from agents.utils.code_inspector import extract_code_structure
from agents.utils.docstring_extractor import extract_docstrings
from agents.utils.syntax_checker import check_python_syntax
from agents.utils.project_overview import detect_capabilities
from agents.utils.logger import get_logger

class CodeAgent(BaseAgent):
    """
    Analyse, restructure et documente le code du projet.
    Utilise extract_code_structure, extract_docstrings, check_python_syntax, etc.
    """
    def __init__(self):
        super().__init__("CodeAgent")
        self.logger = get_logger("CodeAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        structure = extract_code_structure(project_path)
        docstrings = extract_docstrings(project_path)
        syntax = check_python_syntax(project_path)
        capabilities = detect_capabilities(project_path)
        result = {
            "structure": structure,
            "docstrings": docstrings,
            "syntax": syntax,
            "capabilities": capabilities,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
