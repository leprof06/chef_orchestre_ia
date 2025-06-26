import os
import shutil
import subprocess
import logging
from config.config import PROJECT_FOLDER

# Dossier de sauvegarde
BACKUP_FOLDER = os.path.join(PROJECT_FOLDER, "fichiers_fonctionnels_avant_modifications")
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def get_backup_path(file_path):
    """Construit le chemin de sauvegarde pour un fichier donné."""
    filename = os.path.basename(file_path)
    return os.path.join(BACKUP_FOLDER, filename)

def safe_apply_modification(file_path, new_content, test_command=None):
    """
    Sauvegarde l'ancien fichier, applique la nouvelle version,
    exécute les tests (optionnel), et restaure si erreur.
    """
    try:
        # 🔐 Étape 1 : sauvegarde
        backup_path = get_backup_path(file_path)
        shutil.copy(file_path, backup_path)
        logging.info(f"🗂 Fichier sauvegardé : {backup_path}")

        # 💾 Étape 2 : appliquer les modifications
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        # 🧪 Étape 3 : tester le projet (si test_command est fourni)
        if test_command:
            result = subprocess.run(test_command, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info("✅ Tests réussis, suppression de la sauvegarde")
                os.remove(backup_path)
                return True, result.stdout
            else:
                logging.warning("❌ Tests échoués, restauration du fichier précédent")
                restore_backup(file_path)
                return False, result.stdout

        # ✅ Aucun test spécifié → succès par défaut
        return True, "✅ Modifications appliquées (aucun test exécuté)."

    except Exception as e:
        logging.error(f"❌ Erreur lors de la mise à jour sécurisée : {e}")
        restore_backup(file_path)
        return False, str(e)

def restore_backup(file_path):
    """Restaure un fichier depuis le dossier de sauvegarde."""
    backup_path = get_backup_path(file_path)
    if os.path.exists(backup_path):
        shutil.copy(backup_path, file_path)
        logging.info(f"🔁 Fichier restauré depuis la sauvegarde : {file_path}")
    else:
        logging.warning(f"⚠️ Aucune sauvegarde disponible pour : {file_path}")

def cleanup_backup(file_path):
    """Supprime la sauvegarde associée au fichier donné."""
    backup_path = get_backup_path(file_path)
    if os.path.exists(backup_path):
        os.remove(backup_path)
        logging.info(f"🧹 Sauvegarde supprimée : {backup_path}")
