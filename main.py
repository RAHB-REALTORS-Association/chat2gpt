import os
from flask import jsonify
from simpleaichat import AIChat

# Import environment variables
from settings.env_loader import openai_api_key, system_prompt, MAX_TURNS, TTL, MAX_TOKENS_INPUT

# Import utility functions
from utils.tokenizer import num_tokens_from_string
from utils.session_manager import user_sessions, turn_counts, last_received_times

# Import message handling functions
from handlers.text_response_generator import handle_message
from handlers.event_handler import process_event
