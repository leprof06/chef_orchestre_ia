import os
import json
import logging
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from config.config import PROJECT_FOLDER
from core.client import query_openai_model  # utilisé pour les résumés

# 🔍 Config
HISTORY_FILE = Path(PROJECT_FOLDER) / Path("H:/IA/IA programeuse/data/history.json")
ARCHIVE_FOLDER = Path(PROJECT_FOLDER) / Path("H:/IA/IA programeuse/data/archives")
INDEX_FILE = Path(PROJECT_FOLDER) / Path("H:/IA/IA programeuse/data/history_index.json")
MAX_SIZE_MB = 500  # 💡 Ajuste ici si tu veux une taille plus petite ou plus grande

ARCHIVE_FOLDER.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("history_archiver")
logger.setLevel(logging.INFO)


def get_file_size_mb(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)


def summarize_suggestion(entry):
    content = entry.get("suggestion", "")[:1500]
    prompt = f"Voici une suggestion de l'IA :\n{content}\n\nFais-en un résumé en une phrase claire et concise."
    try:
        return query_openai_model(prompt)
    except Exception as e:
        logger.warning(f"❌ Erreur résumé OpenAI : {e}")
        return "Suggestion IA résumée (erreur OpenAI)"


def load_history():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            logger.error("❌ Erreur lors du chargement de history.json")
            return []


def save_archive(data):
    archive_name = f"history_archive_{uuid4().hex[:8]}.json"
    archive_path = ARCHIVE_FOLDER / archive_name
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"🔄 Archive enregistrée : {archive_name}")
    return archive_name


def update_index(entries, archive_name):
    index_data = {}
    if INDEX_FILE.exists():
        with open(INDEX_FILE, encoding="utf-8") as f:
            try:
                index_data = json.load(f)
            except json.JSONDecodeError:
                logger.warning("⚠️ Fichier index corrompu. Remplacement...")

    for entry in entries:
        name = entry.get("filename", f"unknown_{uuid4().hex[:6]}.py")
        index_data[name] = {
            "status": "archivé",
            "archive": archive_name,
            "summary": summarize_suggestion(entry),
            "date": datetime.now().isoformat()
        }

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    logger.info("📄 Index mis à jour.")


def archive_history_if_needed():
    if not HISTORY_FILE.exists():
        logger.warning("Aucun fichier history.json trouvé.")
        return

    size_mb = get_file_size_mb(HISTORY_FILE)
    if size_mb < MAX_SIZE_MB:
        logger.info(f"✅ Taille correcte ({size_mb:.2f} Mo)")
        return

    logger.warning(f"🚨 Taille ({size_mb:.2f} Mo) trop grande. Archivage...")
    history_data = load_history()

    if not history_data:
        logger.warning("⚠️ Aucun contenu à archiver.")
        return

    archive_name = save_archive(history_data)
    update_index(history_data, archive_name)

    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)
        logger.info("✅ Fichier history.json vidé avec succès.")
    except Exception as e:
        logger.error(f"❌ Impossible de vider le fichier history.json : {e}")


if __name__ == "__main__":
    archive_history_if_needed()
