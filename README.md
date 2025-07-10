<p style="text-align:center;" align="center">
  <img align="center" src="https://raw.githubusercontent.com/Malith-Rukshan/whisper-transcriber-bot/refs/heads/main/logo.png" alt="TranscriberXBOT" width="320px" height="320px"/>
</p>
<h1 align="center">🎙️ Whisper Transcriber Bot</h1>
<div align="center">

[![Telegram](https://img.shields.io/badge/Telegram-Demo-01CC1D?logo=telegram&style=flat)](https://t.me/TranscriberXBOT)
[![Docker](https://img.shields.io/badge/Docker-Ready-2D80E3?logo=docker&style=flat)](https://hub.docker.com/r/malithrukshan/whisper-transcriber-bot)
![License](https://img.shields.io/badge/License-MIT-green.svg)

</div>

<h4 align="center">✨ Transform voice into text instantly with AI-powered transcription magic! ✨</h4>

<div align="center">
  - A self-hosted, privacy-focused transcription for Telegram -
  <br/>
  <sup><sub>🚀 No GPU Required • No API Keys • CPU-Only • Low Resource Usage ツ</sub></sup>
</div>

## ✨ Features

- 🎙️ **Voice Transcription** - Convert voice messages to text instantly
- 🎵 **Multi-Format Support** - MP3, M4A, WAV, OGG, FLAC audio files
- ⚡ **Concurrent Processing** - Handle multiple users simultaneously
- 📝 **Smart Text Handling** - Auto-generate text files for long transcriptions
- 🧠 **AI-Powered** - OpenAI Whisper model for accurate transcription
- 💻 **CPU-Only Processing** - No GPU required, runs on basic servers (512MB RAM minimum)
- 🚫 **No API Dependencies** - No external API keys or cloud services needed
- 🐳 **Docker Ready** - Easy deployment with containerization
- 🔒 **Privacy Focused** - Process audio locally, complete data privacy
- 💰 **Cost Effective** - Ultra-low resource usage, perfect for budget hosting

## 🎬 Demo

<img src="https://raw.githubusercontent.com/Malith-Rukshan/whisper-transcriber-bot/refs/heads/main/demo.gif" alt="Whisper Transcriber Bot Demo" width="320px" style="border-radius: 15px; box-shadow: 0 8px 16px rgba(0,0,0,0.15);"/>

## 🚀 One-Click Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)
</br>
[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/Malith-Rukshan/whisper-transcriber-bot/tree/main)

*Deploy instantly to your favorite cloud platform with pre-configured settings! All platforms support CPU-only deployment - no GPU needed!*

## 📝 Quick Start

### Prerequisites

- Docker and Docker Compose
- Telegram Bot Token ([Create Bot](https://t.me/botfather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Malith-Rukshan/whisper-transcriber-bot.git
   cd whisper-transcriber-bot
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Add your bot token
   ```

3. **Download AI model**
   ```bash
   chmod +x download_model.sh
   ./download_model.sh
   ```

4. **Deploy with Docker**
   ```bash
   docker-compose up -d
   ```

🎉 **That's it!** Your bot is now running and ready to transcribe audio!

## 📋 Usage

### Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | 🏠 Welcome message and bot introduction |
| `/help` | 📖 Detailed usage instructions |
| `/about` | ℹ️ Bot information and developer details |
| `/status` | 🔍 Check bot health and configuration |

### How to Use

1. **Send Audio** 🎙️ - Forward voice messages or upload audio files
2. **Wait for AI** ⏳ - Bot processes audio (typically 1-3 seconds)
3. **Get Text** 📝 - Receive transcription or download text file for long content

### Supported Formats

- **Voice Messages** - Direct Telegram voice notes
- **Audio Files** - MP3, M4A, WAV, OGG, FLAC (up to 50MB)
- **Document Audio** - Audio files sent as documents

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  whisper-bot:
    image: malithrukshan/whisper-transcriber-bot:latest
    container_name: whisper-transcriber-bot
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    volumes:
      - ./models:/app/models
```

### Using Docker CLI

```bash
docker run -d \
  --name whisper-bot \
  -e TELEGRAM_BOT_TOKEN=your_token_here \
  -v $(pwd)/models:/app/models \
  malithrukshan/whisper-transcriber-bot:latest
```

## 🛠️ Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/Malith-Rukshan/whisper-transcriber-bot.git
cd whisper-transcriber-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Download model
./download_model.sh

# Configure environment
cp .env.example .env
# Add your bot token to .env

# Run bot
python src/bot.py
```

### Project Structure

```
whisper-transcriber-bot/
├── src/                    # Source code
│   ├── bot.py             # Main bot application
│   ├── transcriber.py     # Whisper integration
│   ├── config.py          # Configuration management
│   └── utils.py           # Utility functions
├── tests/                 # Test files
│   ├── test_bot.py        # Bot functionality tests
│   └── test_utils.py      # Utility function tests
├── .github/workflows/     # CI/CD automation
├── models/                # AI model storage
├── Dockerfile            # Container configuration
├── docker-compose.yml    # Deployment setup
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
└── README.md            # This file
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_bot.py

# Run with verbose output
python -m pytest -v
```

### Test Coverage

The test suite covers:
- ✅ Bot initialization and configuration
- ✅ Command handlers (`/start`, `/help`, `/about`, `/status`)
- ✅ Audio processing workflow
- ✅ Utility functions
- ✅ Error handling scenarios

### Code Quality

```bash
# Format code
black src/ tests/

# Security check
bandit -r src/
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Required |
| `WHISPER_MODEL_PATH` | Path to Whisper model file | `models/ggml-base.en.bin` |
| `WHISPER_MODEL_NAME` | Model name for display | `base.en` |
| `BOT_USERNAME` | Bot username for branding | `TranscriberXBOT` |
| `MAX_AUDIO_SIZE_MB` | Maximum audio file size | `50` |
| `SUPPORTED_FORMATS` | Supported audio formats | `mp3,m4a,wav,ogg,flac` |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Performance Tuning

```bash
# Adjust CPU threads for transcription
export WHISPER_THREADS=4

# Set memory limits
export WHISPER_MAX_MEMORY=512M

# Configure concurrent processing
export MAX_CONCURRENT_TRANSCRIPTIONS=5
```

## 📊 Performance Metrics

| Audio Length | Processing Time | Memory Usage |
|--------------|----------------|--------------|
| 30 seconds   | ~1.2 seconds   | ~180MB       |
| 2 minutes    | ~2.8 seconds   | ~200MB       |
| 5 minutes    | ~6.1 seconds   | ~220MB       |

### Scaling Recommendations

- **Single Instance**: Handles 50+ concurrent users
- **Minimal Resources**: 1 CPU core, 512MB RAM minimum (no GPU required!)
- **Storage**: 1GB for model + temporary files
- **Cost-Effective**: Perfect for budget VPS hosting ($5-10/month)
- **No External APIs**: Zero ongoing API costs or dependencies
- **Load Balancing**: Deploy multiple instances for higher traffic

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation
- Ensure Docker build succeeds
- Run quality checks before PR

## 📈 Technical Architecture

### Core Components

- **Framework**: [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) v22.2
- **AI Model**: [OpenAI Whisper](https://github.com/openai/whisper) base.en (147MB, CPU-optimized)
- **Bindings**: [pywhispercpp](https://github.com/aarnphm/pywhispercpp) for C++ performance (no GPU needed)
- **Runtime**: Python 3.11 with asyncio for concurrent processing
- **Container**: Multi-architecture Docker (AMD64/ARM64)
- **Resource**: CPU-only inference, minimal memory footprint

### Performance Features

- **Async Processing**: Non-blocking audio transcription
- **Concurrent Handling**: Multiple users supported simultaneously
- **Memory Management**: Efficient model loading and cleanup
- **Error Recovery**: Robust error handling and logging

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For the incredible Whisper speech recognition model
- **pywhispercpp** - High-performance Python bindings for whisper.cpp
- **python-telegram-bot** - Excellent Telegram Bot API framework
- **whisper.cpp** - Optimized C++ implementation of Whisper

## 👨‍💻 Developer

**Malith Rukshan**
- 🌐 Website: [malith.dev](https://malith.dev)
- 📧 Email: hello@malith.dev
- 🐦 Telegram: [@MalithRukshan](https://t.me/MalithRukshan)

---

<div align="center">

### ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Malith-Rukshan/whisper-transcriber-bot&type=Date)](https://star-history.com/#Malith-Rukshan/whisper-transcriber-bot&Date)

**If this project helped you, please consider giving it a ⭐!**

Made with ❤️ by [Malith Rukshan](https://malith.dev)

[🚀 Try the Bot](https://t.me/TranscriberXBOT) • [⭐ Star on GitHub](https://github.com/Malith-Rukshan/whisper-transcriber-bot) • [🐳 Docker Hub](https://hub.docker.com/r/malithrukshan/whisper-transcriber-bot)

</div>