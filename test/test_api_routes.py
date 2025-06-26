# test/test_api_routes.py

import unittest
from agents.chef_agent import ChefOrchestreAgent
from agents.test_agent import TestAgent

class TestOrchestration(unittest.TestCase):
    def test_dispatch_to_test_agent(self):
        chef = ChefOrchestreAgent(agents={"TestAgent": TestAgent()})
        result = chef.handle_task("Écris des tests pour une fonction Flask")
        self.assertIn("TestAgent", result)
        self.assertIn("Tests générés", result)

if __name__ == '__main__':
    unittest.main()
