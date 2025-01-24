import unittest
from fastapi.testclient import TestClient
from src.main import app

class FastAPITestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client for the FastAPI application.
        """
        self.client = TestClient(app)

    def test_home(self):
        """
        Test the home route to ensure it returns the correct message.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "API is running!"})

    def test_analyze_replay_base64_no_data(self):
        """
        Test the /analyzeReplayBase64 endpoint with no data.
        Ensure it returns a 422 status code and an appropriate error message.
        """
        response = self.client.post('/analyzeReplayFile', json={})
        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())

    def test_analyze_replay_url_no_data(self):
        """
        Test the /analyzeReplayUrl endpoint with no data.
        Ensure it returns a 422 status code and an appropriate error message.
        """
        response = self.client.post('/analyzeReplayUrl', json={})
        self.assertEqual(response.status_code, 422)
        self.assertIn('detail', response.json())

    def test_analyze_replay_url_invalid_url(self):
        """
        Test the /analyzeReplayUrl endpoint with an invalid URL.
        Ensure it returns a 400 status code and an appropriate error message.
        """
        response = self.client.post('/analyzeReplayUrl', json={'file_url': 'http://invalid-url'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to download file', response.json()['detail'])

if __name__ == '__main__':
    unittest.main()