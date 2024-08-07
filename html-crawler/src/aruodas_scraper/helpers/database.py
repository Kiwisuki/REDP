from typing import Tuple

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.sql import func

from src.aruodas_scraper import DATABASE_URL, Base


class ScrapedHtml(Base):

    """Model for storing scraped HTML content."""

    __tablename__ = "scraped_html"
    object_id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    date_scraped = Column(DateTime, default=func.now())


def get_engine_and_session(database_url: str = DATABASE_URL) -> Tuple[Engine, Session]:
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return engine, Session()
