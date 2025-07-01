# agents/utils/ai_router.py

import os

# Imports des différents SDK IA (à installer selon les besoins)
import openai

try:
    import mistralai
except ImportError:
    mistralai = None

try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    import cohere
except ImportError:
    cohere = None

try:
    import anthropic
except ImportError:
    anthropic = None

# --- Ajoute ici d'autres imports de SDK IA si besoin ---

def detect_ia_providers():
    """
    Retourne la liste des providers IA disponibles et leur clé.
    Priorité : OpenAI > Mistral > HuggingFace > Gemini > Cohere > Anthropic > (ajoute-en d’autres ici)
    """
    providers = []
    if os.environ.get("OPENAI_API_KEY"):
        providers.append(("openai", os.environ["OPENAI_API_KEY"]))
    if os.environ.get("MISTRAL_API_KEY"):
        providers.append(("mistral", os.environ["MISTRAL_API_KEY"]))
    if os.environ.get("HUGGINGFACE_API_TOKEN"):
        providers.append(("huggingface", os.environ["HUGGINGFACE_API_TOKEN"]))
    if os.environ.get("GOOGLE_API_KEY"):
        providers.append(("gemini", os.environ["GOOGLE_API_KEY"]))
    if os.environ.get("COHERE_API_KEY"):
        providers.append(("cohere", os.environ["COHERE_API_KEY"]))
    if os.environ.get("ANTHROPIC_API_KEY"):
        providers.append(("anthropic", os.environ["ANTHROPIC_API_KEY"]))
    # Ajoute ici d'autres providers si tu veux
    return providers

def chat_with_ia(message, model_hint="chat"):
    """
    Route le prompt vers la meilleure IA dispo.
    model_hint = "chat" | "code" | etc.
    """
    providers = detect_ia_providers()
    if not providers:
        return "Aucune clé API IA trouvée dans l'environnement."

    for provider, api_key in providers:
        try:
            if provider == "openai":
                openai.api_key = api_key
                completion = openai.ChatCompletion.create(
                    model="gpt-4o",  # Ou gpt-3.5-turbo selon ton quota
                    messages=[
                        {"role": "system", "content": "Tu es un assistant développeur expert."},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.6,
                )
                return completion.choices[0].message['content']

            elif provider == "mistral" and mistralai:
                client = mistralai.Client(api_key=api_key)
                chat_response = client.chat(
                    model="mistral-medium",  # Ou mistral-large, etc.
                    messages=[{"role": "user", "content": message}],
                )
                return chat_response.choices[0].message.content

            elif provider == "huggingface" and InferenceClient:
                client = InferenceClient(token=api_key)
                resp = client.text_generation(
                    prompt=message,
                    model="HuggingFaceH4/zephyr-7b-beta",  # Tu peux custom ici
                    max_new_tokens=512
                )
                return resp  # Texte direct

            elif provider == "gemini" and genai:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(message)
                return response.text

            elif provider == "cohere" and cohere:
                co = cohere.Client(api_key)
                response = co.chat(message=message, model="command-r-plus")
                return response.text

            elif provider == "anthropic" and anthropic:
                client = anthropic.Anthropic(api_key=api_key)
                response = client.messages.create(
                    model="claude-3-haiku-20240307",  # ou claude-3-opus...
                    max_tokens=1000,
                    messages=[{"role": "user", "content": message}]
                )
                return response.content[0].text

            # Ajoute ici d’autres providers custom...

        except Exception as e:
            # Essaie le provider suivant si échec (ex: quota, bug, indispo)
            continue

    return "Aucun provider IA n'a pu répondre, vérifie tes quotas/clés API."

