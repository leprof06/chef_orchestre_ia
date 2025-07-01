# agents/routes/routes_misc.py
from flask import render_template
def register_routes(app, orchestrator):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/choose_project")
    def choose_project():
        projects = orchestrator.get_existing_projects()
        return render_template("choose_project.html", projects=projects)
