import os
from enum import Enum

import requests
from IPython import get_ipython


def download_images(image_urls: list[str], save_dir: str = "images") -> list[str]:
    """
    Downloads images from a list of URLs and saves them in the specified directory.
    Returns a list of saved file paths.
    """
    os.makedirs(save_dir, exist_ok=True)
    saved_paths = []

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            response.raise_for_status()

            # Try to get a filename from the URL, or use a default one
            filename = os.path.basename(url.split("?")[0])
            if not filename or "." not in filename:
                filename = f"image_{idx}.jpg"
            filename = filename.replace(":", "_").replace(" ", "_")

            filepath = os.path.join(save_dir, filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            saved_paths.append(filepath)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

    return saved_paths


def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        return shell == "ZMQInteractiveShell"
    except NameError:
        return False


def create_headers(token, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Origin": "https://app.getalai.com",
        "Referer": "https://app.getalai.com/",
    }
    if content_type is not False:
        headers["Content-Type"] = content_type
    return headers


def safe(response):
    try:
        return response.json()
    except ValueError:
        return response.content


def create_themes_enum(data, enum_name="Theme"):
    enum_dict = {item["display_name"]: item["id"] for item in data}
    enum = Enum(enum_name, enum_dict)
    for theme in enum:
        print(theme.name.replace(" ", "_"), "=", f'"{theme.value}"')
    return enum
