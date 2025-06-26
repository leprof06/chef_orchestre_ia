# agents/test_agent.py

from agents.base_agent import BaseAgent

class TestAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        # Logique de génération de tests automatiques
        return f"(Simulation) Tests générés pour : {task_description}"
