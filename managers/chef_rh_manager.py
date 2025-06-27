
from managers.base_manager import BaseManager
from agents.rh_agent import RhAgent

class ChefRhManager(BaseManager):
    def __init__(self):
        super().__init__("ChefRhManager")
        self.register_agent("rh", RhAgent())

    def handle_task(self, task):
        task_type = task.get("type")
        if task_type == "rh":
            return self.agents["rh"].execute(task)
        else:
            return {"error": f"Tâche inconnue pour RH : {task_type}"}
