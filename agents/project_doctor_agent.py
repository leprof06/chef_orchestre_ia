# agents/project_doctor_agent.py

from agents.base_agent import BaseAgent
from doctor_modules.analysis.project_analysis import analyze_project
from doctor_modules.core.auto_fixer import auto_fix_project
from doctor_modules.generation.generate_global_report import generate_global_report

class ProjectDoctorAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        task_description = task_description.lower()

        if "analyse" in task_description:
            return analyze_project("workspace")  # dossier à scanner

        elif "corriger" in task_description or "fixer" in task_description:
            return auto_fix_project("workspace")

        elif "rapport" in task_description or "résumé" in task_description:
            return generate_global_report("workspace")

        return "Tâche non reconnue pour le ProjectDoctorAgent."
