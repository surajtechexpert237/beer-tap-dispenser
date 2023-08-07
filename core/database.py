from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import app_settings

engine = create_engine(app_settings.DATABASE_URL, echo=True)

DBSession = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()
