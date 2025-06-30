# agents/infrastructure_builder_agent.py

from agents.base_agent import BaseAgent
from config import CONFIG

try:
    import openai
except ImportError:
    openai = None

class InfrastructureBuilderAgent(BaseAgent):
    """
    Génère des fichiers d'infrastructure pour le projet (Dockerfile, docker-compose, workflows CI/CD).
    Peut aussi créer la structure de dossiers conseillée.
    """
    def __init__(self):
        super().__init__("InfrastructureBuilderAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def infra_with_openai(self, stack="python"):
        if not self.has_openai:
            return None
        prompt = f"Génère une arborescence de projet moderne et les fichiers d'infra associés (Dockerfile, docker-compose, GitHub Actions) pour un projet {stack}."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Expert DevOps et CI/CD {stack}."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def local_infra(self, stack="python"):
        infra = {
            "folders": ["src/", "tests/", "docs/", "infra/", "data/"],
            "dockerfile": "FROM python:3.11\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD ['python', 'app.py']",
            "github_actions": ".github/workflows/ci.yml"
        }
        return infra

    def execute(self, task):
        stack = task.get("stack", "python")
        if self.has_openai:
            result = self.infra_with_openai(stack)
        else:
            result = self.local_infra(stack)
        return {"infrastructure": result}
