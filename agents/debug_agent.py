# agents/debug_agent.py

from agents.base_agent import BaseAgent

class DebugAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        # Logique de détection et correction de bugs dans un code fourni
        return f"(Simulation) Correction appliquée pour : {task_description}"