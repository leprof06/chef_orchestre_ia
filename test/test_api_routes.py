# test/test_api_routes.py

import unittest
from fastapi.testclient import TestClient
from backend.routes import app

client = TestClient(app)

class TestAPIRoutes(unittest.TestCase):

    def test_root_route(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Chef d'Orchestre IA", response.text)

    def test_post_task(self):
        payload = {"task": "génère une fonction qui additionne deux nombres"}
        response = client.post("/task", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("additionne" in response.text.lower())

if __name__ == "__main__":
    unittest.main()
