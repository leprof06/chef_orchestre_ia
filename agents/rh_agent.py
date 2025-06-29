# agents/rh_agent.py

from .base_agent import BaseAgent
from config import CONFIG

try:
    import openai
except ImportError:
    openai = None

class RHAgent(BaseAgent):
    """
    Peut créer dynamiquement un nouvel agent ou manager sur demande.
    Génère le squelette Python correspondant et l'ajoute à l'équipe.
    """
    def __init__(self):
        super().__init__("RHAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def generate_agent_code(self, agent_name, role_desc):
        if self.has_openai:
            prompt = f"Crée une classe Python pour un agent nommé {agent_name} dont le rôle est : {role_desc}. Donne-moi juste le code Python."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Tu es expert en génération de classes Python pour des IA."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response["choices"][0]["message"]["content"].strip()
            except Exception as e:
                return f"Erreur OpenAI : {str(e)}"
        else:
            return f"# class {agent_name}(BaseAgent):\n    # Rôle : {role_desc}\n    pass\n"

    def execute(self, task):
        agent_name = task.get("agent_name", "NewAgent")
        role_desc = task.get("role_desc", "Agent spécialisé.")
        return {"generated_code": self.generate_agent_code(agent_name, role_desc)}
