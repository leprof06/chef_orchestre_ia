# agents/base_agent.py

class BaseAgent:
    """
    Agent de base que tous les agents personnalisés doivent hériter.
    Fournit une interface commune pour l'exécution.
    """
    def __init__(self, name="BaseAgent"):
        self.name = name

    def run(self, *args, **kwargs):
        raise NotImplementedError("La méthode 'run' doit être implémentée dans les sous-classes.")
