# agents/rh_agent.py

from agents.base_agent import BaseAgent

class RHAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        # Simule la création dynamique d’un agent spécialisé
        return f"(Simulation) Nouvel agent simulé pour la tâche : {task_description}"
