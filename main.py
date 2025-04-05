import os
from uuid import uuid4

import requests
from dotenv import load_dotenv

from models import Tone, Verbosity
from utils import create_headers, safe

load_dotenv()


class Creator:
    def __init__(self, ppt_name="Untitled Presentation"):
        self.token = os.getenv("TOKEN")
        self.headers = create_headers(self.token)
        self.ppt_id = str(uuid4())
        self.ppt_name = ppt_name
        self.slides = []

    def get_alai_docs(self):
        url = "https://alai-standalone-backend.getalai.com/openapi.json"

        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            with open("alai_docs.json", encoding="utf-8") as f:
                f.write(response.text)
        else:
            print(f"Failed to fetch OpenAPI schema: {response.status_code}")

        return safe(response)

    def create_new_ppt(self):
        url = "https://alai-standalone-backend.getalai.com/create-new-presentation"

        payload = {
            "presentation_id": self.ppt_id,
            "presentation_title": self.ppt_name,
            "create_first_slide": False,
            "theme_id": "a6bff6e5-3afc-4336-830b-fbc710081012",
            "default_color_set_id": 0,
        }

        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def create_new_slide(self, slide_index=None):
        if not slide_index:
            slide_index = len(self.slides)

        self.slides[slide_index] = str(uuid4())

        url = "https://alai-standalone-backend.getalai.com/create-new-slide"
        payload = {
            "slide_id": self.slides[slide_index],
            "presentation_id": self.ppt_id,
            "product_type": "PRESENTATION_CREATOR",
            "slide_order": slide_index,
            "color_set_id": 0,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def get_ppt_questions(self):
        url = f"https://alai-standalone-backend.getalai.com/get-presentation-questions/{self.ppt_id}"
        response = requests.get(url, headers=self.headers)
        return safe(response)

    def upload_images(self, paths: list[str]):
        url = "https://alai-standalone-backend.getalai.com/upload-images-for-slide-generation"

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
        url = "https://alai-standalone-backend.getalai.com/calibrate-tone"

        payload = {
            "presentation_id": self.ppt_id,
            "original_text": text,
            "tone_type": tone,
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
        url = "https://alai-standalone-backend.getalai.com/calibrate-verbosity"
        payload = {
            "presentation_id": self.ppt_id,
            "original_text": text,
            "verbosity_level": verbosity,
            "previous_verbosity_level": verbosity,
            "tone_type": "PROFESSIONAL",
            "tone_instructions": verbosity_instr,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)
