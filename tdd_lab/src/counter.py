"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

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

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
  """Get a counter"""
  if counter_exists(name):
    return jsonify({name: COUNTERS[name]}, status.HTTP_200_OK)  

@app.route('/counters/<name>', methods=['PUT'])
def increment_counter(name):
  """Create a counter"""
  if not counter_exists(name):
    return jsonify({"error": f"Counter {name} does not exist."}), status.HTTP_409_CONFLICT
  COUNTERS[name] += 1
  return jsonify({name: COUNTERS[name]}), status.HTTP_200_OK

@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
  """Delete a counter"""
  if not counter_exists(name):
      return jsonify({"error": f"Counter {name} does not exist."}), status.HTTP_409_CONFLICT
  
  del COUNTERS[name]
  return jsonify({"message": f"Counter {name} has been deleted."}), status.HTTP_200_OK
