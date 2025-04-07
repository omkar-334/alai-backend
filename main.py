import json

from tqdm import tqdm

from creator import Creator
from llm import describe_image, llm
from models import Slide, SlideWithImage
from prompts import slides_prompt, title_prompt
from scraper import firecrawl_scrape, format_src
from utils import download_images


def main(url, num_slides=4, title=None):
    src = firecrawl_scrape(url)
    print("Scraped data")

    data = format_src(src, url)
    print("Formatted data")

    # with open("data/scraped_data.json", encoding="utf-8") as f:
    #     data = json.load(f)

    title = llm(title_prompt, data["content"])
    print("Generated title")

    creator = Creator(ppt_name=title)

    slides = llm(slides_prompt.format(num_slides), data["content"], schema=list[Slide])
    print("Generated slides")

    images = {}
    for url in tqdm(data["images"], desc="Describing images"):
        if url not in images:
            images[url] = describe_image(url)
        if len(images) >= num_slides:
            break

    image_paths = download_images(list(images.keys()))
    print("Downloaded images")

    new_images = {}
    for path, url in zip(image_paths, images.keys()):
        new_images[path] = images[url]

    data["images"] = new_images
    # # data["other_images"] = data["images"][5:]

    with open("data/final_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    final_slides = []

    for slide, (path, image) in zip(slides, data["images"].items()):
        new_slide = SlideWithImage(title=slide.title, content=slide.content, instruction=slide.instruction, image_url=path, image_description=image)

        final_slides.append(new_slide)

    link = creator.make_presentation(final_slides, image_paths)
    return link


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    url = "https://www.theverge.com/news/622380/lenovo-thinkbook-flip-concept-laptop-foldable-mwc"

    ppt_link = main(url, num_slides=4)
    print(f"Presentation link: {ppt_link}")
    # https://www.loom.com/share/d9e725ea0acf471387dffa6c52290079
