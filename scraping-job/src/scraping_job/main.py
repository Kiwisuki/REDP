import asyncio
import logging

from aiohttp import ClientSession as RequestSession

from src.scraping_job import ALL_OBJECT_TYPES
from src.scraping_job.database.connection import get_engine_and_session
from src.scraping_job.scraping.links_retrieval import retrieve_object_ids
from src.scraping_job.scraping.object_handling import get_scraped_ids, scrape_listing

LOGGER = logging.getLogger(__name__)
PROCESSING_BATCH_SIZE = 20


async def scraping_job(
    page_limit: int = 1,
    object_types_to_scrape: list[str] = ALL_OBJECT_TYPES,
) -> None:
    """Scrape the Aruodas website."""
    # Initialize database engine and session
    engine, database_session = get_engine_and_session()
    try:
        # Retrieve object IDs for scraping
        listing_ids = await retrieve_object_ids(page_limit, object_types_to_scrape)
        scraped_ids = get_scraped_ids(database_session)

        # Filter out already scraped IDs
        target_ids = [
            listing_id
            for listing_id in listing_ids
            if listing_id.id_ not in scraped_ids
        ]
        LOGGER.info(f"Scraping {len(target_ids)} object types.")

        # Prepare and execute scraping tasks in batches
        async with RequestSession() as requests_session:
            scrape_listing_tasks = [
                scrape_listing(listing_id.id_, listing_id.type_, requests_session)
                for listing_id in target_ids
            ]

            # Process scraping tasks in batches
            for i in range(0, len(scrape_listing_tasks), PROCESSING_BATCH_SIZE):
                batch_tasks = scrape_listing_tasks[i : i + PROCESSING_BATCH_SIZE]
                scraped_listings = await asyncio.gather(*batch_tasks)

                LOGGER.info(f"Storing {len(scraped_listings)} scraped listings.")
                database_session.add_all(scraped_listings)
                database_session.commit()
    finally:
        # Clean up database session and engine
        database_session.close()
        engine.dispose()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(scraping_job())
