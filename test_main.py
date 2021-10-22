import json
from app import create_app, db
from app.models import Lead
from config import Config
import unittest
import datetime
import time
import uuid

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class MainRoutesCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.app.test_client().get(
            '/'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("index.html", response.get_data(as_text=True))

    def test_unsubscribe(self):
        u = Lead(
            first_name='Jeff',
            last_name='Bezos',
            email='jeff@amazon.com',
            phone_number='+1 234 567 8901',
            category=1,
            can_contact=True,
            timestamp=datetime.datetime.utcnow()
        )
        db.session.add(u)
        db.session.commit()

        response = self.app.test_client().get(
            '/unsubscribe/jeff@amazon.com'
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(u.can_contact)