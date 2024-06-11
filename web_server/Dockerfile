# Use the official Python image as a parent image
FROM python:3.9-slim
LABEL maintainer="Derick Omuga <derick.omuga@strathmore.edu>"
# Set environment variables
ENV SERVER_ID="web_server"

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container
COPY . .

# Expose port 5000 to the outside world


# Run the Flask application
CMD ["python", "webserver.py"]

