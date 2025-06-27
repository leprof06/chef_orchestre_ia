import logging
import shutil
import openai
from flask import Blueprint, request, render_template, session
from config import README_PATH, OPENAI_API_KEY, HUGGINGFACE_API_KEY, MISTRAL_API_KEY, get_best_available_model
from core.history_manager import save_proposal, load_history
from core.client import query_huggingface_model, query_openai_model, query_cohere_model
from detection.capability_detector import detect_capabilities
from detection.api_key_checker import API_KEYS_DOCS
from decouple import config

chat_routes = Blueprint("chat", __name__)

MODEL_GPT4 = "gpt-4"
MODEL_GPT35 = "gpt-3.5-turbo"

model = None
tokenizer = None
custom_objectives = ""
openai.api_key = OPENAI_API_KEY

def load_readme():
    global custom_objectives
    if README_PATH and README_PATH.endswith(".md"):
        try:
            with open(README_PATH, "r", encoding="utf-8") as f:
                custom_objectives = f.read()
                logging.info("📖 Objectifs utilisateur chargés depuis README.md")
        except Exception as e:
            logging.warning(f"Impossible de lire le README.md : {e}")

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
    print("🧚 La fonction generate_code_proposal() a bien été appelée")
    provider = get_best_available_model("code")
    messages = build_messages(code, filename)
    prompt = "\n".join(m["content"] for m in messages if m["role"] == "user")

    if provider == "HUGGINGFACE":
        try:
            print("🧰 Appel HuggingFace avec le modèle Mistral")
            response = query_huggingface_model(
                model_name="mistralai/Mistral-7B-Instruct-v0.1",
                prompt=prompt,
                parameters={"max_new_tokens": 600}
            )
            save_proposal(filename, code, response, accepted=False)
            return response
        except Exception as e:
            logging.error(f"❌ HuggingFace a échoué : {e}")
            return f"Erreur HuggingFace : {e}"

    elif provider == "OPENAI":
        try:
            chosen_model = MODEL_GPT4 if is_complex_request(prompt) else MODEL_GPT35
            print(f"🧠 Utilisation du modèle OpenAI : {chosen_model}")
            response = openai.ChatCompletion.create(
                model=chosen_model,
                messages=messages,
                temperature=0.4
            )
            suggestion = response.choices[0].message.content
            save_proposal(filename, code, suggestion, accepted=False)
            return suggestion
        except Exception as e:
            logging.error(f"❌ Erreur OpenAI : {e}")
            return f"Erreur OpenAI : {e}"

    elif provider == "COHERE":
        try:
            print("🤞 Appel Cohere")
            suggestion = query_cohere_model(prompt)
            save_proposal(filename, code, suggestion, accepted=False)
            return suggestion
        except Exception as e:
            logging.error(f"❌ Erreur Cohere : {e}")
            return f"Erreur Cohere : {e}"

    elif provider == "MISTRAL":
        return "[Mistral API détectée mais sans implémentation directe côté client — utilisez HuggingFace pour Mistral si disponible.]"

    else:
        logging.warning("⚠️ Aucune clé API valide détectée.")
        return "Aucune clé API valide détectée pour générer une proposition."

def backup_file(filepath):
    backup_path = filepath + ".bak"
    try:
        shutil.copy2(filepath, backup_path)
        logging.info("🗂️ Copie de sauvegarde créée : {backup_path}")
    except Exception as e:
        logging.error(f"❌ Erreur lors de la création de la sauvegarde : {e}")

@chat_routes.route("/chat", methods=["GET", "POST"])
def chat():
    history = load_history()

    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            if user_input.strip().lower() in [
                "#show_missing_features",
                "quelles fonctionnalités me manquent",
                "que pourrais-tu faire avec plus de clés"
            ]:
                capabilities = detect_capabilities()
                missing = []
                for cap, info in capabilities.items():
                    if not info['active']:
                        doc_link = API_KEYS_DOCS.get(info['via'], "")
                        line = f"- ❌ {cap} (nécessite {info['via']})"
                        if doc_link:
                            line += f"\n  📌 Obtiens-la ici : {doc_link}"
                        missing.append(line)
                ai_reply = (
                    "🔍 Fonctionnalités inaccessibles actuellement :\n" + "\n".join(missing)
                    if missing else
                    "🎉 Toutes les fonctionnalités sont disponibles avec les clés actuelles."
                )
            else:
                try:
                    if already_proposed("chat", user_input):
                        ai_reply = "✅ Proposition déjà générée pour ce message."
                    else:
                        ai_reply = generate_code_proposal(user_input, "chat.txt")
                        save_proposal("chat", user_input, ai_reply, accepted=True)
                except Exception as e:
                    ai_reply = f"❌ Erreur : {e}"

            save_proposal("chat", user_input, ai_reply, accepted=True)
            history.append({"user": user_input, "response": ai_reply})

    return render_template("chat.html", history=[h for h in history if h.get("filename") == "chat"], ai_reply=ai_reply if "ai_reply" in locals() else None)
