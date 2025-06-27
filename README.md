# 🤖 Chef d'Orchestre IA

Une IA locale modulaire capable de recevoir des instructions en langage naturel, de créer automatiquement des agents spécialisés (code, test, doc...), d'analyser un projet, et de proposer une interface utilisateur conviviale pour interagir avec les tâches, éditer le code généré, et le modifier manuellement si besoin.

---

## 🚀 Fonctionnalités principales

- 💬 Interface de chat intuitive via navigateur
- 🧠 Création automatique d'agents via `RHAgent`
- 🛠 Agents spécialisés : code, test, debug, doc, UX, optimisation, analyse, liaison API...
- 🔁 Réutilisation de code existant avec GitHub / HuggingFace
- 📄 Analyse de projet complète via `ProjectDoctorAgent`
- 🧪 Tests automatisés générés
- 🛑 Fonction Pause/Play pour modifier le code manuellement
- 🖥 Interface HTML interactive avec éditeur de fichiers
- 📦 Export du projet finalisé (zip + README auto)
- 🔐 Fonctionnement local avec ou sans API externes (OpenAI / HuggingFace)

---

## 🧱 Architecture

```
chef_orchestre_ia/
├── orchestrator.py             # Lancement agents en CLI (optionnel)
├── interface.py                # Interface web (point d'entrée recommandé)
├── config.py                   # Chargement des clés .env
├── config_logger.py            # Configuration des logs
├── .env                        # Stockage des clés API
├── requirements.txt
├── agents/
│   ├── base_agent.py
│   ├── chef_agent.py
│   ├── rh_agent.py
│   ├── code_agent.py
│   ├── test_agent.py
│   ├── debug_agent.py
│   ├── doc_agent.py
│   ├── optimize_agent.py
│   ├── ux_agent.py
│   ├── api_liaison_agent.py
│   ├── reuse_code_agent.py
│   └── project_doctor_agent.py
├── doctor_modules/
│   ├── analysis/
│   ├── core/
│   └── ...
├── frontend/
│   └── interface.html           # Interface utilisateur
├── backend/
│   └── routes/
│       └── routes.py            # API Flask
└── test/
    └── test_api_routes.py
```

---

## ▶️ Lancement

### 1. Installation des dépendances
```bash
pip install -r requirements.txt
```

### 2. Configuration des clés API
Créez un fichier `.env` à la racine :
```bash
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf-...
```
Configurez ensuite `config.py` :
```python
CONFIG = {
    "use_openai": True,
    "use_huggingface": False,
    ...
}
```

### 3. Lancement de l'application
```bash
python interface.py
```
Puis ouvrez votre navigateur à l'adresse : [http://localhost:5000](http://localhost:5000)

---

## 🧠 Exemples d’utilisation dans le chat

> "Corrige tous les fichiers Python dans le projet"

> "Génère un test unitaire pour le module optimize_agent"

> "Crée un agent pour surveiller les dépendances de sécurité"

> "Fais un programme de prise de rendez-vous automatique chez le médecin"

---

## 🌐 Interface Web

- Chat interactif avec les agents
- Upload de projet (zip)
- Édition de fichiers générés
- Suivi en temps réel des échanges
- Boutons : Pause / Reprise / Analyse Projet / Sauvegarde

---

## 🛠 API Flask

| Route           | Méthode | Description                             |
|----------------|---------|-----------------------------------------|
| `/run`         | POST    | Envoie une tâche à l'IA                  |
| `/upload`      | POST    | Upload d'un fichier zip de projet       |
| `/files`       | GET     | Liste les fichiers disponibles          |
| `/file`        | GET/POST| Lire / sauvegarder un fichier           |
| `/toggle_pause`| POST    | Active / désactive le mode pause        |

---

## 📦 Développement local sans cloud

Pour simuler les appels API sans internet :
```bash
export USE_REQUESTS_STUB=1
```
Prévoir un fichier `requests_stub.py` pour gérer les requêtes fictives.

---

## 🛡️ Licence

MIT - projet libre, améliorable en communauté
