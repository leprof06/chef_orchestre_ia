# agents/rh_agent.py

import os

class RHAgent:
    def __init__(self, agents_directory="agents"):
        self.agents_directory = agents_directory

    def handle_task(self, task_name: str, agents_dict: dict) -> str:
        agent_name = task_name.lower().replace(" ", "_") + "_agent"
        class_name = ''.join(word.capitalize() for word in agent_name.split('_'))
        filename = f"{agent_name}.py"
        filepath = os.path.join(self.agents_directory, filename)

        if os.path.exists(filepath):
            return f"L'agent '{agent_name}' existe déjà."

        try:
            with open(filepath, "w") as f:
                f.write(f"# agents/{filename}\n\n")
                f.write("from agents.base_agent import BaseAgent\n\n")
                f.write(f"class {class_name}(BaseAgent):\n")
                f.write("    def handle_task(self, task_description: str) -> str:\n")
                f.write("        return f'Agent {agent_name} prêt, tâche non encore implémentée.'\n")

            # Ajout dynamique (si nécessaire en cours d'exécution)
            if agent_name not in agents_dict:
                agents_dict[agent_name] = None  # Placeholder

            return f"Nouvel agent '{agent_name}' créé avec succès."
        except Exception as e:
            return f"Erreur lors de la création de l'agent '{agent_name}' : {e}"
