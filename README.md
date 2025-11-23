# WhisPay: The Empathetic, Predictive, and Trust-Aware Financial Assistant

## Overview

WhisPay is an AI-powered voice banking companion that listens, understands, and acts securely, intelligently, and with empathy. It reimagines digital banking as a relationship-driven, emotionally aware experience designed to be accessible for everyone, especially the elderly and less tech-savvy users.

## Key Features

### 🎤 Natural Voice Interactions
- **Speech Recognition**: Natural language understanding for intuitive conversations
- **Voice Biometrics**: Secure authentication through voice patterns
- **Emotion Detection**: Detects hesitation, stress, or uncertainty in user's tone

### 🛡️ Advanced Security
- **Voice Biometrics Authentication**: Unique voice pattern recognition
- **Adaptive Trust Mode**: Adjusts behavior based on environmental noise and context
- **Private Mode**: Secure sharing of sensitive information via SMS/WhatsApp
- **Transaction Limits**: User-defined thresholds with re-verification for high-value transactions
- **Multi-Factor Authentication**: Additional security layers when needed

### 🤖 Predictive Intelligence
- **Spending Pattern Analysis**: Understands and predicts financial behaviors
- **Proactive Suggestions**: Anticipates user needs based on transaction history
- **Monthly Summaries**: Automatic spending habit reports
- **Recurring Transaction Reminders**: Suggests regular payments at appropriate times

### ❤️ Empathy & Accessibility
- **Emotional Confidence Check (ECC)**: Detects uncertainty and offers reassurance
- **Explainable AI**: Users can always ask why a suggestion was made
- **Hands-Free Operation**: Complete banking without touching a screen
- **Natural Conversations**: No complex commands required

### 🏦 Banking Operations
- Check account balances
- Transfer funds
- Inquire about loans
- Set payment reminders
- Manage recurring payments
- View transaction history

## Project Structure

```
WhisPay/
├── app/
│   ├── main.py                 # Main application entry point
│   ├── api.py                  # REST API endpoints
│   └── config.py               # Configuration management
├── core/
│   ├── speech/
│   │   ├── recognizer.py       # Speech-to-text processing
│   │   ├── synthesizer.py      # Text-to-speech generation
│   │   └── voice_biometrics.py # Voice authentication
│   ├── nlp/
│   │   ├── intent_detector.py  # Intent classification
│   │   ├── entity_extractor.py # Extract entities (amounts, dates, etc.)
│   │   └── emotion_analyzer.py # Emotion and tone detection
│   └── security/
│       ├── authentication.py   # Authentication manager
│       ├── trust_mode.py       # Adaptive trust system
│       └── privacy.py          # Private mode handlers
├── banking/
│   ├── operations.py           # Banking operations (transfer, balance, etc.)
│   ├── predictor.py            # Predictive analytics
│   └── database.py             # Simulated banking database
├── empathy/
│   ├── ecc.py                  # Emotional Confidence Check
│   └── response_generator.py   # Empathetic response generation
├── evaluation/
│   ├── metrics.py              # Evaluation metrics
│   ├── feedback.py             # User feedback collection
│   └── testing.py              # Test scenarios
├── utils/
│   ├── logger.py               # Logging utilities
│   └── helpers.py              # Helper functions
├── tests/
│   └── ...                     # Unit and integration tests
├── data/
│   ├── users/                  # User profiles and voice prints
│   ├── transactions/           # Transaction history
│   └── models/                 # ML models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
└── README.md                  # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Microphone for voice input
- Internet connection for cloud services (optional)

### Setup

1. **Clone the repository**
```bash
cd d:\vcpkg\some_hackathon
```

2. **Create a virtual environment**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Install dependencies**
```powershell
pip install -r requirements.txt
```

4. **Configure environment variables**
```powershell
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```powershell
python run_whispay.py
```

## Usage

### Starting WhisPay

```powershell
# Run full voice assistant
python run_whispay.py

# Or run demo (no voice required)
python run_demo.py
```

### Example Conversations

**Balance Check:**
```
User: "What's my account balance?"
WhisPay: "Your current balance is ₹45,230. Is there anything else you'd like to know?"
```

**Transfer Funds:**
```
User: "Transfer 5000 rupees to Mom"
WhisPay: "I'll transfer ₹5,000 to Mom's account. Please confirm."
User: "Yes, proceed"
WhisPay: "Transaction successful. ₹5,000 has been sent to Mom."
```

**Emotional Confidence Check:**
```
User: "Um... I want to... maybe transfer some money..."
WhisPay: "You sound unsure. Would you like me to review the details before proceeding?"
```

**Adaptive Trust Mode:**
```
WhisPay: "I detected background noise and can't verify your voice clearly. Let's switch to a secure PIN check for your safety."
```

**Predictive Suggestion:**
```
WhisPay: "It's the 1st of the month. You usually transfer ₹1,000 to your parents around this time. Would you like me to do that now?"
```

## Evaluation Goals

WhisPay's pilot focuses on evaluating:

1. **Accuracy & Response Time**
   - Intent recognition accuracy
   - Entity extraction precision
   - Average response latency

2. **User Trust & Comfort**
   - Trust perception surveys
   - Comfort level ratings
   - Feature adoption rates

3. **Authentication Reliability**
   - Voice biometric accuracy
   - False acceptance/rejection rates
   - Error handling effectiveness

4. **Accessibility**
   - Onboarding time for elderly users
   - Task completion success rates
   - User satisfaction scores

## Security Considerations

- All sensitive data is encrypted at rest and in transit
- Voice biometrics are stored as one-way hashes
- Transaction limits prevent unauthorized high-value transfers
- Adaptive trust mode provides context-aware security
- Private mode ensures sensitive information isn't spoken aloud in public

## Technology Stack

- **Speech Processing**: SpeechRecognition, pyttsx3, pyaudio
- **NLP**: Transformers (BERT), spaCy, NLTK
- **Emotion Analysis**: librosa, TensorFlow/PyTorch
- **Security**: cryptography, hashlib
- **Backend**: Flask/FastAPI
- **Database**: SQLite (pilot), PostgreSQL (production)
- **ML Framework**: scikit-learn, TensorFlow

## Roadmap

- [x] Core voice interaction system
- [x] Basic banking operations
- [x] Emotion detection and ECC
- [x] Voice biometrics
- [ ] Real-world banking API integration
- [ ] Multi-language support
- [ ] Advanced fraud detection
- [ ] Mobile app development
- [ ] Cloud deployment

## Contributing

This is a hackathon project. Contributions and suggestions are welcome!

## License

MIT License - See LICENSE file for details

## Contact

For questions or feedback about WhisPay, please open an issue in the repository.

---

**WhisPay: Banking that listens, protects, predicts, and truly understands.**
