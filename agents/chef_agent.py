from agents.base_agent import BaseAgent
from agents.utils.project_structure import analyser_fichier, analyse_structure_globale
from agents.utils.project_overview import should_analyze_file, detect_capabilities
from agents.utils.scan_vulnerabilities import scan_python_vuln
from agents.utils.scan_secrets import scan_for_secrets
from agents.utils.logger import get_logger

class ChefAgent(BaseAgent):
    """
    Chef d'orchestration d'analyse de projets, délègue les scans et analyses structurelles/fonctionnelles aux outils utils.
    """
    def __init__(self):
        super().__init__("ChefAgent")
        self.logger = get_logger("ChefAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        structure = analyse_structure_globale(project_path)
        secrets = scan_for_secrets(project_path)
        vuln_report = scan_python_vuln(project_path)
        result = {
            "structure": structure,
            "secrets": secrets,
            "vulnerabilities": vuln_report,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
