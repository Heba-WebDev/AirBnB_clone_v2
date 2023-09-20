#!/usr/bin/python3
""" State Module """
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """getter for cities"""
            cities_list = [i for i in list(models.storage.all(City).values())
                           if i.state_id == self.id]
            return cities_list
