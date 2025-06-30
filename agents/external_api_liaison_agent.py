from agents.base_agent import BaseAgent
from agents.utils.dependency_utils import detect_and_install_dependencies
from agents.utils.import_connectors import import_from_github, import_from_http, import_from_s3
from agents.utils.logger import get_logger

class ExternalAPILiaisonAgent(BaseAgent):
    """
    S'occupe de la gestion, liaison et intégration d'API externes au projet.
    Utilise dependency_utils et import_connectors des utils.
    """
    def __init__(self):
        super().__init__("ExternalAPILiaisonAgent")
        self.logger = get_logger("ExternalAPILiaisonAgent")

    def execute(self, task):
        api_source = task.get("api_source")
        project_path = task.get("project_path")
        if not api_source or not project_path:
            return {"error": "Source API ou chemin projet manquant."}
        if api_source.startswith("github.com"):
            result = import_from_github(api_source)
        elif api_source.startswith("s3://"):
            result = import_from_s3(api_source)
        elif api_source.startswith("http"):
            result = import_from_http(api_source)
        else:
            result = {"error": "Type de source API inconnu."}
        return {"import_result": result}

    # (autres méthodes métier à laisser inchangées si présentes dans ton fichier original)
