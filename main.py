import json
import os
from uuid import uuid4

import requests
from dotenv import load_dotenv

from models import Theme, Tone, Verbosity
from utils import create_headers, safe

load_dotenv()


class Creator:
    def __init__(self, ppt_id=None, ppt_name=None):
        if ppt_id:
            self.ppt_id = ppt_id
        else:
            self.ppt_id = str(uuid4())
            self.ppt_name = "Untitled Presentation"

        self.token = os.getenv("TOKEN")
        self.base_url = "https://alai-standalone-backend.getalai.com"
        self.headers = create_headers(self.token)
        self.ppt_id = str(uuid4())
        self.ppt_name = ppt_name
        self.slides = []
        with open("alai_docs.json", encoding="utf-8") as f:
            self.docs = json.load(f)

    # Helper
    def get_doc_for_function(self, func):
        func_name = func.__name__.replace("_", "-")
        endpoint_key = f"/{func_name}"
        return self.docs["paths"].get(endpoint_key, f"No docs found for endpoint '{endpoint_key}'")

    # Helper
    def get_alai_docs(self):
        url = f"{self.base_url}/openapi.json"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            with open("alai_docs.json", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print(f"Failed to fetch OpenAPI schema: {response.status_code}")

        return safe(response)

    def get_presentations_list(self):
        url = f"{self.base_url}/get-presentations-list"
        payload = {"url_token": None}
        response = requests.get(url, headers=self.headers, json=payload)
        return safe(response)

    def get_themes(self):
        url = f"{self.base_url}/get-themes"
        response = requests.post(url, headers=self.headers)
        return safe(response)

    def create_new_presentation(self, first_slide=False, theme: Theme = Theme.Figment):
        url = f"{self.base_url}/create-new-presentation"

        payload = {
            "presentation_id": self.ppt_id,
            "presentation_title": self.ppt_name,
            "create_first_slide": first_slide,
            "theme_id": theme.value,
            "default_color_set_id": 0,
        }

        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def create_new_slide(self, slide_index=None):
        if not slide_index:
            slide_index = len(self.slides)

        self.slides.insert(slide_index, str(uuid4()))
        # self.slides[slide_index] = str(uuid4())

        url = f"{self.base_url}/create-new-slide"
        payload = {
            "slide_id": self.slides[slide_index],
            "presentation_id": self.ppt_id,
            "product_type": "PRESENTATION_CREATOR",
            "slide_order": slide_index,
            "color_set_id": 0,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def get_presentation_questions(self):
        url = f"{self.base_url}/get-presentation-questions/{self.ppt_id}"
        response = requests.get(url, headers=self.headers)
        return safe(response)

    def upload_images_for_slide_generation(self, paths: list[str]):
        url = f"{self.base_url}/upload-images-for-slide-generation"

        files = [("files", (os.path.basename(path), open(path, "rb"), f"image/{path.split('.')[-1]}")) for path in paths]
        data = {"upload_input": {"presentation_id": self.ppt_id}}

        response = requests.post(url, files=files, data=data)
        return safe(response)

    def calibrate_tone(
        self,
        text: str,
        tone: Tone = Tone.DEFAULT,
        tone_instr: str = None,
    ):
        url = f"{self.base_url}/calibrate-tone"

        payload = {
            "presentation_id": self.ppt_id,
            "original_text": text,
            "tone_type": tone.value,
            "tone_instructions": tone_instr,
        }

        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def calibrate_verbosity(
        self,
        text: str,
        verbosity: Verbosity = Verbosity.MEDIUM,
        verbosity_instr: str = None,
    ):
        url = f"{self.base_url}/calibrate-verbosity"
        payload = {
            "presentation_id": self.ppt_id,
            "original_text": text,
            "verbosity_level": verbosity,
            "previous_verbosity_level": verbosity.value,
            "tone_type": "PROFESSIONAL",
            "tone_instructions": verbosity_instr,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)
