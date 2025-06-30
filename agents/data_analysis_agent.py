import os
import json
from agents.base_agent import BaseAgent
from config import CONFIG
from agents.utils.syntax_checker import analyze_folder_for_syntax
from agents.utils.project_structure import analyser_structure_projet
from agents.utils.file_tools import list_files_recursive
from agents.utils.big_file_detector import find_big_files
from agents.utils.scan_secrets import scan_for_secrets
from agents.utils.logger import get_logger

try:
    import openai
except ImportError:
    openai = None
try:
    import requests
except ImportError:
    requests = None

class DataAnalysisAgent(BaseAgent):
    """
    Analyse de projet ultra-complète :
    - Vérifie la syntaxe sur .py/.json/.js
    - Analyse les dépendances Python/Node
    - Cherche des fichiers lourds
    - Cherche des secrets dans le code (API key, tokens)
    - Peut résumer via OpenAI/HF si la clé est dispo
    - Structure le résultat pour affichage + log
    """
    def __init__(self):
        super().__init__("DataAnalysisAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)
        self.has_hf = bool(CONFIG.get("use_huggingface") and requests)
        self.logger = get_logger(__name__)

    def analyze_syntax(self, folder_path):
        errors = {}
        for root, _, files in os.walk(folder_path):
            for f in files:
                ext = f.split('.')[-1].lower()
                path = os.path.join(root, f)
                try:
                    if ext == "py":
                        with open(path, "r", encoding="utf-8") as file:
                            import ast
                            ast.parse(file.read())
                    elif ext == "json":
                        with open(path, "r", encoding="utf-8") as file:
                            json.load(file)
                except Exception as e:
                    errors[path] = f"Erreur {ext.upper()} : {e}"
        return errors

    def analyze_dependencies(self, folder_path):
        reqs, pkgs = [], []
        for root, _, files in os.walk(folder_path):
            for f in files:
                if f == "requirements.txt":
                    with open(os.path.join(root, f), encoding="utf-8") as file:
                        reqs += [l.strip() for l in file if l.strip()]
                if f == "package.json":
                    with open(os.path.join(root, f), encoding="utf-8") as file:
                        try:
                            data = json.load(file)
                            pkgs += list(data.get("dependencies", {}).keys())
                        except Exception:
                            pass
        return {"python_requirements": reqs, "node_packages": pkgs}

    def analyze_with_openai(self, folder_path):
        if not self.has_openai:
            return None
        files = []
        for root, _, fs in os.walk(folder_path):
            for f in fs:
                if f.endswith((".py", ".js", ".json")):
                    try:
                        with open(os.path.join(root, f), "r", encoding="utf-8") as file:
                            snippet = file.read()[:600]
                            files.append(f"Fichier: {f}\n{snippet}")
                    except Exception:
                        pass
        prompt = (
            "Voici une sélection de fichiers d'un projet logiciel. Résume l'architecture, "
            "détecte les problèmes majeurs, et donne les points d'amélioration prioritaires :\n\n"
            + "\n\n".join(files[:5])
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Tu es un expert de l'analyse de code."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI: {str(e)}"

    def analyze_with_huggingface(self, folder_path):
        if not self.has_hf:
            return None
        # Placeholder pour une future extension HuggingFace
        return "Analyse HuggingFace non implémentée (à brancher sur un modèle de ton choix)."

    def execute(self, task):
        folder_path = task.get("project_path")
        if not folder_path or not os.path.exists(folder_path):
            return {"error": "Chemin projet invalide."}

        # Analyse syntaxique
        syntax = self.analyze_syntax(folder_path)
        # Analyse structurelle (arborescence, Flask, etc)
        structure = analyser_structure_projet(folder_path)
        # Dépendances
        deps = self.analyze_dependencies(folder_path)
        # Recherche de secrets/tokens
        secrets = scan_for_secrets(folder_path)
        # Recherche fichiers lourds
        big_files = find_big_files(folder_path, size_limit_mb=5)

        # IA - Résumé global
        ia_resume = None
        if self.has_openai:
            ia_resume = self.analyze_with_openai(folder_path)
        elif self.has_hf:
            ia_resume = self.analyze_with_huggingface(folder_path)
        else:
            ia_resume = "Résumé IA indisponible (mode local)."

        # Résumé humain lisible pour l'UI
        readable = (
            f"**Analyse du projet :**\n"
            f"- Erreurs de syntaxe : {'Aucune' if not syntax else json.dumps(syntax, ensure_ascii=False, indent=2)}\n"
            f"- Dépendances : {deps}\n"
            f"- Secrets détectés : {secrets or 'Aucun'}\n"
            f"- Fichiers volumineux (>5Mo) : {big_files or 'Aucun'}\n"
            f"- Structure : {structure}\n"
            f"- Résumé IA : {ia_resume}\n"
        )

        # Résultat structuré pour API/front/logs
        return {
            "result": {
                "syntax_errors": syntax or "OK",
                "dependencies": deps,
                "secrets": secrets,
                "big_files": big_files,
                "structure": structure,
                "ia_resume": ia_resume,
            },
            "answer": readable
        }
