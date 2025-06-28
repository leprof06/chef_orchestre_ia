# agents/reuse_code_agent.py

import requests
import logging
import base64
from typing import Dict
from .api_key_scanner_agent import APIKeyScannerAgent
from config_logger import get_logger
import os

class ReuseCodeAgent:
    def __init__(self, api_agent: APIKeyScannerAgent | None = None) -> None:
        self.logger = get_logger(__name__)
        self.api_agent = api_agent or APIKeyScannerAgent()

    def handle_task(self, query: str) -> str | None:
        if requests is None:
            self.logger.error("La bibliothèque 'requests' n'est pas installée.")
            return None
        search_url = "https://api.github.com/search/code"
        params = {"q": query}
        try:
            self.logger.info(f"Recherche GitHub pour : {query}")
            resp = requests.get(search_url, params=params, timeout=10)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            if not items:
                return None
            file_url = items[0]["url"]
            self.logger.info(f"Récupération du fichier depuis {file_url}")
            file_resp = requests.get(file_url, timeout=10)
            file_resp.raise_for_status()
            encoded = file_resp.json().get("content", "")
            if not encoded:
                return None
            return base64.b64decode(encoded).decode("utf-8")
        except Exception as exc:
            self.logger.error(f"Échec de récupération pour '{query}' : {exc}")
            return None

    def fetch_readme(self, repo_full_name: str) -> str:
        if requests is None:
            self.logger.error("La bibliothèque 'requests' n'est pas installée.")
            return ""
        url = f"https://raw.githubusercontent.com/{repo_full_name}/HEAD/README.md"
        try:
            self.logger.info(f"Récupération du README de {repo_full_name}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as exc:
            self.logger.error(f"Erreur de récupération du README : {exc}")
            return ""

    def search_and_fetch(self, query: str) -> Dict[str, str]:
        repos = self.api_agent.search_github(query)
        results: Dict[str, str] = {}
        for repo in repos:
            readme = self.fetch_readme(repo)
            if readme:
                results[repo] = readme
            else:
                self.logger.warning(f"README introuvable pour {repo}")
        if not results:
            self.logger.warning(f"Aucun README trouvé pour la requête '{query}'")
        return results
