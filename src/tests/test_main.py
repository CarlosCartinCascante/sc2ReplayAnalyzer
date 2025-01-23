import unittest
import json
from src.main import app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test client for the Flask application.
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """
        Test the home route to ensure it returns the correct message.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "API is running!")

    def test_analyze_replay_base64_no_data(self):
        """
        Test the /analyzeReplayBase64 endpoint with no data.
        Ensure it returns a 400 status code and an appropriate error message.
        """
        response = self.app.post('/analyzeReplayBase64', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file_base64 provided', response.data.decode())

    def test_analyze_replay_url_no_data(self):
        """
        Test the /analyzeReplayUrl endpoint with no data.
        Ensure it returns a 400 status code and an appropriate error message.
        """
        response = self.app.post('/analyzeReplayUrl', data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file_url provided', response.data.decode())

    def test_analyze_replay_url_invalid_url(self):
        """
        Test the /analyzeReplayUrl endpoint with an invalid URL.
        Ensure it returns a 400 status code and an appropriate error message.
        """
        response = self.app.post('/analyzeReplayUrl', data=json.dumps({'file_url': 'http://invalid-url'}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Failed to download file', response.data.decode())

if __name__ == '__main__':
    unittest.main()