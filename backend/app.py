from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, static_folder='../frontend/dist')

# Enable CORS for all routes and methods
#CORS(app, origins=["http://127.0.0.1:5000", "http://192.168.1.131:5000"])
CORS(app)

# In-memory list to store session history
session_history = []

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    # send_static_file will guess the correct MIME type
    return send_from_directory(app.static_folder, path)

@app.route('/manifest.json')
def manifest():
    return send_from_directory(app.static_folder, 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory(app.static_folder, 'service-worker.js')

@app.route('/api/start_timer', methods=['POST', 'OPTIONS'])
def start_timer():
    if request.method == 'OPTIONS':
        # CORS preflight handling
        return _build_cors_preflight_response()
    
    data = request.json
    session_name = data.get('session_name', 'Unnamed Session')
    session_start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Store session in history
    session_history.append({'name': session_name, 'start_time': session_start_time})

    return jsonify({"message": "Timer started", "duration": data['duration']})


@app.route('/api/stop_timer', methods=['POST', 'OPTIONS'])
def stop_timer():
    if request.method == 'OPTIONS':
        # CORS preflight handling
        return _build_cors_preflight_response()

    return jsonify({"message": "Timer stopped"})


@app.route('/api/reset_timer', methods=['POST', 'OPTIONS'])
def reset_timer():
    if request.method == 'OPTIONS':
        # CORS preflight handling
        return _build_cors_preflight_response()

    return jsonify({"message": "Timer reset"})


@app.route('/api/get_history', methods=['GET', 'OPTIONS'])
def get_history():
    if request.method == 'OPTIONS':
        # CORS preflight handling
        return _build_cors_preflight_response()

    return jsonify(session_history)


def _build_cors_preflight_response():
    """
    This function builds the response for preflight requests.
    """
    response = jsonify({'message': 'CORS Preflight'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
    return response


def _corsify_actual_response(response):
    """
    This function adds CORS headers to the actual response.
    """
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)