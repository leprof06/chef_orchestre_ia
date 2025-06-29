# agents/ux_agent.py

from .base_agent import BaseAgent
from config import CONFIG

try:
    import openai
except ImportError:
    openai = None

class UXAgent(BaseAgent):
    """
    Analyse d’interface utilisateur (HTML/CSS/JS) et propose des améliorations UX/UI.
    Peut utiliser OpenAI, sinon vérifie des points basiques d’accessibilité.
    """
    def __init__(self):
        super().__init__("UXAgent")
        self.has_openai = bool(CONFIG.get("use_openai") and openai)

    def ux_with_openai(self, html_code):
        if not self.has_openai:
            return None
        prompt = f"Analyse ce code HTML/CSS/JS et propose les améliorations UX/UI prioritaires avec des exemples de code si possible :\n\n{html_code}\n"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Expert UX/UI design."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Erreur OpenAI : {str(e)}"

    def local_ux(self, html_code):
        tips = [
            "✔️ Vérifier que toutes les images ont un attribut alt.",
            "✔️ Assurer un contraste suffisant des couleurs pour l’accessibilité.",
            "✔️ Tester la navigation complète au clavier (tab, entrée).",
            "✔️ Ajouter des labels explicites aux champs de formulaire.",
            "✔️ Utiliser des boutons bien visibles pour chaque action clé.",
            "✔️ Privilégier une mise en page responsive (CSS media queries).",
            "✔️ Prévoir des messages de confirmation ou d’erreur clairs après chaque action.",
        ]
        return "\n".join(tips)

    def execute(self, task):
        html_code = task.get("code", "")
        if self.has_openai:
            result = self.ux_with_openai(html_code)
        else:
            result = self.local_ux(html_code)
        return {"ux_advice": result}
