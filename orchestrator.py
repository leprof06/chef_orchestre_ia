# orchestrator.py

from agents.chef_agent import ChefOrchestreAgent
from agents.rh_agent import RHAgent
from agents.code_agent import CodeAgent
from agents.test_agent import TestAgent
from agents.debug_agent import DebugAgent
from agents.doc_agent import DocAgent
from agents.optimize_agent import OptimizeAgent
from agents.api_liaison_agent import APILiaisonAgent
from agents.ux_agent import UXAgent
from agents.data_analysis_agent import DataAnalysisAgent
from agents.reuse_code_agent import ReuseCodeAgent
from agents.project_doctor_agent import ProjectDoctorAgent
from config_logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Initialisation des agents...")
    agents = {
        "CodeAgent": CodeAgent(),
        "TestAgent": TestAgent(),
        "DebugAgent": DebugAgent(),
        "DocAgent": DocAgent(),
        "OptimizeAgent": OptimizeAgent(),
        "APILiaisonAgent": APILiaisonAgent(),
        "UXAgent": UXAgent(),
        "DataAnalysisAgent": DataAnalysisAgent(),
        "ReuseCodeAgent": ReuseCodeAgent(),
        "ProjectDoctorAgent": ProjectDoctorAgent(),
    }

    logger.info("Lancement du Chef d'Orchestre...")
    chef = ChefOrchestreAgent(agents)

    while True:
        task = input("Que souhaitez-vous faire ? (ou 'exit')\n> ")
        if task.lower() in ("exit", "quit"):
            break
        response = chef.handle_task(task)
        print(response)

if __name__ == "__main__":
    main()
