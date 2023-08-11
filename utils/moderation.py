import openai

import openai

def moderate_content(text: str) -> dict:
    response = openai.Moderation.create(input=text)
    return response["results"][0]
