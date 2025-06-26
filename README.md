# 🤖 Chef d'Orchestre IA

Une IA locale modulaire capable de recevoir des instructions en langage naturel, de créer automatiquement des agents spécialisés (code, test, doc...), et d'opérer dans un environnement 100% local (avec option OpenAI ou HuggingFace).

---

## 🚀 Fonctionnalités principales

- 💬 Instructions en langage naturel
- 🧠 Création automatique d'agents via `RHAgent`
- 🛠 Agents spécialisés : code, test, debug, doc, UX, etc.
- 🔁 Réutilisation de code existant avec GitHub
- 📄 Rapport de santé global du projet avec `ProjectDoctorAgent`
- 🧪 Tests automatisés
- 🔐 Fonctionnement local sans dépendre du cloud (optionnel)
- 🧩 Interface web avec des routes dynamiques pour chat, analyse, auto-fix, etc.

---

## 🧱 Architecture

```
chef_orchestre_ia/
├── orchestrator.py
├── config.py
├── config_logger.py
├── .env
├── requirements.txt
├── agents/
│   ├── base_agent.py
│   ├── chef_agent.py
│   ├── code_agent.py
│   ├── rh_agent.py
│   ├── test_agent.py
│   ├── debug_agent.py
│   ├── doc_agent.py
│   ├── optimize_agent.py
│   ├── ux_agent.py
│   ├── data_analysis_agent.py
│   ├── api_liaison_agent.py
│   ├── reuse_code_agent.py
│   └── project_doctor_agent.py
├── doctor_modules/
│   ├── core/
│   ├── analysis/
│   ├── tools/
│   ├── routes/
│   └── templates/
├── frontend/
│   └── index.html
├── backend/
│   └── routes/
│       ├── __init__.py
│       ├── routes_chat.py
│       ├── routes_deep_analysis.py
│       ├── routes_analyze_full.py
│       ├── routes_auto_fix.py
│       ├── routes_auto_fix_combined.py
│       ├── routes_capabilities.py
│       ├── routes_feedback.py
│       └── routes_proxy.py
└── test/
    └── test_api_routes.py
```

---

## 🧪 Lancement

```bash
pip install -r requirements.txt
python -m backend.routes
```

---

## 🔑 Configuration des clés API

Créez un fichier `.env` à la racine :

```
OPENAI_API_KEY=sk-...
HUGGINGFACE_API_KEY=hf_...
```

Dans `config.py`, les options à activer :
```python
CONFIG = {
    "use_openai": True,
    "use_huggingface": False,
    ...
}
```

---

## 📦 Stub réseau local

Si vous souhaitez simuler les appels réseau sans accès Internet :
```bash
export USE_REQUESTS_STUB=1
```

Prévoir un fichier `requests_stub.py` dans le projet si nécessaire.

---

## 🧠 Exemple de commande utilisateur

> "Corrige tous les fichiers Python dans le projet"

> "Génère un test unitaire pour le module optimize_agent"

> "Crée un nouvel agent pour analyser les dépendances de sécurité"

---

## 🛡️ Licence

MIT - projet libre, améliorable en communauté
