import os
import shutil
from agents.utils.logger import get_logger

logger = get_logger("CacheTools")

def purge_cache(folder):
    """
    Supprime tout le contenu d’un dossier de cache (fichiers et sous-dossiers).
    """
    if not os.path.isdir(folder):
        logger.warning(f"Dossier inexistant: {folder}")
        return False
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        try:
            if os.path.isdir(fpath):
                shutil.rmtree(fpath)
                logger.info(f"Dossier supprimé: {fpath}")
            else:
                os.remove(fpath)
                logger.info(f"Fichier supprimé: {fpath}")
        except Exception as e:
            logger.error(f"Erreur suppression {fpath}: {e}")
            continue
    return True

def purge_large_or_old_cache(folder, max_size_mb=50, max_files_to_keep=5):
    """
    Supprime les fichiers trop volumineux (>max_size_mb) et garde les X plus récents (max_files_to_keep).
    """
    if not os.path.isdir(folder):
        logger.warning(f"Dossier inexistant: {folder}")
        return False
    files = []
    for f in os.listdir(folder):
        full_path = os.path.join(folder, f)
        if os.path.isfile(full_path):
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            files.append((full_path, os.path.getmtime(full_path), size_mb))
    # 🔥 Supprimer les fichiers trop gros
    for path, _, size_mb in files:
        if size_mb > max_size_mb:
            logger.info(f"🧹 Fichier trop lourd supprimé : {os.path.basename(path)} ({int(size_mb)} Mo)")
            os.remove(path)
    # 📆 Supprimer les plus anciens (garder les X plus récents max)
    files.sort(key=lambda x: x[1], reverse=True)  # tri par date
    for path, _, _ in files[max_files_to_keep:]:
        logger.info(f"🧽 Suppression cache ancien : {os.path.basename(path)}")
        os.remove(path)
    return True
