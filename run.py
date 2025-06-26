# run.py

import sys
import os

# Assure-toi que le dossier du projet est dans sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from orchestrator import main

if __name__ == "__main__":
    main()
