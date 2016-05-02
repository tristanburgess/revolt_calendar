from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, Integer, String, Time
from models.base import Base
from models.event_type import EventType
from models.input_set import InputSet
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(500))
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    address = Column(String(500))
    type_id = Column(Integer, ForeignKey('event_type.id'))
    type = relationship(EventType)
    input_set_id = Column(Integer, ForeignKey('input_set.id'))
    input_set = relationship(InputSet)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'startTime': self.startTime,
            'endTime': self.endTime,
            'address': self.address,
            'type': self.type,
            'input_set': self.input_set
        }
