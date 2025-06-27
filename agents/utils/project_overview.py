import os
from agents.utils.code_inspector import is_code_file, extract_code_structure

EXCLUDED_DIRS = {'node_modules', 'venv', '__pycache__', '.git'}
EXCLUDED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.wav', '.mp3', '.mp4', '.mov', '.avi',
    '.zip', '.tar', '.gz', '.rar', '.fit'
}
ALLOWED_EXTENSIONS = {'.py', '.js', '.html', '.css', '.json', '.md'}

def should_analyze_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in ALLOWED_EXTENSIONS and ext not in EXCLUDED_EXTENSIONS

def should_skip_dir(dirname):
    return any(excluded in dirname for excluded in EXCLUDED_DIRS)

def detect_capabilities(path):
    capabilities = set()
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(".py"):
                with open(file_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "flask" in content or "@app.route" in content:
                        capabilities.add("web_api")
                    if "torch" in content or "tensorflow" in content:
                        capabilities.add("machine_learning")
                    if "openai" in content or "langchain" in content:
                        capabilities.add("nlp_ia")
            elif file.endswith(".html") or file.endswith(".js") or file.endswith(".jsx"):
                capabilities.add("frontend_ui")
    return list(capabilities)

def analyze_project(path):
    project_info = {
        "files": [],
        "structures": [],
        "capabilities": []
    }

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if not should_skip_dir(d)]
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, path)
            if should_analyze_file(file_path):
                project_info["files"].append(rel_path)
                if is_code_file(file_path):
                    structure = extract_code_structure(file_path)
                    if structure:
                        project_info["structures"].append({
                            "path": rel_path,
                            **structure
                        })

    project_info["capabilities"] = detect_capabilities(path)
    return project_info
