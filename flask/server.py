# server.py (Flask server)
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/data', methods=['POST'])
def receive_data():
    if request.is_json:
        data = request.json
        print("Received JSON data:", data)
        return jsonify({"status": "success", "received_data": data}), 200
    else:
        print("Received non-JSON data:", request.data)
        return jsonify({"status": "error", "message": "Expected JSON"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)