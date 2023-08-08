import datetime
from flask import jsonify
from simpleaichat import AIChat
from ..utils.session_manager import user_sessions, turn_counts, last_received_times
from .slash_commands import handle_slash_command
from ..settings.env_loader import openai_api_key, system_prompt, MAX_TURNS, TTL, MAX_TOKENS_INPUT
from ..utils.tokenizer import num_tokens_from_string


def handle_message(user_id, user_message):
    try:
        current_time = datetime.datetime.now()

        # Get the AIChat instance for the user, or create a new one
        ai_chat = user_sessions.get(user_id)
        turn_count = turn_counts.get(user_id, 0)
        last_received_time = last_received_times.get(user_id)

        # Count the tokens in the user message
        num_tokens = num_tokens_from_string(user_message + system_prompt)

        # Check if the message starts with a slash
        if user_message.startswith('/'):
            return handle_slash_command(user_id, user_message.split()[0][1:], ' '.join(user_message.split()[1:]))
    
        # If the message is too large, return an error message
        elif num_tokens > MAX_TOKENS_INPUT:
            return jsonify({'text': 'Sorry, your message is too large. Please try a shorter message.'})

        # If it's not a reset command, handle it normally
        else:
            if ai_chat is None or turn_count >= MAX_TURNS or (last_received_time is not None and (current_time - last_received_time).total_seconds() > TTL):
                ai_chat = AIChat(api_key=openai_api_key, system=system_prompt)
                user_sessions[user_id] = ai_chat
                turn_count = 0

            # Generate the response
            response = ai_chat(user_message)
            bot_message = response

            # Update the turn count and the last received time
            turn_count += 1
            turn_counts[user_id] = turn_count
            last_received_times[user_id] = current_time

    except Exception as e:
        bot_message = "Sorry, I'm currently unable to generate a response."
    
    # Check and truncate the response if it's too long
    if len(bot_message) > 4096:
        bot_message = bot_message[:4060] + " (MESSAGE TRUNCATED)"

    return jsonify({'text': bot_message})
