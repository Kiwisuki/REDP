from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.scraping_job.database import DATABASE_URL, Base


def get_engine_and_session(database_url: str = DATABASE_URL) -> tuple[Engine, Session]:
    """Create a database engine and session."""
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return engine, session
