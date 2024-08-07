import logging
from pathlib import Path

from sqlalchemy.orm import DeclarativeBase

LOGGER = logging.getLogger(__name__)
DATABASE_URL = "postgresql://myuser:mypassword@db:5432/myapp"
SEARCH_URLS = {
    "butai": "https://www.aruodas.lt/butai/puslapis/{page_number}/",
    "namai": "https://www.aruodas.lt/namai/puslapis/{page_number}/",
    "patalpos": "https://www.aruodas.lt/patalpos/puslapis/{page_number}/",
    "butu-nuoma": "https://www.aruodas.lt/butu-nuoma/puslapis/{page_number}/",
    "patalpu-nuoma": "https://www.aruodas.lt/patalpu-nuoma/puslapis/{page_number}/",
    "sklypai-pardavimui": "https://www.aruodas.lt/sklypai-pardavimui/puslapis/{page_number}/?FOfferType=1&FBuildingType=1",
    "garazai-pardavimui": "https://www.aruodas.lt/garazai-pardavimui/puslapis/{page_number}/?FOfferType=1&FBuildingType=1",
    "trumpalaike-nuoma": "https://www.aruodas.lt/trumpalaike-nuoma/puslapis/{page_number}/",
}

ALL_OBJECT_TYPES = list(SEARCH_URLS.keys())
CURRENT_SCRIPT_PATH = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_SCRIPT_PATH.parents[2]
DATA_DIR = PROJECT_ROOT / "scraped_data"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] - <%(name)s> - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
)


class Base(DeclarativeBase):

    """Base class for all SQLAlchemy models."""


try:
    from dotenv import load_dotenv

    assert load_dotenv(), "No .env file found, have you copied .env.tmpl to .env?"
except ImportError:
    LOGGER.warning(
        "python-dotenv not installed, skipping .env loading, this is expected if running via Docker."
    )
