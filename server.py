from flask import Flask, request, jsonify, send_from_directory
from main import process_event
import json

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def root():
    return send_from_directory('.', 'interface.html')

@app.route('/api', methods=['POST'])
def google_chat_event():
    try:
        # Log the raw request data for debugging
        print("Raw Request Data:", request.data)

        # Get the event data from the request body
        response = process_event(request)

        # Log the raw request data for debugging
        print("Raw Response Data:", json.dumps(response.get_json(), indent=4))

        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
