from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager

class Orchestrator:
    def __init__(self):
        self.managers = {
            "analyse": ChefAnalyseManager(),
            "code": ChefCodeManager(),
            "devops": ChefDevOpsManager(),
            "rh": ChefRHManager(),
            "ux": ChefUXManager()
        }

    def dispatch_task(self, task):
        manager_role = task.get("manager")  # e.g. "analyse", "code", "devops", etc.
        if not manager_role or manager_role not in self.managers:
            return {"error": "Manager non spécifié ou inconnu."}

        return self.managers[manager_role].dispatch(task)
