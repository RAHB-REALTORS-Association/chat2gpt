import os
import datetime
from flask import jsonify
from simpleaichat import AIChat
import tiktoken

# Try to get the OpenAI API key from an environment variable
try:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None:
        raise ValueError('OPENAI_API_KEY environment variable not set.')
except Exception as e:
    print(f"Error getting OpenAI API key: {str(e)}")

# Try to get the system prompt from an environment variable
try:
    system_prompt = os.getenv('SYSTEM_PROMPT')
    if system_prompt is None:
        raise ValueError('SYSTEM_PROMPT environment variable not set.')
except Exception as e:
    print(f"Error getting system prompt: {str(e)}")

# Try to get the max turns from an environment variable
try:
    MAX_TURNS = int(os.getenv('MAX_TURNS', 10))
except Exception as e:
    print(f"Error getting max turns: {str(e)}")

# Try to get the TTL from an environment variable
try:
    TTL = int(os.getenv('TTL', 600))  # Default to 600 seconds (10 minutes)
except Exception as e:
    print(f"Error getting TTL: {str(e)}")

# Try to get the max tokens from an environment variable
try:
    MAX_TOKENS_INPUT = int(os.getenv('MAX_TOKENS_INPUT', 2000))  # Default to 2000 tokens
except Exception as e:
    print(f"Error getting MAX_TOKENS_INPUT: {str(e)}")

# Define globals
user_sessions = {}  # A dictionary to track the AIChat instances for each user
turn_counts = {}  # A dictionary to track the turn count for each user
last_received_times = {}  # A dictionary to track the last received time for each user


# Define the function for token counting
def num_tokens_from_string(string: str, model_name: str) -> int:
    tokenizer = Tokenizer(models.get_encoder(model_name))
    num_tokens = len(tokenizer.encode(string))
    return num_tokens


def process_event(request):
    try:
        event = request.get_json()
        event_type = event['type']
        user_id = event['user']['name']

        if event_type == 'ADDED_TO_SPACE':
            return jsonify({'text': 'Hello! I am your Chat bot. How can I assist you today?'})
        elif event_type == 'MESSAGE':
            message = event['message']
            user_message = message['text']

            # Check if the bot was mentioned in the room, if so, remove the mention
            if 'annotations' in message:
                for annotation in message['annotations']:
                    if annotation['type'] == 'USER_MENTION':
                        if annotation['userMention']['user']['name'] == event['space']['name']:
                            user_message = user_message.replace(annotation['userMention']['text'], '').strip()

            return handle_message(user_id, user_message)
        else:
            return jsonify({'text': 'Sorry, I can only process messages and being added to a space.'})

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return jsonify({'text': 'Sorry, I encountered an error while processing your message.'})


def handle_message(user_id, user_message):
    try:
        current_time = datetime.datetime.now()

        # Get the AIChat instance for the user, or create a new one
        ai_chat = user_sessions.get(user_id)
        turn_count = turn_counts.get(user_id, 0)
        last_received_time = last_received_times.get(user_id)

        # Count the tokens in the user message
        num_tokens = num_tokens_from_string(user_message, system_prompt)

        # If the message is too large, return an error message
        if num_tokens > MAX_TOKENS_INPUT:
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
        print(f"Error calling OpenAI API: {str(e)}")
        bot_message = "Sorry, I'm currently unable to generate a response."
    return jsonify({'text': bot_message})
