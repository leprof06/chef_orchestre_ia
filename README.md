🤖 Chef d'Orchestre IA

Une IA locale modulaire pour gérer vos projets en langage naturel :

- Créez, analysez, optimisez, débugguez, documentez et développez vos projets depuis une interface web ultra intuitive.
- Orchestration automatique via un système PDG > Managers > Agents spécialisés.


🚀 **Fonctionnalités principales**

- 💬 Chat IA en français (navigateur) pour piloter votre projet
- 🧩 Architecture ultra-modulaire : orchestrateur, managers, agents
- 🧠 Agents spécialisés : code, test, analyse, doc, UX, gestion dépendances…
- 📦 Import de projet existant (zip), ou création de zéro
- 🔍 Analyse de code et détection de failles / erreurs / clés API
- 🛠️ Génération, optimisation, et correction de code automatique
- 🛑 Pause/Play pour éditer manuellement le code pendant la génération
- 🖥️ Interface HTML responsive avec éditeur et timeline des actions
- 📄 Export du projet complet (zip + README)
- 🔐 Fonctionne en local, avec gestion de clés API externes


🧱 **Architecture du projet**

chef_orchestre_ia/
├── app.py # Point d'entrée Flask (routes web + API)
├── orchestrator.py # Chef d'orchestre (route les tâches vers les managers)
├── managers/
│ ├── chef_analyse_manager.py # Manager d'analyse (analyse, scan, clé API)
│ ├── chef_code_manager.py # Manager code (génération, debug, optimisation)
│ ├── chef_devops_manager.py # Manager devops (dépendances)
│ ├── chef_rh_manager.py # Manager RH (agents, managers dynamiques)
│ └── chef_ux_manager.py # Manager UX (analyse interface)
├── agents/
│ ├── ... # Agents spécialisés, appelés par les managers
├── frontend/
│ └── templates/
│ ├── index.html # Accueil
│ ├── choose_project.html # Import projet existant (.zip)
│ └── chat.html # Interface principale (chat + logs + code)
├── workspace/ # (créé à l'exécution) : stockage temporaire des projets uploadés
├── requirements.txt # Liste des dépendances à installer
├── .env # Fichier de configuration des clés API (à créer, cf. plus bas)
└── README.md # Ce fichier

🛠️ **Installation & Prérequis**

1. **Cloner le projet**
    cd chef_orchestre_ia

2. **Créer un fichier `.env`** à la racine du projet (obligatoire pour renseigner vos clés API OpenAI et HuggingFace).  
   Exemple :
    OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxx

3. **Installer les dépendances Python**
    pip install -r requirements.txt

🚦 **Démarrage**
python app.py
Puis ouvrez http://localhost:5000 dans votre navigateur.

🖥️ Utilisation rapide

Nouveau projet : démarre un projet vierge et discutez avec l’IA.

Projet existant : importez votre code sous forme de .zip, analysez ou éditez-le.

Chat : tapez vos instructions (“Analyse mon code”, “Optimise ce fichier”, etc.)

Pause/Play : modifiez le code généré avant de relancer la génération automatique.

Analyse : lance une revue globale du projet par les agents.

Export : téléchargez le projet finalisé (ZIP) avec README généré.

💡 Clés API nécessaires

OpenAI : Créer une clé API OpenAI
HuggingFace : Créer une clé HuggingFace

Copiez vos clés dans .env (voir plus haut).
Si aucune clé n’est renseignée, l’IA utilisera uniquement les modules locaux.

🔍 Explication rapide des modules

app.py : Centralise toutes les routes Flask (web & API).

orchestrator.py : Le cerveau du projet : décode la demande utilisateur, choisit le manager, et agrège les logs/retours pour l’interface.

managers/ : Un manager par domaine (analyse, code, devops, RH, UX).

agents/ : Petits modules spécialisés (analyse, scan, code, test…).

frontend/templates/ : Les 3 templates HTML pour l’interface web.

workspace/ : Espace temporaire pour les fichiers uploadés pendant une session.

🔄 Extensibilité

Ajouter un agent ou manager : Copier un fichier existant dans managers/ ou agents/ et adapter.

Custom IA : Enrichir les méthodes handle() des managers ou les agents.

Front : Personnaliser les templates HTML/JS/CSS pour de nouvelles vues ou outils.

📋 Commandes utiles

Installer les dépendances :
pip install -r requirements.txt

Lancer le serveur :
python app.py

Mettre à jour les clés API :
Modifier .env à la racine

🙏 Remerciements & Contributions

Projet conçu par Yann (full-stack, IA pédagogique) avec le copilote GPT-CodeAssistant.

Pull requests, suggestions, forks bienvenus !

Pour toute question ou bug : ouvre une issue sur GitHub
👉 Voir les issues
ou contacte-moi directement sur GitHub !

Licence : MIT. Projet open-source, contributions bienvenues.