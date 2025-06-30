from managers.base_manager import BaseManager
from agents.ux_agent import UXAgent

class ChefUXManager(BaseManager):
    """
    Manager UX : gère les tâches liées à l’expérience utilisateur (UI/UX).
    """
    def __init__(self):
        super().__init__("ChefUXManager")
        self.ux_agent = UXAgent()

    def dispatch(self, task):
        # Toutes les tâches UX passent par UXAgent (ajoute d’autres agents si besoin)
        return self.ux_agent.execute(task)

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
