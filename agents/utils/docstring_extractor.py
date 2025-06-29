# agents/utils/docstring_extractor.py

import ast

def extract_docstrings(path):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    module = ast.parse(content)
    docstrings = {"module": ast.get_docstring(module), "functions": {}, "classes": {}}
    for node in module.body:
        if isinstance(node, ast.FunctionDef):
            docstrings["functions"][node.name] = ast.get_docstring(node)
        elif isinstance(node, ast.ClassDef):
            docstrings["classes"][node.name] = ast.get_docstring(node)
    return docstrings
