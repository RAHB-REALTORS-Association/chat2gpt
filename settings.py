SETTINGS = {
    "OPENAI_API_KEY": {
        "default": None,
        "required": True,
        "type": str,
        "description": "Your OpenAI API key."
    },
    "MODEL_NAME": {
        "default": "gpt-3.5-turbo",
        "required": False,
        "type": str,
        "description": "Name of the GPT model to use."
    },
    "SYSTEM_PROMPT": {
        "default": "You are a helpful assistant.",
        "required": False,
        "type": str,
        "description": "Prompt to set the behavior of the assistant."
    },
    "PROMPT_PREFIX": {
        "default": "[INST]",
        "required": False,
        "type": str,
        "description": "Prefix added to beginning of user prompt for local model API. Default: LLaMa2"
    },
    "PROMPT_SUFFIX": {
        "default": "[/INST]",
        "required": False,
        "type": str,
        "description": "Suffix added to ending of user prompt for local model API. Default: LLaMa2"
    },
    "MAX_TURNS": {
        "default": 10,
        "required": False,
        "type": int,
        "description": "Maximum number of conversation turns."
    },
    "TTL": {
        "default": 600,
        "required": False,
        "type": int,
        "description": "Time to live (in seconds) for the conversation context."
    },
    "MAX_TOKENS_INPUT": {
        "default": 1000,
        "required": False,
        "type": int,
        "description": "Maximum number of tokens in the input prompt."
    },
    "MAX_TOKENS_OUTPUT": {
        "default": 1000,
        "required": False,
        "type": int,
        "description": "Maximum number of tokens in the output response."
    },
    "TEMPERATURE": {
        "default": 0.8,
        "required": False,
        "type": float,
        "description": "Temperature parameter for randomness in generation."
    },
    "IMAGE_SIZE": {
        "default": "512x512",
        "required": False,
        "type": str,
        "description": "Size of the images."
    },
    "API_URL": {
        "default": None,
        "required": False,
        "type": str,
        "description": "API endpoint for chat completions."
    },
    "ELEVENLABS_API_KEY": {
        "default": None,
        "required": False,
        "type": str,
        "description": "ElevenLabs Text-to-Speech API key."
    },
    "ELEVENLABS_MODEL_NAME": {
        "default": "eleven_multilingual_v2",
        "required": False,
        "type": str,
        "description": "Name of the ElevenLabs Text-to-Speech model."
    },
    "GCS_BUCKET_NAME": {
        "default": None,
        "required": False,
        "type": str,
        "description": "Name of the Google Cloud Storage bucket."
    },
    "LOG_FILE": {
        "default": None,
        "required": False,
        "type": str,
        "description": "Path to save server log file. Disabled if none."
    },
    "LOG_LEVEL": {
        "default": "INFO",
        "required": False,
        "type": str,
        "description": "Enable debugging for server by setting to 'DEBUG'"
    },
    "HOST": {
        "default": "0.0.0.0",
        "required": False,
        "type": str,
        "description": "Server host."
    },
    "PORT": {
        "default": 5000,
        "required": False,
        "type": int,
        "description": "Server port."
    }
}
