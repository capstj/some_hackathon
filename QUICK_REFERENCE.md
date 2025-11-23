# WhisPay Quick Reference

## 🚀 Running WhisPay

### From Root Directory (ALWAYS)
```powershell
# Full voice assistant
python run_whispay.py

# Demo mode (no voice)
python run_demo.py

# Test setup
python test_setup.py
```

## ⚡ Quick Commands

### Setup
```powershell
# Windows automated setup
.\setup.bat

# Manual setup
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Activate Environment
```powershell
# Every time you open a new terminal
.\venv\Scripts\activate
```

### Create Directories
```powershell
mkdir data, data\users, data\users\voice_prints, data\transactions, data\metrics, logs
```

## 🎤 Voice Commands

### Banking Operations
- "What's my balance?"
- "Transfer 5000 to Mom"
- "Show my recent transactions"
- "When did I pay my electricity bill?"

### Loans
- "Do I have any active loans?"
- "What's my loan EMI?"
- "When is my next loan payment?"

### Reminders
- "Set a reminder to pay rent on the 1st"
- "What are my reminders?"
- "Show payment reminders"

### Predictions
- "What are my spending patterns?"
- "Any upcoming bills?"
- "Show monthly summary"

### Account
- "Exit" or "Logout"

## 🔐 Default Demo Credentials

```
User ID: user001
PIN: 1234
Voice: Enroll during first login
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `run_whispay.py` | Launch full app |
| `run_demo.py` | Launch demo |
| `test_setup.py` | Verify installation |
| `.env` | Configuration |
| `requirements.txt` | Dependencies |
| `data/whispay.db` | Database |
| `logs/` | Application logs |

## 🛠️ Common Fixes

### Import Error
```powershell
# Always run from root
cd d:\vcpkg\some_hackathon
python run_whispay.py
```

### Missing Packages
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Missing Directories
```powershell
.\setup.bat
```

### Reset Database
```powershell
Remove-Item data\whispay.db
```

## 📊 Features Overview

✅ Voice Recognition (STT)  
✅ Voice Synthesis (TTS)  
✅ Voice Biometrics  
✅ Natural Language Understanding  
✅ Emotion Detection  
✅ Empathetic Responses  
✅ Balance Inquiries  
✅ Money Transfers  
✅ Transaction History  
✅ Loan Management  
✅ Payment Reminders  
✅ Spending Predictions  
✅ Adaptive Security  
✅ Private Mode (SMS)  
✅ Performance Metrics  

## 📝 Environment Variables

Key `.env` settings:
```bash
# Security
VOICE_MATCH_THRESHOLD=0.8
PIN_MIN_LENGTH=4
SESSION_TIMEOUT_MINUTES=15

# Trust Mode
TRUST_HIGH_NOISE_THRESHOLD=0.3
TRUST_MEDIUM_CONFIDENCE=0.7

# SMS (Optional)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Logging
LOG_LEVEL=INFO
```

## 🏗️ Project Structure
```
some_hackathon/
├── app/                 # Main application
├── core/                # Core components
│   ├── speech/         # Voice processing
│   ├── nlp/            # NLP models
│   └── security/       # Auth & security
├── banking/             # Banking logic
├── empathy/             # ECC & responses
├── evaluation/          # Metrics
├── utils/               # Utilities
├── data/                # User data
├── logs/                # Log files
├── run_whispay.py      # Main launcher
└── run_demo.py         # Demo launcher
```

## 📚 Documentation

- `README.md` - Overview
- `QUICKSTART.md` - Setup guide
- `ARCHITECTURE.md` - System design
- `PROJECT_SUMMARY.md` - Features
- `TROUBLESHOOTING.md` - Common issues

## 🎯 Development Workflow

1. Activate environment: `.\venv\Scripts\activate`
2. Make changes to code
3. Test: `python test_setup.py`
4. Run: `python run_demo.py` or `python run_whispay.py`
5. Check logs: `type logs\whispay_*.log`

## 🔍 Debugging

```powershell
# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Test imports
python -c "from app.main import WhisPayAssistant; print('OK')"

# View logs
Get-Content logs\whispay_*.log -Tail 50

# List audio devices
python -c "import sounddevice as sd; print(sd.query_devices())"
```

## 💡 Tips

- Run from project root only
- Keep environment activated
- Check logs for errors
- Start with demo mode
- Use quiet environment for voice
- Backup `data/` directory regularly

---

**Need Help?** See `TROUBLESHOOTING.md`
