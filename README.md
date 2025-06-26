# Chef d'Orchestre IA

Ce dépôt contient un petit système d'orchestration écrit en Python. Il expose deux agents :

- **APILiaisonAgent** : interagit avec l'API GitHub pour rechercher des dépôts.
- **ReuseCodeAgent** : récupère le contenu des README des dépôts trouvés.

L'orchestrateur (`orchestrator.py`) utilise ces agents pour afficher un extrait de README correspondant à une requête de recherche.

## Arborescence des fichiers importants

```
agents/
    __init__.py           # Exporte les agents
    api_liaison_agent.py  # Requêtes GitHub avec gestion d'erreurs
    reuse_code_agent.py   # Récupération des README
orchestrator.py           # Point d'entrée principal
```

## Exécution

```bash
python orchestrator.py
```

L'orchestrateur recherche des dépôts relatifs au mot-clé `python` et affiche la première ligne de leur README.

## Dépendances

- Python 3.12 ou plus récent
- `requests` (pour les appels HTTP)

Installez `requests` si nécessaire :

```bash
pip install requests
```
