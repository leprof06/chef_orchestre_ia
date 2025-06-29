# config.py
import os
from dotenv import load_dotenv
load_dotenv()

CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
    "HUGGINGFACE_API_KEY": os.getenv("HUGGINGFACE_API_KEY", ""),
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", ""),
    "DEEPL_API_KEY": os.getenv("DEEPL_API_KEY", ""),
    # ...ajoute ici d’autres clés API si besoin

    # Flags activés/désactivés selon la présence des clés
    "use_openai": bool(os.getenv("OPENAI_API_KEY")),
    "use_huggingface": bool(os.getenv("HUGGINGFACE_API_KEY")),
    "use_github": bool(os.getenv("GITHUB_TOKEN")),
    "use_deepl": bool(os.getenv("DEEPL_API_KEY")),
}
