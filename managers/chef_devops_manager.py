from managers.base_manager import BaseManager
from agents.dependency_agent import DependencyAgent

class ChefDevOpsManager(BaseManager):
    def __init__(self):
        super().__init__("ChefDevOpsManager")
        self.agents = {
            "dependency": DependencyAgent()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "manage_dependencies":
            return self.agents["dependency"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefDevOpsManager"}
