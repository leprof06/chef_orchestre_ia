from agents.base_agent import BaseAgent

class OptimizeAgent(BaseAgent):
    def __init__(self):
        super().__init__("OptimizeAgent")

    def execute(self, task):
        project_path = task.get("project_path", "")
        return f"Optimisation réalisée sur le projet : {project_path or '(aucun chemin)'}"
