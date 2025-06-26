# backend/routes/__init__.py

from flask import Flask
from doctor_modules.routes.chat import chat_blueprint
from doctor_modules.routes.analysis import analysis_blueprint
from doctor_modules.routes.utils import utils_blueprint

app = Flask(__name__)

# Enregistrement des blueprints
app.register_blueprint(chat_blueprint)
app.register_blueprint(analysis_blueprint)
app.register_blueprint(utils_blueprint)

@app.route("/")
def index():
    return "Bienvenue dans l'interface Chef d'Orchestre IA"

if __name__ == "__main__":
    app.run(debug=True)
