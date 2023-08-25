import openai
import tiktoken

def initialize_openai(api_key, temperature, max_tokens_output):
    # Set the OpenAI API key
    openai.api_key = api_key

    # Set the temperature and max_tokens for output
    params = {'temperature': temperature, 'max_tokens': max_tokens_output}
    return params

def moderate_content(text: str) -> dict:
    response = openai.Moderation.create(input=text, model="text-moderation-latest")
    return response["results"][0]

# Define the function for token counting
def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Define the function for image generation
def generate_image(prompt, n=1, size="512x512"):
    return openai.Image.create(prompt=prompt, n=n, size=size)