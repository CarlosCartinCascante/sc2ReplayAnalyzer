from flask import Flask, request, jsonify
import base64
import requests
import spawningtool.parser
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running!"

@app.route('/analyzeReplayBase64', methods=['POST'])
def analyze_replay_base64():
    data = request.json
    base64_string = data.get('file_base64')

    if not base64_string:
        return jsonify({"error": "No file_base64 provided"}), 400

    decoded_data = base64.b64decode(base64_string)
    replay_file = io.BytesIO(decoded_data)

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return jsonify(replay_info), 200

@app.route('/analyzeReplayUrl', methods=['POST'])
def analyze_replay_url():
    data = request.json
    replay_url = data.get('file_url')

    if not replay_url:
        return jsonify({"error": "No file_url provided"}), 400

    response = requests.get(replay_url)
    if response.status_code != 200:
        return jsonify({"error": "Failed to download file"}), 400

    replay_file = io.BytesIO(response.content)

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return jsonify(replay_info), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)