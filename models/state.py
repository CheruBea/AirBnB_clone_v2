#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class or table model """
    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')
    else:
        name = ""

        @property
        def cities(self):

            """returns the list of City instances with the state_id
                equals the current State_id
                FileStorage relationship between State and City
            """
            from models import storage
            cities_related = []
            cities = storage.all(City)
            for city in cities.values():
                if city.state_id == self.id:
                    cities_related.append(city)
            return cities_related
