# agents/base_agent.py

class BaseAgent:
    """
    Agent de base que tous les agents personnalisés doivent hériter.
    Fournit une interface commune pour l'exécution.
    """
    
    def __init__(self):
        super().__init__("CodeAgent")

    def execute(self, task):
        # Simule la génération de code (exemple simplifié)
        instruction = task.get("instruction") or "Aucune instruction fournie."
        return f"Code généré automatiquement pour l'instruction : '{instruction}'"