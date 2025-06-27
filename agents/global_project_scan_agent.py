import os
from agents.base_agent import BaseAgent
from agents.utils.project_scanner import scan_all_projects

class GlobalProjectScanAgent(BaseAgent):
    def __init__(self):
        super().__init__("GlobalProjectScanAgent")

    def execute(self, task):
        base_path = task.get("scan_path")
        if not base_path or not os.path.exists(base_path):
            return {"error": "Chemin invalide ou manquant pour le scan global."}

        try:
            output_file = scan_all_projects(base_path)
            return {
                "result": f"Scan global terminé. Rapport généré : {output_file}"
            }
        except Exception as e:
            return {"error": f"Erreur lors du scan global : {str(e)}"}
