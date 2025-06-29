from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager

class Orchestrator:
    def __init__(self):
        self.logs = []
        self.code_state = ""
        # Instancie tous tes managers personnalisés
        self.analyse_manager = ChefAnalyseManager()
        self.code_manager = ChefCodeManager()
        self.dev_manager = ChefDevOpsManager()
        self.rh_manager = ChefRHManager()
        self.ux_manager = ChefUXManager()

    def init_new_project(self):
        """Initialise un projet vierge."""
        self.logs = ["Projet vierge créé."]
        self.code_state = "# Nouveau projet Python\n"
        # Option : tu peux appeler ici des méthodes de manager si besoin

    def init_from_zip(self, zip_path):
        """Initialise le projet à partir d'un zip uploadé."""
        # Place ici ton extraction/initialisation réelle si besoin
        self.logs = [f"Projet chargé depuis {zip_path}."]
        self.code_state = "# Code extrait du ZIP (simulé)\n"

    def get_logs(self):
        """Retourne les logs à afficher dans la timeline frontend."""
        return self.logs

    def get_code_state(self):
        """Retourne le code du projet courant à afficher (peut être enrichi)."""
        return self.code_state

    def analyse_project(self, project_path):
        result = self.analyse_manager.handle("analyse_code", project_path)
        # Si c’est un dict, formatte pour l’affichage :
        if isinstance(result, dict):
            lines = []
            for key, value in result.items():
                lines.append(f"{key} : {value}")
            log_line = "Analyse du projet :\n" + "\n".join(lines)
        else:
            log_line = f"Analyse du projet : {result}"
        self.logs.append(log_line)
        return log_line

    def dispatch_task(self, task):
        """Router une tâche vers le bon manager/agent."""
        manager = task.get("manager")
        action_type = task.get("type")
        project_path = task.get("project_path")
        # Appelle le bon manager selon le mapping
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
        self.logs.append(res)
        return {"result": res}
