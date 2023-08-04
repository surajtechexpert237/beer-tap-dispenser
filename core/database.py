from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import app_settings

print(app_settings.DATABASE_URL)
engine = create_engine(app_settings.DATABASE_URL, echo=True)

DBSession = sessionmaker(expire_on_commit=False)

Base = declarative_base()
