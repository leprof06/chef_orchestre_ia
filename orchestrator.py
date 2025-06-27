import sys
import os
import webbrowser
from dotenv import load_dotenv
from tkinter import Tk, filedialog

# Ajout du répertoire du projet au sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_logger import get_logger

# Chargement de .env
load_dotenv()

logger = get_logger(__name__)

# Définition globale (visible par les modules importés ensuite)
PROJECT_FOLDER = None

def select_project_folder():
    """Ouvre une fenêtre pour sélectionner un dossier."""
    root = Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Choisissez le dossier du projet à analyser")
    return folder if folder else os.getenv("DEFAULT_PROJECT_FOLDER")

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

    # Import dynamique des agents après sélection du projet
    from agents.chef_agent import ChefOrchestreAgent
    from agents.rh_agent import RHAgent
    from agents.code_agent import CodeAgent
    from agents.test_agent import TestAgent
    from agents.debug_agent import DebugAgent
    from agents.doc_agent import DocAgent
    from agents.optimize_agent import OptimizeAgent
    from agents.api_liaison_agent import APILiaisonAgent
    from agents.ux_agent import UXAgent
    from agents.data_analysis_agent import DataAnalysisAgent
    from agents.reuse_code_agent import ReuseCodeAgent
    from agents.project_doctor_agent import ProjectDoctorAgent

    logger.info("Initialisation des agents...")
    agents = {
        "CodeAgent": CodeAgent(),
        "TestAgent": TestAgent(),
        "DebugAgent": DebugAgent(),
        "DocAgent": DocAgent(),
        "OptimizeAgent": OptimizeAgent(),
        "APILiaisonAgent": APILiaisonAgent(),
        "UXAgent": UXAgent(),
        "DataAnalysisAgent": DataAnalysisAgent(),
        "ReuseCodeAgent": ReuseCodeAgent(),
        "ProjectDoctorAgent": ProjectDoctorAgent(),
    }

    logger.info("Lancement du Chef d'Orchestre...")
    chef = ChefOrchestreAgent(agents)

    while True:
        task = input("\n🧠 Que souhaitez-vous faire ? (ou 'exit')\n> ")
        if task.lower() in ("exit", "quit"):
            break
        response = chef.handle_task(task)
        print(response)

if __name__ == "__main__":
    main()
