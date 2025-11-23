"""
WhisPay Launcher
Run this script from the root directory to start WhisPay.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the main application
from app.main import WhisPayAssistant

if __name__ == "__main__":
    try:
        # Initialize database with sample data (for demo)
        from banking.database import db
        db.create_sample_data()
        
        # Create and start assistant
        assistant = WhisPayAssistant()
        assistant.start()
    except KeyboardInterrupt:
        print("\n\nThank you for using WhisPay. Goodbye!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
        print("Please check the logs for more details.")
