#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.city import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    reviews = relationship('Review', backref='place', cascade='delete')
    amenities = relationship('Amenity', secondary='place_amenity',
                             viewonly=False)

    @property
    def amenities(self):
        """Return list of Amenity instances"""
        return self.amenity_ids

    @amenities.setter
    def amenities(self, obj=None):
        """Add Amenity.id to amenity_ids"""
        if obj and type(obj) == Amenity:
            self.amenity_ids.append(obj.id)

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Return list of related Review objects."""
            return [review for review in models.storage.all(Review).values()
                    if review.place_id == Place.id]
