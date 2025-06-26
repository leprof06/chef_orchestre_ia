import os

CACHE_FOLDER = "cache"
MAX_FILE_SIZE_MB = 50
MAX_FILES_TO_KEEP = 5

def purge_large_or_old_cache():
    files = []
    for f in os.listdir(CACHE_FOLDER):
        full_path = os.path.join(CACHE_FOLDER, f)
        if os.path.isfile(full_path):
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            files.append((full_path, os.path.getmtime(full_path), size_mb))

    # 🔥 Supprimer les fichiers trop gros
    for path, _, size_mb in files:
        if size_mb > MAX_FILE_SIZE_MB:
            print(f"🧹 Fichier trop lourd supprimé : {os.path.basename(path)} ({int(size_mb)} Mo)")
            os.remove(path)

    # 📆 Supprimer les plus anciens (garder les 5 plus récents max)
    files.sort(key=lambda x: x[1], reverse=True)  # tri par date
    for path, _, _ in files[MAX_FILES_TO_KEEP:]:
        print(f"🧽 Suppression cache ancien : {os.path.basename(path)}")
        os.remove(path)
