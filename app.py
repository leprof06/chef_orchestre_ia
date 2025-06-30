from flask import Flask
from orchestrator import Orchestrator
from routes import register_routes

app = Flask(__name__)
app.secret_key = "dev-secret-1234"
orchestrator = Orchestrator()

# Plug toutes les routes à l'app
register_routes(app, orchestrator)

if __name__ == "__main__":
    app.run(debug=True)

