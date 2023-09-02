from flask import Flask, request, jsonify, send_from_directory
from main import process_event

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def root():
    return send_from_directory('.', 'test_interface.html')

@app.route('/post', methods=['POST'])
def google_chat_event():
    try:
        # Get the Google Chat-like event data from the request body
        event_data = request.json

        # Call process_event function from main.py
        response = process_event(event_data)

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
