
import os
from doctor_modules.analysis.utils import is_code_file, extract_code_structure
from detection.dependency_checker import check_dependencies

API_CALL_CACHE = set()  # Pour éviter les appels redondants

EXCLUDED_DIRS = {'node_modules', 'venv', '__pycache__', '.git'}
EXCLUDED_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg',
    '.wav', '.mp3', '.mp4', '.mov', '.avi',
    '.zip', '.tar', '.gz', '.rar',
    '.fit'
}

ALLOWED_EXTENSIONS = {
    '.py', '.js', '.html', '.css', '.json', '.md'
}

def should_analyze_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    return ext in ALLOWED_EXTENSIONS and ext not in EXCLUDED_EXTENSIONS

def should_skip_dir(dirname):
    return any(excluded in dirname for excluded in EXCLUDED_DIRS)

def analyze_project(path):
    project_info = {
        "files": [],
        "api_keys": [],
        "dependencies": [],
        "capabilities": [],
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
                        project_info.setdefault("structures", []).append(structure)

    # Vérification unique des APIs et dépendances
    if 'check_api_keys' not in API_CALL_CACHE:
        project_info["api_keys"] = check_api_keys(path)
        API_CALL_CACHE.add('check_api_keys')

    if 'check_dependencies' not in API_CALL_CACHE:
        project_info["dependencies"] = check_dependencies(path)
        API_CALL_CACHE.add('check_dependencies')

    if 'detect_capabilities' not in API_CALL_CACHE:
        project_info["capabilities"] = detect_capabilities(path)
        API_CALL_CACHE.add('detect_capabilities')

    return project_info
