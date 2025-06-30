from managers.base_manager import BaseManager
from agents.code_agent import CodeAgent
from agents.optimize_agent import OptimizeAgent
from agents.doc_agent import DocAgent
from agents.test_agent import TestAgent
from agents.reuse_code_agent import ReuseCodeAgent

class ChefCodeManager(BaseManager):
    def __init__(self):
        super().__init__("ChefCodeManager")
        self.agents = {
            "code": CodeAgent(),
            "optimize": OptimizeAgent(),
            "doc": DocAgent(),
            "test": TestAgent(),
            "reuse_code": ReuseCodeAgent(),
        }

    def dispatch(self, task):
        task_type = task.get("type")

        if task_type == "generate_code":
            return self.agents["generate_code"].execute(task)
        elif task_type == "optimize_code":
            return self.agents["optimize_code"].execute(task)
        elif task_type == "debug_code":
            return self.agents["debug_code"].execute(task)
        else:
            return {"error": f"Type de tâche inconnu pour ChefCodeManager : {task_type}"}

    # Pour compatibilité avec Orchestrator
    def handle(self, action_type, project_path=None):
        task = {"type": action_type, "project_path": project_path}
        return self.dispatch(task)
