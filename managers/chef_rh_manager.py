from managers.base_manager import BaseManager
from agents.agent_factory import AgentFactory

class ChefRHManager(BaseManager):
    def __init__(self):
        super().__init__("ChefRHManager")
        self.agents = {
            "factory": AgentFactory()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "create_agent":
            return self.agents["factory"].create_agent(task)
        elif task_type == "create_manager":
            return self.agents["factory"].create_manager(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefRHManager"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
