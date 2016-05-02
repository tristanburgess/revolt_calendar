from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///revolt_calendar.db')
Base.metadata.bind = engine

db_session = sessionmaker(bind=engine)
session = db_session()
