from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import check_python_syntax, check_json_syntax
from agents.utils.code_inspector import is_code_file, extract_code_structure
from agents.utils.docstring_extractor import extract_docstrings
from agents.utils.project_structure import analyser_fichier, analyse_structure_globale
from agents.utils.project_overview import should_analyze_file, detect_capabilities
from agents.utils.scan_vulnerabilities import scan_python_vuln
from agents.utils.logger import get_logger

class DataAnalysisAgent(BaseAgent):
    """
    Analyse le code source, détecte la structure, la qualité, les erreurs, les failles, etc.
    Utilise massivement les outils du dossier utils.
    """
    def __init__(self):
        super().__init__("DataAnalysisAgent")
        self.logger = get_logger("DataAnalysisAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}
        # Exemple : analyser la structure, checker la syntaxe
        structure = analyse_structure_globale(project_path)
        syntax_ok = check_python_syntax(project_path)
        vuln_report = scan_python_vuln(project_path)
        result = {
            "structure": structure,
            "syntax": syntax_ok,
            "vulnerabilities": vuln_report,
        }
        return result

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
