#!usr/bin/python3
"""Definition of the BaseModel class."""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

Base = declarative_base()


class BaseModel:
    """Defines all common attributes/methods for other classes."""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel class.

        Args:
            self (BaseModel): the current instance
            args (any): not used here
            kwargs (dict): dictionary of key/value pairs attributes
        """
        # public instance attributes
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key in kwargs:
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                elif key != '__class__':
                    setattr(self, key, kwargs[key])
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                if not hasattr(kwargs, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(kwargs, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(kwargs, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    # public instance methods
    def save(self):
        """Updates the public instance attribute updated_at \
            with the current datetime."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all \
            keys/values of __dict__ of the instance."""
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        for key in dict_copy:
            if type(dict_copy[key]) is datetime:
                dict_copy[key] = dict_copy[key].isoformat()
        if '_sa_instance_state' in dict_copy.keys():
            del(dict_copy['_sa_instance_state'])
        return dict_copy

    def delete(self):
        """Delete current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return the string representation of the instance."""
        _dict = self.__dict__.copy()
        _dict.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, dict)
