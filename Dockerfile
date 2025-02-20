# Dockerfile

# Use a lightweight Python image
FROM python:3.12-slim as base

# Install OS-level dependencies if needed (for example, build tools)
# Install system dependencies
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    python3-pyaudio \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Streamlit uses (default is 8501)
EXPOSE 8501

# Command to run your Streamlit app
CMD ["streamlit", "run", "run.py"]
