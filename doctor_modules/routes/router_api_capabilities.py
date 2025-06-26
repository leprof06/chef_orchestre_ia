# router_api_capabilities.py
from decouple import config  # ✅ Ajouté
import json
from dotenv import dotenv_values
from flask import Blueprint, render_template

api_map = Blueprint("api_router", __name__)

# 📚 Liste complète des APIs supportées avec usage principal et modèle associé
API_USAGE_DETAILS = {
    "OPENAI_API_KEY": {
        "model": "gpt-4",
        "task": "Analyse et génération avancée de code, texte et raisonnement",
        "paying": True
    },
    "MISTRAL_API_KEY": {
        "model": "mistral-7b",
        "task": "Génération rapide locale ou cloud de texte/code",
        "paying": False
    },
    "COHERE_API_KEY": {
        "model": "cohere",
        "task": "Embeddings, résumé, NLP et classification",
        "paying": True
    },
    "HUGGINGFACE_API_KEY": {
        "model": "huggingface-hub",
        "task": "Accès à modèles open source (BERT, LLaMA...)",
        "paying": False
    },
    "DEEPL_API_KEY": {
        "model": "deepl",
        "task": "Traduction pro (précision syntaxique et contexte)",
        "paying": True
    },
    "GOOGLE_API_KEY": {
        "model": "google-cloud-nlp",
        "task": "Traduction, NLP, recherche, cloud",
        "paying": True
    },
    "AWS_API_KEY": {
        "model": "aws-polly",
        "task": "Voix naturelles, cloud, stockage, OCR",
        "paying": True
    },
    "ELEVENLABS_API_KEY": {
        "model": "elevenlabs",
        "task": "Synthèse vocale réaliste pour avatars et vidéos",
        "paying": True
    },
    "LLAMA_API_KEY": {
        "model": "llama",
        "task": "Modèle open source local de Meta (texte/code)",
        "paying": False
    }
}

# 🧠 Choix du meilleur modèle selon tâche
PREFERRED_ORDER = [
    ("gratuit", ["mistral-7b", "huggingface-hub", "llama"]),
    ("payant", ["gpt-4", "cohere", "deepl", "aws-polly", "google-cloud-nlp"])
]

@api_map.route("/api_map")
def show_api_capabilities():
    env_path = config("ENV_PATH", default="H:/IA/clé API pour projet/.env")  # ✅ corrigé
    env = dotenv_values(env_path)

    table = []
    for key, info in API_USAGE_DETAILS.items():
        status = "présente" if key in env and env[key] else "absente"
        table.append({
            "clé": key,
            "modèle": info["model"],
            "usage": info["task"],
            "payant": "✅" if info["paying"] else "❌",
            "statut": status
        })

    return render_template("api_map.html", apis=table)

def auto_select_model(task: str, env_vars: dict) -> str:
    for type_, model_list in PREFERRED_ORDER:
        for model in model_list:
            for key, info in API_USAGE_DETAILS.items():
                if info["model"] == model and key in env_vars and env_vars[key]:
                    if task.lower() in info["task"].lower():
                        return info["model"]

    return "gpt-4"
