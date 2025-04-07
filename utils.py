from enum import Enum

from models import ResponseModel


def create_headers(token, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Origin": "https://app.getalai.com",
        "Referer": "https://app.getalai.com/",
    }
    if content_type is not False:
        headers["Content-Type"] = content_type
    return headers


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
