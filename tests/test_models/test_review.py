#!/usr/bin/python3
""" Tests for the class test review"""
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
import os


class test_review(test_basemodel):
    """Test for class Review """

    def __init__(self, *args, **kwargs):
        """Initializes the review class"""
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """Testing review place_id attr """
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_user_id(self):
        """Testing Review class user_id attr """
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))

    def test_text(self):
        """Testing Review text attribute """
        new = self.value()
        self.assertEqual(type(new.text), str if
                         os.getenv('HBNB_TYPE_STORAGE') != 'db' else
                         type(None))
