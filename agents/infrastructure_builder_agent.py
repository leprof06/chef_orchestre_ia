from agents.base_agent import BaseAgent
import os

class InfrastructureBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("InfrastructureBuilderAgent")

    def execute(self, task):
        project_root = task.get("project_path", ".")
        managers_dir = os.path.join(project_root, "managers")
        agents_dir = os.path.join(project_root, "agents")

        known_managers = {
            "chef_analyse_manager": ["data_analysis", "optimize", "doctor"],
            "chef_code_manager": ["code", "debug", "reuse"],
            "chef_ux_manager": ["ux", "test", "doc"],
            "chef_devops_manager": ["api_liaison", "dependency"],
            "chef_rh_manager": ["rh"]
        }

        agent_files = [f for f in os.listdir(agents_dir) if f.endswith("_agent.py") and not f.startswith("__")]
        found_agents = [f.replace("_agent.py", "") for f in agent_files]

        suggestions = []
        for agent in found_agents:
            assigned = any(agent in agents for agents in known_managers.values())
            if not assigned:
                manager_name = f"chef_auto_{agent}_manager"
                filename = f"{manager_name}.py"
                suggestions.append({
                    "manager": manager_name,
                    "agent": agent,
                    "suggested_file": os.path.join(managers_dir, filename)
                })

        return {
            "result": "Analyse de l'infrastructure complétée.",
            "unassigned_agents": suggestions,
            "message": (
                "Les agents ci-dessus ne sont associés à aucun manager connu. "
                "Souhaitez-vous générer automatiquement leur manager ?"
            )
        }
