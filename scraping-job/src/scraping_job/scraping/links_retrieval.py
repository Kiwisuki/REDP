import asyncio
import logging
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pydantic import BaseModel

from src.scraping_job import SEARCH_URLS
from src.scraping_job.scraping.html_retrieval import scrape_url

LOGGER = logging.getLogger(__name__)


def filter_strings(string_list: list[str]) -> list[str]:
    """Filter out a list of strings, returning only the patterns that potentially represent RE links."""
    pattern = r"\b(\d{1,2}-\d{3,})\b"
    return [
        re.search(pattern, s).group(1) for s in string_list if re.search(pattern, s)
    ]


def get_max_page_number(source: str) -> int:
    """Return the maximum page number from the given HTML page."""
    soup = BeautifulSoup(source, "html.parser")
    page_numbers = soup.find_all("a", class_="page-bt")
    parsed_numbers = [a.get("href").split("/")[-2] for a in page_numbers]
    verified_numbers = [n for n in parsed_numbers if n.isdigit()]
    return max([int(n) for n in verified_numbers])


def retrieve_re_ids(source: str) -> list[str]:
    """Retrieve all RE ids from the given HTML page."""
    soup = BeautifulSoup(source, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links]
    valid_hrefs = [href for href in hrefs if href is not None]
    return list(set(filter_strings(valid_hrefs)))


class ListingId(BaseModel):
    """A Pydantic model for a listing object."""

    type_: str
    id_: str


async def retrieve_object_ids(
    page_limit: int,
    object_types: list[str],
) -> list[ListingId]:
    """Retrieve object IDs for the given object types."""
    LOGGER.info(f"Retrieving object IDs for {object_types}")
    target_types = {
        obj_type: url
        for obj_type, url in SEARCH_URLS.items()
        if obj_type in object_types
    }
    final_retrieved_listings = []
    async with ClientSession() as session:
        for object_type, search_url in target_types.items():
            max_page_html = await scrape_url(search_url.format(page_number=1), session)
            max_page = get_max_page_number(max_page_html, session)

            scrape_listing_list_tasks = [
                scrape_url(search_url.format(page_number=page_number), session)
                for page_number in range(1, min(max_page, page_limit) + 1)
            ]
            retrieved_listing_pages_html = await asyncio.gather(
                *scrape_listing_list_tasks,
            )
            retrieved_id_lists = [
                retrieve_re_ids(page) for page in retrieved_listing_pages_html
            ]
            retrieved_listings = [
                ListingId(type_=object_type, id_=listing_id)
                for listing_id in sum(retrieved_id_lists, [])
            ]
            final_retrieved_listings.extend(retrieved_listings)
            LOGGER.info(
                f"Found {len(retrieved_listings)} object links for {object_type}.",
            )
    return final_retrieved_listings
