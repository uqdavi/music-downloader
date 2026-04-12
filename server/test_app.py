from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET', 'POST', 'OPTIONS'])
def test():
    print(f"Request received: {request.method}")
    if request.method == 'POST':
        data = request.json
        print(f"Data: {data}")
        return jsonify({"received": True, "data": data}), 200
    return jsonify({"status": "ok"}), 200

@app.errorhandler(Exception)
def handle_all(err):
    print(f"ERROR: {err}")
    import traceback
    traceback.print_exc()
    return jsonify({"error": str(err)}), 500

if __name__ == '__main__':
    print("Starting test app on port 5001")
    app.run(port=5001, debug=False)
