import json
import logging
from flask import Blueprint, render_template, request
from pathlib import Path
from detection.capability_detector import detect_capabilities
from config.config import API_KEYS

routes_capabilities = Blueprint("capabilities", __name__)

ALL_CAPABILITIES = [
    "correction code",
    "génération IA GPT",
    "alternative GPT locale",
    "traduction haut niveau",
    "traduction",
    "stockage cloud",
    "voix AWS Polly",
    "synthèse vocale",
    "vision",
    "voix réaliste pour avatars ou cours",
    "paiement en ligne",
    "modèles spécialisés",
    "analyse NLP",
    "reconnaissance vocale chinoise"
]

# Suggestions potentielles si certaines API sont détectées
IMPROVEMENT_SUGGESTIONS = {
    "IFLYTEK_API_KEY": "Ajouter une interface vocale en chinois pour la reconnaissance ou la synthèse.",
    "AWS_API_KEY": "Activer les voix naturelles AWS Polly ou le stockage cloud (S3).",
    "ELEVENLABS_API_KEY": "Activer les voix ultra-réalistes pour les avatars ou les cours.",
    "MISTRAL_API_KEY": "Proposer une génération de texte locale via Mistral API.",
    "ANTHROPIC_API_KEY": "Ajouter Claude comme modèle alternatif à GPT.",
    "STRIPE_SECRET_KEY": "Configurer un espace sécurisé avec paiement par carte.",
    "DEEPL_API_KEY": "Traduction plus précise dans les langues européennes."
}

@routes_capabilities.route("/capabilities", methods=["GET", "POST"])
def view_capabilities():
    requested = request.form.getlist("requested") if request.method == "POST" else []
    logic_results = detect_capabilities(API_KEYS)

    json_path = Path("H:/IA/clé API pour projet/api_keys_reference.json")
    capabilities_json = []
    existing_keys = set()
    if json_path.exists():
        try:
            with open(json_path, encoding="utf-8") as f:
                data = json.load(f)
                for key, val in data.items():
                    if key.startswith("_"): continue
                    capabilities_json.append({
                        "name": key,
                        "status": val.get("status", "?"),
                        "doc": val.get("doc", "")
                    })
                    if val.get("status") == "présente":
                        existing_keys.add(key)
        except json.JSONDecodeError as e:
            logging.warning(f"Erreur JSON dans {json_path} : {e}")
        except OSError as e:
            logging.warning(f"Erreur d'accès au fichier {json_path} : {e}")

    filtered_results = {
        cap: logic_results.get(cap, {"active": False, "via": "aucune API connue"})
        for cap in requested
    } if requested else None

    # Génération des suggestions d’amélioration en fonction des clés présentes
    suggestions = []
    for key in existing_keys:
        if key in IMPROVEMENT_SUGGESTIONS:
            suggestions.append(IMPROVEMENT_SUGGESTIONS[key])

    return render_template(
        "capabilities.html",
        capabilities_json=capabilities_json,
        all_options=ALL_CAPABILITIES,
        requested=requested,
        results=filtered_results,
        suggestions=suggestions
    )
