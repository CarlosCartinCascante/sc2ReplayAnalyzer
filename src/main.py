from flask import Flask, request, jsonify
import base64
import requests
import spawningtool.parser
import io

app = Flask(__name__)

@app.route('/')
def home():
    """
    Home route to check if the API is running.
    Returns:
        str: A message indicating that the API is running.
    """
    return "API is running!"

@app.route('/analyzeReplayBase64', methods=['POST'])
def analyze_replay_base64():
    """
    Endpoint to analyze a replay file provided as a base64 encoded string.
    Expects a JSON payload with a 'file_base64' key.
    Returns:
        JSON: Parsed replay information or an error message.
    """
    data = request.json
    base64_string = data.get('file_base64')

    if not base64_string:
        return jsonify({"error": "No file_base64 provided"}), 400

    replay_file = io.BytesIO()
    chunk_size = 8192  # Define the chunk size for processing

    for i in range(0, len(base64_string), chunk_size):
        chunk = base64_string[i:i + chunk_size]
        decoded_chunk = base64.b64decode(chunk)
        replay_file.write(decoded_chunk)

    replay_file.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return jsonify(replay_info), 200

@app.route('/analyzeReplayUrl', methods=['POST'])
def analyze_replay_url():
    """
    Endpoint to analyze a replay file provided as a URL.
    Expects a JSON payload with a 'file_url' key.
    Returns:
        JSON: Parsed replay information or an error message.
    """
    data = request.json
    replay_url = data.get('file_url')

    if not replay_url:
        return jsonify({"error": "No file_url provided"}), 400

    try:
        with requests.get(replay_url, stream=True) as response:
            response.raise_for_status()
            replay_file = io.BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                replay_file.write(chunk)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to download file", "details": str(e)}), 400

    replay_file.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return jsonify(replay_info), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)