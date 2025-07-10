#!/bin/bash

# Download Whisper model script
# This script downloads the Whisper model for the transcriber bot

set -e

MODEL_DIR="models"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main"
MODEL_NAME="ggml-base.en.bin"

echo "🔽 Downloading Whisper model..."

# Create models directory if it doesn't exist
mkdir -p "$MODEL_DIR"

# Download the model
if [ ! -f "$MODEL_DIR/$MODEL_NAME" ]; then
    echo "📥 Downloading $MODEL_NAME..."
    wget -O "$MODEL_DIR/$MODEL_NAME" "$MODEL_URL/$MODEL_NAME"
    echo "✅ Model downloaded successfully!"
else
    echo "ℹ️  Model already exists: $MODEL_DIR/$MODEL_NAME"
fi

# Verify download
if [ -f "$MODEL_DIR/$MODEL_NAME" ]; then
    file_size=$(stat -c%s "$MODEL_DIR/$MODEL_NAME")
    echo "📊 Model size: $((file_size / 1024 / 1024)) MB"
    echo "🎯 Model ready for use!"
else
    echo "❌ Model download failed!"
    exit 1
fi