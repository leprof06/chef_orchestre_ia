# agents/utils/ai_api_connector.py

import os
import requests

class AIAPIConnector:
    def __init__(self):
        # Charge toutes les clés API dispo
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.mistral_key = os.getenv("MISTRAL_API_KEY")
        self.hf_key     = os.getenv("HUGGINGFACE_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        # Ajoute ici d'autres clés si besoin

    def chat(self, prompt):
        """
        Envoie un prompt à la première IA dispo.  
        Prend en charge OpenAI (GPT), Mistral, HuggingFace (text-generation), Gemini.
        """
        # ---------- OPENAI ----------
        if self.openai_key:
            try:
                return self._chat_openai(prompt)
            except Exception as e:
                return f"Erreur OpenAI : {e}"
        # ---------- MISTRAL ----------
        if self.mistral_key:
            try:
                return self._chat_mistral(prompt)
            except Exception as e:
                return f"Erreur Mistral : {e}"
        # ---------- HUGGINGFACE ----------
        if self.hf_key:
            try:
                return self._chat_huggingface(prompt)
            except Exception as e:
                return f"Erreur HF : {e}"
        # ---------- GEMINI (Google) ----------
        if self.gemini_key:
            try:
                return self._chat_gemini(prompt)
            except Exception as e:
                return f"Erreur Gemini : {e}"

        # Aucun provider dispo
        return "Aucune clé API IA trouvée (OpenAI, Mistral, HuggingFace, Gemini...)"

    # === OPENAI GPT ===
    def _chat_openai(self, prompt):
        import openai
        openai.api_key = self.openai_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    # === Mistral API ===
    def _chat_mistral(self, prompt):
        import requests
        url = "https://api.mistral.ai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.mistral_key}"}
        data = {
            "model": "mistral-tiny",  # Ou autre modèle
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 400,
        }
        r = requests.post(url, json=data, headers=headers)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()

    # === HuggingFace Inference ===
    def _chat_huggingface(self, prompt):
        import requests
        endpoint = "https://api-inference.huggingface.co/models/bigscience/bloomz-560m"
        headers = {"Authorization": f"Bearer {self.hf_key}"}
        payload = {"inputs": prompt}
        response = requests.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list):
            return result[0]["generated_text"].strip()
        return str(result)

    # === Google Gemini (PaLM) ===
    def _chat_gemini(self, prompt):
        import google.generativeai as genai
        genai.configure(api_key=self.gemini_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip()
