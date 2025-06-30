# agents/utils/big_file_detector.py

import os

def detect_big_files(folder, threshold_mb=5):
    """
    Détecte les fichiers dont la taille dépasse un seuil (en Mo).
    Retourne une liste de tuples (fichier, taille Mo).
    """
    big_files = []
    for root, _, files in os.walk(folder):
        for f in files:
            path = os.path.join(root, f)
            try:
                size_mb = os.path.getsize(path) / (1024*1024)
                if size_mb > threshold_mb:
                    big_files.append((path, size_mb))
            except Exception:
                continue
    return big_files
