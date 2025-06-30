from agents.base_agent import BaseAgent
from agents.utils.project_scanner import scan_all_projects, extract_imports
from agents.utils.project_overview import should_analyze_file
from agents.utils.syntax_checker import analyze_folder_for_syntax
from agents.utils.scan_secrets import scan_for_secrets
from agents.utils.logger import get_logger

class GlobalProjectScanAgent(BaseAgent):
    """
    Scanne tous les projets du workspace, détecte les imports, la syntaxe, les secrets, etc.
    Utilise scan_all_projects, extract_imports, analyze_folder_for_syntax, scan_for_secrets, etc.
    """
    def __init__(self):
        super().__init__("GlobalProjectScanAgent")
        self.logger = get_logger("GlobalProjectScanAgent")

    def execute(self, task):
        workspace = task.get("workspace")
        if not workspace:
            return {"error": "Aucun chemin de workspace fourni."}
        projects = scan_all_projects(workspace)
        imports = extract_imports(workspace)
        syntax = analyze_folder_for_syntax(workspace)
        secrets = scan_for_secrets(workspace)
        result = {
            "projects": projects,
            "imports": imports,
            "syntax": syntax,
            "secrets": secrets,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
