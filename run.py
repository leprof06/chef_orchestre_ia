import sys
import os

# Ajoute le dossier racine du projet (celui contenant orchestrator.py) au sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from orchestrator import main

if __name__ == "__main__":
    main()
