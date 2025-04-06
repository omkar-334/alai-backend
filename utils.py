from enum import Enum

from models import ResponseModel


def create_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "https://app.getalai.com",
        "Referer": "https://app.getalai.com/",
    }


def safe(response) -> ResponseModel:
    try:
        return ResponseModel(
            response=response.json(),
            status_code=response.status_code,
            json=True,
        )
    except ValueError:
        return ResponseModel(
            response=response.text,
            status_code=response.status_code,
            json=False,
        )


def create_themes_enum(data, enum_name="Theme"):
    enum_dict = {item["display_name"]: item["id"] for item in data}
    enum = Enum(enum_name, enum_dict)
    for theme in enum:
        print(theme.name.replace(" ", "_"), "=", f'"{theme.value}"')
    return enum
