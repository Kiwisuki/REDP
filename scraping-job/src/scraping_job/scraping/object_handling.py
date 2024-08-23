import logging

from aiohttp import ClientSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.scraping_job.database.schemas import ScrapedHtml
from src.scraping_job.scraping.html_retrieval import scrape_url

LOGGER = logging.getLogger(__name__)


async def scrape_listing(
    object_id: str,
    object_type: str,
    requests_session: ClientSession,
) -> ScrapedHtml:
    """Scrape and convert the HTML content of a URL to a database entry."""
    LOGGER.info(f"Scraping and storing {object_id}")
    url = f"https://www.aruodas.lt/{object_id}"
    html = await scrape_url(url, requests_session)
    return ScrapedHtml(object_type=object_type, url=url, html_content=html)


def get_scraped_ids(db_session: Session) -> list[str]:
    """Get the set of IDs that have already been scraped."""
    scraped_urls = db_session.execute(select(ScrapedHtml.url)).scalars().all()
    scraped_ids = [url.split("/")[-1] for url in scraped_urls]
    return list(set(scraped_ids))
