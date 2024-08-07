import logging
import re
from typing import Dict, List

from bs4 import BeautifulSoup

from src.aruodas_scraper import SEARCH_URLS
from src.aruodas_scraper.helpers.html_retrieval import url_or_html_parser

LOGGER = logging.getLogger(__name__)


@url_or_html_parser
def get_max_page_number(source: str) -> int:
    """Return the maximum page number from the given HTML page."""
    soup = BeautifulSoup(source, "html.parser")
    page_numbers = soup.find_all("a", class_="page-bt")
    parsed_numbers = [a.get("href").split("/")[-2] for a in page_numbers]
    verified_numbers = [n for n in parsed_numbers if n.isdigit()]
    return max([int(n) for n in verified_numbers])


def filter_strings(string_list: List[str]) -> List[str]:
    """Filter out a list of strings, returning only the patterns that potentially represent RE links."""
    pattern = r"\b(\d{1,2}-\d{3,})\b"
    return [
        re.search(pattern, s).group(1) for s in string_list if re.search(pattern, s)
    ]


@url_or_html_parser
def retrieve_re_ids(source: str) -> List[str]:
    """Retrieve all RE ids from the given HTML page."""
    soup = BeautifulSoup(source, "html.parser")
    links = soup.find_all("a")
    hrefs = [link.get("href") for link in links]
    valid_hrefs = [href for href in hrefs if href is not None]
    return list(set(filter_strings(valid_hrefs)))


def retrieve_object_ids(
    page_limit: int, objects_types_to_retrieve: List[str]
) -> Dict[str, List[str]]:
    """Retrieve object IDs for the given object types."""
    LOGGER.info(f"Retrieving object IDs for {objects_types_to_retrieve}")
    types_to_scrape = {
        key: value
        for key, value in SEARCH_URLS.items()
        if key in objects_types_to_retrieve
    }
    object_ids = {object_type: [] for object_type in types_to_scrape}

    for object_type, search_url in types_to_scrape.items():
        max_page = get_max_page_number(search_url.format(page_number=1))
        for page_number in range(1, min(max_page, page_limit) + 1):
            LOGGER.info(
                f"Scraping listing page {page_number}/{min(max_page, page_limit)}"
            )
            retrieved_ids = retrieve_re_ids(search_url.format(page_number=page_number))
            object_ids[object_type].extend(retrieved_ids)

        LOGGER.info(
            f"Found {len(object_ids[object_type])} object links for {object_type}."
        )
    return object_ids
