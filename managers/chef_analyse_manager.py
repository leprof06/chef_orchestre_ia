from managers.base_manager import BaseManager
from agents.data_analysis_agent import DataAnalysisAgent
from agents.api_key_scanner_agent import APIKeyScannerAgent
from agents.dependency_agent import DependencyAgent

class ChefAnalyseManager(BaseManager):
    """
    Manager analyse : centralise DataAnalysisAgent, APIKeyScannerAgent, DependencyAgent, etc.
    """
    def __init__(self):
        super().__init__("ChefAnalyseManager")
        self.agents = {
            "analyse_code": DataAnalysisAgent(),
            "scan_api_keys": APIKeyScannerAgent(),
            "dependency": DependencyAgent(),
        }

    def dispatch(self, task):
        task_type = task.get("type", "")
        project_path = task.get("project_path", None)
        if task_type in self.agents:
            # On passe project_path dans un dict si besoin
            return self.agents[task_type].execute({"project_path": project_path})
        elif task_type == "analyse_code":
            return self.agents["analyse_code"].execute({"project_path": project_path})
        else:
            return {"error": f"Type de tâche inconnu pour ChefAnalyseManager : '{task_type}'"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)

    def handle_task(self, task):
        # Permet d'être appelé directement depuis orchestrator/analyser route
        return self.dispatch(task)
