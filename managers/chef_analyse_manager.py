from managers.base_manager import BaseManager
from agents.data_analysis_agent import DataAnalysisAgent
from agents.api_key_scanner_agent import APIKeyScannerAgent
from agents.external_api_liaison_agent import ExternalAPILiaisonAgent  # à commenter si ce fichier/agent n'existe pas

class ChefAnalyseManager(BaseManager):
    def __init__(self):
        super().__init__("ChefAnalyseManager")
        self.agents = {
            "data_analysis": DataAnalysisAgent(),
            "api_key_scanner": APIKeyScannerAgent(),
            # "external_api_liaison": ExternalAPILiaisonAgent(),  # à activer si tu veux
        }

    def dispatch(self, task):
        task_type = task.get("type")
        if task_type == "analyse_code":
            return self.agents["data_analysis"].execute(task)
        elif task_type == "detect_api_keys":
            return self.agents["api_key_scanner"].execute(task)
        # elif task_type == "external_api_liaison":
        #     return self.agents["external_api_liaison"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefAnalyseManager"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)

    def handle_task(self, params):
        return self.dispatch(params)

    # Toutes les autres méthodes/metiers déjà présentes dans ta classe sont conservées ci-dessous !
