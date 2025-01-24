# Use the official Python 3.13.1 alpine image as the base image
FROM python:3.13.1-alpine3.21

# Set the working directory inside the container to /app
WORKDIR /app

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev

# Copy the requirements.txt file from the host to the working directory in the container
COPY src/requirements.txt requirements.txt

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from the host to the working directory in the container
COPY src/ .

# Define the command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "4"]