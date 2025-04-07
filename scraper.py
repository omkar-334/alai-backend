import json
import os

from bs4 import BeautifulSoup
from firecrawl import FirecrawlApp


def format_src(src, url, title=None):
    soup = BeautifulSoup(src, "html.parser")

    if not title:
        title = soup.title.string if soup.title else "No title found"
    description = soup.find("meta", attrs={"name": "description"})
    description = description["content"] if description else ""

    body = soup.find("body")
    all_text = body.get_text(strip=True, separator=" ") if body.name not in {"script", "style", "head", "title", "meta", "[document]"} else ""

    base_url = "/".join(url.split("/")[:3])

    images = extract_image_data(soup, base_url)
    images = filter_image_urls(images)

    content = deduplicate_text(all_text)
    data = {
        "url": url,
        "title": title,
        "content": content,
        "images": images,
    }

    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    return data


def extract_image_data(soup, base_url):
    images_data = []

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src:
            if src.startswith("//"):
                src = f"https:{src}"
            elif src.startswith("/"):
                src = f"{base_url.rstrip('/')}{src}"
            elif not src.startswith(("http://", "https://")):
                src = f"{base_url.rstrip('/')}/{src.lstrip('/')}"

        images_data.append({"src": src, "alt": img.get("alt", "")})

    return images_data


def filter_image_urls(image_data):
    exclude_keywords = {
        "thumbnail",
        "icon",
        "logo",
        "search",
        "linkedin",
        "undefined",
        "gift",
        "author-image",
        "thecaptable",
        "twitter",
        "facebook",
        "instagram",
        "newsletter_loggedin",
    }
    filtered_image_urls = []
    for image in image_data:
        alt_text = image.get("alt", "").lower()
        src = image.get("src", "")

        # Include only images that have meaningful alt text and are not SVGs
        if alt_text and not any(keyword in alt_text for keyword in exclude_keywords) and not src.lower().endswith(".svg"):
            filtered_image_urls.append(src)
    return filtered_image_urls


def deduplicate_text(text):
    sentences = list(set(text.split(". ")))
    return ". ".join(sentences)


def firecrawl_scrape(url, format_="html"):
    app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
    d = app.scrape_url(url, params={"formats": [format_]})
    return d[format_]
