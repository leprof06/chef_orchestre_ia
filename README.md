# Chef Orchestre IA

Un système modulaire en Python orchestré par une IA centrale (ChefOrchestreAgent) qui délègue automatiquement des tâches à des agents spécialisés : génération de code, tests, documentation, debug, ergonomie, réutilisation de code GitHub, etc.

## 🧠 Fonctionnement général

1. L'utilisateur donne une consigne en langage naturel.
2. Le ChefOrchestre analyse la tâche.
3. Il répartit les sous-tâches aux bons agents.
4. Chaque agent travaille, retourne son résultat.
5. Le chef compile les retours et fournit une sortie complète.

## 🤖 Agents disponibles

- `CodeAgent` : génère du code Python
- `TestAgent` : crée des tests unitaires
- `DebugAgent` : corrige des bugs
- `DocAgent` : génère des README/docs
- `OptimizeAgent` : améliore le code
- `APILiaisonAgent` : vérifie la cohérence API front/back
- `UXAgent` : propose des améliorations UI/UX
- `DataAnalysisAgent` : analyse des jeux de données
- `RHAgent` : crée de nouveaux agents si besoin
- `ReuseCodeAgent` : recherche du code libre existant sur GitHub

## 🔧 Structure du projet

```
chef_orchestre_ia/
├── orchestrator.py
├── config.py
├── workspace/
├── agents/
│   ├── code_agent.py, test_agent.py, ...
├── backend/routes.py
├── frontend/index.html
├── test/test_api_routes.py
├── requirements.txt
└── README.md
```

## 🗝️ Configuration API

Dans `config.py`, renseignez :
```python
CONFIG = {
    "use_openai": True,
    "api_key_openai": "sk-...",
    ...
}
```

## ▶️ Lancement (mode API Flask)
```bash
pip install -r requirements.txt
python backend/routes.py
```
Puis allez sur `http://localhost:5000` ou utilisez l'interface HTML (`frontend/index.html`).
