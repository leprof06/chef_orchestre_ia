# 🤖 Chef d'Orchestre IA

Une IA locale modulaire capable de recevoir des instructions en langage naturel, de créer automatiquement des agents spécialisés (code, test, doc...), d'analyser un projet, et de proposer une interface utilisateur conviviale pour interagir avec les tâches, éditer le code généré, et le modifier manuellement si besoin.

---

## 🚀 Fonctionnalités principales

- 💬 Instructions en langage naturel (via interface chat)
- 🧠 Création automatique d'agents via `RHAgent`
- 🛠 Agents spécialisés : code, test, debug, doc, UX, optimisation, analyse, liaison API...
- 🔁 Réutilisation de code existant (GitHub, HuggingFace...)
- 📄 Analyse de projet complète via `ProjectDoctorAgent`
- 🧪 Tests automatisés générés
- 🛑 Fonction Pause/Play pour modifier le code manuellement
- 🖥 Interface HTML interactive
- 📦 Export du projet finalisé (zip + README auto)
- 🔐 Fonctionnement local avec option OpenAI ou HuggingFace

---

## 🧱 Architecture

```
chef_orchestre_ia/
├── orchestrator.py             # Lancement agents via ligne de commande (optionnel)
├── interface.py                # Point d'entrée principal avec interface web
├── config.py                   # Chargement de clés .env
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
├── doctor_modules/            # Analyse & auto-fix
│   ├── analysis/
│   ├── core/
│   └── ...
├── frontend/
│   └── interface.html          # Interface utilisateur complète
├── backend/routes/
│   └── routes.py               # API backend Flask
└── test/
    └── test_api_routes.py
```

---

## 🧪 Lancement

### Interface web (recommandée)

```bash
python interface.py
```

### Mode CLI (agents seuls)
```bash
python orchestrator.py
```

---

## 🔑 Configuration des clés API

Créez un fichier `.env` à la racine :

```
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf-...
```

Dans `config.py`, activez les options souhaitées :

```python
CONFIG = {
    "use_openai": True,
    "use_huggingface": False,
    ...
}
```

---

## 🧠 Exemple de commandes utilisateur

> "Corrige tous les fichiers Python dans le projet"

> "Génère un test unitaire pour le module optimize_agent"

> "Crée un agent pour surveiller les dépendances de sécurité"

> "Fais un programme de prise de rendez-vous chez le médecin automatiquement tous les mois"

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
| `/upload`      | POST    | Upload un fichier zip de projet         |
| `/files`       | GET     | Liste des fichiers disponibles          |
| `/file`        | GET/POST| Lire / sauvegarder un fichier           |
| `/toggle_pause`| POST    | Active / désactive le mode pause        |

---

## 🛡️ Licence

MIT - projet libre, améliorable en communauté
