"""
Counter API Implementation
"""
from flask import Flask, jsonify
from . import status

COUNTERS = {}

app = Flask(__name__)

def counter_exists(name):
    """Check if counter exists"""
    return name in COUNTERS

@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: COUNTERS[name]}), status.HTTP_201_CREATED

MINECRAFT_COUNTERS = {}

@app.route('/minecraft_server/<name>', methods=['POST'])
def create_minecraft_counter(name):
    """Create a counter"""
    if counter_exists(name):
        return jsonify({"error": f"Minecraft counter {name} already exists"}), status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return jsonify({name: MINECRAFT_COUNTERS[name]}), status.HTTP_201_CREATED