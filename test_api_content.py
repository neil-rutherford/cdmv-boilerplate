import unittest
from config import Config
import json
from app import create_app, db
from app.models import Content
import datetime
import time

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    PUBLISHER_KEY = 'example_publisher_key'

class ContentApiRoutesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_content(self):
        # Test success
        response = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'file_name.html',
                'slug': 'example-slug',
                'author_name': 'Me',
                'author_handle': '@me',
                'title': 'My Interesting Title',
                'description': 'My interesting description',
                'category': 1,
                'section': 'Section name',
                'tags': 'a, list, of, tags',
                'image_url': 'https://www.website.com/image.jpg'
            }
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['file_name'], 'file_name.html')
        self.assertEqual(data['slug'], 'example-slug')
        self.assertEqual(data['author_name'], 'Me')
        self.assertEqual(data['author_handle'], '@me')
        self.assertEqual(data['title'], 'My Interesting Title')
        self.assertEqual(data['description'], 'My interesting description')
        self.assertEqual(data['category'], 1)
        self.assertEqual(data['section'], 'Section name')
        self.assertEqual(len(data['tags']), 4)
        self.assertEqual(data['tags'][-1], 'tags')
        self.assertEqual(data['image_url'], 'https://www.website.com/image.jpg')
        self.assertEqual(data['published_time'], data['modified_time'])
        self.assertEqual(data['views'], 0)

        # Test wrong publisher_key
        response = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'wrong_publisher_key',
                'file_name': 'file_name2.html',
                'slug': 'example-slug-2',
                'author_name': 'Me2',
                'author_handle': '@me2',
                'title': 'My Interesting Title 2',
                'description': 'My interesting description 2',
                'category': 2,
                'section': 'Section name 2',
                'tags': 'a, long, list, of, tags',
                'image_url': 'https://www.website.com/image2.jpg'
            }
        )
        self.assertEqual(response.status_code, 403)

        # Test wrong method
        response = self.app.test_client().get(
            '/_api/create/content'
        )
        self.assertEqual(response.status_code, 405)

        # Test misc. error
        response = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'A'*301,
                'slug': 'example-slug',
                'author_name': 'A'*71,
                'author_handle': 'A'*71,
                'title': 'A'*71,
                'description': 'A'*156,
                'category': 'Not an integer',
                'section': 'A'*51,
                'tags': 'A'*101,
                'image_url': 'A'*301
            }
        )
        self.assertEqual(response.status_code, 500)


    def test_read_content(self):
        c = Content(
            file_name='file.html',
            slug='example-slug',
            author_name='Me McGee',
            author_handle='@itsmemcgee',
            title='Title',
            description='This is a description.',
            category=1,
            section='Section',
            tags='list, of, tags',
            image_url='http://www.website.com/image.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow()
        )
        db.session.add(c)
        db.session.commit()

        # Test success
        response = self.app.test_client().get(
            '/_api/read/content/example-slug'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['file_name'], 'file.html')
        self.assertEqual(data['slug'], 'example-slug')
        self.assertEqual(data['author_name'], 'Me McGee')
        self.assertEqual(data['author_handle'], '@itsmemcgee')
        self.assertEqual(data['title'], 'Title')
        self.assertEqual(data['description'], 'This is a description.')
        self.assertEqual(data['category'], 1)
        self.assertEqual(data['section'], 'Section')
        self.assertEqual(len(data['tags']), 3)
        self.assertEqual(data['tags'][1], 'of')
        self.assertEqual(data['image_url'], 'http://www.website.com/image.jpg')
        self.assertEqual(data['published_time'], data['modified_time'])
        self.assertEqual(data['views'], 0)

        # Test 404
        response = self.app.test_client().get(
            '/_api/read/content/example-slug-2'
        )
        self.assertEqual(response.status_code, 404)

        # Test wrong method
        response = self.app.test_client().post(
            '/_api/read/content/example-slug',
            data={
                'publisher_key': 'example_publisher_key',
                'slug': 'changed-slug'
            }
        )
        self.assertEqual(response.status_code, 405)


    def test_update_content(self):
        # Set up
        pre_call = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'file_name.html',
                'slug': 'example-slug',
                'author_name': 'Me',
                'author_handle': '@me',
                'title': 'My Interesting Title',
                'description': 'My interesting description',
                'category': 1,
                'section': 'Section name',
                'tags': 'a, list, of, tags',
                'image_url': 'https://www.website.com/image.jpg'
            }
        )
        self.assertEqual(pre_call.status_code, 201)

        # Test incorrect publisher_key
        response = self.app.test_client().post(
            '/_api/update/content/example-slug',
            data={
                'publisher_key': 'incorrect_publisher_key'
            }
        )
        self.assertEqual(response.status_code, 403)

        # Test wrong method
        response = self.app.test_client().get(
            '/_api/update/content/example-slug'
        )
        self.assertEqual(response.status_code, 405)

        # Test misc. error
        response = self.app.test_client().post(
            '/_api/update/content/example-slug',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'A'*301,
                'author_name': 'A'*71,
                'author_handle': 'A'*71,
                'title': 'A'*71,
                'description': 'A'*156,
                'category': 'Not an integer',
                'section': 'A'*51,
                'tags': 'A'*101,
                'image_url': 'A'*301
            }
        )
        self.assertEqual(response.status_code, 500)

        # Test success
        time.sleep(1)
        response = self.app.test_client().post(
            '/_api/update/content/example-slug',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'different_file.html',
                'author_name': 'You',
                'author_handle': '@you',
                'title': 'My Boring Title',
                'description': 'My boring description',
                'category': 2,
                'section': 'Section name',
                'tags': 'a, long, list, of, tags',
                'image_url': 'https://www.website.com/image1.jpg'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['file_name'], 'different_file.html')
        self.assertEqual(data['slug'], 'example-slug')
        self.assertEqual(data['author_name'], 'You')
        self.assertEqual(data['author_handle'], '@you')
        self.assertEqual(data['title'], 'My Boring Title')
        self.assertEqual(data['description'], 'My boring description')
        self.assertEqual(data['category'], 2)
        self.assertEqual(data['section'], 'Section name')
        self.assertEqual(len(data['tags']), 5)
        self.assertEqual(data['tags'][1], 'long')
        self.assertEqual(data['image_url'], 'https://www.website.com/image1.jpg')
        self.assertNotEqual(data['published_time'], data['modified_time'])
        self.assertEqual(data['views'], 0)


    def test_delete_content(self):
        # Set up
        pre_call = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'example_publisher_key',
                'file_name': 'file_name.html',
                'slug': 'example-slug',
                'author_name': 'Me',
                'author_handle': '@me',
                'title': 'My Interesting Title',
                'description': 'My interesting description',
                'category': 1,
                'section': 'Section name',
                'tags': 'a, list, of, tags',
                'image_url': 'https://www.website.com/image.jpg'
            }
        )
        self.assertEqual(pre_call.status_code, 201)

        # Wrong method
        response = self.app.test_client().get(
            '/_api/delete/content/example-slug'
        )
        self.assertEqual(response.status_code, 405)

        # Wrong publisher_key
        response = self.app.test_client().post(
            '/_api/create/content',
            data={
                'publisher_key': 'wrong_publisher_key'
            }
        )
        self.assertEqual(response.status_code, 403)

        # Test success
        response = self.app.test_client().post(
            '/_api/delete/content/example-slug',
            data={
                'publisher_key': 'example_publisher_key'
            }
        )
        self.assertEqual(response.status_code, 204)
        response = self.app.test_client().get(
            '/_api/read/content/example-slug'
        )
        self.assertEqual(response.status_code, 404)