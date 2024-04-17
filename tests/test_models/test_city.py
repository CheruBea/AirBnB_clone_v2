#!/usr/bin/python3
"""Tests the city class """
from tests.test_models.test_base_model import test_basemodel
from models.city import City
import os


class test_City(test_basemodel):
    """ Tests the City class"""

    def __init__(self, *args, **kwargs):
        """ Initializes the testIcity class"""
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    def test_state_id(self):
        """Testing the state_id type"""
        new = self.value()
        self.assertEqual(type(new.state_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_name(self):
        """ Testing name type"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
