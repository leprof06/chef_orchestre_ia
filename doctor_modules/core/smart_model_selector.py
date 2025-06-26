import os
import logging
import openai
import requests

def get_best_model_response(prompt):
    try:
        # 1. OpenAI GPT-4 (prioritaire)
        if os.getenv("OPENAI_API_KEY"):
            logging.info("🧠 Utilisation du modèle OpenAI : gpt-4")
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es une IA programmeuse experte."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"]

        # 2. Mistral via HuggingFace
        elif os.getenv("HUGGINGFACE_API_KEY"):
            logging.info("🧠 Utilisation du modèle Mistral (HuggingFace)")
            hf_token = os.getenv("HUGGINGFACE_API_KEY")
            headers = {"Authorization": f"Bearer {hf_token}"}
            payload = {"inputs": prompt}
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers=headers,
                json=payload
            )
            if response.status_code == 200:
                return response.json()[0]["generated_text"]
            else:
                return f"❌ Erreur Mistral : {response.text}"

        # 3. Cohere
        elif os.getenv("COHERE_API_KEY"):
            logging.info("🧠 Utilisation du modèle Cohere")
            cohere_key = os.getenv("COHERE_API_KEY")
            headers = {"Authorization": f"Bearer {cohere_key}"}
            payload = {
                "model": "command",
                "prompt": prompt,
                "max_tokens": 500
            }
            response = requests.post(
                "https://api.cohere.ai/generate",
                headers=headers,
                json=payload
            )
            return response.json()["generations"][0]["text"]

        # 4. DeepL (mention uniquement)
        elif os.getenv("DEEPL_API_KEY"):
            logging.info("🧠 DeepL actif, mais utilisé uniquement pour la traduction.")

        # 5. AWS (placeholder)
        elif os.getenv("AWS_API_KEY"):
            logging.info("🧠 AWS activé, mais pas encore intégré.")

        return "❌ Aucun modèle IA utilisable actuellement."

    except Exception as e:
        logging.error(f"❌ Erreur IA : {e}")
        return f"❌ Erreur IA : {e}"
