# WhisPay System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            USER INTERACTION                              │
│                     (Voice Input / Audio Output)                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        SPEECH PROCESSING LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Speech Recognizer│  │Voice Biometrics  │  │Speech Synthesizer│     │
│  │   (STT Engine)   │  │  Authentication  │  │   (TTS Engine)   │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      NLP & UNDERSTANDING LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Intent Detector  │  │Entity Extractor  │  │ Emotion Analyzer │     │
│  │ (Intent Classify)│  │ (NER/Parsing)    │  │ (Sentiment/Tone) │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         SECURITY & TRUST LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │  Authentication  │  │ Adaptive Trust   │  │  Privacy Mode    │     │
│  │   Manager        │  │     Mode         │  │  (SMS/WhatsApp)  │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EMPATHY & INTELLIGENCE LAYER                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Emotional Conf.  │  │  Response        │  │   Banking        │     │
│  │ Check (ECC)      │  │  Generator       │  │  Predictor       │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        BANKING OPERATIONS LAYER                          │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Balance Checks   │  │  Transfers       │  │ Loan Inquiries   │     │
│  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤     │
│  │ Transaction      │  │  Reminders       │  │ History/Reports  │     │
│  │ History          │  │                  │  │                  │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA PERSISTENCE LAYER                          │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ User Database    │  │ Transaction DB   │  │ Voice Prints     │     │
│  │ (Accounts, Auth) │  │ (History, Logs)  │  │ (Biometrics)     │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      EVALUATION & MONITORING LAYER                       │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │
│  │ Metrics Collector│  │ Feedback System  │  │ Performance      │     │
│  │ (Accuracy, Time) │  │ (User Ratings)   │  │ Analytics        │     │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘     │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Speech Processing Layer

**Speech Recognizer** (`core/speech/recognizer.py`)
- Converts speech to text using Google Speech API
- Handles ambient noise calibration
- Measures background noise levels
- Returns transcribed text

**Voice Biometrics** (`core/speech/voice_biometrics.py`)
- Extracts MFCC features from voice
- Enrolls users with voice samples
- Verifies identity (1:1 matching)
- Identifies users (1:N matching)

**Speech Synthesizer** (`core/speech/synthesizer.py`)
- Converts text responses to speech
- Configurable voice, rate, volume
- Supports saving audio to file

### 2. NLP & Understanding Layer

**Intent Detector** (`core/nlp/intent_detector.py`)
- Classifies user utterances into banking intents
- Pattern-based matching with confidence scoring
- Supports: balance, transfer, history, loans, reminders, etc.

**Entity Extractor** (`core/nlp/entity_extractor.py`)
- Extracts amounts, recipients, dates
- Parses account types, loan types
- Handles time periods and frequencies

**Emotion Analyzer** (`core/nlp/emotion_analyzer.py`)
- Text-based emotion detection
- Audio prosodic feature analysis
- Detects stress, uncertainty, confidence

### 3. Security & Trust Layer

**Authentication Manager** (`core/security/authentication.py`)
- Multi-factor authentication (voice, PIN, OTP)
- Session management
- OTP generation and verification

**Adaptive Trust Mode** (`core/security/trust_mode.py`)
- Assesses trust level based on context
- Adjusts security requirements dynamically
- Determines allowed operations

**Privacy Mode** (`core/security/privacy.py`)
- Sends sensitive info via SMS/WhatsApp
- Prevents speaking balances/OTPs aloud
- Activated in noisy/public environments

### 4. Empathy & Intelligence Layer

**Emotional Confidence Check** (`empathy/ecc.py`)
- Detects user hesitation/uncertainty
- Generates reassuring responses
- Provides explanations for actions

**Response Generator** (`empathy/response_generator.py`)
- Creates contextual responses
- Adds empathetic touches
- Handles errors gracefully

**Banking Predictor** (`banking/predictor.py`)
- Analyzes spending patterns
- Detects recurring transactions
- Generates proactive suggestions
- Creates monthly summaries

### 5. Banking Operations Layer

**Banking Operations** (`banking/operations.py`)
- Balance checking
- Money transfers
- Transaction history
- Loan inquiries
- Reminder management

### 6. Data Persistence Layer

**Database** (`banking/database.py`)
- SQLAlchemy ORM models
- Users, Accounts, Transactions
- Beneficiaries, Loans, Reminders
- SQLite (pilot) / PostgreSQL (production)

