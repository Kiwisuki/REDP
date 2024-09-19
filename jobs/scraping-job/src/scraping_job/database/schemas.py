import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.scraping_job.database import Base


class ScrapedHtml(Base):
    """Model for storing scraped HTML content."""

    __tablename__ = "scraped_html"
    html_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_scraped = Column(DateTime, default=func.now())
    object_type = Column(String, nullable=False)
    url = Column(String, nullable=False)
    html_content = Column(String, nullable=True)
