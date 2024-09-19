import logging
import os

from aiohttp import ClientSession

LOGGER = logging.getLogger(__name__)

SCRAPING_SERVICE_URL = os.environ["SCRAPING_SERVICE_URL"]
LOGGER.info(f"Using scraping service at {SCRAPING_SERVICE_URL}")


async def scrape_url(
    url: str,
    session: ClientSession,
    wait_to_load: int | None = None,
    scraping_service_url: str = SCRAPING_SERVICE_URL,
) -> str:
    """Scrape the HTML content of a given URL asynchronously.

    Args:
        url (str): URL to scrape
        session (ClientSession): AIOHTTP session object to execute the request
        wait_to_load (int): Time to wait for the page to load
        scraping_service_url (str): URL of the scraping service
    Returns:
        str: HTML content of the URL
    """
    body = {"url": url, **({"wait_to_load": wait_to_load} if wait_to_load else {})}
    async with session.get(scraping_service_url, json=body) as response:
        response_data = await response.json()
        return response_data["html"]
