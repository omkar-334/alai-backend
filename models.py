from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


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


class ResponseModel(BaseModel):
    response: str | dict
    json: bool
    status_code: int
