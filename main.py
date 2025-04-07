import json
import os
from uuid import uuid4

import requests
from dotenv import load_dotenv

from login import refresh_token
from models import Theme, Tone, Verbosity
from sockets import create_variants
from utils import create_headers, is_notebook, safe

load_dotenv()


class Creator:
    def __init__(self, ppt_id=None, ppt_name=None):
        if is_notebook():
            self.token = os.getenv("TOKEN")
        else:
            self.token = refresh_token()

        self.base_url = "https://alai-standalone-backend.getalai.com"
        self.headers = create_headers(self.token)
        self.slides = []
        with open("alai_docs.json", encoding="utf-8") as f:
            self.docs = json.load(f)

        if ppt_id:
            self.ppt_id = ppt_id
            self.ppt = self.get_presentation(ppt_id)
        else:
            self.ppt_id = str(uuid4())
            self.ppt_name = ppt_name or "Untitled Presentation"

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

    def get_presentation(self, ppt_id=None):
        if not ppt_id:
            ppt_id = self.ppt_id
        url = f"{self.base_url}/get-presentation/{ppt_id}"
        response = requests.get(url, headers=self.headers)
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
        headers = create_headers(self.token, content_type=False)

        files = []

        for path in paths:
            files.append(("files", (os.path.basename(path), open(path, "rb"), f"image/{path.split('.')[-1]}")))
        # payload = {"upload_input": {"presentation_id": self.ppt_id}}
        payload = {"upload_input": json.dumps({"presentation_id": self.ppt_id})}

        response = requests.post(url, files=files, data=payload, headers=headers)
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

    def set_active_variant(self, slide_id: str, variant_id: str):
        url = f"{self.base_url}/set-active-variant"
        payload = {"slide_id": slide_id, "variant_id": variant_id}
        response = requests.post(url, headers=self.headers, json=payload)
        return safe(response)

    def make_full_slide(
        self,
        instructions,
        content,
        images=[],
        tone=Tone.DEFAULT,
        tone_instr=None,
        verbosity=Verbosity.MEDIUM,
        verbosity_instr=None,
    ):
        slide = self.create_new_slide()
        self.upload_images_for_slide_generation(images)
        t = self.calibrate_tone(content, tone, tone_instr)
        v = self.calibrate_verbosity(content, verbosity, verbosity_instr)
        create_variants(self.ppt_id, self.slides[-1], instructions, content, images)
        self.ppt = self.get_presentation(self.ppt_id)
        active_variant_id = None
        self.set_active_variant(self.slides[-1], active_variant_id)
