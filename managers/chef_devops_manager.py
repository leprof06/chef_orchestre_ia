
from managers.base_manager import BaseManager
from agents.api_liaison_agent import ApiLiaisonAgent
from agents.dependency_agent import DependencyAgent

class ChefDevOpsManager(BaseManager):
    def __init__(self):
        super().__init__("ChefDevOpsManager")
        self.register_agent("api_liaison", ApiLiaisonAgent())
        self.register_agent("dependency", DependencyAgent())

    def handle_task(self, task):
        task_type = task.get("type")
        if task_type == "api_liaison":
            return self.agents["api_liaison"].execute(task)
        elif task_type == "dependency":
            return self.agents["dependency"].execute(task)
        else:
            return {"error": f"Tâche inconnue pour DevOps : {task_type}"}
