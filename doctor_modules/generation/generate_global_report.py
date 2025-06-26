import os
import json
from config.config import PROJECT_FOLDER

REPORT_FOLDER = os.path.join(PROJECT_FOLDER, "..", "rapports")
os.makedirs(REPORT_FOLDER, exist_ok=True)


def extract_readme_summary(project_path):
    readme_path = os.path.join(project_path, "README.md")
    if not os.path.exists(readme_path):
        return ""
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if "## 🚀 Objectif du projet" in line:
            return "".join(lines[i+1:i+6]).strip()
    return ""


def generate_project_report(project_path):
    report = {
        "nom": os.path.basename(project_path),
        "fichiers": [],
        "import_detectes": set(),
        "readme_resume": extract_readme_summary(project_path)
    }

    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, encoding="utf-8") as f:
                        contenu = f.read()
                        report["fichiers"].append(file)
                        for ligne in contenu.splitlines():
                            if ligne.strip().startswith("import") or ligne.strip().startswith("from"):
                                report["import_detectes"].add(ligne.strip())
                except Exception as e:
                    print(f"Erreur lecture {file}: {e}")

    report["import_detectes"] = list(report["import_detectes"])
    return report


def save_project_report(project_name, report_data):
    report_path = os.path.join(REPORT_FOLDER, f"rapport_{project_name}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)


def generate_global_summary():
    summary = {}
    for file in os.listdir(REPORT_FOLDER):
        if file.startswith("rapport_") and file.endswith(".json"):
            with open(os.path.join(REPORT_FOLDER, file), encoding="utf-8") as f:
                data = json.load(f)
                summary[data["nom"]] = data

    global_path = os.path.join(REPORT_FOLDER, "rapport_global.json")
    with open(global_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def scan_and_generate_report():
    for dossier in os.listdir(PROJECT_FOLDER):
        projet_path = os.path.join(PROJECT_FOLDER, dossier)
        if os.path.isdir(projet_path):
            rapport = generate_project_report(projet_path)
            save_project_report(dossier, rapport)
    generate_global_summary()


__all__ = ["scan_and_generate_report"]
