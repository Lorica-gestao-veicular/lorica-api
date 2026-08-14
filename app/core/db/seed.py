# seed file to create the first users

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import admin_settings, db_settings
from app.core.db.models import User
from app.core.security import get_password_hash

engine = create_engine(db_settings.database_url, echo=True)


# Seed query to create an admin user if none exists
with Session(engine) as session:
    selection = session.query(User).all()
    if selection == []:
        session.add(
            User(
                name="admin",
                email=admin_settings.admin_email,
                password=get_password_hash(admin_settings.admin_password),
                role="admin",
            )
        )
        session.commit()
session.close()

# Seed query to create a regular user if none exists
with Session(engine) as session:
    selection = session.query(User).filter_by(role="USER").all()
    if selection == []:
        session.add(
            User(
                name="user",
                email="user@example.com",
                password=get_password_hash("12345"),
                role="user",
            )
        )
        session.commit()
session.close()
