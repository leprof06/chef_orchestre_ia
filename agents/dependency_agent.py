# agents/dependency_agent.py

from .base_agent import BaseAgent
from config import CONFIG
import os
import json
from agents.utils.requirements_parser import parse_requirements, parse_package_json
from agents.utils.scan_vulnerabilities import scan_python_vuln, scan_node_vuln
from agents.utils.logger import get_logger

try:
    import openai
except ImportError:
    openai = None

class DependencyAgent(BaseAgent):
    """
    Analyse et gère les dépendances du projet (Python/JS).
    Peut proposer des mises à jour, vérifier la cohérence, générer requirements.txt ou package.json.
    """
    def __init__(self):
        super().__init__("DependencyAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def parse_requirements(self, folder):
        reqs = []
        for root, _, files in os.walk(folder):
            for f in files:
                if f == "requirements.txt":
                    with open(os.path.join(root, f), encoding="utf-8") as file:
                        reqs += [l.strip() for l in file if l.strip()]
        return reqs

    def parse_package_json(self, folder):
        pkgs = []
        for root, _, files in os.walk(folder):
            for f in files:
                if f == "package.json":
                    try:
                        with open(os.path.join(root, f), encoding="utf-8") as file:
                            data = json.load(file)
                            pkgs += list(data.get("dependencies", {}).keys())
                    except Exception:
                        pass
        return pkgs

    def suggest_updates_openai(self, reqs, pkgs):
        if not self.has_openai:
            return None
        prompt = f"""Voici les dépendances Python et JS du projet. 
Pour chacune, dis si une mise à jour est conseillée, ou s'il y a un problème de version :
Python: {', '.join(reqs) if reqs else 'Aucune'}
Node.js: {', '.join(pkgs) if pkgs else 'Aucune'}"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es expert en gestion de dépendances logicielle."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def execute(self, task):
        folder = task.get("project_path")
        if not folder or not os.path.isdir(folder):
            return {"error": "Chemin projet invalide."}
        reqs = self.parse_requirements(folder)
        pkgs = self.parse_package_json(folder)
        suggestion = None
        if self.has_openai:
            suggestion = self.suggest_updates_openai(reqs, pkgs)
        return {
            "python_requirements": reqs,
            "node_packages": pkgs,
            "update_suggestions": suggestion or "Mise à jour IA indisponible (mode local)."
        }
