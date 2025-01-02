# Use official Python image as base
FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container
COPY . .

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set environment variables (they will be passed at runtime)
# The environment variables will be passed at runtime, so no need to define them here

# Run the application
CMD ["python", "main.py"]