# agents/utils/project_tools.py

import os
import json
import shutil
import zipfile

PROJECTS_FOLDER = "projects"  # Tu peux le rendre configurable si besoin

def get_projects_folder():
    if not os.path.exists(PROJECTS_FOLDER):
        os.makedirs(PROJECTS_FOLDER)
    return PROJECTS_FOLDER

def create_project(project_name):
    folder = os.path.join(get_projects_folder(), project_name)
    os.makedirs(folder, exist_ok=True)
    # Création d’un fichier état vide pour la sauvegarde
    with open(os.path.join(folder, "state.json"), "w", encoding="utf-8") as f:
        json.dump({}, f)
    return folder

def list_projects():
    folder = get_projects_folder()
    return [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]

def save_project_state(project_name, state):
    folder = os.path.join(get_projects_folder(), project_name)
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Projet {project_name} inexistant.")
    with open(os.path.join(folder, "state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def load_project_state(project_name):
    folder = os.path.join(get_projects_folder(), project_name)
    state_path = os.path.join(folder, "state.json")
    if not os.path.exists(state_path):
        return {}
    with open(state_path, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_project(project_name):
    folder = os.path.join(get_projects_folder(), project_name)
    if os.path.exists(folder):
        shutil.rmtree(folder)
        return True
    return False

def export_project(project_name, export_path):
    folder = os.path.join(get_projects_folder(), project_name)
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Projet {project_name} inexistant.")
    with zipfile.ZipFile(export_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder)
                zipf.write(file_path, arcname)
    return export_path

def import_project_from_zip(zip_path, project_name=None):
    dest_folder = get_projects_folder()
    if not project_name:
        # Récupère le nom du zip
        base = os.path.splitext(os.path.basename(zip_path))[0]
        project_name = base
    target = os.path.join(dest_folder, project_name)
    os.makedirs(target, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target)
    return project_name

def import_zip_file(zip_path):
    if not os.path.exists(zip_path):
        return False, "Fichier ZIP introuvable."
    try:
        extract_dir = os.path.splitext(zip_path)[0]
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        return True, f"Projet importé dans {extract_dir}"
    except Exception as e:
        return False, f"Erreur lors de l'import ZIP : {e}"