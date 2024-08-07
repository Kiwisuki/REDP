import logging
from pathlib import Path

from sqlalchemy.orm import Session

from src.aruodas_scraper import DATA_DIR
from src.aruodas_scraper.helpers.database import ScrapedHtml
from src.aruodas_scraper.helpers.html_retrieval import scrape_url

LOGGER = logging.getLogger(__name__)


def scrape_and_store_object(
    object_id: str, object_type: str, db_session: Session
) -> None:
    """Scrape and store the object with the given ID."""
    LOGGER.info(f"Scraping and storing {object_id}")
    url = f"https://www.aruodas.lt/{object_id}"
    html = scrape_url(url)

    filename = DATA_DIR / f"{id}.html"
    with Path.open(filename, "w") as f:
        f.write(html)

    db_entry = ScrapedHtml(url=url, filename=str(filename), content_type=object_type)
    db_session.add(db_entry)
    db_session.commit()
    LOGGER.info(f"Successfully scraped and stored {object_id}")
