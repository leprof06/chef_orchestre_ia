# agents/data_analysis_agent.py

from agents.base_agent import BaseAgent
from config import CONFIG
import os
import json
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
    Agent d'analyse de projet :
    - Analyse syntaxique Python/JS/JSON
    - Analyse dépendances (requirements.txt, package.json)
    - Peut utiliser OpenAI, HuggingFace, ou fallback local pour résumé intelligent
    - Donne un rapport complet pour le front
    """
    def __init__(self):
        super().__init__("DataAnalysisAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)
        self.has_hf = bool(CONFIG.get("use_huggingface") and requests)

    def analyze_syntax(self, folder_path):
        result = {}
        for root, _, files in os.walk(folder_path):
            for f in files:
                ext = f.split('.')[-1].lower()
                path = os.path.join(root, f)
                if ext == "py":
                    try:
                        with open(path, "r", encoding="utf-8") as file:
                            import ast
                            ast.parse(file.read())
                    except Exception as e:
                        result[path] = f"Erreur Python: {e}"
                elif ext == "json":
                    try:
                        with open(path, "r", encoding="utf-8") as file:
                            json.load(file)
                    except Exception as e:
                        result[path] = f"Erreur JSON: {e}"
        return result

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
        return "Analyse HuggingFace (à brancher sur un modèle de ton choix)"

    def execute(self, task):
        folder_path = task.get("project_path")
        if not folder_path or not os.path.exists(folder_path):
            return {"error": "Chemin projet invalide."}
        syntax = self.analyze_syntax(folder_path)
        deps = self.analyze_dependencies(folder_path)
        ia_resume = None
        if self.has_openai:
            ia_resume = self.analyze_with_openai(folder_path)
        elif self.has_hf:
            ia_resume = self.analyze_with_huggingface(folder_path)
        else:
            ia_resume = "Résumé IA indisponible (mode local)."
        return {
            "syntax_errors": syntax or "OK",
            "dependencies": deps,
            "ia_resume": ia_resume
        }
