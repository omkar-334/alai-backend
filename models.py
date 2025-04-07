from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


def to_string(slide) -> str:
    return f"title: {slide.title}\ncontent: {slide.content}\ninstruction: {slide.instruction}\n image_description: {slide.image_description}"


def slides_to_string(slides: list[Slide]) -> str:
    return "\n".join(to_string(slide) for slide in slides)


def prepare_slide(slide):
    content = f"title: {slide.title}\ncontent: {slide.content}\n image_description: {slide.image_description}"
    instruction = slide.instruction
    return content, instruction


class Slide(BaseModel):
    title: str
    content: str
    instruction: str | None = None
    # image_url: str | None = None


class SlideWithImage(BaseModel):
    title: str
    content: str
    instruction: str | None = None
    image_url: str | None = None
    image_description: str | None = None


class Presentation(BaseModel):
    slides: list[Slide]
    title: str | None = None
    calibrate: Calibrate | None = None


class Calibrate(BaseModel):
    tone: Tone | None = None
    tone_instruction: str | None = None
    verbosity: Verbosity | None = None
    verbosity_instruction: str | None = None


class Tone(str, Enum):
    DEFAULT = "DEFAULT"
    PROFESSIONAL = "PROFESSIONAL"
    CASUAL = "CASUAL"
    PERSUASIVE = "PERSUASIVE"
    INSPIRATIONAL = "INSPIRATIONAL"
    EDUCATIONAL = "EDUCATIONAL"
    NARRATIVE = "NARRATIVE"
    AUTHORITATIVE = "AUTHORITATIVE"
    TECHNICAL = "TECHNICAL"
    EMPATHETIC = "EMPATHETIC"
    CUSTOM_TONE = "CUSTOM TONE"


class Verbosity(int, Enum):
    LOW = 1
    LOW_MEDIUM = 2
    MEDIUM = 3
    MEDIUM_HIGH = 4
    HIGH = 5


class Theme(str, Enum):
    Figment = "a6bff6e5-3afc-4336-830b-fbc710081012"
    Fable = "c21fba8f-fab1-4314-bcf9-ce5ce9183da0"
    Light_Glow = "3645a4e0-9292-4fa7-ada2-2be94669d8e3"
    Verdant = "41681167-8ab8-440d-a3e7-601e222127e3"
    Essential_Press = "653eab90-c8ba-4d0e-81fb-f27fa3a98408"
    Casual_vibes = "349ca344-9cab-4f9c-9277-93ec172dea51"
    Sienna = "134abba8-bf0a-443c-809d-a126622704dd"
    Sienna_Glow = "79d04427-ca74-4227-b20e-f0105b829ac4"
    Sapphire_Cut = "482b9b7a-3607-449b-bbd9-c703444a0830"
    Crimson_Edge = "5fd73b6a-b896-4ae5-8b01-9d6ed9750d00"
    Indigo_Bloom = "4d6bfd69-0373-43a1-839e-4e741574cebd"
    Lavender_Sky = "fbd638ff-2dd5-4c6e-83f2-62d2091ad366"
    Mint_Breeze = "365c001d-083c-4950-b6cd-bccf13405a07"
    Pastel_Dreams = "5173e252-a38b-43e0-9878-2f3862d0dcd1"
    Peach_Blossom = "0fdd1048-e16c-4ec4-a6a9-64b198dbfafe"
    Ocean_Depths = "6f3af64d-6790-41e9-9efd-86f2b2d50e91"
    Cosmic_Aurora = "1353b78e-3716-4be2-9776-d464014111be"
    Sunset_Horizon = "20012fb9-f0e0-442a-82d5-ca20fd6b836e"
    Emerald_Forest = "3109a90e-bbdf-4c6d-8c4e-51a687b5d8db"
    Aurora_Borealis = "6fa65faa-2e9d-4bc3-bc46-54645eb8b8d6"
    Chromatic_Horizon = "0bbe1154-3616-4a17-b4cc-e5724ec3f3c2"
    Celestial_Aura = "7d9e9586-e523-4e43-89a1-ed14eb3c2002"


class Layout(Enum):
    TITLE_AND_BODY = "TITLE_AND_BODY_LAYOUT"
    LIST_SECTIONS_AND_CONCLUSION = "LIST_SECTIONS_AND_CONCLUSION_LAYOUT"
    TEXT_SECTIONS_AND_CONCLUSION = "TEXT_SECTIONS_AND_CONCLUSION_LAYOUT"
    IMAGE_ONLY = "IMAGE_ONLY_LAYOUT"
    IMAGE_SECTIONS_AND_CONCLUSION = "IMAGE_SECTIONS_AND_CONCLUSION_LAYOUT"
    ICON_SECTIONS_AND_CONCLUSION = "ICON_SECTIONS_AND_CONCLUSION_LAYOUT"
    TITLE_AND_TABLE = "TITLE_AND_TABLE_LAYOUT"
    TITLE_AND_TIMELINE = "TITLE_AND_TIMELINE_LAYOUT"
    TITLE_AND_IMAGE_TIMELINE = "TITLE_AND_IMAGE_TIMELINE_LAYOUT"
    TITLE_AND_FUNNEL = "TITLE_AND_FUNNEL_LAYOUT"
    AI_GENERATED = "AI_GENERATED_LAYOUT"
    SECTION_BREAK = "SECTION_BREAK_LAYOUT"
    TITLE_AND_AUTHOR = "TITLE_AND_AUTHOR_LAYOUT"
    HEADLINE_WITH_CENTERED_TEXT = "HEADLINE_WITH_CENTERED_TEXT_LAYOUT"
    HEADLINE_WITH_RIGHT_TEXT = "HEADLINE_WITH_RIGHT_TEXT_LAYOUT"
    BIG_NUMBER = "BIG_NUMBER_LAYOUT"
    TITLE_AND_TABLE_VARIATIONS = "TITLE_AND_TABLE_VARIATIONS_LAYOUT"
    TITLE_AND_SECTION_VARIATIONS = "TITLE_AND_SECTION_VARIATIONS_LAYOUT"
    TEXT_AND_IMAGE = "TEXT_AND_IMAGE_LAYOUT"
    IMAGE_AND_TEXT = "IMAGE_AND_TEXT_LAYOUT"
