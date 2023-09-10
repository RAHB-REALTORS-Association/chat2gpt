import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from env_loader import get_env
from main import process_event

LOG_FILE = get_env("LOG_FILE")
HOST = get_env("HOST")
PORT = get_env("PORT")

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
    app.run(host=HOST, port=PORT)
