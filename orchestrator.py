import os
import json
import shutil

from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager
from agents.utils.ai_router import chat_with_ia

PROJECTS_DIR = "projects"  # Dossier racine pour les projets

class Orchestrator:
    def __init__(self):
        os.makedirs(PROJECTS_DIR, exist_ok=True)
        self.logs = []
        self.projects = {}  # {project_name: {"path": ..., "state": ..., "code": ...}}
        self.code_state = ""
        self.current_project = None

        # Managers
        self.analyse_manager = ChefAnalyseManager()
        self.code_manager = ChefCodeManager()
        self.dev_manager = ChefDevOpsManager()
        self.rh_manager = ChefRHManager()
        self.ux_manager = ChefUXManager()

        self.load_all_projects()

    def load_all_projects(self):
        """Charge tous les projets existants dans le dossier local."""
        self.projects = {}
        for name in os.listdir(PROJECTS_DIR):
            path = os.path.join(PROJECTS_DIR, name)
            if os.path.isdir(path):
                code = self._read_file(os.path.join(path, "main.py"))
                state = self._read_json(os.path.join(path, "state.json"))
                self.projects[name] = {
                    "path": path,
                    "state": state,
                    "code": code
                }

    def _read_file(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    def _read_json(self, filepath):
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_project(self, project_name):
        proj = self.projects.get(project_name)
        if not proj:
            return False
        path = proj["path"]
        os.makedirs(path, exist_ok=True)
        # Sauve code
        code_file = os.path.join(path, "main.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write(proj.get("code", ""))
        # Sauve état
        state_file = os.path.join(path, "state.json")
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(proj.get("state", {}), f, indent=2, ensure_ascii=False)
        return True

    def create_new_project(self, project_name):
        path = os.path.join(PROJECTS_DIR, project_name)
        os.makedirs(path, exist_ok=True)
        self.projects[project_name] = {
            "path": path,
            "state": {},
            "code": "# Nouveau projet Python\n"
        }
        self.current_project = project_name
        self._save_project(project_name)
        self.logs.append(f"Nouveau projet '{project_name}' créé.")
        return True

    def get_existing_projects(self):
        return list(self.projects.keys())

    def load_project(self, project_name):
        if project_name in self.projects:
            self.current_project = project_name
            # Recharge code et state
            path = self.projects[project_name]["path"]
            self.projects[project_name]["code"] = self._read_file(os.path.join(path, "main.py"))
            self.projects[project_name]["state"] = self._read_json(os.path.join(path, "state.json"))
            self.logs.append(f"Projet '{project_name}' chargé.")
            return True
        return False

    def save_project(self, project_name):
        return self._save_project(project_name)

    def delete_project(self, project_name):
        if project_name in self.projects:
            shutil.rmtree(self.projects[project_name]["path"])
            del self.projects[project_name]
            if self.current_project == project_name:
                self.current_project = None
            self.logs.append(f"Projet '{project_name}' supprimé.")
            return True
        return False

    def export_project(self, project_name):
        # Zippe le dossier projet et retourne le chemin du zip
        if project_name in self.projects:
            folder = self.projects[project_name]["path"]
            zip_path = f"{folder}.zip"
            shutil.make_archive(folder, 'zip', folder)
            return True, zip_path
        return False, "Projet inexistant"

    def init_new_project(self):
        self.create_new_project(f"Projet_{len(self.projects)+1}")

    def init_from_zip(self, zip_path):
        """Importe un projet ZIP en local (extraction + indexation)."""
        import zipfile
        if not os.path.exists(zip_path):
            self.logs.append(f"ZIP non trouvé : {zip_path}")
            return False
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extract_dir = os.path.join(PROJECTS_DIR, os.path.splitext(os.path.basename(zip_path))[0])
            os.makedirs(extract_dir, exist_ok=True)
            zip_ref.extractall(extract_dir)
            # Ajoute le projet à la liste
            project_name = os.path.basename(extract_dir)
            self.projects[project_name] = {
                "path": extract_dir,
                "state": {},
                "code": self._read_file(os.path.join(extract_dir, "main.py"))
            }
            self.current_project = project_name
            self.logs.append(f"Projet chargé depuis {zip_path}.")
        return True

    def get_logs(self):
        """Retourne la liste des logs (timeline)."""
        return self.logs

    def get_code_state(self):
        """Retourne le code du projet courant."""
        if self.current_project:
            return self.projects[self.current_project]["code"]
        return ""

    def analyse_project(self, project_path=None):
        # Chemin du projet à analyser (ou courant si absent)
        if not project_path and self.current_project:
            project_path = self.projects[self.current_project]["path"]
        result = self.analyse_manager.handle("analyse_code", project_path)
        # Ajoute au log et retourne l'analyse
        if isinstance(result, dict):
            lines = [f"{key} : {value}" for key, value in result.items()]
            log_line = "Analyse du projet :\n" + "\n".join(lines)
        else:
            log_line = f"Analyse du projet : {result}"
        self.logs.append(log_line)
        return log_line

    def dispatch_task(self, task):
        """Router une tâche vers le bon manager/agent."""
        manager = task.get("manager")
        action_type = task.get("type")
        project_path = task.get("project_path")
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

    def chat(self, message):
        # Appel le router IA qui gère toutes les clés/API disponibles
        return chat_with_ia(message)
