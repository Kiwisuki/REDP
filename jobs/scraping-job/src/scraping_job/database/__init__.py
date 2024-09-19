import os

from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.environ["DATABASE_URL"]


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
