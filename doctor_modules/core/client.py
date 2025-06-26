from decouple import config
import requests
import os

HUGGINGFACE_API_KEY = config("HUGGINGFACE_API_KEY")
OPENAI_API_KEY = config("OPENAI_API_KEY")
MISTRAL_API_KEY = config("MISTRAL_API_KEY")
DEEPL_API_KEY = config("DEEPL_API_KEY")
AWS_API_KEY = config("AWS_API_KEY")
GOOGLE_API_KEY = config("GOOGLE_API_KEY")
COHERE_API_KEY = config("COHERE_API_KEY")

HEADERS_HF = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
}

HEADERS_OPENAI = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}


def query_huggingface_model(model_name: str, prompt: str, parameters: dict = None) -> str:
    url = f"https://api-inference.huggingface.co/models/{model_name}"
    payload = {"inputs": prompt}
    if parameters:
        payload.update(parameters)
    try:
        response = requests.post(url, headers=HEADERS_HF, json=payload)
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "") if isinstance(result, list) else result.get("generated_text", "")
    except Exception as e:
        return f"[HF API Error] {e}"


def query_openai_model(prompt: str, model: str = "gpt-4") -> str:
    url = "https://api.openai.com/v1/chat/completions"
    messages = [
        {"role": "system", "content": "Tu es une IA experte en amélioration de code."},
        {"role": "user", "content": prompt}
    ]
    payload = {
        "model": model,
        "messages": messages
    }
    try:
        response = requests.post(url, headers=HEADERS_OPENAI, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OpenAI API Error] {e}"


def query_mistral_api_model(prompt: str) -> str:
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, headers=headers, json={"inputs": prompt})
        response.raise_for_status()
        result = response.json()
        return result[0].get("generated_text", "") if isinstance(result, list) else str(result)
    except Exception as e:
        return f"[Mistral API Error] {e}"


def query_cohere_model(prompt: str) -> str:
    url = "https://api.cohere.ai/generate"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "command-xlarge-nightly",
        "prompt": prompt,
        "max_tokens": 500
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("generations", [{}])[0].get("text", "")
    except Exception as e:
        return f"[Cohere API Error] {e}"


def query_google_model(prompt: str) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GOOGLE_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"[Google Gemini API Error] {e}"


def query_aws_model(prompt: str) -> str:
    return "[AWS] Fonction en attente d'intégration : API non reliée pour l'instant."

def query_deepl_translation(text: str, target_lang: str = "EN") -> str:
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        return f"[DeepL API Error] {e}"

__all__ = [
    "query_huggingface_model",
    "query_openai_model",
    "query_mistral_api_model",
    "query_cohere_model",
    "query_google_model",
    "query_aws_model",
    "query_deepl_translation"
]
