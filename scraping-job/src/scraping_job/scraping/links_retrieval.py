import asyncio
import logging
import re

from aiohttp import ClientSession as RequestSession
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

    id_: str
    type_: str


async def retrieve_object_ids(
    page_limit: int,
    object_types: list[str],
) -> list[ListingId]:
    """Retrieve object IDs for the given object types."""
    LOGGER.info(f"Retrieving object IDs for {object_types}")

    # Filter and prepare the search URLs for the specified object types
    target_types = {
        obj_type: url
        for obj_type, url in SEARCH_URLS.items()
        if obj_type in object_types
    }

    final_retrieved_listings = []

    async with RequestSession() as session:
        for object_type, search_url in target_types.items():
            # Scrape the first page to determine the maximum number of pages
            first_page_html = await scrape_url(
                search_url.format(page_number=1),
                session,
            )
            max_page = get_max_page_number(first_page_html, session)

            # Determine the pages to scrape, up to the specified page limit
            page_numbers = range(1, min(max_page, page_limit) + 1)

            # Gather all the pages' HTML content asynchronously
            pages_html = await asyncio.gather(
                *[
                    scrape_url(search_url.format(page_number=page), session)
                    for page in page_numbers
                ],
            )

            # Extract and aggregate listing IDs from all the pages
            all_ids = [
                listing_id
                for page in pages_html
                for listing_id in retrieve_re_ids(page)
            ]

            # Create ListingId objects and add them to the final list
            listings = [
                ListingId(type_=object_type, id_=listing_id) for listing_id in all_ids
            ]
            final_retrieved_listings.extend(listings)

            LOGGER.info(f"Found {len(listings)} object links for {object_type}.")

    return final_retrieved_listings
