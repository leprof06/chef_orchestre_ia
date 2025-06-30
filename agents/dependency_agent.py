from agents.base_agent import BaseAgent
from agents.utils.dependency_utils import detect_missing_python_dependencies, is_package_installed, detect_and_install_dependencies
from agents.utils.requirements_parser import parse_requirements, parse_package_json
from agents.utils.logger import get_logger

class DependencyAgent(BaseAgent):
    """
    Gère la détection et l'installation des dépendances du projet (Python, Node, etc).
    Utilise dependency_utils et requirements_parser des utils.
    """
    def __init__(self):
        super().__init__("DependencyAgent")
        self.logger = get_logger("DependencyAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        missing = detect_missing_python_dependencies(project_path)
        reqs = parse_requirements(project_path)
        result = {
            "missing_dependencies": missing,
            "requirements": reqs,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
