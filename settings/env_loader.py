import os

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
