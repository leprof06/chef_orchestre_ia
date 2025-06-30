import os
import ast
import json
import re

def scan_workspace_in_detail(base_folder, output_json=True):
    """
    Scanne tout un workspace (dossiers projets). Pour chaque fichier :
      - Compte lignes
      - Extrait imports (AST pour .py, regex sinon)
      - Note type fichier
      - Détecte orphelins Python
    Retourne le rapport (et écrit JSON si output_json=True)
    """
    extensions = (".py", ".js", ".html", ".json", ".env", ".txt", ".md")
    result = {}
    all_py_imports = {}
    all_py_files = set()
    for project in os.listdir(base_folder):
        project_path = os.path.join(base_folder, project)
        if not os.path.isdir(project_path):
            continue
        files_data = {}
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    entry = {
                        "lines": 0,
                        "imports": [],
                        "type": os.path.splitext(file)[-1],
                    }
                    try:
                        with open(path, encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        entry["lines"] = len(content.splitlines())
                        # PYTHON : AST + indexation pour orphelins
                        if file.endswith('.py'):
                            all_py_files.add(path)
                            try:
                                tree = ast.parse(content)
                                py_imports = []
                                for node in tree.body:
                                    if isinstance(node, ast.Import):
                                        for n in node.names:
                                            py_imports.append(n.name)
                                    elif isinstance(node, ast.ImportFrom):
                                        mod = node.module if node.module else ''
                                        for n in node.names:
                                            py_imports.append(f"{mod}.{n.name}")
                                entry["imports"] = py_imports
                                all_py_imports[path] = py_imports
                            except Exception as e:
                                entry["error"] = f"AST fail: {e}"
                        else:
                            # Autres : regex basique pour 'import ...', 'from ...'
                            lines = content.splitlines()
                            entry["imports"] = [
                                line.strip() for line in lines if re.match(r"^(import|from) ", line.strip())
                            ]
                    except Exception as e:
                        entry["error"] = str(e)
                    files_data[path] = entry
        result[project] = files_data

    # --- Détection fichiers Python orphelins ---
    imported = set()
    for imports in all_py_imports.values():
        for imp in imports:
            # Cherche correspondance par nom de module/fichier
            for pyfile in all_py_files:
                mod_name = os.path.splitext(os.path.basename(pyfile))[0]
                if imp == mod_name or imp.endswith('.' + mod_name):
                    imported.add(pyfile)
    orphelins = list(all_py_files - imported)
    rapport = {
        "projects": result,
        "python_orphans": orphelins,
    }

    if output_json:
        output_path = os.path.join(base_folder, "rapport_global.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        return rapport, output_path
    return rapport

def extract_imports(content):
    """
    Extrait la liste des imports d’un code Python donné (par AST).
    """
    import ast
    try:
        tree = ast.parse(content)
        imports = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module if node.module else ''
                for n in node.names:
                    if mod:
                        imports.append(f"{mod}.{n.name}")
                    else:
                        imports.append(n.name)
        return imports
    except Exception as e:
        return []

# Compatibilité rétroactive avec anciens imports
scan_all_projects = scan_workspace_in_detail
