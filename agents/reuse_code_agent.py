import base64
import requests

class ReuseCodeAgent:
    """Agent that searches GitHub and retrieves code snippets."""

    SEARCH_URL = "https://api.github.com/search/code"

    def handle_task(self, query: str):
        """Search GitHub for the given query and return the first file's code.

        Parameters
        ----------
        query: str
            The search query.

        Returns
        -------
        str or None
            The decoded code from the first search result or ``None`` if
            nothing is found or a request fails.
        """
        params = {"q": query}
        try:
            search_resp = requests.get(self.SEARCH_URL, params=params)
        except Exception:
            return None
        if search_resp.status_code != 200:
            return None
        data = search_resp.json()
        items = data.get("items") or []
        if not items:
            return None
        file_url = items[0].get("url")
        if not file_url:
            return None
        file_resp = requests.get(file_url)
        if file_resp.status_code != 200:
            return None
        file_data = file_resp.json()
        encoded = file_data.get("content")
        if not encoded:
            return None
        try:
            return base64.b64decode(encoded).decode("utf-8")
        except Exception:
            return None
