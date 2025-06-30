from agents.base_agent import BaseAgent
from agents.utils.docstring_extractor import extract_docstrings
from agents.utils.file_tools import read_file_safe
from agents.utils.logger import get_logger

class DocAgent(BaseAgent):
    """
    Extrait et analyse la documentation (docstrings) des fichiers sources.
    Utilise extract_docstrings des utils.
    """
    def __init__(self):
        super().__init__("DocAgent")
        self.logger = get_logger("DocAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        docstrings = extract_docstrings(project_path)
        return {"docstrings": docstrings}

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
