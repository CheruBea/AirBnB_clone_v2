#!/usr/bin/python3
""" Test for the User class"""
from tests.test_models.test_base_model import test_basemodel
from models.user import User
import os


class test_User(test_basemodel):
    """ Tests class for the user model"""

    def __init__(self, *args, **kwargs):
        """ Initializes the user test class"""
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """Testing user first name attr """
        new = self.value()
        self.assertEqual(type(new.first_name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_last_name(self):
        """ Tests user last name attribute"""
        new = self.value()
        self.assertEqual(type(new.last_name), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """Testing the user password attribute """
        new = self.value()
        self.assertEqual(type(new.password), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
