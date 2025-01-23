# Use the official Python 3.9 slim image as the base image
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file from the host to the working directory in the container
COPY src/requirements.txt requirements.txt

# Install the Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code from the host to the working directory in the container
COPY src/ .

# Set environment variables for Flask
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# Define the command to run the Flask application
CMD ["python3", "main.py"]