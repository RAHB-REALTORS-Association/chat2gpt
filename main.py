import datetime
from flask import jsonify
from simpleaichat import AIChat
from env_loader import get_env
from utils.openai import initialize_openai, moderate_content, num_tokens_from_string, generate_image
from utils.elevenlabs import get_voices_data, text_to_speech
from utils.misc import generate_unique_card_id, get_docs

# Load environment variables
OPENAI_API_KEY = get_env("OPENAI_API_KEY")
MODEL_NAME = get_env("MODEL_NAME")
SYSTEM_PROMPT = get_env("SYSTEM_PROMPT")
MAX_TURNS = get_env("MAX_TURNS")
TTL = get_env("TTL")
MAX_TOKENS_INPUT = get_env("MAX_TOKENS_INPUT")
MAX_TOKENS_OUTPUT = get_env("MAX_TOKENS_OUTPUT")
TEMPERATURE = get_env("TEMPERATURE")
IMAGE_SIZE = get_env("IMAGE_SIZE")
API_URL = get_env("API_URL")
ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")

# Initialize OpenAI parameters
params = initialize_openai(OPENAI_API_KEY, TEMPERATURE, MAX_TOKENS_OUTPUT)

# Define globals
user_sessions = {}  # A dictionary to track the AIChat instances for each user
turn_counts = {}  # A dictionary to track the turn count for each user
last_received_times = {}  # A dictionary to track the last received time for each user


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
        num_tokens = num_tokens_from_string(user_message + SYSTEM_PROMPT)

        # If the user types '/reset', reset the session
        if user_message.strip().lower() == '/reset':
            if user_id in user_sessions:
                del user_sessions[user_id]  # Delete the user's chat session if it exists
            turn_count = 0
            bot_message = "Your session has been reset. How can I assist you now?"

        # Check if the user input starts with /image
        elif user_message.strip().lower().startswith('/image'):
            prompt = user_message.split('/image', 1)[1].strip()
            if not prompt:
                return jsonify({'text': 'Please provide a prompt for the image generation. Example: `/image sunset over a beach`.'})
            
            try:
                image_resp = generate_image(prompt, n=1, size=IMAGE_SIZE)
                image_url = image_resp["data"][0]["url"]
                return jsonify({
                    'text': 'Processing your image request...',
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
                                                    'imageUrl': image_url,
                                                    'onClick': {
                                                        'openLink': {
                                                            'url': image_url
                                                        }
                                                    }
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
                print(f"Error generating image: {str(e)}"); return jsonify({'text': "Sorry, I encountered an internal error generating the image. Please try again later."})

        # Check if the user input starts with /voice (assuming you meant /voices)
        elif user_message.strip().lower() == '/voices':
            if not ELEVENLABS_API_KEY:
                return jsonify({'text': 'This function is disabled.'})
            
            voices_data, error = get_voices_data()
            if error:
                print(f"Error: {error}"); return jsonify({'text': "An internal error has occurred. Please try again later."})
            
            voice_names_list = list(voices_data.keys())
            
            # Join voice names with commas and spaces for readability
            voices_string = ', '.join(voice_names_list)
            return jsonify({'text': f"Available voices: {voices_string}"})

        # Check if the user input starts with /tts
        elif user_message.strip().lower().startswith('/tts'):
            if not ELEVENLABS_API_KEY:
                return jsonify({'text': 'This function is disabled.'})
            parts = user_message.split(' ')
            if len(parts) < 3:  # Checking for /tts, voice, and message
                return jsonify({'text': 'Please use the format /tts <voice> <message>.'})
            
            voice = parts[1].lower()
            
            voices_data_dict, error = get_voices_data()
            if error:
                print(f"Error: {error}"); return jsonify({'text': "An internal error has occurred. Please try again later."})
            
            if voice not in voices_data_dict:
                return jsonify({'text': f"Sorry, I couldn't recognize the voice {voice}. Please choose a valid voice."})

            prompt = ' '.join(parts[2:])
            audio_url, error = text_to_speech(prompt, voice)
            
            if audio_url:
                # Return a card with the audio link in a button
                return jsonify({
                    'text': 'Processing your TTS request...',
                    'cardsV2': [
                        {
                            'cardId': generate_unique_card_id(),
                            'card': {
                                'header': {
                                    'title': 'Generated Audio',
                                    'subtitle': 'Click to Play Audio'
                                },
                                'sections': [
                                    {
                                        'collapsible': False,
                                        'uncollapsibleWidgetsCount': 1,
                                        'widgets': [
                                            {
                                                'buttonList': {
                                                    'buttons': [
                                                        {
                                                            'text': 'Play ▶️',
                                                            'onClick': {
                                                                'openLink': {
                                                                    'url': audio_url
                                                                }
                                                            }
                                                        }
                                                    ]
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                })
            else:
                print(f"Error generating audio: {error}"); return jsonify({'text': "Sorry, I encountered an internal error generating the audio. Please try again later."})

        # Check if the user input starts with /help
        elif user_message.strip().lower() == '/help':
            help_content = get_docs("usage/help")
            return jsonify({'text': help_content})

        # If the message is too large, return an error message
        elif num_tokens > MAX_TOKENS_INPUT:
            return jsonify({'text': 'Sorry, your message is too large. Please try a shorter message.'})

        # If it's not a slash command, handle it normally
        else:
            if ai_chat is None or turn_count >= MAX_TURNS or (last_received_time is not None and (current_time - last_received_time).total_seconds() > TTL):
                if API_URL:
                    ai_chat = AIChat(api_key=None, api_url=API_URL, system=SYSTEM_PROMPT, params=params)
                else:
                    ai_chat = AIChat(api_key=OPENAI_API_KEY, system=SYSTEM_PROMPT, model=MODEL_NAME, params=params)
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
