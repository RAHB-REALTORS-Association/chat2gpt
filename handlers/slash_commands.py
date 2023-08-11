import json
from flask import jsonify

import json
from flask import jsonify

def slash_commands(command):
    # Add logic for handling slash commands
    if command == '/reset':
        return jsonify({'text': 'Reset command executed'})
    elif command == '/image':
        return jsonify({'text': 'Image command executed'})
    elif command == '/voices':
        return jsonify({'text': 'Voices command executed'})
    elif command == '/tts':
        return jsonify({'text': 'TTS command executed'})
    else:
        return jsonify({'text': 'Unknown command'})