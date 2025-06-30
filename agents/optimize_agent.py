# agents/optimize_agent.py

from .base_agent import BaseAgent
from config import CONFIG
from agents.utils.file_tools import read_file_safe, write_file_safe
from agents.utils.logger import get_logger

import openai
import requests

class OptimizeAgent(BaseAgent):
    """
    Agent d'optimisation :
    - Prend un code, propose un refactoring ou une amélioration
    - Utilise OpenAI/HF si possible, sinon règle simple (formatage auto)
    """
    def __init__(self):
        super().__init__("OptimizeAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)
        self.has_hf = bool(CONFIG.get("use_huggingface") and requests)

    def optimize_with_openai(self, code, language):
        if not self.has_openai:
            return None
        prompt = f"Optimise et modernise ce code {language} :\n\n{code}\n\nDonne une version plus efficace et bien commentée."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Expert {language} en clean code et optimisation."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def optimize_with_huggingface(self, code, language):
        if not self.has_hf:
            return None
        return "Optimisation HuggingFace (à brancher sur modèle code instruct)."

    def local_optimize(self, code, language):
        if language == "python":
            try:
                import autopep8
                return autopep8.fix_code(code)
            except ImportError:
                return code + "\n# (autopep8 non dispo, installe le package pour formatage auto)"
        return code + "\n// (Pas d'optimisation locale dispo)"

    def execute(self, task):
        code = task.get("code", "")
        language = task.get("language", "python")
        if self.has_openai:
            res = self.optimize_with_openai(code, language)
        elif self.has_hf:
            res = self.optimize_with_huggingface(code, language)
        else:
            res = self.local_optimize(code, language)
        return {"optimized_code": res}
