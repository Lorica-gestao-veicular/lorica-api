from sqlalchemy import create_engine

from app.core.config import db_settings
from app.core.db.models import Base

engine = create_engine(db_settings.database_url, echo=True)

Base.metadata.create_all(engine)

print("Database tables created successfully.")
