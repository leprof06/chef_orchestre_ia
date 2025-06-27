import os
import json
from pathlib import Path
from agents.base_agent import BaseAgent
from agents.utils.syntax_checker import analyze_folder_for_syntax
from agents.utils.project_structure import analyser_structure_projet

class DeepProjectAnalyzer:
    CACHE_PATH = Path("cache/deep_summary.json")
    MAX_CACHE_BYTES = 50 * 1024 * 1024  # 50 Mo

    def __init__(self, project_folder):
        self.project_folder = project_folder
        self.scanned_files = {}
        self.updates = []

    def load_cache(self):
        if self.CACHE_PATH.exists():
            try:
                with open(self.CACHE_PATH, encoding="utf-8") as f:
                    self.scanned_files = json.load(f)
                    return True
            except Exception:
                pass
        return False

    def scan(self):
        new_scan = {}

        for root, _, files in os.walk(self.project_folder):
            for f in files:
                if f.endswith((".py", ".html", ".json", ".env")):
                    path = os.path.join(root, f)
                    try:
                        with open(path, "r", encoding="utf-8") as file:
                            content = file.read()
                            new_scan[path] = content
                            if path not in self.scanned_files:
                                self.updates.append((path, "🆕 Nouveau fichier détecté"))
                            elif self.scanned_files[path] != content:
                                self.updates.append((path, "♻️ Fichier mis à jour"))
                    except Exception as e:
                        self.updates.append((path, f"❌ Erreur de lecture : {e}"))

        self.save_cache(new_scan)
        return new_scan, self.updates

    def save_cache(self, new_scan):
        try:
            self.CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            json_str = json.dumps(new_scan, indent=2, ensure_ascii=False)
            if len(json_str.encode("utf-8")) <= self.MAX_CACHE_BYTES:
                with open(self.CACHE_PATH, "w", encoding="utf-8") as f:
                    f.write(json_str)
        except Exception:
            pass

    def purge_cache(self):
        try:
            if self.CACHE_PATH.exists():
                self.CACHE_PATH.unlink()
                return True
        except Exception:
            pass
        return False

class DataAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("DataAnalysisAgent")

    def execute(self, task):
        folder_path = task.get("project_path")
        if not folder_path or not os.path.exists(folder_path):
            return {"error": "Chemin de projet invalide ou manquant."}

        # Analyse syntaxique
        syntax_result = analyze_folder_for_syntax(folder_path)

        # Analyse de structure approfondie
        analyzer = DeepProjectAnalyzer(folder_path)
        analyzer.load_cache()
        structure_result, updates = analyzer.scan()

        # Analyse des fichiers par structure logique
        file_structure = analyser_structure_projet(folder_path)

        result = {}
        if syntax_result:
            result["syntax_errors"] = syntax_result
        else:
            result["syntax"] = "Aucune erreur de syntaxe détectée."

        result["structure_updates"] = updates if updates else "Aucun changement détecté."
        result["structure_details"] = file_structure

        return {"result": result}
