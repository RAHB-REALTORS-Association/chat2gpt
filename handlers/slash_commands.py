from flask import jsonify
from simpleaichat import AIChat
from ..utils.session_manager import user_sessions, turn_counts
from ..settings.env_loader import openai_api_key, system_prompt


def handle_slash_command(user_id, command, prompt=None):
    if command == "reset":
        ai_chat = AIChat(api_key=openai_api_key, system=system_prompt)
        user_sessions[user_id] = ai_chat
        turn_counts[user_id] = 0
        return jsonify({'text': 'Your session has been reset. How can I assist you now?'})
    elif command == "image":
        # Placeholder for /image command
        return jsonify({'text': 'Image generation functionality coming soon!'})
    else:
        return jsonify({'text': f"Unknown command: {command}. Please try again."})
