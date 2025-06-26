import os

README_FILENAME = "README_PROJECT.md"
TODO_FILENAME = "todo.md"
README_BACKEND = "README_BACKEND.md"
README_FRONTEND = "README_FRONTEND.md"

# Mots-clés pour repérage
BUG_KEYWORDS = ["bug", "erreur", "problème", "crash", "ne fonctionne pas", "incorrect"]
FIX_KEYWORDS = ["corriger", "corrigé", "fix", "amélioration", "à faire", "à corriger", "proposer"]


def extraire_lignes_utiles(texte):
    lignes = texte.splitlines()
    lignes_utiles = []
    for ligne in lignes:
        ligne_basse = ligne.lower()
        if any(mot in ligne_basse for mot in BUG_KEYWORDS + FIX_KEYWORDS):
            lignes_utiles.append(ligne.strip())
    return lignes_utiles


def charger_contenu_fichier(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def generer_todo(project_path):
    todo_path = os.path.join(project_path, TODO_FILENAME)

    contenu_sources = ""
    for nom in [README_FILENAME, README_BACKEND, README_FRONTEND]:
        contenu_sources += charger_contenu_fichier(os.path.join(project_path, nom)) + "\n"

    lignes = extraire_lignes_utiles(contenu_sources)

    if not lignes:
        print(f"ℹ️ Aucun bug ou amélioration détecté dans les README.")
        return

    with open(todo_path, "w", encoding="utf-8") as f:
        f.write("# 📝 Liste des bugs et améliorations détectés\n\n")
        f.write("## 🐛 Bugs\n")
        for ligne in lignes:
            if any(mot in ligne.lower() for mot in BUG_KEYWORDS):
                f.write(f"- [ ] {ligne}\n")

        f.write("\n## 🚀 Améliorations prévues\n")
        for ligne in lignes:
            if any(mot in ligne.lower() for mot in FIX_KEYWORDS):
                f.write(f"- [ ] {ligne}\n")

    print(f"✅ Fichier todo.md généré dans : {project_path}")
