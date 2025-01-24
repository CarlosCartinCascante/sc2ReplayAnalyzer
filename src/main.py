from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import base64
import aiohttp
import spawningtool.parser
import io
import uvicorn

app = FastAPI()

class Base64Request(BaseModel):
    file_base64: str

class URLRequest(BaseModel):
    file_url: str

@app.get("/")
def read_root():
    """
    Root endpoint to check if the API is running.
    Returns:
        dict: A message indicating that the API is running.
    """
    return {"message": "API is running!"}

@app.post("/analyzeReplayBase64")
async def analyze_replay_base64(request: Base64Request):
    """
    Endpoint to analyze a replay file provided as a base64 encoded string.
    Args:
        request (Base64Request): The request body containing the base64 encoded string.
    Returns:
        dict: Parsed replay information.
    Raises:
        HTTPException: If the base64 string is not provided.
    """
    base64_string = request.file_base64

    if not base64_string:
        raise HTTPException(status_code=400, detail="No file_base64 provided")

    replay_file = io.BytesIO()
    chunk_size = 8192  # Define the chunk size for processing

    for i in range(0, len(base64_string), chunk_size):
        chunk = base64_string[i:i + chunk_size]
        decoded_chunk = base64.b64decode(chunk)
        replay_file.write(decoded_chunk)

    replay_file.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return replay_info

@app.post("/analyzeReplayUrl")
async def analyze_replay_url(request: URLRequest):
    """
    Endpoint to analyze a replay file provided as a URL.
    Args:
        request (URLRequest): The request body containing the URL of the replay file.
    Returns:
        dict: Parsed replay information.
    Raises:
        HTTPException: If the URL is not provided or if the file download fails.
    """
    replay_url = request.file_url

    if not replay_url:
        raise HTTPException(status_code=400, detail="No file_url provided")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(replay_url) as response:
                response.raise_for_status()
                replay_file = io.BytesIO()
                async for chunk in response.content.iter_chunked(8192):
                    replay_file.write(chunk)
    except aiohttp.ClientError as e:
        raise HTTPException(status_code=400, detail=f"Failed to download file: {str(e)}") from e

    replay_file.seek(0)  # Reset the pointer to the beginning of the BytesIO object

    replay_info = spawningtool.parser.parse_replay(replay_file)
    return replay_info

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)