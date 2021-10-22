import unittest
from config import Config
import json
from app import create_app, db
from app.models import Lead
import datetime
import time

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ADMIN_KEY = 'example_admin_key'

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

    def test_read_leads(self):
        u1 = Lead(
            first_name='John',
            last_name='Doe',
            email='johndoe@gmail.com',
            phone_number='+1 123 456 7890',
            category=1,
            can_contact=False,
            timestamp=datetime.datetime.utcnow()
        )
        u2 = Lead(
            first_name='Elon',
            last_name='Musk',
            email='elonmusk@tesla.com',
            phone_number='+1 234 567 8901',
            category=1,
            can_contact=True,
            timestamp=datetime.datetime.utcnow()
        )
        u3 = Lead(
            first_name='Jeff',
            last_name='Bezos',
            email='jeff@amazon.com',
            phone_number='+1 345 678 9012',
            category=2,
            can_contact=True,
            timestamp=datetime.datetime.utcnow()
        )
        u4 = Lead(
            first_name='Mark',
            last_name='Zuckerberg',
            email='zuck@facebook.com',
            phone_number='+1 456 789 0123',
            category=2,
            can_contact=True,
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add_all([u1,u2,u3,u4])
        db.session.commit()

        # Test wrong admin_key
        response = self.app.test_client().post(
            '/_api/read/leads',
            data={
                'admin_key': 'wrong_admin_key'
            }
        )
        self.assertEqual(response.status_code, 403)

        # Test wrong method
        response = self.app.test_client().get(
            '/_api/read/leads'
        )
        self.assertEqual(response.status_code, 405)

        # Test success
        response = self.app.test_client().post(
            '/_api/read/leads',
            data={
                'admin_key': 'example_admin_key'
            }
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        self.assertTrue(data[0]['can_contact'])

        self.assertTrue(data[1]['can_contact'])

        self.assertTrue(data[2]['can_contact'])
