
# managers/base_manager.py
from agents.base_agent import BaseAgent

class BaseManager:
    def __init__(self, name="BaseManager"):
        self.agent = BaseAgent()
        self.name = name

    def register_agent(self, agent_name, agent_instance):
        self.agents[agent_name] = agent_instance

    def handle_task(self, task):
        raise NotImplementedError("Chaque manager doit implémenter handle_task.")
