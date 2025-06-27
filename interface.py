import sys
import os
import webbrowser
from dotenv import load_dotenv
from tkinter import Tk, filedialog

# Ajout du répertoire du projet au sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_logger import get_logger
from orchestrator import Orchestrator

# Chargement de .env
load_dotenv()
logger = get_logger(__name__)

PROJECT_FOLDER = None

def select_project_folder():
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choisissez le dossier du projet à analyser")
    return folder if folder else os.getenv("DEFAULT_PROJECT_FOLDER")

def parse_user_input(user_input, project_path=None):
    user_input = user_input.lower()

    if "analyse" in user_input or "scanner" in user_input:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path}
    elif "clé api" in user_input or "api key" in user_input:
        return {"manager": "analyse", "type": "detect_api_keys", "project_path": project_path}
    elif "dépendance" in user_input or "requirement" in user_input:
        return {"manager": "devops", "type": "manage_dependencies", "project_path": project_path}
    elif "génère" in user_input or "écris" in user_input:
        return {"manager": "code", "type": "generate_code", "project_path": project_path}
    elif "optimise" in user_input:
        return {"manager": "code", "type": "optimize_code", "project_path": project_path}
    elif "debug" in user_input or "corrige" in user_input:
        return {"manager": "code", "type": "debug_code", "project_path": project_path}
    elif "agent" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_agent"}
    elif "manager" in user_input and "crée" in user_input:
        return {"manager": "rh", "type": "create_manager"}
    elif "interface" in user_input or "ui" in user_input:
        return {"manager": "ux", "type": "analyze_ui", "project_path": project_path}
    else:
        return {"manager": "analyse", "type": "analyse_code", "project_path": project_path, "note": "🔍 Interprétation approximative"}

def main():
    global PROJECT_FOLDER

    print("\n🎯 Bienvenue dans Chef d'Orchestre IA !")
    print("Que souhaitez-vous faire :")
    print("1. Sélectionner un dossier existant")
    print("2. Créer un nouveau projet vide")
    print("3. Continuer sans projet (mode exploration)")
    print("4. Lancer l'interface chat")

    choice = input("\nVotre choix (1/2/3/4) : ")

    if choice == "1":
        PROJECT_FOLDER = select_project_folder()
        if not PROJECT_FOLDER or not os.path.isdir(PROJECT_FOLDER):
            logger.error("❌ Dossier non valide.")
            return
        logger.info(f"📁 Dossier sélectionné : {PROJECT_FOLDER}")
    elif choice == "2":
        path = input("Entrez le nom du nouveau dossier : ")
        os.makedirs(path, exist_ok=True)
        PROJECT_FOLDER = os.path.abspath(path)
        logger.info(f"📁 Nouveau dossier créé : {PROJECT_FOLDER}")
    elif choice == "3":
        logger.warning("⚠️ Aucune analyse de projet ne sera disponible.")
    elif choice == "4":
        index_path = os.path.abspath("frontend/index.html")
        if os.path.exists(index_path):
            webbrowser.open(f"file://{index_path}")
            logger.info("✅ Interface ouverte dans le navigateur.")
        else:
            logger.error("❌ Fichier index.html introuvable dans le dossier frontend.")
        return
    else:
        print("Choix invalide.")
        return

    orchestrator = Orchestrator()
    logger.info("🎬 Orchestrateur initialisé.")

    while True:
        task_input = input("\n🧠 Que souhaitez-vous faire ? (ou 'exit')\n> ")
        if task_input.lower() in ("exit", "quit"):
            break

        task = parse_user_input(task_input, PROJECT_FOLDER)
        response = orchestrator.dispatch_task(task)
        print(response)

if __name__ == "__main__":
    main()
