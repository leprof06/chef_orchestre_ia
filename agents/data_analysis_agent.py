import os
from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import analyze_folder_for_syntax

class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataAnalysisAgent")

    def execute(self, task):
        folder_path = task.get("project_path")
        if not folder_path or not os.path.exists(folder_path):
            return {"error": "Chemin de projet invalide ou manquant."}

        result = analyze_folder_for_syntax(folder_path)
        if not result:
            return {"result": "Aucune erreur de syntaxe détectée."}

        return {"result": "Erreurs détectées dans certains fichiers.", "details": result}
