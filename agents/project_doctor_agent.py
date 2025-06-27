# agents/project_doctor_agent.py
from agents.base_agent import BaseAgent
from doctor_modules.analysis.code_utils import is_code_file, extract_code_structure
from doctor_modules.core.auto_fixer import auto_fix_project
from doctor_modules.generation.generate_global_report import generate_global_report
from config_logger import get_logger

class ProjectDoctorAgent(BaseAgent):
    def __init__(self):
        self.logger = get_logger(__name__)

    def handle_task(self, task_description: str) -> str:
        task_description = task_description.lower()
        self.logger.info(f"Analyse de la tâche : {task_description}")

        if "analyse" in task_description:
            self.logger.info("→ Analyse du projet déclenchée")
            return analyze_project("workspace")

        elif "corriger" in task_description or "fixer" in task_description:
            self.logger.info("→ Correction automatique du projet déclenchée")
            return auto_fix_project("workspace")

        elif "rapport" in task_description or "résumé" in task_description:
            self.logger.info("→ Génération du rapport déclenchée")
            return generate_global_report("workspace")

        self.logger.warning("Tâche non reconnue pour le ProjectDoctorAgent")
        return "Tâche non reconnue pour le ProjectDoctorAgent."
