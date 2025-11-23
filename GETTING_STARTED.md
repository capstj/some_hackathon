# Getting Started with WhisPay

## First Time Setup

### 1. Start WhisPay
```powershell
cd d:\vcpkg\some_hackathon
.\venv\Scripts\activate
python run_whispay.py
```

### 2. Initial Authentication

WhisPay will detect this is your first time and guide you through setup:

**WhisPay:** "Good morning. I'm WhisPay, your voice banking assistant..."

**WhisPay:** "I notice this is your first time using WhisPay. For security, I'll verify your identity with your PIN first, then we can enroll your voice for future logins. Please speak your 4-digit PIN."

**You:** "1234" (or "one two three four")

### 3. Voice Enrollment (Optional but Recommended)

**WhisPay:** "Great! Now, would you like to enroll your voice for faster authentication next time? Say 'yes' to enroll, or 'no' to skip."

**You:** "Yes"

**WhisPay:** "Great! I'll record your voice now. Please say a few sentences so I can learn your voice. For example, you could say: 'I want to check my account balance and transfer money.'"

**You:** [Speak naturally for 5 seconds - any sentences work]

**WhisPay:** "Perfect! Your voice has been enrolled successfully. Next time, you can just say a few words and I'll recognize you automatically."

### 4. You're Ready!

Now you can use all banking features. WhisPay will listen for your commands.

## Default Demo Account

- **User ID:** user001
- **Name:** Test User
- **PIN:** 1234
- **Initial Balance:** ₹50,000
- **Saved Beneficiaries:** Mom, Dad, Sister

## What You Can Do

### Check Balance
**You:** "What's my balance?"  
**WhisPay:** Tells you your current account balance

### Transfer Money
**You:** "Transfer 5000 rupees to Mom"  
**WhisPay:** Confirms and processes the transfer

### View Transactions
**You:** "Show my recent transactions"  
**WhisPay:** Lists your recent banking activity

### Check Loans
**You:** "Do I have any active loans?"  
**WhisPay:** Shows your loan information

### Set Reminders
**You:** "Set a reminder to pay rent on the 1st"  
**WhisPay:** Creates a payment reminder

### Get Insights
**You:** "What are my spending patterns?"  
**WhisPay:** Analyzes and explains your spending habits

### Exit
**You:** "Exit" or "Logout"  
**WhisPay:** Ends the session securely

## Next Time You Use WhisPay

### With Voice Enrolled:
1. Start WhisPay: `python run_whispay.py`
2. **WhisPay:** "Please say a few words so I can verify your identity."
3. **You:** [Say anything - e.g., "This is me"]
4. **WhisPay:** Recognizes you and logs you in automatically!

### Without Voice (PIN Only):
1. Start WhisPay: `python run_whispay.py`
2. **WhisPay:** "Please say a few words so I can verify your identity."
3. **You:** [WhisPay can't recognize you]
4. **WhisPay:** "Let's try using your PIN for verification. Please speak your 4-digit PIN."
5. **You:** "1234"
6. Logged in!

## Tips for Best Experience

### Voice Input
- **Speak clearly** in a quiet environment
- **Natural pace** - no need to speak slowly
- **Wait for the prompt** - WhisPay will say "Listening..." when ready
- **Microphone** should be enabled and accessible

### Commands
- Use natural language - no need for exact phrases
- WhisPay understands variations like:
  - "What's my balance?" = "How much money do I have?" = "Check balance"
  - "Transfer to Mom" = "Send money to Mom" = "Pay Mom"

### Emotional Support
WhisPay detects uncertainty and provides reassurance:
- If you sound unsure, WhisPay will offer to explain
- Feel free to ask "What does that mean?" or "Can you explain?"

### Security
- **Adaptive Trust Mode** adjusts security based on:
  - Background noise levels
  - Voice confidence
  - Transaction amounts
- High-value transactions may require additional verification
- Use **Private Mode** for sensitive operations (sends confirmation via SMS)

## Troubleshooting

### "I couldn't record your voice"
- Check microphone is connected and enabled
- Grant microphone permission to Python/Terminal
- Reduce background noise

### "I didn't catch that"
- Speak a bit louder or closer to microphone
- Reduce background noise
- Try again - WhisPay is patient!

### "The PIN you entered is incorrect"
- Remember: Demo PIN is **1234**
- You can say it as "one two three four" or "1234"
- Make sure you speak all 4 digits

### Voice not recognized after enrollment
- Environment might be too noisy - try PIN instead
- Voice recognition works best in consistent environments
- Re-enroll if needed (delete `data/users/voice_prints/user001.npy`)

## Advanced Features

### Proactive Suggestions
WhisPay automatically suggests:
- Upcoming bill payments based on history
- Recurring transactions it detects
- Unusual spending patterns

### Emotional Confidence Check (ECC)
WhisPay monitors your tone and words for signs of:
- Uncertainty
- Stress
- Confusion

And responds with:
- Reassurance
- Explanations
- Simplified options

### Spending Analytics
Ask WhisPay to:
- Analyze spending patterns
- Identify recurring expenses
- Provide monthly summaries
- Suggest budget optimizations

## Getting Help

- Say **"Help"** to hear available commands
- Ask **"What can you do?"** for feature overview
- Say **"Explain"** when you need clarification
- Check logs in `logs/whispay_*.log` for technical details

## Data Location

Your data is stored locally:
- **Database:** `data/whispay.db`
- **Voice Prints:** `data/users/voice_prints/`
- **Logs:** `logs/`
- **Metrics:** `data/metrics/`

To reset everything, delete the `data/` directory and restart WhisPay.

---

**Enjoy using WhisPay - Your Empathetic Banking Assistant!** 🎤💰
