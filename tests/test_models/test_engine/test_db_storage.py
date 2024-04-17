#!/usr/bin/python3
"""module for the file_storage tests"""
import unittest
import MySQLdb
from models.user import User
from models import storage
from datetime import datetime
import os


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 'db_storage test not supported')
class TestDBStorage(unittest.TestCase):
    """testing dbstorage engine"""
    def test_new_and_save(self):
        """testing the new and save methods"""
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MYSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        new_user = User(**{'first_name': 'Reginah',
                           'last_name': 'Shikanda',
                           'email': 'regina@gmail.com',
                           'password': 12345})
        curs = db.cursor()
        curs.execute('SELECT COUNT(*) FROM users')
        count_old = curs.fetchall()
        curs.close()
        db.close()
        n_user.save()
        db = MySQLdb.connect(user=os.getenv('HBNB_MYSQL_USER'),
                             host=os.getenv('HBNB_MYSQL_HOST'),
                             passwd=os.getenv('HBNB_MTSQL_PWD'),
                             port=3306,
                             db=os.getenv('HBNB_MYSQL_DB'))
        curs = db.cursor()
        curs.execute('SELECT COUNT(*) FROM users')
        count_new = curs.fetchall()
        self.assertEqual(count_new[0][0], count_old[0][0])
        curs.close()
        db.close()

    def test_new(self):
        """new obj is correctly added to db"""
        new = User(
            email='regina@gmail.com',
            password='password',
            first_name='Reginah',
            last_name='Shikanda'
        )
        self.assertFalse(new in storage.all().values())
        new.save()
        self.assertTrue(new in storage.all().values())
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MTSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = dbc.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cur.fetchone()
        self.assertTrue(res is not None)
        self.assertIn('regina@gmail.com', res)
        self.assertIn('password', res)
        self.assertIn('Reginah', res)
        self.assertIn('Shikanda', res)
        cur.close()
        db.close()

    def test_delete(self):
        """obj is correctly deleted from db"""
        new = User(
            email='regina@gmail.com',
            password='password',
            first_name='Reginah',
            last_name='Shikanda'
        )
        obj_key = 'User.{}'.format(new.id)
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        new.save()
        self.assertTrue(new in storage.all().values())
        cur = dbc.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cur.fetchone()
        self.assertTrue(res is not None)
        self.assertIn('regina@gmail.com', res)
        self.assertIn('password', res)
        self.assertIn('Reginah', res)
        self.assertIn('Shikanda', res)
        self.assertIn(obj_key, storage.all(User).keys())
        new.delete()
        self.assertNotIn(obj_key, storage.all(User).keys())
        cur.close()
        db.close()

    def test_reload(self):
        """Test the reloading of the db session"""
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB'),
        )
        cur = dbc.cursor()
        cur.execute(
            'INSERT INTO users(id, created_at, updated_at, email, password' +
            ', first_name, last_name) VALUES(%s, %s, %s, %s, %s, %s, %s);',
            [
                '4447-by-me',
                str(datetime.now()),
                str(datetime.now()),
                'milly@yahoo.com',
                'pass',
                'Milly',
                'Wanderi',
            ]
        )
        self.assertNotIn('User.4447-by-me', storage.all())
        dbc.commit()
        storage.reload()
        self.assertIn('User.4447-by-me', storage.all())
        cur.close()
        db.close()

    def test_save(self):
        """obj is successfully saved to db"""
        new = User(
            email='regina@gmail.com',
            password='password',
            first_name='Reginah',
            last_name='Shikanda'
        )
        dbc = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur = dbc.cursor()
        cur.execute('SELECT * FROM users WHERE id="{}"'.format(new.id))
        res = cursor.fetchone()
        cur.execute('SELECT COUNT(*) FROM users;')
        old_count = cur.fetchone()[0]
        self.assertTrue(res is None)
        self.assertFalse(new in storage.all().values())
        new.save()
        dbc1 = MySQLdb.connect(
            host=os.getenv('HBNB_MYSQL_HOST'),
            port=3306,
            user=os.getenv('HBNB_MYSQL_USER'),
            passwd=os.getenv('HBNB_MYSQL_PWD'),
            db=os.getenv('HBNB_MYSQL_DB')
        )
        cur1 = dbc1.cursor()
        cur1.execute('SELECT COUNT(*) FROM users;')
        result = cur1.fetchone()[0]
        cur1.execute('SELECT COUNT(*) FROM users;')
        new_count = cur1.fetchone()[0]
        self.assertFalse(result is not None)
        self.assertEqual(old_count + 1, new_count)
        self.assertTrues(new in storage.all().values())
        cur1.close()
        dbc1.close()
        cur.close()
        dbc.close()
