"""
Simple test script to verify WhisPay components are working.
Run this to check if the basic setup is correct.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        from app.config import settings
        print("✓ Config module")
        
        from utils.logger import log
        print("✓ Logger module")
        
        from utils.helpers import format_currency, extract_amount
        print("✓ Helper utilities")
        
        from core.nlp.intent_detector import IntentDetector
        print("✓ Intent detector")
        
        from core.nlp.entity_extractor import EntityExtractor
        print("✓ Entity extractor")
        
        from core.nlp.emotion_analyzer import EmotionAnalyzer
        print("✓ Emotion analyzer")
        
        from banking.database import db
        print("✓ Database module")
        
        from banking.operations import BankingOperations
        print("✓ Banking operations")
        
        from banking.predictor import BankingPredictor
        print("✓ Banking predictor")
        
        from empathy.ecc import EmotionalConfidenceCheck
        print("✓ Emotional confidence check")
        
        from empathy.response_generator import ResponseGenerator
        print("✓ Response generator")
        
        from evaluation.metrics import metrics
        print("✓ Evaluation metrics")
        
        print("\n✅ All imports successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Import failed: {e}")
        return False


def test_intent_detection():
    """Test intent detection."""
    print("\nTesting intent detection...")
    
    try:
        from core.nlp.intent_detector import IntentDetector
        
        detector = IntentDetector()
        
        test_cases = [
            ("What's my balance?", "check_balance"),
            ("Transfer 1000 to Mom", "transfer_money"),
            ("Show transaction history", "transaction_history"),
        ]
        
        for text, expected_intent in test_cases:
            result = detector.detect(text)
            detected = result['intent']
            success = detected == expected_intent
            status = "✓" if success else "✗"
            print(f"{status} '{text}' → {detected} (expected: {expected_intent})")
        
        print("✅ Intent detection working!")
        return True
        
    except Exception as e:
        print(f"❌ Intent detection failed: {e}")
        return False


def test_entity_extraction():
    """Test entity extraction."""
    print("\nTesting entity extraction...")
    
    try:
        from utils.helpers import extract_amount, extract_recipient
        
        test_cases = [
            ("Transfer 5000 rupees", 5000.0),
            ("Send ₹10,000 to someone", 10000.0),
            ("Pay 1500 rs", 1500.0),
        ]
        
        for text, expected_amount in test_cases:
            amount = extract_amount(text)
            success = amount == expected_amount
            status = "✓" if success else "✗"
            print(f"{status} '{text}' → ₹{amount} (expected: ₹{expected_amount})")
        
        print("✅ Entity extraction working!")
        return True
        
    except Exception as e:
        print(f"❌ Entity extraction failed: {e}")
        return False


def test_database():
    """Test database operations."""
    print("\nTesting database...")
    
    try:
        from banking.database import db
        
        # Try to create sample data
        db.create_sample_data()
        print("✓ Database initialized with sample data")
        
        from banking.operations import BankingOperations
        ops = BankingOperations()
        
        # Test balance check
        result = ops.check_balance("user001")
        if result['success']:
            print(f"✓ Balance check: {result['formatted_balance']}")
        
        print("✅ Database operations working!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False


def test_response_generation():
    """Test response generation."""
    print("\nTesting response generation...")
    
    try:
        from empathy.response_generator import ResponseGenerator
        
        gen = ResponseGenerator()
        
        # Test greeting
        greeting = gen.generate_greeting("Test User", "returning")
        print(f"✓ Greeting: {greeting[:50]}...")
        
        # Test help
        help_msg = gen.generate_help_message()
        print(f"✓ Help message generated ({len(help_msg)} chars)")
        
        print("✅ Response generation working!")
        return True
        
    except Exception as e:
        print(f"❌ Response generation failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("WhisPay Component Tests")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_intent_detection,
        test_entity_extraction,
        test_database,
        test_response_generation
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test crashed: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 60)
    
    if all(results):
        print("\n🎉 All tests passed! WhisPay is ready to use.")
        print("\nNext steps:")
        print("  1. Run demo: python demo.py")
        print("  2. Run full app: python app/main.py")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    
    return all(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
