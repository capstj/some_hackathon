"""
WhisPay Demo Launcher
Run this script from the root directory to start the WhisPay demo.
"""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the demo
if __name__ == "__main__":
    import demo
