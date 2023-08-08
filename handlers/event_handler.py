from flask import jsonify
from .text_response_generator import handle_message
from ..utils.tokenizer import num_tokens_from_string
from ..settings.env_loader import openai_api_key, system_prompt, MAX_TURNS, TTL, MAX_TOKENS_INPUT
from ..utils.session_manager import user_sessions, turn_counts, last_received_times


def process_event(request):
    try:
        event = request.get_json()
        event_type = event['type']
        user_id = event['user']['name']

        if event_type == 'ADDED_TO_SPACE':
            return jsonify({'text': f"Thanks for adding me! How can I assist you today?"})
        elif event_type == 'MESSAGE':
            return handle_message(user_id, event['message']['text'])
        else:
            return jsonify({'text': 'Sorry, I encountered an error while processing your message.'})
    except Exception as e:
        return jsonify({'text': f"Error: {str(e)}"})
