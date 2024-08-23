import logging
from typing import List

from src.property_data_pipeline import ALL_OBJECT_TYPES
from src.property_data_pipeline.crawler.links_retrieval import retrieve_object_ids
from src.property_data_pipeline.crawler.object_handling import (
    get_scraped_ids,
    scrape_and_store_object,
)
from src.property_data_pipeline.database.connection import get_engine_and_session
from src.property_data_pipeline.parser.html_to_db import parse_and_store_flat

LOGGER = logging.getLogger(__name__)


def crawling_job(
    page_limit: int = 1, object_types_to_scrape: List[str] = ALL_OBJECT_TYPES
) -> None:
    """Scrape the Aruodas website."""
    engine, session = get_engine_and_session()
    object_ids = retrieve_object_ids(page_limit, object_types_to_scrape)
    scraped_ids = get_scraped_ids(session)
    for object_type, retrieved_ids in object_ids.items():
        for object_id in retrieved_ids:
            if object_id not in scraped_ids:
                html_orm = scrape_and_store_object(object_id, object_type, session)
                parse_and_store_flat(html_orm.html_content, html_orm.html_id, session)

            else:
                LOGGER.info(f"Skipping {object_id} as it has already been scraped")
    session.close()
    engine.dispose()


if __name__ == "__main__":
    crawling_job()
