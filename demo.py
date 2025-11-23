"""
Demo script for WhisPay.
Demonstrates key features without requiring full voice interaction.
"""

from banking.database import db, User, Account, Beneficiary
from banking.operations import BankingOperations
from banking.predictor import BankingPredictor
from core.nlp.intent_detector import IntentDetector
from core.nlp.entity_extractor import EntityExtractor
from core.nlp.emotion_analyzer import EmotionAnalyzer
from empathy.ecc import EmotionalConfidenceCheck
from empathy.response_generator import ResponseGenerator
from evaluation.metrics import metrics
from utils.logger import log
from datetime import datetime


def setup_demo_data():
    """Setup demo database with sample data."""
    print("\n" + "="*60)
    print("Setting up demo data...")
    print("="*60 + "\n")
    
    db.create_sample_data()
    print("✓ Sample user created (ID: user001)")
    print("✓ Sample account created with ₹50,000 balance")
    print("✓ Sample beneficiaries added (Mom, Dad, Sister)")


def demo_intent_detection():
    """Demonstrate intent detection."""
    print("\n" + "="*60)
    print("DEMO: Intent Detection & Entity Extraction")
    print("="*60 + "\n")
    
    detector = IntentDetector()
    extractor = EntityExtractor()
    
    test_inputs = [
        "What's my account balance?",
        "Transfer 5000 rupees to Mom",
        "Show me my transaction history",
        "I want to apply for a home loan",
        "Remind me to pay my electricity bill"
    ]
    
    for user_input in test_inputs:
        print(f"User: \"{user_input}\"")
        
        # Detect intent
        intent_result = detector.detect(user_input)
        print(f"  → Intent: {intent_result['intent']} (confidence: {intent_result['confidence']:.2f})")
        
        # Extract entities
        entities = extractor.extract(user_input)
        if entities:
            print(f"  → Entities: {entities}")
        
        print()


def demo_emotion_analysis():
    """Demonstrate emotion analysis."""
    print("\n" + "="*60)
    print("DEMO: Emotion Analysis & Confidence Check")
    print("="*60 + "\n")
    
    analyzer = EmotionAnalyzer()
    ecc = EmotionalConfidenceCheck()
    
    test_inputs = [
        "I'm sure I want to transfer the money",
        "Um, I think maybe I should... uh... transfer?",
        "I'm worried about this transaction",
        "This is confusing, I don't understand"
    ]
    
    for user_input in test_inputs:
        print(f"User: \"{user_input}\"")
        
        # Analyze emotion
        result = analyzer.analyze_text(user_input)
        print(f"  → Emotion: {result['primary_emotion']}")
        print(f"  → Uncertainty level: {result['uncertainty_level']:.2f}")
        
        # ECC response
        ecc_result = ecc.check_confidence(user_input)
        if ecc_result['should_intervene']:
            print(f"  → ECC Response: \"{ecc_result['response']}\"")
        
        print()


def demo_banking_operations():
    """Demonstrate banking operations."""
    print("\n" + "="*60)
    print("DEMO: Banking Operations")
    print("="*60 + "\n")
    
    ops = BankingOperations()
    user_id = "user001"
    
    # Check balance
    print("1. Checking balance...")
    balance_result = ops.check_balance(user_id)
    if balance_result['success']:
        print(f"   Balance: {balance_result['formatted_balance']}")
    
    # Transfer money
    print("\n2. Transferring ₹1,000 to Mom...")
    transfer_result = ops.transfer_money(user_id, "Mom", 1000.0)
    if transfer_result['success']:
        print(f"   ✓ Transfer successful")
        print(f"   Transaction ID: {transfer_result['transaction_id']}")
        print(f"   New balance: {transfer_result['formatted_balance']}")
    
    # Get transaction history
    print("\n3. Getting transaction history...")
    history_result = ops.get_transaction_history(user_id, limit=5)
    if history_result['success']:
        print(f"   Found {history_result['count']} transactions:")
        for txn in history_result['transactions'][:3]:
            print(f"   - {txn['formatted_amount']} to {txn['recipient']}")
    
    # Loan inquiry
    print("\n4. Inquiring about personal loan...")
    loan_result = ops.inquire_loan(user_id, "personal", 100000)
    if loan_result['success']:
        print(f"   Interest rate: {loan_result['interest_rate']}%")
        print(f"   EMI: {loan_result['formatted_emi']}/month")


