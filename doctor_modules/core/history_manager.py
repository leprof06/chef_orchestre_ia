import json
from pathlib import Path
from datetime import datetime
import logging
from analysis.utils import load_json_file, save_json_file


HISTORY_PATH = Path("data") / "history.json"

def load_history():
    """Charge l'historique depuis le fichier JSON."""
    if HISTORY_PATH.exists():
        try:
            return load_json_file(HISTORY_PATH)
        except json.JSONDecodeError:
            logging.warning("⚠️ Le fichier JSON de l'historique est mal formé. Il a été ignoré.")
            return []
    return []

def save_proposal(filename, code, proposal, accepted):
    """Enregistre une proposition avec timestamp dans l'historique."""
    history = load_history()
    history.append({
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "filename": filename,
        "accepted": accepted,
        "code_snapshot": code,
        "proposal": proposal
    })
    save_json_file(HISTORY_PATH, history)

def already_proposed(file_or_context: str, user_input: str) -> bool:
    """
    Vérifie si une proposition a déjà été faite pour ce message et ce fichier.
    """
    history = load_history()
    for entry in history:
        if entry.get("filename") == file_or_context and entry.get("user") == user_input:
            return True
    return False

def get_last_proposal(filename):
    """Retourne la dernière proposition faite pour un fichier donné."""
    history = load_history()
    for entry in reversed(history):
        if entry["filename"] == filename:
            return entry["proposal"]
    return None
