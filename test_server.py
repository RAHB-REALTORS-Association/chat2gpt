from flask import Flask, request, jsonify, send_from_directory
from main import process_event
import json

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def root():
    return send_from_directory('.', 'test_interface.html')

@app.route('/post', methods=['POST'])
def google_chat_event():
    try:
        # Debug: Print the raw request data
        print("Raw Request Data:", request.data)

        # Get the event data from the request body
        response = process_event(request)
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
