import os
from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager
from agents.utils.ai_router import chat_with_ia
from agents.utils.project_tools import (
    create_project, list_projects, save_project_state, load_project_state,
    delete_project, export_project, import_project_from_zip
)

class Orchestrator:
    def __init__(self):
        self.logs = []
        self.current_project = None
        self.projects = {name: {} for name in list_projects()}
        # Managers
        self.analyse_manager = ChefAnalyseManager()
        self.code_manager = ChefCodeManager()
        self.dev_manager = ChefDevOpsManager()
        self.rh_manager = ChefRHManager()
        self.ux_manager = ChefUXManager()

    # ----------- Gestion des projets -----------

    def create_new_project(self, project_name):
        if create_project(project_name):
            self.current_project = project_name
            self.logs.append(f"Nouveau projet '{project_name}' créé.")
            return True
        return False

    def get_existing_projects(self):
        return list_projects()

    def load_project(self, project_name):
        state = load_project_state(project_name)
        if state is not None:
            self.current_project = project_name
            self.logs.append(f"Projet '{project_name}' chargé.")
            return True
        return False

    def save_project(self, project_name):
        return save_project_state(project_name, {})

    def delete_project(self, project_name):
        ok = delete_project(project_name)
        if ok:
            self.logs.append(f"Projet '{project_name}' supprimé.")
            if self.current_project == project_name:
                self.current_project = None
        return ok

    def export_project(self, project_name):
        success, zip_path = export_project(project_name, export_path=None)
        if success:
            self.logs.append(f"Projet '{project_name}' exporté.")
        return success, zip_path

    def import_project(self, zip_path, project_name=None):
        ok = import_project_from_zip(zip_path, project_name)
        if ok:
            self.logs.append(f"Projet importé depuis {zip_path}.")
        return ok

    # ----------- Logs & état -----------

    def get_logs(self):
        return self.logs

    def get_code_state(self):
        if self.current_project:
            state = load_project_state(self.current_project)
            return state.get("code", "")
        return ""

    # ----------- Analyse & dispatch -----------

    def analyse_project(self, project_path=None):
        if not project_path and self.current_project:
            project_path = self.current_project
        result = self.analyse_manager.handle("analyse_code", project_path)
        log_line = f"Analyse du projet : {result}"
        self.logs.append(log_line)
        return log_line

    def dispatch_task(self, task):
        manager = task.get("manager")
        action_type = task.get("type")
        project_path = task.get("project_path", self.current_project)
        if manager == "analyse":
            res = self.analyse_manager.handle(action_type, project_path)
        elif manager == "code":
            res = self.code_manager.handle(action_type, project_path)
        elif manager == "devops":
            res = self.dev_manager.handle(action_type, project_path)
        elif manager == "rh":
            res = self.rh_manager.handle(action_type, project_path)
        elif manager == "ux":
            res = self.ux_manager.handle(action_type, project_path)
        else:
            res = f"[Orchestrator] Tâche inconnue : {manager}/{action_type}"
        self.logs.append(str(res))
        return {"result": res}

    # ----------- IA chat -----------

    def chat(self, message):
        return chat_with_ia(message)

