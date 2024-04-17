#!/usr/bin/python3
"""Tests the class State"""
from tests.test_models.test_base_model import test_basemodel
from models.state import State
import os


class test_state(test_basemodel):
    """States the test class """

    def __init__(self, *args, **kwargs):
        """Initializes the state class """
        super().__init__(*args, **kwargs)
        self.name = "State"
        self.value = State

    def test_name3(self):
        """ Testing the same name attribute"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
