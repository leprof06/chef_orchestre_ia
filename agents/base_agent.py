from agents.utils.dependency_utils import detect_missing_python_dependencies, is_package_installed, detect_and_install_dependencies
from agents.utils.docstring_extractor import extract_docstrings
from agents.utils.import_connectors import import_zip_file, import_from_github, import_from_gdrive, import_from_dropbox, import_from_icloud, import_from_s3, import_from_http, import_from_ftp, import_from_svn, import_from_bitbucket, import_from_gitlab
from agents.utils.scan_vulnerabilities import scan_python_vuln, scan_node_vuln
# ... ajoute d'autres imports utils selon les besoins du reste du fichier ...

# TODO : toute fonction précédemment copiée dans ce fichier et présente dans un utils a été supprimée.
# Utilise systématiquement les fonctions importées ci-dessus !

class BaseAgent:
    """
    Agent de base que tous les agents personnalisés doivent hériter.
    Fournit une interface commune pour l'exécution.
    """
    def __init__(self, name="BaseAgent"):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError("La méthode 'run' doit être implémentée dans les sous-classes.")

