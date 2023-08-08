import datetime
from flask import jsonify
from simpleaichat import AIChat
from ..utils.session_manager import user_sessions, turn_counts, last_received_times
from .slash_commands import handle_slash_command
from ..settings.env_loader import openai_api_key, system_prompt, MAX_TURNS, TTL, MAX_TOKENS_INPUT, MAX_TOKENS_OUTPUT
from ..utils.tokenizer import num_tokens_from_string
from ..utils.moderation import moderate_content


def handle_message(user_id, user_message):
    try:
        # Check the user input for any policy violations
        moderation_result = moderate_content(user_message)
        if moderation_result["flagged"]:
            return jsonify({'text': 'Sorry, your message does not comply with our content policy. Please refrain from inappropriate content.'})

        current_time = datetime.datetime.now()

        # Get the AIChat instance for the user, or create a new one
        ai_chat = user_sessions.get(user_id)
        turn_count = turn_counts.get(user_id, 0)
        last_received_time = last_received_times.get(user_id)

        # Count the tokens in the user message
        num_tokens = num_tokens_from_string(user_message + system_prompt)

        # Check if the message is a slash command
        if user_message.startswith('/'):
            return handle_slash_command(user_id, user_message.split()[0][1:], ' '.join(user_message.split()[1:]))
    
        # If the message is too large, return an error message
        elif num_tokens > MAX_TOKENS_INPUT:
            return jsonify({'text': 'Sorry, your message is too large. Please try a shorter message.'})

        # If it's not a slash command, handle it normally
        else:
            if ai_chat is None or turn_count >= MAX_TURNS or (last_received_time is not None and (current_time - last_received_time).total_seconds() > TTL):
                ai_chat = AIChat(api_key=openai_api_key, system=system_prompt)
                user_sessions[user_id] = ai_chat
                turn_count = 0

            # Generate the response
            # Conditional API call based on MAX_TOKENS_OUTPUT
            if MAX_TOKENS_OUTPUT == 0:
                response = ai_chat(user_message)
            else:
                response = ai_chat(user_message, max_tokens=MAX_TOKENS_OUTPUT)

            bot_message = response

            # Check the bot's response for any policy violations
            moderation_result = moderate_content(bot_message)
            if moderation_result["flagged"]:
                bot_message = 'Sorry, the generated response does not comply with our content policy.'

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
