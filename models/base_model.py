#!usr/bin/python3
"""Definition of the BaseModel class."""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

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
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if len(kwargs):
            iso_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.strptime(value, iso_format)
                else:
                    self.__dict__[key] = value
        else:
            models.storage.new(self)

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
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy.pop('_sa_instance_state', None)

        return (dict_copy)

    def delete(self):
        """Delete current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return the string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
