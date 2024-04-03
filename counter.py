import os
import json

# Define the path to the file where you want to store catch_counter
SESSION_NAME = os.getenv('SESSION_NAME')

# Create the json_info folder if it doesn't exist
os.makedirs('json_info', exist_ok=True)

# Specify the json_info folder in the file path
CATCH_COUNTER_FILE = f"json_info/catch_{SESSION_NAME}.json"

def save_counters(counters):
    # Save counters to a file
    with open(CATCH_COUNTER_FILE, 'w') as f:
        json.dump(counters, f)

def load_counters():
    # Load counters from a file
    if os.path.exists(CATCH_COUNTER_FILE):
        with open(CATCH_COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data
    else:
        return {'catch_counter': 0, 'fish_counter': 0}