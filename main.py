import os
import datetime
import uuid
from flask import jsonify
from simpleaichat import AIChat
import openai
import tiktoken

# Try to get the OpenAI API key from an environment variable
try:
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if openai_api_key is None:
        raise ValueError('OPENAI_API_KEY environment variable not set.')
except Exception as e:
    print(f"Error getting OpenAI API key: {str(e)}")

# Try to get the model from an environment variable
try:
    MODEL_NAME = os.getenv('MODEL_NAME', 'gpt-3.5-turbo')
except Exception as e:
    print(f"Error getting model name: {str(e)}")

# Try to get the system prompt from an environment variable
try:
    system_prompt = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')
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

# Try to get the max tokens (input) from an environment variable
try:
    MAX_TOKENS_INPUT = int(os.getenv('MAX_TOKENS_INPUT', 1000))  # Default to 1000 tokens
except Exception as e:
    print(f"Error getting MAX_TOKENS_INPUT: {str(e)}")

# Try to get the max tokens (output) from an environment variable
try:
    MAX_TOKENS_OUTPUT = int(os.getenv('MAX_TOKENS_OUTPUT', 1000))  # Default to 1000 tokens
except Exception as e:
    print(f"Error getting MAX_TOKENS_OUTPUT: {str(e)}")

# Define globals
user_sessions = {}  # A dictionary to track the AIChat instances for each user
turn_counts = {}  # A dictionary to track the turn count for each user
last_received_times = {}  # A dictionary to track the last received time for each user

# Set the OpenAI API key
openai.api_key = openai_api_key

# Set the max_tokens for output
params = {'max_tokens': MAX_TOKENS_OUTPUT}

# define the function for moderation
def moderate_content(text: str) -> dict:
    response = openai.Moderation.create(input=text)
    return response["results"][0]

# Function to generate a unique cardId
def generate_unique_card_id():
    return f"image_card_{int(datetime.datetime.now().timestamp())}_{uuid.uuid4().hex[:6]}"


# Define the function for token counting
def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
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

        # If the user types '/reset', reset the session
        if user_message.strip().lower() == '/reset':
            ai_chat = AIChat(api_key=openai_api_key, system=system_prompt, model=MODEL_NAME, params=params)
            user_sessions[user_id] = ai_chat
            turn_count = 0
            bot_message = "Your session has been reset. How can I assist you now?"

        # Check if the user input starts with /image
        elif user_message.strip().lower().startswith('/image'):
            prompt = user_message.split('/image', 1)[1].strip()
            if not prompt:
                return jsonify({'text': 'Please provide a prompt for the image generation. Example: `/image sunset over a beach`.'})
            
            try:
                image_resp = openai.Image.create(prompt=prompt, n=1, size="512x512")
                image_url = image_resp["data"][0]["url"]
                return jsonify({
                    'cardsV2': [
                        {
                            'cardId': generate_unique_card_id(),
                            'card': {
                                'header': {
                                    'title': 'Generated Image',
                                    'subtitle': prompt,
                                },
                                'sections': [
                                    {
                                        'widgets': [
                                            {
                                                'image': {
                                                    'imageUrl': image_url
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                })
            except Exception as e:
                return jsonify({'text': f"Sorry, I encountered an error generating the image: {str(e)}"})

        # If the message is too large, return an error message
        elif num_tokens > MAX_TOKENS_INPUT:
            return jsonify({'text': 'Sorry, your message is too large. Please try a shorter message.'})

        # If it's not a slash command, handle it normally
        else:
            if ai_chat is None or turn_count >= MAX_TURNS or (last_received_time is not None and (current_time - last_received_time).total_seconds() > TTL):
                ai_chat = AIChat(api_key=openai_api_key, system=system_prompt, model=MODEL_NAME, params=params)
                user_sessions[user_id] = ai_chat
                turn_count = 0

            # Generate the response
            response = ai_chat(user_message)

            # Ensure the response is less than 4096 characters
            if len(response) > 4096:
                response = response[:4070] + "<MESSAGE TRUNCATED>"  # truncated to leave space for the appended message

            # Check the API output for any policy violations
            moderation_result = moderate_content(response)
            if moderation_result["flagged"]:
                return jsonify({'text': 'Sorry, your message does not comply with our content policy. Please refrain from inappropriate content.'})

            bot_message = response

            # Update the turn count and the last received time
            turn_count += 1
            turn_counts[user_id] = turn_count
            last_received_times[user_id] = current_time

    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        bot_message = "Sorry, I'm currently unable to generate a response."
    return jsonify({'text': bot_message})
