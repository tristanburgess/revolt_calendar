from sqlalchemy import Column, PrimaryKeyConstraint, Integer, String
from models.base import Base
from sqlalchemy.orm import relationship

class InputSet(Base):
    __tablename__ = 'input_set'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
