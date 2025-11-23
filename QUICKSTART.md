# WhisPay - Quick Start Guide

Welcome to WhisPay! This guide will help you get started with the empathetic, predictive, and trust-aware financial assistant.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Microphone (for voice interaction)
- Windows/Linux/macOS

## Installation Steps

### 1. Navigate to Project Directory

```powershell
cd d:\vcpkg\some_hackathon
```

### 2. Create Virtual Environment

```powershell
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows CMD:**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

**Note:** Some dependencies like `pyaudio` may require additional system libraries:

**Windows:**
- Download and install PyAudio wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
- Or use: `pip install pipwin; pipwin install pyaudio`

**Linux:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### 5. Configure Environment

```powershell
cp .env.example .env
```

Edit `.env` file and configure:
- Twilio credentials (optional, for SMS/WhatsApp features)
- Database settings
- Model preferences

### 6. Create Required Directories

```powershell
mkdir data, logs, data\users, data\users\voice_prints, data\transactions, data\metrics, data\models
```

## Running WhisPay

### Option 1: Run Demo (Recommended for First Time)

The demo script demonstrates all features without requiring voice input:

```powershell
python run_demo.py
```

This will show you:
- Intent detection and entity extraction
- Emotion analysis and confidence checks
- Banking operations (balance, transfers, loans)
- Predictive analytics and suggestions
- Empathetic response generation
- Evaluation metrics

### Option 2: Run Full Voice Assistant

**Important:** Always run from the project root directory:

```powershell
# Make sure you're in the project root (d:\vcpkg\some_hackathon)
python run_whispay.py
```

This starts the full voice-interactive banking assistant.

**Default Demo Credentials:**
- User ID: `user001`
- PIN: `1234`
- Initial Balance: ₹50,000
- Saved Beneficiaries: Mom, Dad, Sister

## Basic Usage Examples

Once WhisPay is running, you can say:

### Check Balance
```
"What's my account balance?"
"How much money do I have?"
```

### Transfer Money
```
"Transfer 5000 rupees to Mom"
"Send 1000 to Sister"
```

### View History
```
"Show me my recent transactions"
"What did I spend last month?"
```

### Loan Inquiry
```
"I want to apply for a personal loan"
"Tell me about home loans"
```

### Get Help
```
"What can you do?"
"Help me"
```

## Key Features

### 🎤 Voice Interaction
- Natural language understanding
- Hands-free operation
- Voice biometric authentication

### 🛡️ Security
- Multi-factor authentication
- Adaptive trust mode
- Transaction limits
- Private mode for sensitive info

### 🤖 Predictive Intelligence
- Spending pattern analysis
- Recurring transaction detection
- Proactive suggestions
- Monthly summaries

### ❤️ Empathy
- Emotion detection
- Confidence checks
- Reassuring responses
- Error handling with empathy

## Troubleshooting

### Microphone Not Working
1. Check microphone permissions
2. Test with: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`
3. Ensure no other app is using the microphone

### Import Errors
```powershell
# Make sure you're in the virtual environment
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Errors
```powershell
# Delete and recreate database
rm data\whispay.db
python demo.py
```

### Speech Recognition Not Working
- Check internet connection (Google Speech API requires internet)
- Try adjusting microphone volume
- Reduce background noise

## Project Structure

```
WhisPay/
├── app/                    # Main application
│   ├── main.py            # Entry point
│   └── config.py          # Configuration
├── core/                  # Core modules
│   ├── speech/           # Speech processing
│   ├── nlp/              # Natural language processing
│   └── security/         # Security features
├── banking/              # Banking operations
├── empathy/              # Empathy features
├── evaluation/           # Metrics and feedback
├── utils/                # Utilities
├── data/                 # Data storage
└── logs/                 # Application logs
```

## Configuration

Edit `.env` file to customize:

```ini
# Enable/disable features
ENABLE_PREDICTIONS=True
STRESS_DETECTION_ENABLED=True
PRIVATE_MODE_ENABLED=True

# Adjust thresholds
VOICE_BIOMETRIC_THRESHOLD=0.85
HIGH_VALUE_THRESHOLD=25000

# Speech settings
SPEECH_LANGUAGE=en-IN
TTS_RATE=150
```

## Development

### Running Tests
```powershell
pytest tests/
```

### Code Formatting
```powershell
black .
flake8 .
```

### Generate Metrics Report
```python
from evaluation.metrics import metrics
report = metrics.generate_report()
metrics.export_metrics()
```

## Next Steps

1. **Customize**: Modify intents, responses, and thresholds for your use case
2. **Integrate**: Connect to real banking APIs (replace simulated backend)
3. **Extend**: Add new features like bill payments, investments, etc.
4. **Evaluate**: Use the evaluation framework to measure performance
5. **Deploy**: Set up on cloud platform for production use

## Support

For issues or questions:
1. Check the logs in `logs/whispay.log`
2. Review the README.md for detailed documentation
3. Open an issue in the repository

## Security Note

⚠️ This is a pilot/demo version. For production use:
- Use real authentication services
- Implement proper encryption
- Add fraud detection
- Use HTTPS for API calls
- Comply with banking regulations
- Conduct security audits

---

**Happy Banking with WhisPay!** 🎤💰🤖
