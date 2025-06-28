from managers.base_manager import BaseManager
from agents.ux_agent import UXAgent

class ChefUXManager(BaseManager):
    def __init__(self):
        super().__init__("ChefUXManager")
        self.agents = {
            "ui_feedback": UXAgent()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "analyze_ui":
            return self.agents["ui_feedback"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefUXManager"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
