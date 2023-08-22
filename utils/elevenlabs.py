import requests
import uuid
from env_loader import get_env
from utils.gcs import initialize_gcs_client

ELEVENLABS_API_KEY = get_env("ELEVENLABS_API_KEY")
ELEVENLABS_MODEL_NAME = get_env("ELEVENLABS_MODEL_NAME")
GCS_BUCKET_NAME = get_env("GCS_BUCKET_NAME")

if GCS_BUCKET_NAME:
    storage_client = initialize_gcs_client(GCS_BUCKET_NAME)

# Define the function for downloading voices data
def get_voices_data():
    BASE_URL = "https://api.elevenlabs.io/v1/voices"

    endpoint = BASE_URL
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
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
        print(f"API request error: {str(re)}"); return None, "An internal error has occurred. Please try again later."
    except Exception as e:
        print(f"Error fetching and filtering voice data: {str(e)}"); return None, "An internal error has occurred. Please try again later."


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
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "text": prompt,
        "model_id": ELEVENLABS_MODEL_NAME,
    }
    response = requests.post(endpoint, json=payload, headers=headers)    

    if response.status_code == 200:
        # Get the raw audio data
        audio_data = response.content

        # Generate a unique filename for the audio
        file_name = f"tts_{uuid.uuid4()}.mp3"

        # Use the authenticated GCS client to upload
        bucket = storage_client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_string(audio_data, content_type="audio/mpeg")

        # Set the blob to be publicly readable
        blob.make_public()

        # Return the blob's public URL
        return blob.public_url, None

    else:
        return None, response.text
