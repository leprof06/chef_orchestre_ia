# agents/chef_agent.py

from agents.base_agent import BaseAgent

class ChefOrchestreAgent(BaseAgent):
    def __init__(self, agents):
        self.agents = agents

    def handle_task(self, task_description: str) -> str:
        # 1. ProjectDoctorAgent agit en priorité sur des requêtes complexes
        doctor_agent = self.agents.get("ProjectDoctorAgent")
        if doctor_agent:
            doctor_response = doctor_agent.handle_task(task_description)
            if doctor_response and "Tâche non reconnue" not in doctor_response:
                return f"[ProjectDoctorAgent] → {doctor_response}"

        # 2. Tenter de réutiliser du code existant avec ReuseCodeAgent
        reuse_agent = self.agents.get("ReuseCodeAgent")
        if reuse_agent:
            reused = reuse_agent.handle_task(task_description)
            if reused and "(Aucun code trouvé)" not in reused:
                return f"[ReuseCodeAgent] → {reused}"

        # 3. Sinon, demander à CodeAgent de générer le code
        code_agent = self.agents.get("CodeAgent")
        if code_agent:
            generated = code_agent.handle_task(task_description)
            return f"[CodeAgent] → {generated}"

        return "Aucun agent n'a pu traiter cette tâche."
