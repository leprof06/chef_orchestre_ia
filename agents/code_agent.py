# agents/code_agent.py

from agents.base_agent import BaseAgent
import os
import openai
import requests
from config import CONFIG
from config_logger import get_logger

class CodeAgent(BaseAgent):
    def __init__(self):
        self.logger = get_logger(__name__)
        if CONFIG.get("use_openai"):
            openai.api_key = CONFIG.get("api_key_openai")

    def handle_task(self, task_description: str) -> str:
        self.logger.info(f"Génération de code demandée pour : {task_description}")

        if CONFIG.get("use_openai"):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Tu es un assistant qui génère du code propre et documenté."},
                        {"role": "user", "content": task_description}
                    ]
                )
                result = response["choices"][0]["message"]["content"].strip()
                self.logger.info("Code généré avec OpenAI")
                return result
            except Exception as e:
                self.logger.error(f"Erreur OpenAI : {e}")
                return f"Erreur OpenAI : {str(e)}"

        elif CONFIG.get("use_huggingface"):
            try:
                headers = {"Authorization": f"Bearer {CONFIG['api_key_huggingface']}"}
                payload = {"inputs": task_description}
                response = requests.post(
                    "https://api-inference.huggingface.co/models/bigcode/starcoder",
                    headers=headers,
                    json=payload
                )
                result = response.json().get("generated_text", "(Pas de réponse Hugging Face)")
                self.logger.info("Code généré avec HuggingFace")
                return result
            except Exception as e:
                self.logger.error(f"Erreur HuggingFace : {e}")
                return f"Erreur HuggingFace : {str(e)}"

        self.logger.info("Mode local activé - simulation")
        return f"[Mode local] Code simulé pour : {task_description}"
