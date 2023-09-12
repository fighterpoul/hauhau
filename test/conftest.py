import sys
import os

# Get the root directory (where your scripts are located)
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the root directory to the Python path
sys.path.insert(0, root_dir)