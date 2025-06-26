import logging
from pathlib import Path
import json
from dotenv import dotenv_values
from detection.capability_detector import detect_capabilities_from_env as detect_capabilities

logger = logging.getLogger("api_key_checker")
logger.setLevel(logging.INFO)

# 🔑 Documentation des API disponibles
API_KEYS_DOCS = {
    "OPENAI_API_KEY": "https://platform.openai.com/account/api-keys",
    "DEEPL_API_KEY": "https://www.deepl.com/fr/pro-api",
    "MISTRAL_API_KEY": "https://docs.mistral.ai/",
    "IFLYTEK_API_KEY": "https://www.xfyun.cn/services/online_tts",
    "ANTHROPIC_API_KEY": "https://console.anthropic.com/account/keys",
    "AWS_API_KEY": "https://aws.amazon.com/fr/blogs/security/manage-access-keys/",
    "ELEVENLABS_API_KEY": "https://www.elevenlabs.io/docs/api",
    "HUGGINGFACE_API_KEY": "https://huggingface.co/settings/tokens",
    "LLAMA_API_KEY": "https://llama-api.com/docs",
    "GOOGLE_API_KEY": "https://console.cloud.google.com/apis/credentials",
    "COHERE_API_KEY": "https://dashboard.cohere.com/api-keys",
    "STRIPE_KEY": "https://dashboard.stripe.com/apikeys",
    "STRIPE_SECRET_KEY": "https://dashboard.stripe.com/apikeys",
    "STRIPE_WEBHOOK_SECRET": "https://dashboard.stripe.com/webhooks"
}

class ApiKeyCheckerException(Exception):
    """Erreur générale du module de vérification des clés API."""
    pass

class DirectoryNotFoundException(ApiKeyCheckerException):
    def __init__(self, message):
        super().__init__(message)

def write_summary_to_file(summary, output_path):
    output_dir = Path(output_path).parent

    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True)
            logger.info(f"📁 Dossier de sortie créé automatiquement : {output_dir}")
        except OSError as err:
            msg = f"❌ Impossible de créer le dossier {output_dir} : {err}"
            logger.error(msg)
            raise DirectoryNotFoundException(msg)

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Résumé écrit dans : {output_path}")
    except OSError as e:
        logger.error(f"❌ Erreur d'écriture du fichier {output_path} : {e}")
        raise

def check_api_keys(env_path: str, output_path: str):
    env_path = Path(env_path).resolve()
    output_path = Path(output_path).resolve()

    if not env_path.exists():
        logger.error(f"❌ Fichier .env introuvable à : {env_path}")
        raise FileNotFoundError(f".env introuvable à : {env_path}")

    env_vars = dotenv_values(env_path)
    summary = {}

    for key, url in API_KEYS_DOCS.items():
        status = "présente" if key in env_vars and env_vars[key] else "manquante"
        summary[key] = {
            "status": status,
            "doc": url
        }

    capabilities = detect_capabilities(env_path)
    summary["_capabilities"] = capabilities

    write_summary_to_file(summary, output_path)
    return summary

if __name__ == "__main__":
    ENV_PATH = "H:/IA/clé API pour projet/.env"
    OUTPUT_PATH = "H:/IA/clé API pour projet/api_keys_reference.json"

    resultat = check_api_keys(ENV_PATH, OUTPUT_PATH)
    for k, v in resultat.items():
        if not k.startswith("_"):
            logger.info(f"🔑 {k} : {v['status']}")
