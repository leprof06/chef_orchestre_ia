
from managers.base_manager import BaseManager
from agents.ux_agent import UxAgent
from agents.test_agent import TestAgent
from agents.doc_agent import DocAgent

class ChefUxManager(BaseManager):
    def __init__(self):
        super().__init__("ChefUxManager")
        self.register_agent("ux", UxAgent())
        self.register_agent("test", TestAgent())
        self.register_agent("doc", DocAgent())

    def handle_task(self, task):
        task_type = task.get("type")
        if task_type == "ux":
            return self.agents["ux"].execute(task)
        elif task_type == "test":
            return self.agents["test"].execute(task)
        elif task_type == "doc":
            return self.agents["doc"].execute(task)
        else:
            return {"error": f"Tâche inconnue pour UX : {task_type}"}
