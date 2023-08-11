import json
from flask import jsonify

import json
from flask import jsonify

def handle_message(user_id, user_message):
    # Add logic for processing user message and generating bot's response
    # Replace the static JSON response with the actual implementation logic
    # For example:
    if user_message == 'Hello':
        bot_response = 'Hi there!'
    else:
        bot_response = 'I'm sorry, I didn't understand.'
    return jsonify({'text': bot_response})