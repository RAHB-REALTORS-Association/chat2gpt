import os
import datetime
import uuid
import base64
from google.cloud import storage
from google.oauth2.service_account import Credentials
from flask import jsonify
from simpleaichat import AIChat
import requests
import json
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
    SYSTEM_PROMPT = os.getenv('SYSTEM_PROMPT', 'You are a helpful assistant.')
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

# Try to get the temperature value from an environment variable
try:
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.8)) # Default to 0.8
except Exception as e:
    print(f"Error getting TEMPERATURE: {str(e)}")

# Try to get the image size from an environment variable
try:
    IMAGE_SIZE = os.getenv('IMAGE_SIZE', '512x512')
except Exception as e:
    print(f"Error getting image size: {str(e)}")

# Try to get the chat completions API endpoint from an environment variable
# Example: https://example.com:8000/v1/chat/completions
API_URL = os.getenv('API_URL') # Defaults to OpenAI API if not set

# Eleven Labs Text-to-Speech API
xi_api_key = os.getenv('ELEVENLABS_API_KEY')
xi_model_name = os.getenv('ELEVENLABS_MODEL_NAME', 'eleven_monolingual_v1')

bucket_name = os.getenv('GCS_BUCKET_NAME')

if bucket_name:
    # Decode the base64 service account JSON
    decoded_service_account_info = base64.b64decode(os.getenv('GCP_SA_KEY')).decode('utf-8')
    service_account_info = json.loads(decoded_service_account_info)
    
    # Create credentials from the decoded service account JSON
    credentials = Credentials.from_service_account_info(service_account_info)
    
    # Create a GCS client with the credentials
    storage_client = storage.Client(credentials=credentials)

# Define globals
user_sessions = {}  # A dictionary to track the AIChat instances for each user
turn_counts = {}  # A dictionary to track the turn count for each user
last_received_times = {}  # A dictionary to track the last received time for each user

# Set the OpenAI API key
openai.api_key = openai_api_key

# Set the temperature and max_tokens for output
params = {'temperature': TEMPERATURE, 'max_tokens': MAX_TOKENS_OUTPUT}


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

# Define the function for downloading voices data
def get_voices_data():
    BASE_URL = "https://api.elevenlabs.io/v1/voices"

    endpoint = BASE_URL
    headers = {
        "xi-api-key": xi_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Fetch data from the ElevenLabs voices API
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        data = response.json()

        # Ensure 'voices' key exists in the data
        if 'voices' not in data:
            return None, "Error: 'voices' key not found in the API response."

        # Extract the list of voices and filter it
        voices_data = {
            voice["name"].lower(): voice["voice_id"]
            for voice in data["voices"]
        }

        return voices_data, None

    except requests.RequestException as re:
        return None, f"API request error: {str(re)}"
    except Exception as e:
        return None, f"Error fetching and filtering voice data: {str(e)}"


def get_voice_id(voice_name):
    voices_data, error = get_voices_data()
    if error:
        return None, error
    
    voice_id = voices_data.get(voice_name.lower())
    if not voice_id:
        return None, f"Voice {voice_name} not found."
    
    return voice_id, None


def text_to_speech(prompt, voice_name):
    BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/"

    voice_id, error = get_voice_id(voice_name)
    if error:
        return None, error

    endpoint = BASE_URL + voice_id
    headers = {
        "xi-api-key": xi_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": prompt,
        "model_id": xi_model_name,
    }
    response = requests.post(endpoint, json=payload, headers=headers)    

    if response.status_code == 200:
        # Get the raw audio data
        audio_data = response.content

        # Generate a unique filename for the audio
        file_name = f"tts_{uuid.uuid4()}.mp3"

        # Use the authenticated GCS client to upload
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        blob.upload_from_string(audio_data, content_type="audio/mpeg")

        # Set the blob to be publicly readable
        blob.make_public()

        # Return the blob's public URL
        return blob.public_url, None

    else:
        return None, response.text


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
                image_resp = openai.Image.create(prompt=prompt, n=1, size=IMAGE_SIZE)
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
                return jsonify({'text': f"Sorry, I encountered an error generating the image: {str(e)}"})

        # Check if the user input starts with /voice (assuming you meant /voices)
        elif user_message.strip().lower() == '/voices':
            if not xi_api_key:
                return jsonify({'text': 'This function is disabled.'})
            
            voices_data, error = get_voices_data()
            if error:
                return jsonify({'text': error})
            
            voice_names_list = list(voices_data.keys())
            
            # Join voice names with commas and spaces for readability
            voices_string = ', '.join(voice_names_list)
            return jsonify({'text': f"Available voices: {voices_string}"})

        # Check if the user input starts with /tts
    elif user_message.strip().lower().startswith('/tts'):
        if not xi_api_key:
            return jsonify({'text': 'This function is disabled.'})
        parts = user_message.split(' ')
        if len(parts) < 3:  # Checking for /tts, voice, and message
            return jsonify({'text': 'Please use the format /tts <voice> <message>.'})
        
        voice = parts[1].lower()
        
        voices_data_dict, error = get_voices_data()
        if error:
            return jsonify({'text': error})
        
        if voice not in voices_data_dict:
            return jsonify({'text': f"Sorry, I couldn't recognize the voice {voice}. Please choose a valid voice."})

        
        prompt = ' '.join(parts[2:])
        audio_url, error = text_to_speech(prompt, voice)
        
        if audio_url:
            # Return a card with the audio link in a button
            return jsonify({
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
            return jsonify({'text': f"Sorry, I encountered an error generating the audio: {error}"})

    # If the message is too large, return an error message
    elif num_tokens > MAX_TOKENS_INPUT:
        return jsonify({'text': 'Sorry, your message is too large. Please try a shorter message.'})

    # If it's not a slash command, handle it normally
    elif user_message.strip().lower() == '/help':
        try:
            # Read the docs/usage.md file
            with open('docs/usage.md', 'r') as file:
                content = file.read()

            # Split the content at the "---" header line and get the second part
            help_content = content.split("---", 2)[-1].strip()

            # Return the extracted content as the bot's response
            return jsonify({'text': help_content})

        except Exception as e:
            print(f"Error reading help content: {str(e)}")
            return jsonify({'text': 'Sorry, I encountered an error retrieving the help content.'})

    else:
        if ai_chat is None or turn_count >= MAX_TURNS or (last_received_time is not None and (current_time - last_received_time).total_seconds() > TTL):
            if API_URL:
                ai_chat = AIChat(api_key=None, api_url=API_URL, system=SYSTEM_PROMPT, params=params)
            else:
                ai_chat = AIChat(api_key=openai_api_key, system=SYSTEM_PROMPT, model=MODEL_NAME, params=params)
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