# agents/doc_agent.py

from agents.base_agent import BaseAgent

class DocAgent(BaseAgent):
    def handle_task(self, task_description: str) -> str:
        # Génère un README ou une doc simple à partir d'une description
        template = f"""# Documentation générée automatiquement\n\n## Objectif\n{task_description}\n\n## Contenu\n- Description des modules\n- Instructions d'utilisation\n- Informations techniques\n"""
        return template