### 7. Evaluation Layer

**Metrics Collector** (`evaluation/metrics.py`)
- Intent recognition accuracy
- Response time tracking
- Authentication success rates
- Transaction results

**Feedback System** (`evaluation/feedback.py`)
- Session feedback collection
- Feature-specific feedback
- Error feedback
- User satisfaction ratings

## Data Flow Example: Money Transfer

```
1. User: "Transfer 5000 rupees to Mom"
   │
   ▼
2. Speech Recognizer → Text: "transfer 5000 rupees to mom"
   │
   ▼
3. Intent Detector → Intent: "transfer_money" (confidence: 0.95)
   Entity Extractor → {amount: 5000, recipient: "Mom"}
   │
   ▼
4. Emotion Analyzer → Confidence: 0.8 (confident)
   │
   ▼
5. Trust Mode → Level: MEDIUM
   Authentication → Verified
   │
   ▼
6. ECC → Check: User confident, no intervention needed
   │
   ▼
7. Banking Operations → Request confirmation
   Response Generator → "I'll transfer ₹5,000 to Mom. Please confirm."
   │
   ▼
8. Speech Synthesizer → Speaks confirmation prompt
   │
   ▼
9. User: "Yes, proceed"
   │
   ▼
10. Banking Operations → Execute transfer
    Update database
    │
    ▼
11. Response Generator → Success message
    Speech Synthesizer → "Transaction successful..."
    │
    ▼
12. Metrics → Record intent accuracy, response time, transaction success
```

## Security Flow

```
┌──────────────┐
│ User Request │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Measure Noise Level  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Voice Biometric Auth │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Assess Trust Level   │
│ (noise, confidence,  │
│  amount, location)   │
└──────┬───────────────┘
       │
       ├─── HIGH TRUST ────► Allow all operations
       │
       ├─── MEDIUM ───────► Normal operations
       │
       ├─── LOW ──────────► Require PIN for transfers
       │
       └─── CRITICAL ─────► Require PIN + OTP, No high-value ops
```

## Empathy Flow

```
User Input
    │
    ▼
Emotion Analysis
    │
    ├─── Confident ────► Proceed normally
    │
    ├─── Uncertain ────► Offer clarification
    │                    "You sound unsure. Shall I review?"
    │
    ├─── Stressed ─────► Reassurance + slow pace
    │                    "Let's take this slowly..."
    │
    └─── Confused ─────► Simplify explanation
                         "Let me explain in a different way..."
```

## Predictive Analytics Flow

```
┌─────────────────────┐
│ Analyze Last 90 Days│
│ of Transactions     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Group by Recipient  │
│ & Amount Pattern    │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Detect Frequency    │
│ (daily/weekly/      │
│  monthly)           │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Calculate Next Due  │
│ Date                │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Generate Suggestion │
│ "You usually        │
│  transfer ₹1000..."│
└─────────────────────┘
```

## Technology Stack

- **Language**: Python 3.8+
- **Speech**: SpeechRecognition, pyttsx3, pyaudio
- **NLP**: spaCy, NLTK, regex
- **Audio**: librosa, sounddevice
- **Database**: SQLAlchemy, SQLite/PostgreSQL
- **Security**: cryptography, hashlib
- **Communication**: Twilio (SMS/WhatsApp)
- **Evaluation**: Custom metrics framework

## Deployment Architecture (Production)

```
┌─────────────┐
│   User      │
│  (Mobile/   │
│   Desktop)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│   Load Balancer         │
└──────┬──────────────────┘
       │
       ├──────┬──────┬─────┐
       ▼      ▼      ▼     ▼
    ┌────┐ ┌────┐ ┌────┐
    │App │ │App │ │App │  (WhisPay instances)
    │Srv1│ │Srv2│ │Srv3│
    └─┬──┘ └─┬──┘ └─┬──┘
      └──────┴──────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
┌──────────┐  ┌──────────┐
│PostgreSQL│  │  Redis   │
│ Database │  │  Cache   │
└──────────┘  └──────────┘
      │             │
      └──────┬──────┘
             ▼
      ┌─────────────┐
      │  Monitoring │
      │   & Logs    │
      └─────────────┘
```

---

**WhisPay Architecture designed for:**
- ✅ Scalability
- ✅ Security
- ✅ User empathy
- ✅ Predictive intelligence
- ✅ Accessibility
