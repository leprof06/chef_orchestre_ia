import os
import subprocess
import logging
from orchestrator import PROJECT_FOLDER
from core.install_utils import check_and_install_packages
from detection.capability_detector import detect_capabilities
from analysis.utils import load_json_file

logger = logging.getLogger("auto_fixer")

AUTO_FIX_LOG = os.path.join(PROJECT_FOLDER, "rapports", "auto_fixer_log.txt")

# 📦 Dépendances de base qu'on pourrait détecter dans les projets
DEFAULT_REQUIRED_PACKAGES = ["flask", "openai", "requests", "dotenv", "pytest"]


def log_auto_fix(message):
    with open(AUTO_FIX_LOG, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    logger.info(message)


def auto_fix_project(project_path):
    log_auto_fix(f"🧠 Tentative de correction automatique pour {project_path}")

    # Étape 1 : installer les dépendances principales
    check_and_install_packages(*DEFAULT_REQUIRED_PACKAGES)
    log_auto_fix("✅ Dépendances principales installées")

    # Étape 2 : lancer les tests
    try:
        result = subprocess.run(["pytest", project_path], capture_output=True, text=True)
        log_auto_fix("🔍 Résultat des tests :")
        log_auto_fix(result.stdout)

        if result.returncode == 0:
            log_auto_fix("✅ Tous les tests sont passés avec succès.")
            return True
        else:
            log_auto_fix("⚠️ Des tests ont échoué. Tentative de correction IA possible...")
            # ➕ ICI tu pourras appeler ta fonction generate_code_proposal() si besoin
            # (à intégrer dans la suite de l’automatisation si autorisé)
            return False

    except Exception as e:
        log_auto_fix(f"❌ Erreur lors du test : {e}")
        return False


def auto_fix_all_projects():
    for name in os.listdir(PROJECT_FOLDER):
        full_path = os.path.join(PROJECT_FOLDER, name)
        if os.path.isdir(full_path):
            auto_fix_project(full_path)


if __name__ == "__main__":
    auto_fix_all_projects()
