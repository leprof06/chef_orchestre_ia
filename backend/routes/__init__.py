# backend/routes/__init__.py

from flask import Flask

# Importation des blueprints des routes spécialisées
from backend.routes.routes_analyze_full import analyze_full_blueprint
from backend.routes.routes_auto_fix import auto_fix_blueprint
from backend.routes.routes_auto_fix_combined import auto_fix_combined_blueprint
from backend.routes.routes_capabilities import capabilities_blueprint
from backend.routes.routes_chat import chat_blueprint
from backend.routes.routes_deep_analysis import deep_analysis_blueprint
from backend.routes.routes_feedback import feedback_blueprint
from backend.routes.routes_proxy import proxy_blueprint

app = Flask(__name__)

# Enregistrement des blueprints
app.register_blueprint(analyze_full_blueprint)
app.register_blueprint(auto_fix_blueprint)
app.register_blueprint(auto_fix_combined_blueprint)
app.register_blueprint(capabilities_blueprint)
app.register_blueprint(chat_blueprint)
app.register_blueprint(deep_analysis_blueprint)
app.register_blueprint(feedback_blueprint)
app.register_blueprint(proxy_blueprint)

@app.route("/")
def index():
    return "Bienvenue dans l'interface Chef d'Orchestre IA"

if __name__ == "__main__":
    app.run(debug=True)
