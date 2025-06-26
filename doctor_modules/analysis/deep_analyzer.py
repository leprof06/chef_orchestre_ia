import os
import json
from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from routes.routes import get_active_project_folder
from pathlib import Path
from datetime import datetime

scan_deep = Blueprint("deep_scan", __name__)
CACHE_PATH = Path("cache/deep_summary.json")
MAX_CACHE_SIZE_MB = 50
MAX_CACHE_BYTES = MAX_CACHE_SIZE_MB * 1024 * 1024

@scan_deep.route("/scan_deep_project")
def scan():
    """
    Analyse tous les fichiers du projet sélectionné en profondeur pour identifier :
    - Les fonctions, classes, décorateurs, imports
    - Affiche les fichiers ajoutés ou mis à jour depuis le dernier scan
    """
    scanned_files = {}
    updates = []

    if CACHE_PATH.exists():
        try:
            with open(CACHE_PATH, encoding="utf-8") as f:
                scanned_files = json.load(f)
                current_app.logger.info("✅ Résultats chargés depuis le cache.")
        except Exception as e:
            current_app.logger.warning(f"⚠️ Erreur lecture cache : {e}")

    new_scan = {}
    project_folder = get_active_project_folder()

    try:
        for root, dirs, files in os.walk(project_folder):
            for f in files:
                if f.endswith(('.py', '.html', '.json', '.env')):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8") as file:
                            content = file.read()
                            new_scan[path] = content
                            if path not in scanned_files:
                                updates.append((path, "🆕 Nouveau fichier détecté"))
                            elif scanned_files[path] != content:
                                updates.append((path, "♻️ Fichier mis à jour"))
                    except Exception as e:
                        updates.append((path, f"❌ Erreur de lecture : {e}"))

        # Écriture du nouveau cache avec limitation de taille
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        json_str = json.dumps(new_scan, indent=2, ensure_ascii=False)
        if len(json_str.encode("utf-8")) > MAX_CACHE_BYTES:
            current_app.logger.warning(f"⚠️ Résultat trop volumineux ({len(json_str) / 1024 / 1024:.2f} Mo). Cache non enregistré.")
            flash("⚠️ Résultat trop volumineux. Cache non sauvegardé.", "warning")
        else:
            with open(CACHE_PATH, "w", encoding="utf-8") as f:
                f.write(json_str)

        return render_template("scan_result.html", files=new_scan, updates=updates)

    except Exception as e:
        current_app.logger.error(f"Erreur d'analyse approfondie : {e}")
        return f"❌ Erreur pendant l'analyse : {e}"


@scan_deep.route("/purge_cache", methods=["POST"])
def purge_cache():
    """
    Supprime le cache JSON de l’analyse approfondie pour forcer une réanalyse complète.
    """
    try:
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()
            current_app.logger.info("♻️ Cache supprimé manuellement.")
        return redirect(url_for("scan_deep.scan"))
    except Exception as e:
        current_app.logger.error(f"Erreur lors du nettoyage du cache : {e}")
        return f"❌ Impossible de supprimer le cache : {e}"
