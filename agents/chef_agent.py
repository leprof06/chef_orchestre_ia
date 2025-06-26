# agents/chef_agent.py

from agents.base_agent import BaseAgent

class ChefOrchestreAgent(BaseAgent):
    def __init__(self, agents):
        self.agents = agents

    def handle_task(self, task_description: str) -> str:
        # Simulation du dispatch : cherche un agent capable de traiter la tâche
        for agent_name, agent in self.agents.items():
            if hasattr(agent, 'handle_task'):
                result = agent.handle_task(task_description)
                if result:
                    return f"[{agent_name}] → {result}"
        return "Aucun agent n'a pu traiter cette tâche."
