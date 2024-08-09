# NOTE: The current implementation raises some issues, since this database table won't be accessible by other microservices,
# NOTE: we might need to create a shared package that contains the database models and the database connection function.
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.property_data_pipeline.database import Base


class ScrapedHtml(Base):

    """Model for storing scraped HTML content."""

    __tablename__ = "scraped_html"
    object_id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    content_type = Column(String, nullable=False)  # TODO: Rename to object_type
    date_scraped = Column(DateTime, default=func.now())
    html_content = Column(String, nullable=True)
