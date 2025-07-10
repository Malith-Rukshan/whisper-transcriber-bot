# Contributing to Whisper Transcriber Bot

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. **Fork the repository** and create your branch from `main`
2. **Clone your fork** locally
3. **Create a feature branch**: `git checkout -b feature/amazing-feature`
4. **Set up development environment** (see below)
5. **Make your changes** and ensure the tests pass
6. **Commit your changes**: `git commit -m 'Add amazing feature'`
7. **Push to the branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
- Docker (for testing containerization)
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/your-username/whisper-transcriber-bot.git
cd whisper-transcriber-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Download model for testing
./download_model.sh

# Set up environment variables
cp .env.example .env
# Add your test bot token to .env
```

## Code Style and Quality

We use several tools to maintain code quality:

### Code Formatting

```bash
# Format Python code
black src/ tests/

# Sort imports
isort src/ tests/
```

### Linting

```bash
# Check code style
flake8 src/ tests/
```

### Security

```bash
# Security check
bandit -r src/
```

### Pre-commit Hooks

Set up pre-commit hooks to automatically run checks:

```bash
# Install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/test_bot.py

# Run with verbose output
python -m pytest tests/ -v
```

### Test Files

The project includes tests for all main modules:

- `tests/test_bot.py` - Tests for bot functionality and commands
- `tests/test_transcriber.py` - Tests for audio transcription
- `tests/test_utils.py` - Tests for utility functions
- `tests/test_config.py` - Tests for configuration management

### Writing Tests

- Write minimal but comprehensive tests
- Tests should be in the `tests/` directory
- Use descriptive test names
- Mock external dependencies (Telegram API, Whisper models)
- Focus on core functionality

### Test Guidelines

```python
# Good test example
def test_format_transcription_with_text():
    """Test transcription formatting with normal text"""
    result = format_transcription("Hello world")
    assert "Hello world" in result
    assert "📝 *Transcription:*" in result
```

## Documentation

### Code Documentation

- Use docstrings for all functions and classes
- Follow Google-style docstring format
- Include type hints where appropriate

```python
def transcribe_audio(self, file_path: str) -> Optional[str]:
    """
    Transcribe audio file to text.
    
    Args:
        file_path: Path to the audio file
        
    Returns:
        Transcribed text or None if failed
        
    Raises:
        FileNotFoundError: If audio file doesn't exist
    """
```

### README Updates

- Update README.md if your changes affect usage
- Add new features to the features list
- Update configuration sections if needed

## Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/Malith-Rukshan/whisper-transcriber-bot/issues).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: [e.g. Ubuntu 20.04]
- Python version: [e.g. 3.11.0]
- Bot version: [e.g. 1.0.0]

## Additional Context
Any other context about the problem
```

## Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Use the feature request template**
3. **Provide clear use cases**
4. **Consider implementation complexity**

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other context or screenshots
```

## Commit Messages

We follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Examples
```bash
feat(bot): add support for video transcription
fix(transcriber): handle empty audio files
docs(readme): update installation instructions
test(utils): add tests for file cleanup
```

## Code Review Process

The core team looks at Pull Requests on a regular basis. After feedback has been given we expect responses within two weeks. After two weeks we may close the pull request if it isn't showing any activity.

### Review Criteria

- **Code Quality**: Follows style guide and best practices
- **Testing**: Adequate test coverage for new features
- **Documentation**: Updated documentation where necessary
- **Functionality**: Feature works as described
- **Performance**: No significant performance regressions

## Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Docker image is automatically built and pushed

## Community Guidelines

### Code of Conduct

- **Be respectful**: Treat everyone with respect
- **Be inclusive**: Welcome newcomers and diverse perspectives
- **Be collaborative**: Work together constructively
- **Be professional**: Maintain professionalism in all interactions

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Email**: contact@malith.dev for sensitive matters

## Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes
- Project documentation

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the project.

## Questions?

Don't hesitate to reach out if you have questions about contributing:

- Create an issue for technical questions
- Email contact@malith.dev for other inquiries
- Check existing issues and discussions

Thank you for contributing to Whisper Transcriber Bot! 🎙️