from flask import Flask
from orchestrator import Orchestrator
from agents.routes.routes_project import register_routes as register_project_routes
from agents.routes.routes_import import register_routes as register_import_routes
from agents.routes.routes_chat import register_routes as register_chat_routes
from agents.routes.routes_misc import register_routes as register_misc_routes
import os

app = Flask(__name__)
app.secret_key = "dev-secret-1234"
orchestrator = Orchestrator()

# CHEMIN où tu veux stocker les uploads
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Plug toutes les routes à l'app
register_project_routes(app, orchestrator)
register_import_routes(app, orchestrator)
register_chat_routes(app, orchestrator)
register_misc_routes(app, orchestrator)


if __name__ == "__main__":
    app.run(debug=True)

