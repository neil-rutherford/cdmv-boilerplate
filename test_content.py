import json
from app import create_app, db
from app.models import Content
from config import Config
import unittest
import datetime
import time
import uuid

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class ContentRoutesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_blog(self):
        response = self.app.test_client().get(
            '/blog'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("blog.html", response.get_data(as_text=True))
        

    def test_content(self):
        c = Content(
            file_name='unittest.html',
            slug='unit-test',
            author_name='Me McGee',
            author_handle='@itsmemcgee',
            title='Testing 1 2 3',
            description='This is for the unit test.',
            category=1,
            section='Testing',
            tags='testing, flask, apps, fml',
            image_url='https://asia.olympus-imaging.com/content/000107506.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow()
        )
        db.session.add(c)
        db.session.commit()

        response = self.app.test_client().get(
            '/blog/content/unit-test'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("unittest.html", response.get_data(as_text=True))

        response = self.app.test_client().get(
            '/blog/content/doesnt-exist'
        )
        self.assertEqual(response.status_code, 404)


    def test_load_content(self):
        c1 = Content(
            file_name='file1.html',
            slug='sample-slug',
            author_name='Me McGee',
            author_handle='@itsmemcgee',
            title='Testing 1 2 3',
            description='This is for the unit test.',
            category=1,
            section='Testing',
            tags='testing, flask, apps, fml',
            image_url='https://asia.olympus-imaging.com/content/000107506.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime(2001,1,1)
        )
        c2 = Content(
            file_name='file2.html',
            slug='sample-slug-2',
            author_name='Me McGee',
            author_handle='@itsmemcgee',
            title='Testing 1 2 3',
            description='This is for the unit test.',
            category=1,
            section='Testing',
            tags='testing, flask, apps, fml',
            image_url='https://asia.olympus-imaging.com/content/000107506.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime(2021,10,22)
        )
        c3 = Content(
            file_name='file3.html',
            slug='sample-slug-3',
            author_name='Me McGee',
            author_handle='@itsmemcgee',
            title='Testing 1 2 3',
            description='This is for the unit test.',
            category=1,
            section='Testing',
            tags='testing, flask, apps, fml',
            image_url='https://asia.olympus-imaging.com/content/000107506.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime(2005,1,5)
        )
        db.session.add_all([c1, c2, c3])
        db.session.commit()
        
        response = self.app.test_client().get(
            '/_api/load/content?counter=0'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data[0]['modified_time'], '2021-10-22 00:00:00')
        self.assertEqual(data[1]['modified_time'], '2005-01-05 00:00:00')
        self.assertEqual(data[2]['modified_time'], '2001-01-01 00:00:00')

        response = self.app.test_client().get(
            '/_api/load/content?counter=5'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

        response = self.app.test_client().get(
            '/_api/load/content'
        )
        self.assertEqual(response.status_code, 500)