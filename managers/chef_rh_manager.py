from managers.base_manager import BaseManager
from agents.rh_agent import RHAgent

class ChefRHManager(BaseManager):
    """
    Manager RH : gère les tâches liées aux ressources humaines (RH).
    """
    def __init__(self):
        super().__init__("ChefRHManager")
        self.rh_agent = RHAgent()

    def dispatch(self, task):
        task_type = task.get("type")
        # Un seul agent RH pour l'instant :
        return self.rh_agent.execute(task)

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
