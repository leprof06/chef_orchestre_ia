import logging
import shutil
from orchestrator import PROJECT_FOLDER
from core.history_manager import save_proposal
from core.client import (
    query_huggingface_model,
    query_openai_model,
)
from decouple import config

MODEL_GPT4 = "gpt-4"
MODEL_GPT35 = "gpt-3.5-turbo"

custom_objectives = ""

def get_best_available_model(prompt: str = ""):
    if config("OPENAI_API_KEY", default=None):
        return "OPENAI"
    if config("HUGGINGFACE_API_KEY", default=None):
        return "HUGGINGFACE"
    return None


def build_messages(code, filename):
    return [
        {"role": "system", "content": "Tu es une IA experte en amélioration de code Python. Reste claire, concise et utile."},
        {"role": "user", "content": f"Voici le fichier {filename} à améliorer :\n{code}\n\n{custom_objectives}"}
    ]


def is_complex_request(message: str) -> bool:
    long_msg = len(message) > 500
    has_keywords = any(word in message.lower() for word in [
        "résume", "analyse", "explique", "corrige", "améliore", "optimise", "comparer", "stratégie"
    ])
    return long_msg or has_keywords


def generate_code_proposal(code, filename):
    print("🧪 La fonction generate_code_proposal() a bien été appelée")
    provider = get_best_available_model()
    messages = build_messages(code, filename)
    prompt = "\n".join(m["content"] for m in messages if m["role"] == "user")

    if provider == "OPENAI":
        try:
            chosen_model = MODEL_GPT4 if is_complex_request(prompt) else MODEL_GPT35
            print(f"🧠 Utilisation du modèle OpenAI : {chosen_model}")
            suggestion = query_openai_model(prompt, model=chosen_model)
            save_proposal(filename, code, suggestion, accepted=False)
            return suggestion
        except Exception as e:
            logging.error(f"❌ Erreur OpenAI : {e}")
            return f"Erreur OpenAI : {e}"

    elif provider == "HUGGINGFACE":
        print("🟡 Utilisation de HuggingFace (gpt2 par défaut)")
        return query_huggingface_model("gpt2", prompt)

    else:
        logging.warning("⚠️ Aucune clé API valide détectée.")
        return "Aucune clé API valide détectée pour générer une proposition."


def backup_file(filepath):
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        logging.info(f"🗂️ Copie de sauvegarde créée : {backup_path}")
    except Exception as e:
        logging.error(f"❌ Erreur lors de la création de la sauvegarde : {e}")
