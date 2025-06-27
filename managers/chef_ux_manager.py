from managers.base_manager import BaseManager
from agents.ui_feedback_agent import UIFeedbackAgent

class ChefUXManager(BaseManager):
    def __init__(self):
        super().__init__("ChefUXManager")
        self.agents = {
            "ui_feedback": UIFeedbackAgent()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "analyze_ui":
            return self.agents["ui_feedback"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefUXManager"}
