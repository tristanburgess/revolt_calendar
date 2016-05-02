from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from models.base import Base
from models.event import Event
from models.event_type import EventType
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///revolt_calendar.db')
Base.metadata.create_all(engine)

db_session = sessionmaker(bind=engine)
session = db_session()

init = EventType(name='performance')
session.add(init)
init = EventType(name='panel')
session.add(init)
init = EventType(name='speaker')
session.add(init)
init = EventType(name='party')
session.add(init)
init = EventType(name='workshop')
session.add(init)
init = EventType(name='demo')
session.add(init)
session.commit()