import logging
from typing import Dict

from .api_liaison_agent import APILiaisonAgent

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - environment without requests
    requests = None


class ReuseCodeAgent:
    """Agent used to fetch code snippets from GitHub repositories."""

    def __init__(self, api_agent: APILiaisonAgent | None = None) -> None:
        self.logger = logging.getLogger(__name__)
        self.api_agent = api_agent or APILiaisonAgent()

    def fetch_readme(self, repo_full_name: str) -> str:
        """Fetch the README of a repository."""
        if requests is None:
            self.logger.error("La bibliothèque 'requests' n'est pas installée.")
            return ""
        url = f"https://raw.githubusercontent.com/{repo_full_name}/HEAD/README.md"
        try:
            self.logger.info("Fetching README from %s", repo_full_name)
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except Exception as exc:  # pragma: no cover - network call
            self.logger.error("Failed to fetch README from %s: %s", repo_full_name, exc)
            return ""

    def search_and_fetch(self, query: str) -> Dict[str, str]:
        """Search GitHub and retrieve README contents."""
        repos = self.api_agent.search_github(query)
        results: Dict[str, str] = {}
        for repo in repos:
            readme = self.fetch_readme(repo)
            if readme:
                results[repo] = readme
            else:
                self.logger.warning("README introuvable pour %s", repo)
        if not results:
            self.logger.info("Aucun README récupéré pour la requête '%s'", query)
        return results