#!/usr/bin/python3
"""
A unit test module for the console (command interpreter)
"""

import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream
"""
clear_stream is intended to clear the content of a stream, such as the
stdout or the stdeerr which can be useful during testing to clean up
the output
StringIO, you can create an obj that behaves like a file, allowing
you to read from or write to it as if it were a regular file, useful
when you want to treat a string as file-like object, such as when
working with code that expects file input or output
"""


class TestHBNBCommand(unittest.TestCase):
    """represents the test class for the HBNBCommand class
    """
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorange test')
    def test_fs_create(self):
        """Tests the create cms with fs"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()  # creates an instance of HBNB class
            cons.onecmd('create City name="Texas"')
            mdl_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(mdl_id), storage.all().keys())
            cons.onecmd('show City {}'.format(mdl_id))
            self.assertIn("'name': 'Texas'", cout.getvalue().strip())
            clear_stream(cout)
            cons.onecmd('create User name="Milly" age=17 height=5.9')
            mdl_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(mdl_id), storage.all().keys())
            clear_stream(cout)
            cons.onecmd('show User {}'.format(mdl_id))
            self.assertIn("'name': 'Milly'", cout.getvalue().strip())
            self.assertIn("'age': 17", cout.getvalue().strip())
            self.assertIn("'height': 5.9", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """Tests the create cmd with db storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # creating a model with a non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                cons.onecmd('create User')
            # creating user instance
            clear_stream(cout)
            cons.onecmd('create User email="milly@gmail.com" password="123"')
            mdl_id = cout.getvalue().strip()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbc.cursor()
            cur.execute('SELECT * FROM users WHERE id="{}"'.format(mdl_id))
            result = cur.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('milly@gmail.com', result)
            self.assertIn('123', result)
            cur.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """Tests the show cmd with the db storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            # showing a User instance
            obj = User(email="milly@gmail.com", password='123')
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbc.cursor()
            cur.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cur.fetchone()
            self.assertTrue(result is None)
            cons.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbc.cursor()
            cur.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            cons.onecmd('show User {}'.format(obj.id))
            result = cur.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('milly@gmail.com', result)
            self.assertIn('123', result)
            self.assertIn('milly@gmail.com', cout.getvalue())
            self.assetIn('123', cout.getvalue())
            cur.close()
            dbc.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """Tests the count cmd with the db storage"""
        with patch('sys.stdout', new=StringIO()) as cout:
            cons = HBNBCommand()
            dbc = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cur = dbc.cursor()
            cur.execute('SELECT COUNT(*) FROM states;')
            res = cur.fetchoone()
            prev_count = int(res[0])
            cons.onecmd('create State name="Egypt"')
            clear_stream(cout)
            cons.onecmd('count State')
            count = cout.getvalue().strp()
            self.assertEqual(int(count), prev_count + 1)
            clear_stream(cout)
            cons.onecmd('count State')
            cur.close()
            dbc.close()
