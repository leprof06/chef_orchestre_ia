import json
import os
from pathlib import Path

FILEMAP_DIR = Path("rapports/filemap")
PROJECT_FOLDER = Path("H:/IA")  # à adapter si nécessaire

BACKEND_KEYWORDS = ["flask", "route", "blueprint", "api"]
FRONTEND_KEYWORDS = ["react", "component", "html", "template", "jsx"]


def charger_structure_projet(nom_projet):
    structure_path = FILEMAP_DIR / f"structure_{nom_projet}.json"
    if structure_path.exists():
        with open(structure_path, encoding="utf-8") as f:
            return json.load(f)
    else:
        print(f"❌ Fichier introuvable : {structure_path}")
        return []


def générer_readme_depuis_structure(nom_projet, fichiers):
    backend_lines = [f"# 🧠 Structure Backend – {nom_projet}\n"]
    frontend_lines = [f"# 🎨 Structure Frontend – {nom_projet}\n"]

    for f in fichiers:
        description = f.get("description", "")
        line = f"- `{f['filename']}` : {description}"
        type_ = f.get("type", "")

        if any(k in type_.lower() or k in description.lower() for k in BACKEND_KEYWORDS):
            backend_lines.append(line)
        elif any(k in type_.lower() or k in description.lower() for k in FRONTEND_KEYWORDS):
            frontend_lines.append(line)

    dossier_projet = PROJECT_FOLDER / nom_projet

    with open(dossier_projet / "README_BACKEND.md", "w", encoding="utf-8") as f:
        f.write("\n".join(backend_lines))
    print(f"✅ README_BACKEND.md mis à jour dans {nom_projet}")

    with open(dossier_projet / "README_FRONTEND.md", "w", encoding="utf-8") as f:
        f.write("\n".join(frontend_lines))
    print(f"✅ README_FRONTEND.md mis à jour dans {nom_projet}")


def analyser_tous_les_projets():
    for fichier in FILEMAP_DIR.glob("structure_*.json"):
        nom = fichier.stem.replace("structure_", "")
        fichiers = charger_structure_projet(nom)
        générer_readme_depuis_structure(nom, fichiers)


if __name__ == "__main__":
    analyser_tous_les_projets()
