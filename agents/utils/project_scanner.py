import os
import json

def scan_all_projects(base_folder):
    extensions = (".py", ".html", ".json", ".env")
    result = {}

    for project in os.listdir(base_folder):
        project_path = os.path.join(base_folder, project)
        if not os.path.isdir(project_path):
            continue

        files_data = {}
        for root, _, files in os.walk(project_path):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, encoding="utf-8") as f:
                            content = f.read()
                            files_data[path] = {
                                "lines": len(content.splitlines()),
                                "imports": extract_imports(content),
                            }
                    except Exception as e:
                        files_data[path] = {"error": str(e)}

        result[project] = files_data

    output_path = os.path.join(base_folder, "rapport_global.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    return output_path

def extract_imports(content):
    lines = content.splitlines()
    imports = [line.strip() for line in lines if line.strip().startswith(("import", "from"))]
    return imports
