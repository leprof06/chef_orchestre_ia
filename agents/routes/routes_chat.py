# agents/routes/routes_chat.py
from flask import render_template, request, jsonify, session, flash, redirect, url_for

def register_routes(app, orchestrator):

    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        if request.method == "POST":
            message = request.form.get("message")
            result = orchestrator.chat(message)
            return jsonify({"reply": result})
        return render_template("chat.html")

    @app.route("/analyser", methods=["POST"])
    def analyser():
        project_path = request.form.get("project_path")
        result = orchestrator.analyse_manager.handle("analyse_code", project_path)
        return jsonify({"result": result})

    @app.route("/logs")
    def logs():
        logs = orchestrator.get_logs()
        return render_template("logs.html", logs=logs)

    @app.route("/code")
    def code():
        code_state = orchestrator.get_code_state()
        return render_template("code.html", code=code_state)

    @app.route("/reset")
    def reset():
        session.pop('current_project', None)
        orchestrator.init_new_project()
        flash("Projet réinitialisé avec succès.")
        return redirect(url_for('index'))

    @app.route("/chat_projet")
    def chat_projet():
        show_analyse = bool(session.get('current_project'))
        logs = orchestrator.get_logs()
        code = orchestrator.get_code_state()
        return render_template("chat.html", show_analyse_btn=show_analyse, logs=logs, code=code)
