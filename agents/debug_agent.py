from agents.base_agent import BaseAgent

class DebugAgent(BaseAgent):
    def __init__(self):
        super().__init__("DebugAgent")

    def execute(self, task):
        project_path = task.get("project_path", "")
        return f"Débogage effectué sur le projet : {project_path or '(aucun chemin)'}"
