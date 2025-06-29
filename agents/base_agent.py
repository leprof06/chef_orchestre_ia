# agents/base_agent.py
from agents.base_agent import BaseAgent

class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeAgent")

    def execute(self, task):
        # Simule la génération de code (exemple simplifié)
        instruction = task.get("instruction") or "Aucune instruction fournie."
        return f"Code généré automatiquement pour l'instruction : '{instruction}'"