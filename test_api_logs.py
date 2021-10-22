import unittest
from config import Config
import json
from app import create_app, db
from app.models import Log, Content
import datetime
import time
import uuid

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    PUBLISHER_KEY = 'example_publisher_key'

class LogApiRoutesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_default(self):
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
        tm1 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        tm2 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        tm3 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        lm1 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow() - datetime.timedelta(days=31)
        )
        db.session.add_all([c, tm1, tm2, tm3, lm1])
        db.session.commit()

        response = self.app.test_client().get(
            '/_api/read/logs'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['slug'], 'example-slug')
        self.assertEqual(len(data[0]['cookie_uuid']), 36)
        self.assertEqual(data[0]['timestamp'], data[1]['timestamp'])

        self.assertEqual(data[1]['slug'], 'example-slug')
        self.assertEqual(len(data[1]['cookie_uuid']), 36)
        self.assertEqual(data[1]['timestamp'], data[2]['timestamp'])

        self.assertEqual(data[2]['slug'], 'example-slug')
        self.assertEqual(len(data[2]['cookie_uuid']), 36)
        self.assertEqual(data[2]['timestamp'], data[0]['timestamp'])

        self.assertNotEqual(data[0]['cookie_uuid'], data[1]['cookie_uuid'])
        self.assertNotEqual(data[1]['cookie_uuid'], data[2]['cookie_uuid'])
        self.assertNotEqual(data[2]['cookie_uuid'], data[0]['cookie_uuid'])

    
    def test_filter_by_content(self):
        c1 = Content(
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
        c2 = Content(
            file_name='file2.html',
            slug='another-slug',
            author_name='You Tu',
            author_handle='@itsu2',
            title='Title',
            description='This is a description.',
            category=2,
            section='Section',
            tags='list, of, tags',
            image_url='http://www.website.com/image.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow()
        )
        l1 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        l2 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        l3 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        l4 = Log(
            content_id=2,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add_all([c1, c2, l1, l2, l3, l4])
        db.session.commit()

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['slug'], 'example-slug')
        
        response = self.app.test_client().get(
            '/_api/read/logs?slug=another-slug'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['slug'], 'another-slug')


    def test_filter_by_user(self):
        c1 = Content(
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
        c2 = Content(
            file_name='file2.html',
            slug='another-slug',
            author_name='You Tu',
            author_handle='@itsu2',
            title='Title',
            description='This is a description.',
            category=2,
            section='Section',
            tags='list, of, tags',
            image_url='http://www.website.com/image.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow()
        )
        u1 = str(uuid.uuid4())
        u2 = str(uuid.uuid4())
        l1 = Log(
            content_id=1,
            cookie_uuid=u1,
            timestamp=datetime.datetime.utcnow()
        )
        l2 = Log(
            content_id=2,
            cookie_uuid=u1,
            timestamp=datetime.datetime.utcnow()
        )
        l3 = Log(
            content_id=1,
            cookie_uuid=u1,
            timestamp=datetime.datetime.utcnow()
        )
        l4 = Log(
            content_id=1,
            cookie_uuid=u2,
            timestamp=datetime.datetime.utcnow()
        )
        l5 = Log(
            content_id=1,
            cookie_uuid=u2,
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add_all([c1, c2, l1, l2, l3, l4, l5])
        db.session.commit()

        response = self.app.test_client().get(
            '/_api/read/logs?cookie_uuid={}'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        response = self.app.test_client().get(
            '/_api/read/logs?cookie_uuid={}'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)


    def test_filter_by_date(self):
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
        l1 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 1, 1)
        )
        l2 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 2, 1)
        )
        l3 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 3, 1)
        )
        l4 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 4, 1)
        )
        l5 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 5, 1)
        )
        l6 = Log(
            content_id=1,
            cookie_uuid=str(uuid.uuid4()),
            timestamp=datetime.datetime(2021, 6, 1)
        )
        db.session.add_all([c, l1, l2, l3, l4, l5, l6])
        db.session.commit()

        response = self.app.test_client().get(
            '/_api/read/logs?start_date=2021-03-01'
        )
        
        data = json.loads(response.data)
        self.assertEqual(len(data), 4)

        response = self.app.test_client().get(
            '/_api/read/logs?start_date=2021-01-01&end_date=2021-05-01'
        )
        data = json.loads(response.data)
        self.assertEqual(len(data), 5)


    def test_combining_filters(self):
        u1 = str(uuid.uuid4())
        u2 = str(uuid.uuid4())
        u3 = str(uuid.uuid4())

        d1 = datetime.datetime(2001, 9, 11)
        d2 = datetime.datetime(2021, 1, 6)
        d3 = datetime.datetime.utcnow()

        c1 = Content(
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
        c2 = Content(
            file_name='file2.html',
            slug='another-slug',
            author_name='You Tu',
            author_handle='@itsu2',
            title='Title',
            description='This is a description.',
            category=2,
            section='Section',
            tags='list, of, tags',
            image_url='http://www.website.com/image.jpg',
            published_time=datetime.datetime.utcnow(),
            modified_time=datetime.datetime.utcnow()
        )
        l1 = Log(
            content_id=1,
            cookie_uuid=u1,
            timestamp=d1
        )
        l2 = Log(
            content_id=1,
            cookie_uuid=u1,
            timestamp=d2
        )
        l3 = Log(
            content_id=1,
            cookie_uuid=u1,
            timestamp=d3
        )

        l4 = Log(
            content_id=2,
            cookie_uuid=u1,
            timestamp=d1
        )
        l5 = Log(
            content_id=2,
            cookie_uuid=u1,
            timestamp=d2
        )
        l6 = Log(
            content_id=2,
            cookie_uuid=u1,
            timestamp=d3
        )
        
        l7 = Log(
            content_id=1,
            cookie_uuid=u2,
            timestamp=d1
        )
        l8 = Log(
            content_id=1,
            cookie_uuid=u2,
            timestamp=d2
        )
        l9 = Log(
            content_id=1,
            cookie_uuid=u2,
            timestamp=d3
        )

        l10 = Log(
            content_id=2,
            cookie_uuid=u2,
            timestamp=d1
        )
        l11 = Log(
            content_id=2,
            cookie_uuid=u2,
            timestamp=d2
        )
        l12 = Log(
            content_id=2,
            cookie_uuid=u2,
            timestamp=d3
        )
        db.session.add_all([c1, c2])
        db.session.add(l1)
        db.session.add(l2)
        db.session.add(l3)
        db.session.add(l4)
        db.session.add(l5)
        db.session.add(l6)
        db.session.add(l7)
        db.session.add(l8)
        db.session.add(l9)
        db.session.add(l10)
        db.session.add(l11)
        db.session.add(l12)
        db.session.commit()

        # One filter

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 6)

        response = self.app.test_client().get(
            '/_api/read/logs?slug=another-slug'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 6)

        response = self.app.test_client().get(
            '/_api/read/logs?cookie_uuid={}'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 6)

        response = self.app.test_client().get(
            '/_api/read/logs?cookie_uuid={}'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 6)

        response = self.app.test_client().get(
            '/_api/read/logs?start_date=2001-09-10&end_date=2002-01-01'
        )
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(len(data), 4)
       
       # Two filters
        
        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        response = self.app.test_client().get(
            '/_api/read/logs?slug=another-slug&cookie_uuid={}'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        response = self.app.test_client().get(
            '/_api/read/logs?slug=another-slug&cookie_uuid={}'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)

        # Find a specific thing

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}&start_date=2000-01-01&end_date=2002-01-01'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['slug'], 'example-slug')
        self.assertEqual(data[0]['cookie_uuid'], u1)
        self.assertEqual(data[0]['timestamp'], '2001-09-11 00:00:00')

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}&start_date=2000-01-01&end_date=2002-01-01'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['slug'], 'example-slug')
        self.assertEqual(data[0]['cookie_uuid'], u2)
        self.assertEqual(data[0]['timestamp'], '2001-09-11 00:00:00')

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}&start_date=2000-01-01&end_date=2021-01-07'.format(u1)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)

        response = self.app.test_client().get(
            '/_api/read/logs?slug=example-slug&cookie_uuid={}&start_date=2000-01-01&end_date=2021-01-07'.format(u2)
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)