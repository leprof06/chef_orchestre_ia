# run.py
import sys
import os

# Ajout du chemin racine du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator import main

if __name__ == "__main__":
    main()
# This script serves as the entry point for the application.