import logging
from typing import List

try:
    import requests
except ModuleNotFoundError:  # pragma: no cover - environment without requests
    requests = None


class APILiaisonAgent:
    """Agent responsible for talking to external APIs."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def search_github(self, query: str) -> List[str]:
        """Search public GitHub repositories."""
        if requests is None:
            self.logger.error("La bibliothèque 'requests' n'est pas installée.")
            return []
        url = "https://api.github.com/search/repositories"
        params = {"q": query}
        try:
            self.logger.info("Searching GitHub for '%s'", query)
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return [item.get("full_name", "") for item in data.get("items", [])]
        except Exception as exc:  # pragma: no cover - network call
            self.logger.error("GitHub search failed: %s", exc)
            return []

    def process_task(self, query: str) -> List[str]:
        """High level task processing."""
        results = self.search_github(query)
        if not results:
            self.logger.warning("Unable to process task for query '%s'", query)
        return results
