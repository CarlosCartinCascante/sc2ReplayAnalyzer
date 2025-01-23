# SC2ReplayAnalyzer Web Application
A web application to analyze StarCraft 2 replay files using the Spawning Tool parser and other resources.

### Project Info
- **Website**: [SC2ReplayAnalyzer](https://github.com/CarlosCartinCascante/sc2ReplayAnalyzer.git)
- **Resources**:
  - [Spawning Tool Parser Documentation](https://github.com/StoicLoofah/spawningtool)
  - [Flask Documentation](https://flask.palletsprojects.com/)
  - [Requests Documentation](https://docs.python-requests.org/)

## Local Development Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/CarlosCartinCascante/sc2ReplayAnalyzer.git
    cd sc2ReplayAnalyzer
    ```

2. Install Dependencies:
    Run the following command to install all necessary packages:
    ```bash
    pip install -r src/requirements.txt
    ```

3. Start Development Server:
    Run the following command to start the Flask development server:
    ```bash
    python3 src/main.py
    ```

    The application will be available at [http://0.0.0.0:5000](http://0.0.0.0:5000).

## API Endpoints

### Home
- **URL**: `/`
- **Method**: `GET`
- **Description**: Home route to check if the API is running.
- **Response**: A message indicating that the API is running.

### Analyze Replay (Base64)
- **URL**: `/analyzeReplayBase64`
- **Method**: `POST`
- **Description**: Endpoint to analyze a replay file provided as a base64 encoded string.
- **Request Payload**: A JSON object with a `file_base64` key containing the base64 encoded string of the replay file.
- **Response**: Parsed replay information or an error message.

### Analyze Replay (URL)
- **URL**: `/analyzeReplayUrl`
- **Method**: `POST`
- **Description**: Endpoint to analyze a replay file provided as a URL.
- **Request Payload**: A JSON object with a `file_url` key containing the URL pointing to the replay file.
- **Response**: Parsed replay information or an error message.

## Running Tests
To run the tests, use the following command:
```bash
python3 -m unittest discover -s src/tests
```