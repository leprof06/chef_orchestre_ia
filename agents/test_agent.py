# agents/test_agent.py

from agents.base_agent import BaseAgent
from config import CONFIG
from agents.utils.file_tools import list_files_recursive, read_file_safe
from agents.utils.logger import get_logger
import subprocess
try:
    import openai
except ImportError:
    openai = None

class TestAgent(BaseAgent):
    """
    Génère des tests unitaires et les exécute pour valider le code.
    Peut utiliser OpenAI pour la génération auto de tests, sinon utilise pytest/unittest en local.
    """
    def __init__(self):
        super().__init__("TestAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def generate_tests_openai(self, code, language="python"):
        if not self.has_openai:
            return None
        prompt = f"Génère des tests unitaires pour ce code {language} :\n\n{code}\n"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"Expert {language} et tests unitaires."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def run_tests_local(self, folder):
        # Exemple : exécution pytest sur le dossier
        import subprocess
        try:
            result = subprocess.run(
                ["pytest", folder, "--maxfail=2", "--disable-warnings"],
                capture_output=True, text=True, timeout=30
            )
            return result.stdout + "\n" + result.stderr
        except Exception as e:
            return f"Erreur lors de l'exécution des tests : {e}"

    def execute(self, task):
        code = task.get("code", "")
        folder = task.get("project_path", "")
        language = task.get("language", "python")
        if code and self.has_openai:
            return {"generated_tests": self.generate_tests_openai(code, language)}
        elif folder:
            return {"test_report": self.run_tests_local(folder)}
        else:
            return {"result": "Aucun code ni dossier fourni pour tester."}
