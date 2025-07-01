import os
from managers.chef_analyse_manager import ChefAnalyseManager
from managers.chef_code_manager import ChefCodeManager
from managers.chef_devops_manager import ChefDevOpsManager
from managers.chef_rh_manager import ChefRHManager
from managers.chef_ux_manager import ChefUXManager
from agents.utils.ai_router import chat_with_ia
from agents.utils.project_tools import (
    create_project,
    list_projects,
    save_project_state,
    load_project_state,
    delete_project,
    export_project,
    import_project_from_zip,
    import_project_from_local_folder,
    import_project_from_github,
    import_project_from_gdrive,
    import_project_from_dropbox,
    import_project_from_icloud,
    import_project_from_s3,
    import_project_from_http,
    import_project_from_ftp,
    import_project_from_svn,
    import_project_from_bitbucket,
    import_project_from_gitlab,
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

    # ----------- Project management -----------

    def create_new_project(self, project_name):
        ok, msg = create_project(project_name)
        if ok:
            self.current_project = project_name
            self.logs.append(f"New project '{project_name}' created.")
            return True
        self.logs.append(f"Failed to create project '{project_name}': {msg}")
        return False

    def get_existing_projects(self):
        return list_projects()

    def load_project(self, project_name):
        state = load_project_state(project_name)
        if state is not None:
            self.current_project = project_name
            self.logs.append(f"Project '{project_name}' loaded.")
            return True
        self.logs.append(f"Failed to load project '{project_name}'.")
        return False

    def save_project(self, project_name, state=None):
        state = state or {}
        ok = save_project_state(project_name, state)
        if ok:
            self.logs.append(f"Project '{project_name}' saved.")
        else:
            self.logs.append(f"Failed to save project '{project_name}'.")
        return ok

    def delete_project(self, project_name):
        ok = delete_project(project_name)
        if ok:
            self.logs.append(f"Project '{project_name}' deleted.")
            if self.current_project == project_name:
                self.current_project = None
        else:
            self.logs.append(f"Failed to delete project '{project_name}'.")
        return ok

    def export_project(self, project_name):
        success, zip_path = export_project(project_name)
        if success:
            self.logs.append(f"Project '{project_name}' exported to '{zip_path}'.")
        else:
            self.logs.append(f"Failed to export project '{project_name}': {zip_path}")
        return success, zip_path

    # ----------- Imports from multiple sources -----------

    def import_project_from_zip(self, zip_path, project_name=None):
        ok, msg = import_project_from_zip(zip_path, project_name)
        if ok:
            self.logs.append(f"Imported ZIP: {msg}")
        else:
            self.logs.append(f"ZIP import failed: {msg}")
        return ok

    def import_project_from_local_folder(self, folder_path, project_name=None):
        ok, msg = import_project_from_local_folder(folder_path, project_name)
        if ok:
            self.logs.append(f"Imported folder: {msg}")
        else:
            self.logs.append(f"Folder import failed: {msg}")
        return ok

    def import_project_from_github(self, github_url, token=None):
        ok, msg = import_project_from_github(github_url, token)
        if ok:
            self.logs.append(f"Imported GitHub: {msg}")
        else:
            self.logs.append(f"GitHub import failed: {msg}")
        return ok

    def import_project_from_gdrive(self, gdrive_id, gdrive_token=None):
        ok, msg = import_project_from_gdrive(gdrive_id, gdrive_token)
        if ok:
            self.logs.append(f"Imported Google Drive: {msg}")
        else:
            self.logs.append(f"Google Drive import failed: {msg}")
        return ok

    def import_project_from_dropbox(self, dropbox_link, dropbox_token=None):
        ok, msg = import_project_from_dropbox(dropbox_link, dropbox_token)
        if ok:
            self.logs.append(f"Imported Dropbox: {msg}")
        else:
            self.logs.append(f"Dropbox import failed: {msg}")
        return ok

    def import_project_from_icloud(self, icloud_url, icloud_token=None):
        ok, msg = import_project_from_icloud(icloud_url, icloud_token)
        if ok:
            self.logs.append(f"Imported iCloud: {msg}")
        else:
            self.logs.append(f"iCloud import failed: {msg}")
        return ok

    def import_project_from_s3(self, s3_url, aws_access_key=None, aws_secret_key=None):
        ok, msg = import_project_from_s3(s3_url, aws_access_key, aws_secret_key)
        if ok:
            self.logs.append(f"Imported S3: {msg}")
        else:
            self.logs.append(f"S3 import failed: {msg}")
        return ok

    def import_project_from_http(self, http_url):
        ok, msg = import_project_from_http(http_url)
        if ok:
            self.logs.append(f"Imported HTTP: {msg}")
        else:
            self.logs.append(f"HTTP import failed: {msg}")
        return ok

    def import_project_from_ftp(self, ftp_url, ftp_user=None, ftp_pass=None):
        ok, msg = import_project_from_ftp(ftp_url, ftp_user, ftp_pass)
        if ok:
            self.logs.append(f"Imported FTP: {msg}")
        else:
            self.logs.append(f"FTP import failed: {msg}")
        return ok

    def import_project_from_svn(self, svn_url):
        ok, msg = import_project_from_svn(svn_url)
        if ok:
            self.logs.append(f"Imported SVN: {msg}")
        else:
            self.logs.append(f"SVN import failed: {msg}")
        return ok

    def import_project_from_bitbucket(self, bitbucket_url, token=None):
        ok, msg = import_project_from_bitbucket(bitbucket_url, token)
        if ok:
            self.logs.append(f"Imported Bitbucket: {msg}")
        else:
            self.logs.append(f"Bitbucket import failed: {msg}")
        return ok

    def import_project_from_gitlab(self, gitlab_url, token=None):
        ok, msg = import_project_from_gitlab(gitlab_url, token)
        if ok:
            self.logs.append(f"Imported GitLab: {msg}")
        else:
            self.logs.append(f"GitLab import failed: {msg}")
        return ok

    # ----------- Logs & state -----------

    def get_logs(self):
        return self.logs

    def get_code_state(self):
        if self.current_project:
            state = load_project_state(self.current_project)
            return state.get("code", "")
        return ""

    # ----------- Analysis & task dispatch -----------

    def analyse_project(self, project_path=None):
        if not project_path and self.current_project:
            project_path = self.current_project
        result = self.analyse_manager.handle("analyse_code", project_path)
        log_line = f"Project analysis: {result}"
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
            res = f"[Orchestrator] Unknown task: {manager}/{action_type}"
        self.logs.append(str(res))
        return {"result": res}

    # ----------- Chat with AI -----------

    def chat(self, message):
        return chat_with_ia(message)
