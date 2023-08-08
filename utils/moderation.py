import openai
from ..settings.env_loader import openai_api_key

# define the function for moderation
def moderate_content(text: str) -> dict:
    response = openai.Moderation.create(input=text)
    return response["results"][0]
