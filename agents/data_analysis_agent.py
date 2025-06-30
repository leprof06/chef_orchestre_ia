from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import analyze_folder_for_syntax
from agents.utils.code_inspector import extract_code_structure
from agents.utils.docstring_extractor import extract_docstrings
from agents.utils.project_structure import analyse_structure_globale
from agents.utils.project_overview import should_analyze_file, detect_capabilities
from agents.utils.scan_vulnerabilities import scan_python_vuln
from agents.utils.logger import get_logger

class DataAnalysisAgent(BaseAgent):
    """
    Analyse le code source : structure, qualité, erreurs, failles, docstrings, etc.
    Utilise les outils de utils (allégé au max).
    """
    def __init__(self):
        super().__init__("DataAnalysisAgent")
        self.logger = get_logger("DataAnalysisAgent")

    def execute(self, task):
        project_path = task.get("project_path")
        if not project_path:
            return {"error": "Aucun chemin de projet fourni."}

        self.logger.info(f"Analyse projet {project_path}")
        # Analyse la structure globale
        structure = analyse_structure_globale(project_path)
        # Vérifie la syntaxe de tous les fichiers 
        syntax_report = analyze_folder_for_syntax(project_path)
        # Cherche les vulnérabilités
        vuln_report = scan_python_vuln(project_path)
        # (Option) Extrait les docstrings de tous les .py
        docstrings = extract_docstrings(project_path)

        # Capabilities/global
        capabilities = detect_capabilities(project_path)

        result = {
            "structure": structure,
            "syntax": syntax_report,
            "vulnerabilities": vuln_report,
            "docstrings": docstrings,
            "capabilities": capabilities,
        }
        return result

    # (Autres méthodes éventuelles à laisser inchangées)
