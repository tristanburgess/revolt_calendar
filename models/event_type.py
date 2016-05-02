from sqlalchemy import Column, PrimaryKeyConstraint, UniqueConstraint, Integer, String
from models.base import Base

class EventType(Base):
    __tablename__ = 'event_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), unique=True, nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }