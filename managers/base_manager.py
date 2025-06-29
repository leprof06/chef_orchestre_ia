
# managers/base_manager.py

class BaseManager:
    def __init__(self, name):
        self.name = name
        self.agents = {}

    def register_agent(self, agent_name, agent_instance):
        self.agents[agent_name] = agent_instance

    def handle_task(self, task):
        raise NotImplementedError("Chaque manager doit implémenter handle_task.")
