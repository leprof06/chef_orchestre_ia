import os
import shutil

# Chemins des fichiers README de base
global_readme = "README_GLOBAL.md"
auteur_readme = "README_AUTEUR.md"

# Dossier contenant tous les projets
IA_ROOT_FOLDER = "H:/IA"

# Nouveau : pour fournir un aperçu lié à un fichier depuis un README
README_GLOBAL_PATH = os.path.join(IA_ROOT_FOLDER, global_readme)

def synchronize_readmes():
    """Copie les fichiers README globaux dans chaque projet si non déjà présents."""
    for projet in os.listdir(IA_ROOT_FOLDER):
        projet_path = os.path.join(IA_ROOT_FOLDER, projet)
        if os.path.isdir(projet_path):
            for readme_file in [global_readme, auteur_readme]:
                source = os.path.join(IA_ROOT_FOLDER, readme_file)
                target = os.path.join(projet_path, readme_file)

                if os.path.exists(source) and not os.path.exists(target):
                    shutil.copy(source, target)
                    print(f"✅ {readme_file} copié dans {projet}")
                elif not os.path.exists(source):
                    print(f"⚠️ Fichier source {readme_file} manquant dans le dossier racine.")

def get_readme_insight(filepath):
    """Retourne une explication ou un contexte associé à un fichier depuis le README global."""
    if not os.path.exists(README_GLOBAL_PATH):
        return ""

    try:
        with open(README_GLOBAL_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Normaliser le chemin et chercher un bloc marqué
        normalized_path = filepath.replace("\\", "/")
        marker = f"### {normalized_path}"

        if marker in content:
            bloc = content.split(marker, 1)[1]
            lines = bloc.strip().splitlines()
            extracted = []
            for line in lines:
                if line.startswith("###"):
                    break
                extracted.append(line)
            return "\n".join(extracted).strip()

    except Exception:
        pass

    return ""
