from managers.base_manager import BaseManager
from agents.infrastructure_builder_agent import InfrastructureBuilderAgent
from agents.global_project_scan_agent import GlobalProjectScanAgent
from agents.debug_agent import DebugAgent

class ChefDevopsManager(BaseManager):
    def __init__(self):
        super().__init__("ChefDevopsManager")
        self.agents = {
            "infrastructure_builder": InfrastructureBuilderAgent(),
            "global_project_scan": GlobalProjectScanAgent(),
            "debug": DebugAgent(),
        }

    # Toutes tes méthodes existantes sont conservées ici (ne rien supprimer)


    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "manage_dependencies":
            return self.agents["dependency"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefDevOpsManager"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
