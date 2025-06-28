from managers.base_manager import BaseManager
from agents.code_agent import CodeAgent
from agents.optimize_agent import OptimizeAgent
from agents.debug_agent import DebugAgent

class ChefCodeManager(BaseManager):
    def __init__(self):
        super().__init__("ChefCodeManager")
        self.agents = {
            "code_generator": CodeAgent(),
            "code_optimizer": OptimizeAgent(),
            "code_debugger": DebugAgent()
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "generate_code":
            return self.agents["code_generator"].execute(task)
        elif task_type == "optimize_code":
            return self.agents["code_optimizer"].execute(task)
        elif task_type == "debug_code":
            return self.agents["code_debugger"].execute(task)
        else:
            return {"error": "Type de tâche inconnu pour ChefCodeManager"}

    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
