import os
import json

# Define the path to the file where you want to store catch_counter
CATCH_COUNTER_FILE = "catch_counter.json"

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
    