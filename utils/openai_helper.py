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
def generate_image(prompt, n=1, size="1024x1024", model="dall-e-2", style="natural", quality="standard", user=""):
    # If the model is 'dall-e-2' or not specified, use the existing behavior
    if model == "dall-e-2":
        return openai.Image.create(prompt=prompt, n=n, size=size)
    # If the model is 'dall-e-3', use the new enhancements
    elif model == "dall-e-3":
        # Validate that DALL-E 3 is only generating one image at a time
        if n != 1:
            raise ValueError("DALL-E 3 currently supports generation of only 1 image at a time (n=1).")
        # Validate the image size for DALL-E 3
        valid_sizes = ["1024x1024", "1792x1024", "1024x1792"]
        if size not in valid_sizes:
            raise ValueError(f"Invalid size for DALL-E 3. Valid sizes: {valid_sizes}")
        # Make the API call with the DALL-E 3 specific parameters
        return openai.Image.create(
            prompt=prompt,
            n=n,
            size=size,
            model=model,
            style=style,
            quality=quality,
            user=user
        )
    else:
        raise ValueError("Invalid model specified. Valid models: 'dall-e-2', 'dall-e-3'.")
