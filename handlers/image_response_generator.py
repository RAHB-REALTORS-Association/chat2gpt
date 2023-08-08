
import openai
from flask import jsonify
from ..settings.env_loader import openai_api_key, IMAGE_SIZE
from ..utils.moderation import moderate_content


def generate_image(prompt):
    # Ensure prompt is provided
    if not prompt:
        return jsonify({'text': 'Please provide a prompt for the image generation. Example: `/image sunset over a beach`.'})

    # Check the prompt for any policy violations
    moderation_result = moderate_content(prompt)
    if moderation_result["flagged"]:
        return jsonify({'text': 'Sorry, your prompt does not comply with our content policy. Please refrain from inappropriate content.'})

    # Use the DALL-E API to generate the image based on the provided prompt
    try:
        image_resp = openai.Image.create(prompt=prompt, n=1, size=IMAGE_SIZE)
        image_url = image_resp["data"][0]["url"]
        return jsonify({
            'actionResponse': {
                'type': 'NEW_MESSAGE',
                'message': {
                    'text': '',
                    'cards': [
                        {
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
                    ]
                }
            }
        })
    except Exception as e:
        return jsonify({'text': f"Sorry, I encountered an error generating the image: {str(e)}"})
