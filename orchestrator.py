from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager

class Orchestrator:
    def __init__(self):
        # Instancie tes managers ici
        self.logs = []
        self.code_state = ""
        # Exemples de managers, adapte selon ton archi :
        # self.analyse_manager = AnalyseManager()
        # self.dev_manager = DevManager()
        # self.code_manager = CodeManager()
        # self.rh_manager = RHManager()
        # etc.

    def init_new_project(self):
        """Initialise un projet vierge."""
        self.logs = ["Projet vierge créé."]
        self.code_state = ""  # ou une structure par défaut
        # Appelle les managers pour préparer le projet si besoin

    def init_from_zip(self, zip_path):
        """Initialise le projet à partir d'un zip uploadé."""
        # Ici tu fais ce qu’il faut : extraction, analyse initiale, etc.
        self.logs = [f"Projet chargé depuis {zip_path}."]
        self.code_state = ""  # À mettre à jour selon le contenu du zip
        # Tu peux lancer une analyse rapide automatique ici si besoin

    def get_logs(self):
        """Retourne la liste (ou string) des logs à afficher sur le front."""
        return self.logs

    def get_code_state(self):
        """Retourne le code à afficher dans la zone code du front."""
        return self.code_state

    def analyse_project(self, project_path):
        """Appelle l’agent d’analyse via le manager, enregistre les logs."""
        # Appelle ton AnalyseManager/agent ici
        result = "Analyse terminée avec succès."  # ou résultat réel
        self.logs.append(result)
        return result

    def dispatch_task(self, task):
        """Redirige la tâche vers le bon manager/agent."""
        # Ce code existait déjà chez toi : tu routes vers le bon agent selon le type de task
        # Ex :
        manager = task.get("manager")
        action_type = task.get("type")
        project_path = task.get("project_path")
        # Tu routes ici (exemple) :
        if manager == "analyse":
            # res = self.analyse_manager.handle(action_type, project_path)
            res = f"Analyse demandée : {action_type} sur {project_path}"
        elif manager == "code":
            # res = self.code_manager.handle(action_type, project_path)
            res = f"Code demandé : {action_type} sur {project_path}"
        # etc.
        else:
            res = f"Tâche inconnue : {manager}/{action_type}"
        self.logs.append(str(res))
        return {"result": res}
    