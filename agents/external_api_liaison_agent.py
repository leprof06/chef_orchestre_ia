import logging
from typing import List
import os

if os.environ.get("USE_REQUESTS_STUB") == "1":
    try:
        import requests_stub as requests
    except ModuleNotFoundError:
        requests = None
else:
    try:
        import requests
    except ModuleNotFoundError:
        try:
            import requests_stub as requests
        except ModuleNotFoundError:
            requests = None

from agents.base_agent import BaseAgent

class ExternalAPILiaisonAgent(BaseAgent):
    """Agent responsible for querying external APIs (e.g., GitHub)."""

    def __init__(self):
        super().__init__("ExternalAPILiaisonAgent")
        self.logger = logging.getLogger(__name__)

    def search_github(self, query: str) -> List[str]:
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
        except Exception as exc:
            self.logger.error("GitHub search failed: %s", exc)
            return []
