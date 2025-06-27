
from managers.base_manager import BaseManager
from agents.data_analysis_agent import DataAnalysisAgent
from agents.optimize_agent import OptimizeAgent
from agents.project_doctor_agent import ProjectDoctorAgent

class ChefAnalyseManager(BaseManager):
    def __init__(self):
        super().__init__("ChefAnalyseManager")
        self.register_agent("data_analysis", DataAnalysisAgent())
        self.register_agent("optimize", OptimizeAgent())
        self.register_agent("doctor", ProjectDoctorAgent())

    def handle_task(self, task):
        task_type = task.get("type")
        if task_type == "analyze":
            return self.agents["data_analysis"].execute(task)
        elif task_type == "optimize":
            return self.agents["optimize"].execute(task)
        elif task_type == "diagnose":
            return self.agents["doctor"].execute(task)
        else:
            return {"error": f"Tâche inconnue pour Analyse : {task_type}"}
