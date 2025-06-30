# agents/reuse_code_agent.py

from agents.base_agent import BaseAgent
from config import CONFIG

try:
    import requests
except ImportError:
    requests = None

class ReuseCodeAgent(BaseAgent):
    """
    Recherche et intègre du code open source de plateformes (GitHub, StackOverflow...).
    Donne toujours la source du code récupéré.
    """
    def __init__(self):
        super().__init__("ReuseCodeAgent")
        self.has_github = bool(CONFIG.get("use_github") and requests)
        self.has_hf = bool(CONFIG.get("use_huggingface") and requests)

    def search_github(self, query, language="python"):
        if not self.has_github:
            return []
        url = "https://api.github.com/search/code"
        params = {"q": f"{query} language:{language}", "sort": "indexed", "order": "desc"}
        headers = {"Accept": "application/vnd.github.v3+json"}
        if CONFIG.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"token {CONFIG['GITHUB_TOKEN']}"
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=6)
            items = resp.json().get("items", []) if resp.ok else []
            return [
                {"name": it["name"], "url": it["html_url"], "repo": it["repository"]["html_url"]}
                for it in items[:3]
            ]
        except Exception as e:
            return [{"error": f"Erreur recherche GitHub : {e}"}]

    def search_stackoverflow(self, query, language="python"):
        if not requests:
            return []
        url = "https://api.stackexchange.com/2.3/search/advanced"
        params = {
            "order": "desc", "sort": "votes", "accepted": "True",
            "title": query, "tagged": language, "site": "stackoverflow"
        }
        try:
            resp = requests.get(url, params=params, timeout=6)
            items = resp.json().get("items", []) if resp.ok else []
            return [
                {"title": q["title"], "url": q["link"], "score": q["score"]}
                for q in items[:3]
            ]
        except Exception as e:
            return [{"error": f"Erreur recherche StackOverflow : {e}"}]

    def execute(self, task):
        instruction = task.get("instruction", "")
        language = task.get("language", "python")
        # Recherche d'abord sur GitHub, puis StackOverflow
        github_results = self.search_github(instruction, language)
        so_results = self.search_stackoverflow(instruction, language)
        # Fusionne et renvoie tout
        return {
            "github_results": github_results or "Aucun résultat GitHub.",
            "stackoverflow_results": so_results or "Aucun résultat StackOverflow."
        }
