#!/usr/bin/python3
""" State Module for HBNB project """
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
import os
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='delete', backref='state')

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Return list of related City objects."""
            return [city for city in models.storage.all(City).values()
                    if city.state_id == self.id]
