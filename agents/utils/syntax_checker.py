import os
import ast


def is_python_file(filepath):
    return filepath.endswith(".py")


def check_syntax(filepath):
    if not is_python_file(filepath):
        return None  # Ignore non-Python files

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            ast.parse(source, filename=filepath)
        return None  # Pas d'erreur
    except SyntaxError as e:
        return f"Erreur de syntaxe dans {filepath} : {e}"
    except Exception as e:
        return f"Erreur lors de l'analyse de {filepath} : {e}"


def analyze_folder_for_syntax(path):
    syntax_errors = []
    for root, _, files in os.walk(path):
        for file in files:
            full_path = os.path.join(root, file)
            result = check_syntax(full_path)
            if result:
                syntax_errors.append(result)
    return syntax_errors
