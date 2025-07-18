FROM python:3.11-slim

# Metadata
LABEL maintainer="Malith Rukshan <contact@malith.dev>"
LABEL description="Whisper Transcriber Bot - AI-powered audio to text conversion for Telegram"
LABEL version="1.0.1"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    cmake \
    build-essential \
    pkg-config \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY download_model.sh .
COPY .env.example .

# Create necessary directories
RUN mkdir -p models

# Make script executable
RUN chmod +x download_model.sh

# Download Whisper model
RUN ./download_model.sh

# Run bot
CMD ["python", "src/bot.py"]