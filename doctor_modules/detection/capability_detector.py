import json
import logging
from pathlib import Path
from dotenv import dotenv_values

logger = logging.getLogger("capability_detector")
logger.setLevel(logging.INFO)

# 📚 Capacités possibles selon les clés API .env
CAPABILITIES = {
    "OPENAI_API_KEY": ["correction code", "génération IA GPT"],
    "MISTRAL_API_KEY": ["alternative GPT locale"],
    "DEEPL_API_KEY": ["traduction haut niveau"],
    "AWS_API_KEY": ["traduction", "stockage cloud", "voix AWS Polly"],
    "GOOGLE_API_KEY": ["synthèse vocale", "traduction", "vision"],
    "ELEVENLABS_API_KEY": ["voix réaliste pour avatars ou cours"],
    "STRIPE_KEY": ["paiement en ligne"],
    "HUGGINGFACE_API_KEY": ["modèles spécialisés", "analyse NLP"]
}

DEFAULT_ENV_PATH = Path("H:/IA/clé API pour projet/.env")
DEFAULT_README_PATH = Path("README.md")


def detect_capabilities_from_env(env_path=DEFAULT_ENV_PATH, readme_path=DEFAULT_README_PATH):
    """
    Version autonome : scanne .env pour déterminer les capacités disponibles.
    Utilisée dans les scripts CLI ou génération de rapports.
    """
    capabilities = {}
    env_vars = dotenv_values(env_path) if env_path.exists() else {}
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

    for key, options in CAPABILITIES.items():
        if key in env_vars and env_vars[key]:
            for opt in options:
                capabilities[opt] = {
                    "active": True,
                    "via": key
                }
        else:
            for opt in options:
                if opt not in capabilities:
                    capabilities[opt] = {
                        "active": False,
                        "via": key
                    }

    logger.info("📦 Capacités détectées :")
    for cap, info in capabilities.items():
        logger.info(f"- {cap} → {'✅ activée' if info['active'] else '❌ manquante'} ({info['via']})")

    return capabilities


def detect_capabilities(api_keys: dict) -> dict:
    """
    Version utilisée dans le serveur Flask. Prend en paramètre API_KEYS depuis config.
    """
    return {
        "génération IA GPT": bool(api_keys.get("openai") or api_keys.get("anthropic")),
        "alternative GPT locale": bool(api_keys.get("mistral") or api_keys.get("cohere")),
        "traduction": bool(api_keys.get("google") or api_keys.get("deepl")),
        "traduction haut niveau": bool(api_keys.get("deepl")),
        "synthèse vocale": bool(api_keys.get("google") or api_keys.get("aws")),
        "voix AWS Polly": bool(api_keys.get("aws")),
        "vision": False,
        "reconnaissance vocale chinoise": bool(api_keys.get("iflytek")),
        "voix réaliste pour avatars ou cours": bool(api_keys.get("elevenlabs")),
        "paiement en ligne": bool(api_keys.get("stripe")),
        "stockage cloud": bool(api_keys.get("aws")),
        "analyse NLP": True,
        "correction code": True,
        "modèles spécialisés": bool(api_keys.get("openai") or api_keys.get("anthropic"))
    }


def detect_capabilities_missing(env_path=DEFAULT_ENV_PATH):
    capabilities = detect_capabilities_from_env(env_path)
    return {
        cap: info for cap, info in capabilities.items() if not info["active"]
    }


def write_missing_capabilities_report(output_path=Path("H:/IA/rapports_ai/global_missing_capabilities.json")):
    try:
        missing = detect_capabilities_missing()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(missing, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Rapport des capacités manquantes enregistré dans : {output_path}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération du rapport des capacités manquantes : {e}")


if __name__ == "__main__":
    caps = detect_capabilities_from_env()
    with open("data/capabilities_summary.json", "w", encoding="utf-8") as f:
        json.dump(caps, f, indent=2, ensure_ascii=False)
    print("✅ Résumé sauvegardé dans data/capabilities_summary.json")
