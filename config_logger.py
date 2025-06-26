# config_logger.py

import logging
import os
from datetime import datetime

# Création du dossier logs si nécessaire
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Nom du fichier log avec timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(LOG_DIR, f"session_{timestamp}.log")

# Configuration globale du logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
