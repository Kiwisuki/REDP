import logging
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.property_data_pipeline.crawler.html_retrieval import scrape_url
from src.property_data_pipeline.database.schemas import ScrapedHtml

LOGGER = logging.getLogger(__name__)


def scrape_and_store_object(
    object_id: str, object_type: str, db_session: Session
) -> ScrapedHtml:
    """Scrape and store the object with the given ID."""
    LOGGER.info(f"Scraping and storing {object_id}")
    url = f"https://www.aruodas.lt/{object_id}"
    html = scrape_url(url)
    db_entry = ScrapedHtml(url=url, content_type=object_type, html_content=html)
    db_session.add(db_entry)
    db_session.commit()
    LOGGER.info(f"Successfully scraped and stored {object_id}")
    return db_entry


def get_scraped_ids(db_session: Session) -> List[str]:
    """Get the set of IDs that have already been scraped."""
    scraped_urls = db_session.execute(select(ScrapedHtml.url)).scalars().all()
    scraped_ids = [url.split("/")[-1] for url in scraped_urls]
    return list(set(scraped_ids))
