# agents/external_api_miaison_agent.py

from agents.base_agent import BaseAgent
import os
import re
from agents.utils.logger import get_logger
import requests

try:
    import openai
except ImportError:
    openai = None
from config import CONFIG

class ExternalAPIMiaisonAgent(BaseAgent):
    """
    Analyse le projet pour repérer toutes les dépendances à des API externes connues.
    Utilise OpenAI si possible, sinon des heuristiques locales.
    """
    COMMON_API_HINTS = [
        ("openai", r"openai[\.\[]"),
        ("huggingface", r"huggingface|transformers[\.\[]"),
        ("github", r"github[\.\[]"),
        ("deepl", r"deepl[\.\[]"),
        ("stripe", r"stripe[\.\[]"),
        ("google", r"google\.cloud|googleapiclient|googlemaps"),
    ]

    def __init__(self):
        super().__init__("ExternalAPIMiaisonAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def scan_file(self, path):
        hits = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for api, pattern in self.COMMON_API_HINTS:
                    if re.search(pattern, content, re.I):
                        hits.append(api)
        except Exception:
            pass
        return set(hits)

    def local_scan(self, folder):
        apis = set()
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith((".py", ".js", ".json", ".yml", ".yaml")):
                    path = os.path.join(root, f)
                    apis |= self.scan_file(path)
        return list(apis)

    def scan_with_openai(self, folder):
        if not self.has_openai:
            return None
        files = []
        for root, _, fs in os.walk(folder):
            for f in fs:
                if f.endswith((".py", ".js", ".json")):
                    try:
                        with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                            files.append(file.read()[:800])
                    except Exception:
                        pass
        prompt = (
            "Liste toutes les APIs externes (ex : openai, huggingface, github, stripe, etc.) utilisées ou nécessaires dans ce projet :"
            + "\n\n".join(files[:5])
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un auditeur d'intégrations API dans le code."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI: {str(e)}"

    def execute(self, task):
        folder = task.get("project_path")
        if not folder or not os.path.isdir(folder):
            return {"error": "Chemin projet invalide."}
        if self.has_openai:
            ai_result = self.scan_with_openai(folder)
            return {"external_apis": ai_result}
        apis = self.local_scan(folder)
        return {"external_apis": apis or "Aucune API externe détectée."}
