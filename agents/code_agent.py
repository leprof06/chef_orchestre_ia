# agents/code_agent.py

from .base_agent import BaseAgent
import os
import openai
import requests
from config import CONFIG
from config_logger import get_logger

class CodeAgent(BaseAgent):
    """
    Agent avancé de génération et correction de code multilingue (Python, JS, etc.)
    Utilise OpenAI, HuggingFace, ou mode local. Peut détecter le langage, vérifier la syntaxe,
    générer du code à partir d'une consigne, ou corriger du code existant.
    """
    SUPPORTED_LANGUAGES = ["python", "javascript", "json", "bash", "html", "css", "typescript"]

    def __init__(self):
        super().__init__("CodeAgent")
        self.logger = get_logger(__name__)
        if CONFIG.get("use_openai"):
            openai.api_key = CONFIG.get("api_key_openai")

    def detect_language(self, filename=None, task_description=None):
        # Essaie de deviner le langage à partir du nom de fichier OU du prompt
        mapping = {
            "py": "python",
            "js": "javascript",
            "json": "json",
            "sh": "bash",
            "html": "html",
            "css": "css",
            "ts": "typescript"
        }
        if filename:
            ext = filename.split('.')[-1].lower()
            return mapping.get(ext, "python")
        # Fallback sur certains mots-clés dans le prompt
        if task_description:
            for lang in mapping.values():
                if lang in task_description.lower():
                    return lang
        return "python"

    def search_code_open_source(self, query, language="python"):
            """
            Recherche du code open-source sur plusieurs plateformes (GitHub, StackOverflow...).
            Peut être amélioré avec d'autres APIs.
            """
            results = []

            # --- Recherche GitHub ---
            github_api = "https://api.github.com/search/code"
            params = {"q": f"{query} language:{language}", "sort": "indexed", "order": "desc"}
            headers = {"Accept": "application/vnd.github.v3+json"}
            if CONFIG.get("github_token"):
                headers["Authorization"] = f"token {CONFIG['github_token']}"
            try:
                resp = requests.get(github_api, params=params, headers=headers, timeout=6)
                if resp.ok:
                    data = resp.json()
                    for item in data.get("items", [])[:3]:
                        results.append({
                            "source": "GitHub",
                            "name": item["name"],
                            "url": item["html_url"],
                            "repo": item["repository"]["html_url"]
                        })
            except Exception as e:
                self.logger.error(f"Erreur GitHub Search: {e}")

            # --- Recherche StackOverflow (résumé) ---
            so_api = "https://api.stackexchange.com/2.3/search/advanced"
            so_params = {
                "order": "desc", "sort": "votes", "accepted": "True",
                "title": query, "tagged": language, "site": "stackoverflow"
            }
            try:
                resp = requests.get(so_api, params=so_params, timeout=6)
                if resp.ok:
                    data = resp.json()
                    for q in data.get("items", [])[:2]:
                        results.append({
                            "source": "StackOverflow",
                            "title": q["title"],
                            "url": q["link"],
                            "score": q["score"]
                        })
            except Exception as e:
                self.logger.error(f"Erreur StackOverflow Search: {e}")

            # Tu peux étendre à Gist, GitLab, etc.

            return results

    def execute(self, task):
        action = task.get("action", "generate")
        instruction = task.get("instruction", "")
        language = task.get("language") or "python"
        if action == "search_open_source":
            return {"results": self.search_code_open_source(instruction, language)}
    def verify_imports(self, code, language):
        # Vérifie les imports/exports ou la syntaxe selon la techno
        if language == "python":
            try:
                import ast
                ast.parse(code)
                return {"imports_ok": True}
            except Exception as e:
                return {"imports_ok": False, "error": str(e)}
        elif language == "javascript":
            # Ici tu pourrais ajouter une vérification syntaxique JS (ex: avec node + subprocess)
            pass
        return {"imports_ok": True}

    def generate_code_openai(self, prompt, language):
        try:
            response = openai.ChatCompletion.create(
                model=CONFIG.get("openai_model", "gpt-4"),
                messages=[
                    {"role": "system", "content": f"Tu es un expert qui génère du code {language} optimal, commenté, testé et conforme aux bonnes pratiques."},
                    {"role": "user", "content": prompt}
                ]
            )
            code = response["choices"][0]["message"]["content"].strip()
            self.logger.info(f"Code généré (OpenAI, {language})")
            return code
        except Exception as e:
            self.logger.error(f"Erreur OpenAI : {e}")
            return f"Erreur OpenAI : {str(e)}"

    def generate_code_huggingface(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {CONFIG['api_key_huggingface']}"}
            payload = {"inputs": prompt}
            response = requests.post(
                "https://api-inference.huggingface.co/models/bigcode/starcoder",
                headers=headers,
                json=payload
            )
            # Il peut y avoir plusieurs champs possibles selon le modèle
            data = response.json()
            result = data.get("generated_text") or data.get("choices", [{}])[0].get("text") or "(Pas de réponse Hugging Face)"
            self.logger.info("Code généré avec HuggingFace")
            return result
        except Exception as e:
            self.logger.error(f"Erreur HuggingFace : {e}")
            return f"Erreur HuggingFace : {str(e)}"

    def generate_code_local(self, instruction, language):
        # Fallback local (mode démo ou sans API)
        return f"# {language}\n# Simulé : {instruction}\nprint('Hello!')"

    def execute(self, task):
        """
        Exécution principale de l'agent de code.
        task = {
            "action": "generate" | "verify" | "update" | "diff" | ...
            "instruction": str,
            "code": str (optionnel, pour correction)
            "filename": str (optionnel),
            "language": str (optionnel),
            ...
        }
        """
        action = task.get("action", "generate")
        instruction = task.get("instruction", "")
        code = task.get("code", "")
        filename = task.get("filename")
        language = task.get("language") or self.detect_language(filename, instruction)

        # Pour chaque action
        if action == "generate":
            prompt = instruction
            if code:
                prompt = f"Corrige et améliore ce code {language} :\n{code}\n\nConsigne : {instruction}"
            if CONFIG.get("use_openai"):
                result_code = self.generate_code_openai(prompt, language)
            elif CONFIG.get("use_huggingface"):
                result_code = self.generate_code_huggingface(prompt)
            else:
                result_code = self.generate_code_local(prompt, language)
            verif = self.verify_imports(result_code, language)
            return {"code": result_code, "verif": verif, "language": language}

        elif action == "verify":
            return self.verify_imports(code, language)

        elif action == "update":
            # Ex : appliquer une correction ou un diff (non implémenté ici)
            return {"result": "Fonctionnalité update à implémenter."}

        elif action == "diff":
            # Ex : compare deux versions de code
            from difflib import unified_diff
            old = task.get("old_code", "")
            diff = "\n".join(unified_diff(old.splitlines(), code.splitlines(), lineterm=""))
            return {"diff": diff}

        else:
            return {"error": f"Action inconnue pour CodeAgent : {action}"}
