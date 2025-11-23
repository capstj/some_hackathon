# WhisPay Troubleshooting Guide

## Common Issues and Solutions

### Import Errors

#### Error: `ModuleNotFoundError: No module named 'utils'`

**Problem:** Running WhisPay from the wrong directory.

**Solution:** Always run from the project root directory:
```powershell
# ✓ Correct
cd d:\vcpkg\some_hackathon
python run_whispay.py

# ✗ Wrong
cd d:\vcpkg\some_hackathon\app
python main.py
```

#### Error: `ModuleNotFoundError: No module named 'loguru'` (or other packages)

**Problem:** Dependencies not installed.

**Solution:**
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Audio Issues

#### Error: `ModuleNotFoundError: No module named '_portaudio'`

**Problem:** PyAudio not installed correctly on Windows.

**Solutions:**

**Option 1: Use pre-built wheel (Recommended)**
```powershell
# Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Example for Python 3.10, 64-bit:
pip install PyAudio-0.2.11-cp310-cp310-win_amd64.whl
```

**Option 2: Install with pipwin**
```powershell
pip install pipwin
pipwin install pyaudio
```

**Option 3: Use conda**
```powershell
conda install pyaudio
```

#### Error: `OSError: [Errno -9996] Invalid input device`

**Problem:** Microphone not detected or not accessible.

**Solution:**
1. Check microphone is connected
2. Grant microphone permissions to Python
3. Test microphone:
   ```powershell
   python -c "import sounddevice as sd; print(sd.query_devices())"
   ```

### Database Issues

#### Error: `sqlite3.OperationalError: unable to open database file`

**Problem:** Missing data directory.

**Solution:**
```powershell
# Create required directories
mkdir data, data\users, data\users\voice_prints, data\transactions, data\metrics
```

Or run the setup script:
```powershell
.\setup.bat
```

### Configuration Issues

#### Error: `pydantic_core._pydantic_core.ValidationError`

**Problem:** Invalid `.env` configuration.

**Solution:**
```powershell
# Recreate .env from template
copy .env.example .env

# Edit .env and ensure all required fields are filled
```

### Voice Biometrics Issues

#### Voice not recognized during authentication

**Problem:** Noisy environment or inconsistent voice recording.

**Troubleshooting:**
1. Ensure quiet environment during enrollment
2. Speak clearly and consistently
3. Check microphone quality
4. Increase `VOICE_MATCH_THRESHOLD` in `.env` (e.g., to 0.7)

### Performance Issues

#### Slow response times

**Possible causes and solutions:**

1. **Large transaction history:**
   - Archive old transactions periodically
   - Add database indexes

2. **Heavy NLP processing:**
   - Consider using smaller emotion detection models
   - Cache frequently used predictions

3. **Slow TTS:**
   - Adjust speech rate in settings
   - Use faster TTS engine

### Windows-Specific Issues

#### Error: `Microsoft Visual C++ 14.0 is required`

**Problem:** Missing C++ compiler for some packages.

**Solution:**
Download and install Microsoft C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

#### PowerShell execution policy error

**Problem:** Scripts disabled by execution policy.

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Testing Issues

#### Demo script fails

**Problem:** Missing test data.

**Solution:**
```powershell
# Ensure you're in project root
cd d:\vcpkg\some_hackathon

# Run demo with proper path
python run_demo.py
```

## Getting Help

### Check Logs

Logs are stored in `logs/` directory:
```powershell
# View latest log
type logs\whispay_*.log | Select-Object -Last 50
```

### Verify Installation

Run the setup verification script:
```powershell
python test_setup.py
```

### Enable Debug Mode

Edit `.env`:
```
LOG_LEVEL=DEBUG
```

### Report Issues

When reporting issues, include:
1. Python version: `python --version`
2. OS version: `systeminfo | findstr /B /C:"OS Name" /C:"OS Version"`
3. Error message and full traceback
4. Log file contents from `logs/` directory
5. Steps to reproduce

## Common Questions

### Q: Can I run WhisPay without a microphone?

**A:** Yes! Use the demo script:
```powershell
python run_demo.py
```

### Q: How do I reset the database?

**A:** Delete the database file:
```powershell
Remove-Item data\whispay.db
```
The database will be recreated on next run.

### Q: How do I change the voice model?

**A:** Edit `.env`:
```
TTS_VOICE_ID=your_preferred_voice
```

### Q: Can I use a different database?

**A:** Yes! Edit `app/config.py` and update `DATABASE_URL`. Supports PostgreSQL, MySQL, etc.

### Q: How do I backup user data?

**A:** Backup these directories:
```powershell
# Copy to backup location
Copy-Item -Recurse data backup_location\
Copy-Item -Recurse logs backup_location\
```

### Q: How secure is voice biometrics?

**A:** Voice biometrics in WhisPay is for pilot testing. For production:
- Use multi-factor authentication
- Implement liveness detection
- Add fraud monitoring
- Use hardware security modules (HSM)

## Still Having Issues?

1. Check `QUICKSTART.md` for detailed setup instructions
2. Review `ARCHITECTURE.md` to understand system design
3. Examine `PROJECT_SUMMARY.md` for feature details
4. Run `python test_setup.py` to diagnose setup issues
