
from managers.base_manager import BaseManager
from agents.code_agent import CodeAgent
from agents.debug_agent import DebugAgent
from agents.reuse_code_agent import ReuseCodeAgent

class ChefCodeManager(BaseManager):
    def __init__(self):
        super().__init__("ChefCodeManager")
        self.register_agent("code", CodeAgent())
        self.register_agent("debug", DebugAgent())
        self.register_agent("reuse", ReuseCodeAgent())

    def handle_task(self, task):
        task_type = task.get("type")
        if task_type == "code":
            return self.agents["code"].execute(task)
        elif task_type == "debug":
            return self.agents["debug"].execute(task)
        elif task_type == "reuse":
            return self.agents["reuse"].execute(task)
        else:
            return {"error": f"Tâche inconnue pour Code : {task_type}"}
