import os
from generation.generate_todo_from_readme import generer_todo

DOSSIER_PROJETS = "H:/IA"  # à adapter si ton dossier s'appelle autrement


def scanner_et_generer_todos():
    projets = [d for d in os.listdir(DOSSIER_PROJETS) if os.path.isdir(os.path.join(DOSSIER_PROJETS, d))]

    if not projets:
        print("❌ Aucun projet trouvé dans le dossier.")
        return

    for projet in projets:
        print(f"\n📂 Analyse du projet : {projet}")
        chemin = os.path.join(DOSSIER_PROJETS, projet)
        generer_todo(chemin)


if __name__ == "__main__":
    scanner_et_generer_todos()
