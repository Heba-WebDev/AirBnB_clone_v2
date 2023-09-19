#!/usr/bin/python3
""" State Module for HBNB project """
import models
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='delete', backref='State')

    # if os.getenv("HBNB_TYPE_STORAGE") != "db":
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Return list of related City objects."""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
