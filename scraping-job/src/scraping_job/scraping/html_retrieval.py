import logging
import os

from aiohttp import ClientSession

LOGGER = logging.getLogger(__name__)

SCRAPING_SERVICE_URL = os.environ["SCRAPING_SERVICE_URL"]
LOGGER.info(f"Using scraping service at {SCRAPING_SERVICE_URL}")


async def scrape_url(
    url: str,
    session: ClientSession,
    scraping_service_url: str = SCRAPING_SERVICE_URL,
) -> str:
    """Scrape the HTML content of a given URL asynchronously.

    Args:
        url (str): URL to scrape
        scraping_service_url (str): URL of the scraping service
        session (ClientSession): AIOHTTP session object to execute the request
    Returns:
        str: HTML content of the URL
    """
    body = {"url": url}
    async with session.get(scraping_service_url, json=body) as response:
        response_data = await response.json()
        return response_data["html"]
