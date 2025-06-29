# agents/api_key_scanner_agent.py

from .base_agent import BaseAgent
import os
import re

class APIKeyScannerAgent(BaseAgent):
    """
    Scanne un dossier à la recherche de fuites de clés API ou secrets en dur.
    """
    KEY_PATTERNS = [
        r"(sk-\w{20,})",         # OpenAI
        r"(hf_\w{16,})",         # HuggingFace
        r"(ghp_[A-Za-z0-9]{36})",# GitHub PAT
        r"(AIza[0-9A-Za-z-_]{35})", # Google API
        r"(?i)api[_-]?key\s*[:=]\s*['\"]?([A-Za-z0-9\-_=]{16,})" # générique
    ]

    def __init__(self):
        super().__init__("APIKeyScannerAgent")

    def scan_file(self, path):
        results = []
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for pattern in self.KEY_PATTERNS:
                    for match in re.findall(pattern, content):
                        results.append((pattern, match))
        except Exception as e:
            return [("error", f"Impossible de scanner {path}: {e}")]
        return results

    def execute(self, task):
        folder = task.get("project_path")
        all_found = {}
        if not folder or not os.path.isdir(folder):
            return {"error": "Chemin projet invalide."}
        for root, _, files in os.walk(folder):
            for f in files:
                if f.endswith((".py", ".js", ".env", ".json", ".yml", ".yaml")):
                    path = os.path.join(root, f)
                    found = self.scan_file(path)
                    if found:
                        all_found[path] = found
        return {"api_key_leaks": all_found or "Aucune clé API trouvée."}
