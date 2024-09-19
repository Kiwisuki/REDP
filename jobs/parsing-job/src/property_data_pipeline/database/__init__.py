from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql://myuser:mypassword@db:5432/myapp"


class Base(DeclarativeBase):

    """Base class for all SQLAlchemy models."""
