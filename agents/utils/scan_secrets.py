# agents/utils/scan_secrets.py

import os
import re

SECRET_PATTERNS = [
    r"(sk-\w{20,})",         # OpenAI
    r"(hf_\w{16,})",         # HuggingFace
    r"(ghp_[A-Za-z0-9]{36})",# GitHub PAT
    r"(AIza[0-9A-Za-z-_]{35})", # Google API
    r"(?i)api[_-]?key\s*[:=]\s*['\"]?([A-Za-z0-9\-_=]{16,})"
]

def scan_for_secrets(folder):
    leaks = {}
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith((".py", ".js", ".env", ".json", ".yml", ".yaml")):
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        for pattern in SECRET_PATTERNS:
                            for match in re.findall(pattern, content):
                                leaks.setdefault(path, []).append(match)
                except Exception:
                    continue
    return leaks
