import openai
import os
from flask import jsonify

# Try to get the OpenAI API key from an environment variable
try:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if openai.api_key is None:
        raise ValueError('OPENAI_API_KEY environment variable not set.')
except Exception as e:
    print(f"Error getting OpenAI API key: {str(e)}")

# Try to get the model name from an environment variable
try:
    model_name = os.getenv('MODEL_NAME')
    if model_name is None:
        raise ValueError('MODEL_NAME environment variable not set.')
except Exception as e:
    print(f"Error getting model name: {str(e)}")

# Try to get the system prompt from an environment variable
try:
    system_prompt = os.getenv('SYSTEM_PROMPT')
    if system_prompt is None:
        raise ValueError('SYSTEM_PROMPT environment variable not set.')
except Exception as e:
    print(f"Error getting system prompt: {str(e)}")

def process_event(request):
    try:
        event = request.get_json()
        if 'message' in event:
            return handle_message(event['message'])
        else:
            return jsonify({'text': 'Sorry, I can only process text messages.'})
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return jsonify({'text': 'Sorry, I encountered an error while processing your message.'})

def handle_message(message):
    # If the message contains text
    if 'text' in message:
        user_message = message['text']
        try:
            response = openai.ChatCompletion.create(
                model=model_name,  # Use the model name from the environment variable
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt  # Use the system prompt from the environment variable
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )
            bot_message = response.choices[0].message['content']
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            bot_message = "Sorry, I'm currently unable to generate a response."
    else:
        # If the message does not contain text, ignore or send a default response
        bot_message = "I'm sorry, I can only process text messages."

    return jsonify({'text': bot_message})

