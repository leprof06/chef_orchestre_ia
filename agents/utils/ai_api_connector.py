# agents/utils/ai_api_connector.py
"""
Module centralisant la gestion des connexions aux IA (OpenAI, Mistral, HuggingFace, Ollama…)
Permet de brancher dynamiquement la bonne API selon les clés fournies dans l’environnement.
"""

import os
import openai
from typing import Optional

# Optionnel : import autres SDK si dispo (gérer l’absence)
try:
    import mistralai
except ImportError:
    mistralai = None
try:
    from huggingface_hub import InferenceClient
except ImportError:
    InferenceClient = None
try:
    import ollama
except ImportError:
    ollama = None

class AIAPIConnector:
    def __init__(self, env=os.environ):
        self.env = env
        # Récupère toutes les clés API possibles
        self.openai_api_key = env.get("OPENAI_API_KEY")
        self.mistral_api_key = env.get("MISTRAL_API_KEY")
        self.huggingface_token = env.get("HUGGINGFACE_TOKEN")
        self.ollama_url = env.get("OLLAMA_URL", "http://localhost:11434")
        # Ajoute d’autres fournisseurs ici

    def detect_provider(self) -> str:
        """Détecte automatiquement le fournisseur IA à utiliser selon les clés dispo."""
        if self.openai_api_key:
            return "openai"
        if self.mistral_api_key:
            return "mistral"
        if self.huggingface_token:
            return "huggingface"
        if ollama:
            return "ollama"
        return "none"

    def chat(self, prompt: str, provider: Optional[str] = None, **kwargs):
        """Chat universel : route la requête selon le provider détecté."""
        provider = provider or self.detect_provider()

        if provider == "openai":
            openai.api_key = self.openai_api_key
            model = kwargs.get("model", "gpt-3.5-turbo")
            completion = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return completion.choices[0].message['content']

        elif provider == "mistral" and mistralai:
            client = mistralai.Client(api_key=self.mistral_api_key)
            model = kwargs.get("model", "mistral-tiny")
            completion = client.chat(
                model=model,
                messages=[{"role": "user", "content": prompt}],
            )
            return completion['choices'][0]['message']['content']

        elif provider == "huggingface" and InferenceClient:
            client = InferenceClient(token=self.huggingface_token)
            model = kwargs.get("model", "HuggingFaceH4/zephyr-7b-beta")
            resp = client.text_generation(prompt, model=model, **kwargs)
            return resp

        elif provider == "ollama" and ollama:
            model = kwargs.get("model", "llama2")
            resp = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
            return resp["message"]["content"]

        return "Aucun provider IA/API valide trouvé. Configurez vos clés API."

    def available_providers(self):
        return [p for p in ["openai", "mistral", "huggingface", "ollama"] if getattr(self, f"{p}_api_key", None) or p == "ollama"]

# --- Exemple d’utilisation (à supprimer dans l’intégration) ---
if __name__ == "__main__":
    ai = AIAPIConnector()
    print(ai.detect_provider())
    print(ai.chat("Dis bonjour !"))
