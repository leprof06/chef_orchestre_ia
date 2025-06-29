# agents/doc_agent.py

from .base_agent import BaseAgent
from config import CONFIG

try:
    import openai
except ImportError:
    openai = None

class DocAgent(BaseAgent):
    """
    Génère un README, des docstrings et de la documentation de projet.
    Utilise OpenAI si possible, sinon propose un README de base.
    """
    def __init__(self):
        super().__init__("DocAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def doc_with_openai(self, code, language="python"):
        if not self.has_openai:
            return None
        prompt = f"Génère la documentation détaillée (README, docstrings) pour ce code {language} :\n\n{code}\n"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Expert {language} et documentation technique."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def local_doc(self, code, language="python"):
        return f"# Documentation (MODE LOCAL)\n\n## Fichier principal\n\n```{language}\n{code[:300]}\n```\n\n# (Compléter à la main pour plus de détails)\n"

    def execute(self, task):
        code = task.get("code", "")
        language = task.get("language", "python")
        if self.has_openai:
            result = self.doc_with_openai(code, language)
        else:
            result = self.local_doc(code, language)
        return {"documentation": result}
