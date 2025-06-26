# agents/ux_agent.py

from agents.base_agent import BaseAgent

class UXAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        # Analyse d'interface et suggestion d'améliorations UX
        suggestions = [
            "Ajouter des boutons clairs pour chaque action",
            "Utiliser une mise en page responsive",
            "Afficher des messages de confirmation après chaque tâche"
        ]
        return f"Suggestions UX pour '{task_description}':\n- " + "\n- ".join(suggestions)
