"""
Counter API Implementation
"""
from flask import Flask
from flask import jsonify
from src import status

app = Flask(__name__)

COUNTERS = {}


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS

@app.route('/counters/reset', methods=['POST'])
def reset_counters():
    """Reset all counters"""
    COUNTERS.clear()  # Should clear the COUNTERS dictionary
    # Return success status, I assert that this works in the test_reset method
    return jsonify({"message": "All counters have been reset"}), status.HTTP_200_OK