def demo_predictive_features():
    """Demonstrate predictive features."""
    print("\n" + "="*60)
    print("DEMO: Predictive Analytics")
    print("="*60 + "\n")
    
    predictor = BankingPredictor()
    user_id = "user001"
    
    # Analyze spending patterns
    print("1. Analyzing spending patterns...")
    analysis = predictor.analyze_spending_patterns(user_id, days=90)
    if analysis['success']:
        print(f"   Total spent (90 days): {analysis['formatted_total']}")
        print(f"   Average transaction: {analysis['formatted_avg']}")
        print(f"   Number of transactions: {analysis['transaction_count']}")
    
    # Detect recurring transactions
    print("\n2. Detecting recurring transactions...")
    recurring = predictor.detect_recurring_transactions(user_id)
    if recurring:
        print(f"   Found {len(recurring)} recurring patterns:")
        for pattern in recurring[:3]:
            print(f"   - {pattern['formatted_amount']} to {pattern['recipient']} ({pattern['frequency']})")
    else:
        print("   No recurring patterns detected yet")
    
    # Get proactive suggestions
    print("\n3. Getting proactive suggestions...")
    suggestions = predictor.get_proactive_suggestions(user_id)
    if suggestions:
        print(f"   {len(suggestions)} suggestions available:")
        for suggestion in suggestions[:2]:
            print(f"   - [{suggestion['priority']}] {suggestion['message'][:80]}...")
    else:
        print("   No suggestions at this time")


def demo_empathetic_responses():
    """Demonstrate empathetic response generation."""
    print("\n" + "="*60)
    print("DEMO: Empathetic Response Generation")
    print("="*60 + "\n")
    
    response_gen = ResponseGenerator()
    
    # Greeting
    print("1. Greeting")
    greeting = response_gen.generate_greeting("John", context="returning")
    print(f"   WhisPay: \"{greeting}\"")
    
    # Help message
    print("\n2. Help Message")
    help_msg = response_gen.generate_help_message()
    print(f"   WhisPay: \"{help_msg[:150]}...\"")
    
    # Transaction summary
    print("\n3. Transaction Summary")
    txn_data = {
        'success': True,
        'formatted_amount': '₹5,000.00',
        'recipient': 'Mom',
        'formatted_balance': '₹45,000.00',
        'transaction_id': 'TXN123456'
    }
    summary = response_gen.generate_transaction_summary(txn_data)
    print(f"   WhisPay: \"{summary}\"")
    
    # Error recovery
    print("\n4. Error Recovery Message")
    error_msg = response_gen.generate_error_recovery_message('voice_verification')
    print(f"   WhisPay: \"{error_msg}\"")


def demo_evaluation_metrics():
    """Demonstrate evaluation metrics."""
    print("\n" + "="*60)
    print("DEMO: Evaluation Metrics")
    print("="*60 + "\n")
    
    # Record some sample metrics
    metrics.record_intent_recognition(
        "Check my balance",
        "check_balance",
        0.95,
        "check_balance"
    )
    
    metrics.record_response_time("check_balance", 250, True)
    metrics.record_authentication("voice_biometric", True, 0.92)
    metrics.record_transaction("transfer", True, 1000.0)
    
    # Generate report
    report = metrics.generate_report()
    
    print("Evaluation Report:")
    print(f"  Intent Recognition Accuracy: {report['intent_recognition'].get('overall_accuracy', 0):.2%}")
    print(f"  Average Response Time: {report['response_times'].get('average_ms', 0):.0f}ms")
    print(f"  Authentication Success Rate: {report['authentication'].get('overall_success_rate', 0):.2%}")
    
    # Export metrics
    print("\n  Exporting metrics...")
    filepath = metrics.export_metrics()
    print(f"  ✓ Metrics exported to: {filepath}")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  WhisPay - Voice Banking Assistant Demo  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        setup_demo_data()
        demo_intent_detection()
        demo_emotion_analysis()
        demo_banking_operations()
        demo_predictive_features()
        demo_empathetic_responses()
        demo_evaluation_metrics()
        
        print("\n" + "="*60)
        print("Demo completed successfully!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Copy .env.example to .env and configure")
        print("  3. Run main application: python app/main.py")
        print("\n")
        
    except Exception as e:
        log.error(f"Demo error: {e}")
        print(f"\n❌ Error during demo: {e}")
        print("Some features may require additional setup.\n")


if __name__ == "__main__":
    main()
