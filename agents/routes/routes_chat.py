from flask import render_template, request, jsonify, session, flash, redirect, url_for
from agents.utils.ai_router import chat_with_ia
import logging

logger = logging.getLogger("routes_chat")

def register_routes(app, orchestrator):

    @app.route("/chat", methods=["GET", "POST"])
    def chat():
        if request.method == "POST":
            message = request.form.get("message", "").strip()
            if not message:
                return jsonify({"reply": "Please enter a message."}), 400
            try:
                result = orchestrator.chat(message)
                return jsonify({"reply": result})
            except Exception as e:
                logger.error(f"Chat error: {str(e)}")
                return jsonify({"reply": f"Error: {str(e)}"}), 500
        return render_template("chat.html")

    @app.route("/analyser", methods=["POST"])
    def analyser():
        project_path = request.form.get("project_path", "").strip()
        if not project_path:
            return jsonify({"result": "Missing project path."}), 400
        try:
            result = orchestrator.analyse_manager.handle("analyse_code", project_path)
            return jsonify({"result": result})
        except Exception as e:
            logger.error(f"Analyse error: {str(e)}")
            return jsonify({"result": f"Error: {str(e)}"}), 500

    @app.route("/logs")
    def logs():
        try:
            logs = orchestrator.get_logs()
            return render_template("logs.html", logs=logs)
        except Exception as e:
            logger.error(f"Logs error: {str(e)}")
            flash("Error loading logs.", "danger")
            return render_template("logs.html", logs=[])

    @app.route("/code")
    def code():
        try:
            code_state = orchestrator.get_code_state()
            return render_template("code.html", code=code_state)
        except Exception as e:
            logger.error(f"Code state error: {str(e)}")
            return render_template("code.html", code="")

    @app.route("/reset")
    def reset():
        session.pop('current_project', None)
        orchestrator.init_new_project()
        flash("Project has been reset successfully.", "success")
        return redirect(url_for('index'))

    @app.route("/chat_projet")
    def chat_projet():
        show_analyse = bool(session.get('current_project'))
        try:
            logs = orchestrator.get_logs()
            code = orchestrator.get_code_state()
        except Exception as e:
            logger.error(f"Chat projet error: {str(e)}")
            logs, code = [], ""
        return render_template("chat.html", show_analyse_btn=show_analyse, logs=logs, code=code)

    # ------- ROUTE IA API CONNECTEUR (version pro, multi-provider, multilingue) -----------
    @app.route('/chat_ia', methods=['POST'])
    def chat_ia():
        data = request.get_json()
        message = data.get('message', '').strip()
        code = data.get('code', '')
        filename = data.get('filename', '')
        lang = data.get('lang', 'en')

        if not message:
            return jsonify(answer="Please enter a question."), 400

        # Limite la taille du code envoyé (ex: 5000 chars)
        code = code[:5000]

        lang_prompt = {
            'fr': "Réponds en français.",
            'en': "Please answer in English.",
            'de': "Bitte antworte auf Deutsch.",
            'zh': "请用中文回答。",
        }
        prefix = lang_prompt.get(lang, lang_prompt['en'])

        prompt = (
            f"{prefix}\n"
            f"You are an expert AI assistant helping on the file: {filename}.\n\n"
            f"User's question:\n{message}\n\n"
            f"Current file content:\n{code}"
        )
        try:
            answer = chat_with_ia(prompt)
            return jsonify(answer=answer)
        except Exception as e:
            logger.error(f"chat_ia error: {str(e)}")
            return jsonify(answer=f"AI API error: {str(e)}"), 500
