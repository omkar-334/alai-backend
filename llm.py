import json
import os

import requests
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def load_json(response):
    try:
        response = json.loads(response)
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON. Using fallback.")
        response = None
    return response


def describe_image(url):
    image = requests.get(url)
    mime = image.headers["content-type"]

    response = client.models.generate_content(
        # model="gemini-2.0-flash-001",
        model="gemini-2.0-flash-lite",
        contents=["What is this image?", types.Part.from_bytes(data=image.content, mime_type=mime)],
    )
    return response.text


def llm(system_prompt, user_prompt, schema=None, json=False):
    config = {"temperature": 0.5}
    if schema:
        config["response_schema"] = schema
    if schema or json:
        config["response_mime_type"] = "application/json"
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": system_prompt + "\n" + user_prompt}],
                }
            ],
            config=config,
        )

        if schema:
            return response.parsed
        if json:
            return load_json(response.text)
        return response.text  # noqa: TRY300

    except Exception as e:
        print(e)
        return None
