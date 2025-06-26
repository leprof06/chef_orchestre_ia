# agents/chef_agent.py

from agents.base_agent import BaseAgent
from agents.rh_agent import RHAgent
from config_logger import get_logger

class ChefOrchestreAgent(BaseAgent):
    def __init__(self, agents):
        self.agents = agents
        self.rh_agent = RHAgent()
        self.logger = get_logger(__name__)

    def handle_task(self, task_description: str) -> str:
        self.logger.info(f"Nouvelle tâche reçue : {task_description}")

        # 1. ProjectDoctorAgent agit en priorité sur des requêtes complexes
        doctor_agent = self.agents.get("ProjectDoctorAgent")
        if doctor_agent:
            doctor_response = doctor_agent.handle_task(task_description)
            if doctor_response and "Tâche non reconnue" not in doctor_response:
                self.logger.info("Tâche déléguée à ProjectDoctorAgent")
                return f"[ProjectDoctorAgent] → {doctor_response}"

        # 2. Tenter de réutiliser du code existant avec ReuseCodeAgent
        reuse_agent = self.agents.get("ReuseCodeAgent")
        if reuse_agent:
            reused = reuse_agent.handle_task(task_description)
            if reused and "(Aucun code trouvé)" not in reused:
                self.logger.info("Tâche déléguée à ReuseCodeAgent")
                return f"[ReuseCodeAgent] → {reused}"

        # 3. Sinon, demander à CodeAgent de générer le code
        code_agent = self.agents.get("CodeAgent")
        if code_agent:
            generated = code_agent.handle_task(task_description)
            self.logger.info("Tâche déléguée à CodeAgent")
            return f"[CodeAgent] → {generated}"

        # 4. Dernier recours : création d’un nouvel agent avec RHAgent
        result = self.rh_agent.handle_task(task_description, self.agents)
        self.logger.warning("Aucun agent disponible. RHAgent sollicité pour créer un nouvel agent.")
        return f"[RHAgent] → {result}"
