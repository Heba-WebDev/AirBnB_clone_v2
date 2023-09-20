#!/usr/bin/python3
"""The new engine DBStorage"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """Class definition"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates a new DB"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")), pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """"""
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objs = self.__session.query(cls)

        return {"{}.{}".format(
            type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        """Adds obj to the database"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_def = sessionmaker(bind=self.__engine,
                                   expire_on_commit=False)
        Session = scoped_session(session_def)
        self.__session = Session()

    def close(self):
        """Closes current session"""
        self.__session.close()
