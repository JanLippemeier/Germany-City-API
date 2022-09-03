from sqlalchemy import Integer, ForeignKey, Float, String, Column
from sqlalchemy.orm import relationship
from .database import base

class state(base):
    __tablename__ = "state"

    id = Column(Integer, primary_key=True)
    name = Column(String)

class city(base):
    __tablename__ = "city"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    state_id = Column(Integer, ForeignKey("state.id"))
    state = relationship("state", foreign_keys=[state_id])
    area = Column(Float)
    population = Column(Integer)
    female_population = Column(Integer)
    postal_code = Column(Integer)
    longitude = Column(Float)
    latitude = Column(Float)
