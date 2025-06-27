from managers.base_manager import BaseManager
from agents.data_analysis_agent import DataAnalysisAgent
from agents.project_scanner_agent import GlobalProjectScanAgent
from agents.api_key_scanner_agent import APIKeyScannerAgent

class ChefAnalyseManager(BaseManager):
    def __init__(self):
        super().__init__("ChefAnalyseManager")
        self.agents = {
            "data_analysis": DataAnalysisAgent(),
            "global_scan": GlobalProjectScanAgent(),
            "api_key_scanner": APIKeyScannerAgent()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "analyse_code":
            return self.agents["data_analysis"].execute(task)
        elif task_type == "scan_projects":
            return self.agents["global_scan"].execute(task)
        elif task_type == "detect_api_keys":
            return self.agents["api_key_scanner"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefAnalyseManager"}
