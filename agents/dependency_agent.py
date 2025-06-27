import os
from agents.base_agent import BaseAgent
from agents.utils.dependency_utils import detect_and_install_dependencies

class DependencyAgent(BaseAgent):
    def __init__(self):
        super().__init__("DependencyAgent")

    def execute(self, task):
        folder_path = task.get("project_path")
        if not folder_path or not os.path.exists(folder_path):
            return {"error": "Chemin de projet invalide ou manquant."}

        try:
            detect_and_install_dependencies(folder_path)
            return {"result": "Analyse et installation des dépendances terminées."}
        except Exception as e:
            return {"error": f"Erreur lors de l'analyse des dépendances : {str(e)}"}
