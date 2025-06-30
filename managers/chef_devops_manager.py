from managers.base_manager import BaseManager
from agents.dependency_agent import DependencyAgent
from agents.infrastructure_builder_agent import InfrastructureBuilderAgent
from agents.global_project_scan_agent import GlobalProjectScanAgent
from agents.debug_agent import DebugAgent

class ChefDevOpsManager(BaseManager):
    """
    Manager DevOps : gestion dépendances, infrastructure, debug et scan global projet.
    """
    def __init__(self):
        super().__init__("ChefDevOpsManager")
        self.dependency_agent = DependencyAgent()
        self.infrastructure_agent = InfrastructureBuilderAgent()
        self.global_project_scan_agent = GlobalProjectScanAgent()
        self.debug_agent = DebugAgent()

    # Méthodes dédiées, à adapter selon les besoins !

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "manage_dependencies":
            return self.dependency_agent.execute(task)
        elif task_type == "infrastructure_build":
            return self.infrastructure_agent.execute(task)
        elif task_type == "scan_global_project":
            return self.global_project_scan_agent.execute(task)
        elif task_type == "debug":
            return self.debug_agent.execute(task)
        else:
            return {"error": f"Type de tâche inconnu pour ChefDevOpsManager : {task_type}"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
