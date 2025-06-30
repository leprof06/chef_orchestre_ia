# agents/debug_agent.py

from agents.base_agent import BaseAgent
from config import CONFIG

try:
    import openai
except ImportError:
    openai = None
try:
    import requests
except ImportError:
    requests = None

class DebugAgent(BaseAgent):
    """
    Agent de debug avancé :
    - Reçoit un code ou un stacktrace
    - Cherche la cause probable du bug (IA ou analyse locale)
    - Propose des solutions concrètes (patch, ref, doc)
    """
    def __init__(self):
        super().__init__("DebugAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)
        self.has_hf = bool(CONFIG.get("use_huggingface") and requests)

    def local_debug(self, code, error):
        if "KeyError" in error:
            return "Vérifie que ta clé existe dans le dictionnaire avant d'accéder à sa valeur."
        elif "TypeError" in error:
            return "Vérifie les types des variables passées à cette fonction."
        return "Bug non reconnu en local. Essaie le mode IA !"

    def debug_with_openai(self, code, error):
        if not self.has_openai:
            return None
        prompt = f"Corrige ce code ou explique ce bug :\n\nCode :\n{code}\n\nErreur :\n{error}\n"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert en debug Python et JS."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def debug_with_huggingface(self, code, error):
        if not self.has_hf:
            return None
        return "Debug HuggingFace (à brancher sur un modèle code instruct)."

    def execute(self, task):
        code = task.get("code", "")
        error = task.get("error", "")
        if self.has_openai:
            res = self.debug_with_openai(code, error)
        elif self.has_hf:
            res = self.debug_with_huggingface(code, error)
        else:
            res = self.local_debug(code, error)
        return {"debug_result": res}
