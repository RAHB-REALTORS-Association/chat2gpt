from flask import Flask, request, jsonify, send_from_directory
from main import process_event
import json
import logging

LOG_FILE = "chat2gpt-server-log.txt"  # Set to None or an empty string to disable

# Basic logging setup for console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler()]
)

# If LOG_FILE is set, add FileHandler
if LOG_FILE:
    logging.getLogger().addHandler(logging.FileHandler(LOG_FILE))

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def root():
    return send_from_directory('.', 'interface.html')

@app.route('/api', methods=['POST'])
def google_chat_event():
    try:
        # Log the raw request data for debugging
        logging.info("Request Data: %s", request.data)

        # Get the event data from the request body
        response = process_event(request)

        # Log the raw request data for debugging
        logging.info("Response Data: %s", json.dumps(response.get_json(), indent=4))

        return response
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
