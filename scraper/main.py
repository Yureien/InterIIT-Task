import os
import asyncio
import json
import re
import random
from urllib.parse import urlparse

import aiohttp
import meilisearch
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()
# Then load them here
MEILEI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")
SAVED_LINKS = os.getenv("SAVED_LINKS", "scraper/saved_links.json")
VALID_META_PROPERTIES = (
    "og:title",
    "og:description",
    "og:video:tag",
    "og:tag",
    "og:image",
    "og:keywords",
)
VALID_META_TAGS = (
    "title",
    "description",
    "tags",
    "keywords",
    "image",
    "name",
    "genre",
)

# Initialize MeileiSearch client
client = meilisearch.Client("http://localhost:7700", MEILEI_MASTER_KEY)


async def main():
    with open(SAVED_LINKS, "r") as f:
        saved_links = json.load(f)
    saved_links = saved_links["links"]
    random.shuffle(saved_links)

    links_queue = asyncio.Queue()
    for link in saved_links:
        await links_queue.put(link)

    data_queue = asyncio.Queue()

    # Process all the links asynchronously with 10 workers
    # And an additional worker for submitting jobs to MeileiSearch
    await asyncio.gather(
        *(
            [process(links_queue, data_queue) for _ in range(10)]
            + [submit(links_queue, data_queue)]
        ),
    )


async def submit(links_queue: asyncio.Queue, data_queue: asyncio.Queue):
    # Submit every 10 seconds
    while True:
        await asyncio.sleep(10)
        print("Submitting job...")
        combined_data = []
        while not data_queue.empty():
            data = await data_queue.get()
            combined_data.append(data)
        print("Job Size:", len(combined_data))
        if len(combined_data) == 0:
            continue
        job = client.index("links").add_documents(combined_data)
        print(job)

        if links_queue.empty() and data_queue.empty():
            print("Done!")
            break


async def fetch_content(link) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link, verify_ssl=False) as response:
                if response.status >= 400:
                    raise Exception(f"Invalid status code {response.status}: {link}")
                return await response.text()
    except UnicodeDecodeError:
        print("Link:", link)
    except Exception as e:
        with open("scraper/skipped_links.txt", "a") as f:
            f.write(link)
            f.write("\n")
        print("Error:", e)


async def process(links_queue: asyncio.Queue, data_queue: asyncio.Queue):
    combined_data = []

    while not links_queue.empty():
        link = await links_queue.get()

        if ".pdf" in link:
            # TODO: Add PDF support
            print("Skipping PDF:", link)
            with open("scraper/pdf_links.txt", "a") as f:
                f.write(link)
                f.write("\n")
            continue

        print("Processing:", link)
        print(f"Left: {links_queue.qsize()}", end="\r")

        parsed_link = urlparse(link)
        stripped_link = parsed_link.netloc + parsed_link.path
        stripped_link = re.sub(r"[^0-9a-zA-Z-_]+", "_", stripped_link)

        data = {"link": link, "id": stripped_link}

        content = await fetch_content(link)
        if content is None:
            continue
        soup = BeautifulSoup(content, "html.parser")

        meta_tags = soup.find_all("meta")
        for tag in meta_tags:
            content = tag.get("content")
            property = tag.get("property")
            name = tag.get("name") or tag.get("itemprop")
            if not content:
                continue
            if property and property in VALID_META_PROPERTIES:
                data[property[3:]] = content
            if name and name in VALID_META_TAGS:
                data[name] = content

        title = soup.find("title")
        if title:
            data["title"] = title.get_text()

        # Remove all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Fix image
        if "image" in data and not data["image"].startswith("http"):
            data[
                "image"
            ] = f'{parsed_link.scheme}://{parsed_link.netloc}{data["image"]}'

        # Add body
        body = soup.find("body")
        if body:
            body_text = body.get_text()
            data["body"] = re.sub(r"\s+", " ", body_text).strip()

        combined_data.append(data)
        await data_queue.put(data)


if __name__ == "__main__":
    asyncio.run(main())
